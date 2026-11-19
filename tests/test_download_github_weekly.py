"""Offline tests: whole original weekly Markdown, GitHub-only and pinned refs."""
from datetime import date
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('github_weekly_download', ROOT / 'scripts/download_github_weekly.py')
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)
ROOT_SHA = 'a' * 40
ISSUE_SHA = 'b' * 40
DAY = date(2026, 11, 19)
README = '[旧期](docs/issue-418.md)\n[最新](docs/issue-419.md)\n普通文本 docs/issue-9999.md\n'
BODY = '# 科技爱好者周刊（第 419 期）：测试标题\r\n\r\n' + '这是原始周刊完整正文，不删除图片或者链接，也不把其中的新闻摘录宣称为各篇原文。' * 12 + '\r\n\r\n![图片](https://example.org/image.jpg)\n[原始链接](https://example.org)\n\n'


def commits(stamp='2026-11-13T10:22:34Z'):
    return [{'sha': ISSUE_SHA, 'commit': {'committer': {'date': stamp}}}]


class Response(io.BytesIO):
    def __init__(self, url, payload):
        super().__init__(payload)
        self.url = url
    def geturl(self):
        return self.url


class TransportTests(unittest.TestCase):
    def test_rejects_non_github_and_non_repository_urls(self):
        for url in ('http://api.github.com/repos/ruanyf/weekly/commits/master',
                    'https://api.github.com/repos/evil/weekly/commits/master',
                    'https://raw.githubusercontent.com/ruanyf/weekly/master/README.md',
                    'https://raw.githubusercontent.com/ruanyf/weekly/' + ROOT_SHA + '/../../secret',
                    'https://api.github.com@evil.test/repos/ruanyf/weekly/commits/master',
                    'https://raw.githubusercontent.com/ruanyf/weekly/' + ROOT_SHA + '/README.md?token=secret',
                    'https://api.github.com/repos/ruanyf/weekly/commits/master#secret'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                weekly.validate_url(url)

    def test_commit_query_is_exactly_scoped(self):
        url = weekly.API + '/commits?' + urllib.parse.urlencode({'path':'docs/issue-419.md','sha':ROOT_SHA,'per_page':1})
        self.assertEqual(weekly.validate_url(url), url)
        for query in ('path=../../secret&sha=' + ROOT_SHA + '&per_page=1',
                      'path=docs%2Fissue-419.md&sha=master&per_page=1',
                      'path=docs%2Fissue-419.md&sha=' + ROOT_SHA + '&per_page=1&per_page=2'):
            with self.assertRaises(ValueError):
                weekly.validate_url(weekly.API + '/commits?' + query)

    def test_api_bearer_is_optional_and_never_sent_to_raw(self):
        api = weekly.API + '/commits/master'
        raw = weekly.RAW + '/' + ROOT_SHA + '/README.md'
        requests = []
        def open_request(request, timeout):
            requests.append((request, timeout))
            return Response(request.full_url, b'{}')
        opener = mock.Mock()
        opener.open.side_effect = open_request
        with mock.patch.object(weekly.urllib.request, 'build_opener', return_value=opener), \
                mock.patch.dict(os.environ, {'GITHUB_TOKEN':'sensitive-token'}):
            weekly.fetch_bytes(api)
            weekly.fetch_bytes(raw)
        self.assertEqual(requests[0][0].get_header('Authorization'), 'Bearer sensitive-token')
        self.assertIsNone(requests[1][0].get_header('Authorization'))
        self.assertEqual(requests[0][0].method, 'GET')
        self.assertEqual(requests[0][1], 30)
        with mock.patch.object(weekly.urllib.request, 'build_opener', return_value=opener), \
                mock.patch.dict(os.environ, {}, clear=True):
            weekly.fetch_bytes(api)
        self.assertIsNone(requests[2][0].get_header('Authorization'))

    def test_redirects_are_never_followed(self):
        handler = weekly.NoRedirect()
        for destination in (weekly.API + '/commits/master', 'https://evil.test/'):
            with self.assertRaisesRegex(ValueError, 'redirect'):
                handler.redirect_request(None, None, 302, '', {}, destination)

    def test_response_limit_is_enforced(self):
        url = weekly.API + '/commits/master'
        opener = mock.Mock()
        opener.open.return_value = Response(url, b'x' * (weekly.MAX_RESPONSE_BYTES + 1))
        with mock.patch.object(weekly.urllib.request, 'build_opener', return_value=opener), self.assertRaisesRegex(ValueError, '2 MiB'):
            weekly.fetch_bytes(url)

    def test_retry_is_bounded_and_network_errors_do_not_echo_secrets(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.URLError('sensitive-token')
        with mock.patch.object(weekly.urllib.request, 'build_opener', return_value=opener), \
                mock.patch.object(weekly.time, 'sleep') as pause:
            with self.assertRaisesRegex(RuntimeError, 'bounded retries') as error:
                weekly.fetch_bytes(weekly.API + '/commits/master')
        self.assertNotIn('sensitive-token', str(error.exception))
        self.assertEqual(opener.open.call_count, 3)
        self.assertEqual(pause.call_count, 2)

    def test_permanent_http_failure_is_not_retried(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.HTTPError('url', 403, 'secret', {}, None)
        with mock.patch.object(weekly.urllib.request, 'build_opener', return_value=opener), self.assertRaisesRegex(RuntimeError, 'HTTP 403'):
            weekly.fetch_bytes(weekly.API + '/commits/master')
        self.assertEqual(opener.open.call_count, 1)


class SelectionTests(unittest.TestCase):
    def test_highest_readme_markdown_link_not_plain_text_or_external_link(self):
        readme = README + '[假](https://evil.test/docs/issue-9998.md)\n[完整](https://github.com/ruanyf/weekly/blob/' + ROOT_SHA + '/docs/issue-420.md)'
        self.assertEqual(weekly.latest_issue(readme, ROOT_SHA), 420)

    def test_missing_readme_links_rejected(self):
        with self.assertRaises(ValueError):
            weekly.latest_issue('plain docs/issue-419.md', ROOT_SHA)

    def test_freshness_is_issue_update_not_selection_day(self):
        self.assertEqual(weekly.validate_updated_at('2026-11-13T10:22:34Z', DAY, 14), '2026-11-13T10:22:34Z')
        self.assertEqual(weekly.validate_updated_at('2026-11-05T00:00:00Z', DAY, 14), '2026-11-05T00:00:00Z')
        with self.assertRaisesRegex(ValueError, 'older'):
            weekly.validate_updated_at('2026-11-04T00:00:00Z', DAY, 14)

    def test_shanghai_future_date_and_naive_dates_rejected(self):
        with self.assertRaisesRegex(ValueError, 'future'):
            weekly.validate_updated_at('2026-11-19T16:00:00Z', DAY, 14)
        with self.assertRaisesRegex(ValueError, 'timezone'):
            weekly.validate_updated_at('2026-11-13T10:22:34', DAY, 14)

    def test_full_markdown_body_not_modified_and_heading_checked(self):
        self.assertIn('419', weekly.validate_body(BODY, 419))
        for bad in ('<!DOCTYPE html><html>' + BODY, BODY.replace('419', '1419'), '# 第419期\n短文', ''):
            with self.subTest(bad=bad[:30]), self.assertRaises(ValueError):
                weekly.validate_body(bad, 419)

    def test_sha_must_be_full_commit_hash(self):
        for bad in ('master', 'abc', None, 123, 'g' * 40):
            with self.assertRaises(ValueError):
                weekly.commit_sha(bad)


class DownloadTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.out = self.root / 'corpus.md'
        self.diagnostics = self.root / 'diagnostics'

    def mocks(self, history=None, body=BODY):
        return (mock.patch.object(weekly, 'fetch_json', side_effect=[{'sha':ROOT_SHA}, commits() if history is None else history]),
                mock.patch.object(weekly, 'fetch_text', side_effect=[README, body]))

    def test_entire_original_document_is_pinned_and_metadata_is_accurate(self):
        json_mock, text_mock = self.mocks()
        with json_mock as get_json, text_mock as get_text:
            metadata = weekly.download_weekly(self.out, expected_day=DAY, diagnostics_dir=self.diagnostics)
        self.assertEqual(self.out.read_bytes(), BODY.encode('utf-8'))
        self.assertEqual(metadata['article_details'][0]['body'], BODY)
        self.assertEqual(metadata['source_ref'], ISSUE_SHA)
        self.assertEqual(metadata['index_ref'], ROOT_SHA)
        self.assertEqual(metadata['selection_date'], '2026-11-19')
        self.assertEqual(metadata['source_updated_at'], '2026-11-13T10:22:34Z')
        self.assertEqual(metadata['articles'], 1)
        self.assertEqual(metadata['fallback_articles'], 0)
        self.assertIn('原始Markdown未改写', metadata['attribution'])
        digest = hashlib.sha256(BODY.encode('utf-8')).hexdigest()
        self.assertEqual(metadata['corpus_sha256'], digest)
        self.assertEqual(metadata['article_details'][0]['body_sha256'], digest)
        self.assertEqual(metadata['article_details'][0]['body_characters'], len(BODY))
        self.assertEqual(metadata['corpus_bytes'], len(BODY.encode('utf-8')))
        self.assertEqual(get_text.call_args_list[0].args[0], weekly.RAW + '/' + ROOT_SHA + '/README.md')
        self.assertEqual(get_text.call_args_list[1].args[0], weekly.RAW + '/' + ISSUE_SHA + '/docs/issue-419.md')
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(get_json.call_args_list[1].args[0]).query)
        self.assertEqual(query, {'path':['docs/issue-419.md'],'sha':[ROOT_SHA],'per_page':['1']})
        self.assertEqual(json.loads(self.out.with_suffix('.meta.json').read_text(encoding='utf-8')), metadata)
        self.assertEqual(json.loads((self.diagnostics / 'articles.json').read_text(encoding='utf-8'))['status'], 'success')

    def test_failure_keeps_both_existing_outputs_and_saves_diagnostics(self):
        self.out.write_bytes(b'old corpus')
        self.out.with_suffix('.meta.json').write_bytes(b'old metadata')
        json_mock, text_mock = self.mocks(body='<html>login required</html>')
        with json_mock, text_mock, self.assertRaises(ValueError):
            weekly.download_weekly(self.out, expected_day=DAY, diagnostics_dir=self.diagnostics)
        self.assertEqual(self.out.read_bytes(), b'old corpus')
        self.assertEqual(self.out.with_suffix('.meta.json').read_bytes(), b'old metadata')
        diagnostic = json.loads((self.diagnostics / 'articles.json').read_text(encoding='utf-8'))
        self.assertEqual(diagnostic['status'], 'failure')
        self.assertEqual(diagnostic['stage'], 'body')

    def test_stale_or_empty_history_does_not_create_outputs(self):
        for history in ([], commits('2026-10-01T00:00:00Z'), [{'sha':ISSUE_SHA,'commit':{}}]):
            json_mock, text_mock = self.mocks(history=history)
            with json_mock, text_mock, self.assertRaises(ValueError):
                weekly.download_weekly(self.out, expected_day=DAY)
            self.assertFalse(self.out.exists())

    def test_failure_diagnostics_do_not_disclose_optional_token(self):
        token = 'my-private-api-token'
        with mock.patch.dict(os.environ, {'GITHUB_TOKEN':token}), \
                mock.patch.object(weekly, 'fetch_json', side_effect=RuntimeError('request failed ' + token)), \
                self.assertRaises(RuntimeError) as caught:
            weekly.download_weekly(self.out, expected_day=DAY, diagnostics_dir=self.diagnostics)
        self.assertNotIn(token, str(caught.exception))
        self.assertNotIn(token, (self.diagnostics / 'articles.json').read_text(encoding='utf-8'))

    def test_publish_failure_rolls_back_old_pair(self):
        import sys
        scripts = str(ROOT / 'scripts')
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        import download_public_articles as common
        self.out.write_bytes(b'old corpus')
        self.out.with_suffix('.meta.json').write_bytes(b'old metadata')
        actual_replace = common.os.replace
        def fail_metadata(source, target):
            if Path(source).name == 'new-1':
                raise OSError('simulated write failure')
            return actual_replace(source, target)
        json_mock, text_mock = self.mocks()
        with json_mock, text_mock, mock.patch.object(common.os, 'replace', side_effect=fail_metadata), self.assertRaises(OSError):
            weekly.download_weekly(self.out, expected_day=DAY)
        self.assertEqual(self.out.read_bytes(), b'old corpus')
        self.assertEqual(self.out.with_suffix('.meta.json').read_bytes(), b'old metadata')


if __name__ == '__main__':
    unittest.main()
