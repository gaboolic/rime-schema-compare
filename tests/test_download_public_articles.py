"""Public Daily downloader tests: offline fixtures, no browser or credentials."""
from datetime import date, datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.request

SPEC = importlib.util.spec_from_file_location('public_articles', Path(__file__).resolve().parents[1] / 'scripts/download_public_articles.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
DAY = date(2026, 11, 19)
TEXT = '这是一段来自公开文章的真实正文，用于测试中文整句输入和解码效果，不应被摘要或页面导航替代。'
HTML = f'<div class="main-wrap"><div class="meta">作者信息</div><div class="content"><p>{TEXT}</p></div><div class="view-more">查看知乎原文</div></div>'


def feed(ids=(101, 102), day='20261119'):
    return {'date': day, 'stories': [{'id': identifier, 'title': f'文章 {identifier}', 'url': 'https://evil.invalid/untrusted'} for identifier in ids],
            'top_stories': [{'id': 999, 'title': '旧文章'}]}


def detail(identifier):
    return {'id': identifier, 'title': f'公开文章 {identifier}', 'body': HTML,
            'share_url': 'https://evil.invalid/ignored'}


class TemporaryRoot(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.out = self.root / 'corpus.txt'
        self.meta = self.out.with_suffix('.meta.json')
        self.diagnostics = self.root / 'diagnostics'

    def install_old_pair(self):
        self.out.write_bytes(b'old corpus')
        self.meta.write_bytes(b'old metadata')

    def assert_old_pair(self):
        self.assertEqual(self.out.read_bytes(), b'old corpus')
        self.assertEqual(self.meta.read_bytes(), b'old metadata')


class HtmlTests(unittest.TestCase):
    def test_extracts_only_central_text_and_preserves_paragraphs_entities(self):
        html = '''<div class="headline">外部标题</div><div class="meta"><span class="author">作者</span></div>
        <div class="content"><p>正文 a &lt; b 且 c &gt; d，&amp; 是实体。</p>
        <script>窃取或生成内容</script><style>隐藏样式</style><p>第二段<strong>重要内容</strong>。</p>
        <span class="author">不应混入作者</span><a class="originUrl">查看知乎原文</a></div>
        <div class="view-more">导航分享</div>'''
        body = module.extract_body(html, min_hanzi=5)
        self.assertEqual(body, '正文 a < b 且 c > d，& 是实体。\n\n第二段重要内容。')
        for excluded in ('外部标题', '作者', '窃取', '隐藏样式', '查看知乎原文', '导航分享'):
            self.assertNotIn(excluded, body)

    def test_multiple_content_containers_are_all_real_body(self):
        self.assertEqual(module.extract_body('<div class="content"><p>第一条真实正文</p></div><div class="content"><p>第二条真实正文</p></div>', min_hanzi=5),
                         '第一条真实正文\n\n第二条真实正文')

    def test_missing_empty_or_small_body_rejected(self):
        for html in ('', '<html>无正文</html>', '<div class="content"></div>', '<div class="content">广告</div>'):
            with self.subTest(html=html), self.assertRaises(ValueError):
                module.extract_body(html)

    def test_login_or_error_container_is_not_an_article(self):
        for body in ('请先登录后查看完整文章正文', '请完成安全验证后继续访问', 'Access Denied'):
            with self.subTest(body=body), self.assertRaisesRegex(ValueError, 'login/verification/error'):
                module.extract_body(f'<div class="content">{body}</div>', min_hanzi=1)


class FeedAndUrlTests(unittest.TestCase):
    def test_only_current_stories_never_older_top_stories(self):
        chosen = module.select_stories(feed(), DAY, 5)
        self.assertEqual([story['id'] for story in chosen], [101, 102])
        self.assertEqual(module.select_stories(feed(), DAY, 1)[0]['id'], 101)

    def test_stale_missing_invalid_feed_date_rejected(self):
        for value in ('20261118', None, '2026-11-19', '20261340'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.select_stories(feed(day=value), DAY, 5)

    def test_top_stories_only_is_not_a_current_feed(self):
        data = feed()
        data['stories'] = []
        with self.assertRaisesRegex(ValueError, 'current-day stories'):
            module.select_stories(data, DAY, 5)

    def test_duplicate_ids_and_invalid_ids_rejected(self):
        for identifier in ('../secret', '1?token=x', -1, True, 1.5, None, '1%2f2'):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                module.select_stories(feed(ids=(identifier,)), DAY, 5)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            module.select_stories(feed(ids=(1, 1)), DAY, 5)

    def test_fixed_https_host_and_paths_only(self):
        for url in ('http://news-at.zhihu.com/api/4/news/latest',
                    'https://news-at.zhihu.com.evil/api/4/news/latest',
                    'https://news-at.zhihu.com@evil.invalid/api/4/news/latest',
                    'https://news-at.zhihu.com/api/4/news/latest?token=secret',
                    'https://127.0.0.1/api/4/news/1',
                    'https://news-at.zhihu.com/api/4/news/../secret'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                module.validate_api_url(url)
        self.assertEqual(module.validate_api_url(module.FEED_URL), module.FEED_URL)

    def test_redirect_does_not_leave_official_api(self):
        handler = module.FixedHostRedirect()
        request = urllib.request.Request(module.FEED_URL)
        with self.assertRaises(ValueError):
            handler.redirect_request(request, None, 302, 'redirect', {}, 'https://evil.invalid/login')

    def test_default_day_uses_shanghai_timezone(self):
        clock = mock.Mock()
        clock.now.return_value = datetime(2026, 11, 19, 0, 1, tzinfo=module.SHANGHAI)
        with mock.patch.object(module, 'datetime', clock):
            self.assertEqual(module.shanghai_today(), DAY)
        clock.now.assert_called_once_with(module.SHANGHAI)


class FetchTests(unittest.TestCase):
    def response(self, data, *, url=module.FEED_URL):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = url
        response.read.return_value = json.dumps(data).encode('utf-8')
        return response

    def test_get_no_cookie_no_bearer_and_bounded_timeout(self):
        opener = mock.Mock()
        opener.open.return_value = self.response(feed())
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener):
            self.assertEqual(module.fetch_json(module.FEED_URL), feed())
        args, kwargs = opener.open.call_args
        request = args[0]
        self.assertEqual(request.get_method(), 'GET')
        self.assertNotIn('Authorization', dict(request.header_items()))
        self.assertNotIn('Cookie', dict(request.header_items()))
        self.assertEqual(kwargs['timeout'], 30)

    def test_transient_http_failure_is_retried(self):
        opener = mock.Mock()
        opener.open.side_effect = [urllib.error.HTTPError(module.FEED_URL, 503, 'busy', {}, None), self.response(feed())]
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), mock.patch.object(module.time, 'sleep') as sleep:
            self.assertEqual(module.fetch_json(module.FEED_URL), feed())
        self.assertEqual(opener.open.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_incomplete_body_read_is_retried(self):
        opener = mock.Mock()
        incomplete = self.response({})
        incomplete.read.side_effect = module.http.client.IncompleteRead(b'partial', 100)
        opener.open.side_effect = [incomplete, self.response(feed())]
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), mock.patch.object(module.time, 'sleep'):
            self.assertEqual(module.fetch_json(module.FEED_URL), feed())
        self.assertEqual(opener.open.call_count, 2)

    def test_oversized_payload_is_rejected_before_json_parsing(self):
        opener = mock.Mock()
        oversized = self.response({})
        oversized.read.return_value = b'123456789'
        opener.open.return_value = oversized
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), mock.patch.object(module, 'MAX_RESPONSE_BYTES', 8):
            with self.assertRaisesRegex(ValueError, 'size limit'):
                module.fetch_json(module.FEED_URL)
        self.assertEqual(opener.open.call_count, 1)

    def test_404_is_not_retried(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.HTTPError(module.FEED_URL, 404, 'missing', {}, None)
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), mock.patch.object(module.time, 'sleep') as sleep:
            with self.assertRaisesRegex(RuntimeError, 'HTTP 404'):
                module.fetch_json(module.FEED_URL)
        self.assertEqual(opener.open.call_count, 1)
        sleep.assert_not_called()

    def test_network_retry_count_is_finite_and_error_is_sanitized(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.URLError('secret proxy information')
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), mock.patch.object(module.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'bounded retries') as raised:
                module.fetch_json(module.FEED_URL, attempts=2)
        self.assertEqual(opener.open.call_count, 2)
        self.assertNotIn('secret', str(raised.exception))

    def test_certificate_failure_retains_actionable_reason(self):
        opener = mock.Mock()
        certificate = module.ssl.SSLCertVerificationError(1, 'certificate verify failed: certificate has expired')
        opener.open.side_effect = urllib.error.URLError(certificate)
        with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaisesRegex(RuntimeError, 'TLS_CERTIFICATE_VERIFY_FAILED.*expired'):
                module.fetch_json(module.FEED_URL, attempts=1)

    def test_dns_failure_is_distinguished_from_timeout(self):
        self.assertIn('DNS_ERROR', module.network_error_description(urllib.error.URLError(module.socket.gaierror(-2, 'Name not known'))))
        self.assertIn('TIMEOUT', module.network_error_description(TimeoutError('read timed out')))

    def test_network_error_redacts_proxy_credentials_and_tokens(self):
        message = module.network_error_description(OSError('proxy https://alice:private@proxy.example/path token=hidden'))
        self.assertNotIn('private', message)
        self.assertNotIn('alice', message)
        self.assertNotIn('hidden', message)
        self.assertIn('[redacted]', message)

    def test_html_or_non_object_payload_is_not_a_feed(self):
        for payload in (b'<html>403 login required</html>', b'[]'):
            opener = mock.Mock()
            response = self.response({})
            response.read.return_value = payload
            opener.open.return_value = response
            with self.subTest(payload=payload), mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), self.assertRaises(ValueError):
                module.fetch_json(module.FEED_URL)


class DownloadTests(TemporaryRoot):
    def test_success_writes_exact_metadata_contract_and_body_hashes(self):
        with mock.patch.object(module, 'fetch_json', side_effect=[feed(), detail(101), detail(102)]) as fetch, mock.patch.object(module.time, 'sleep') as sleep:
            result = module.download_articles(self.out, expected_day=DAY, diagnostics_dir=self.diagnostics)
        self.assertEqual([call.args[0] for call in fetch.call_args_list], [module.FEED_URL, module.DETAIL_BASE + '101', module.DETAIL_BASE + '102'])
        sleep.assert_called_once_with(5)
        self.assertEqual(set(result), {'source_kind', 'source_id', 'source_name', 'source_url', 'feed_date', 'fetched_at',
                                     'feed_fetched_at', 'articles', 'articles_with_bodies', 'fallback_articles', 'corpus_bytes',
                                     'corpus_sha256', 'article_details'})
        self.assertEqual(result['source_kind'], 'public_articles')
        self.assertEqual(result['source_id'], 'zhihu_daily')
        self.assertEqual(result['source_name'], '知乎日报公开文章')
        self.assertEqual(result['feed_date'], '2026-11-19')
        self.assertEqual(result['articles'], 2)
        self.assertEqual(result['articles_with_bodies'], 2)
        self.assertEqual(result['fallback_articles'], 0)
        self.assertIsNotNone(datetime.fromisoformat(result['fetched_at']).tzinfo)
        corpus = self.out.read_bytes()
        self.assertEqual(result['corpus_bytes'], len(corpus))
        self.assertEqual(result['corpus_sha256'], hashlib.sha256(corpus).hexdigest())
        for index, record in enumerate(result['article_details'], start=101):
            self.assertEqual(record['url'], f'https://daily.zhihu.com/story/{index}')
            self.assertEqual(record['api_url'], module.DETAIL_BASE + str(index))
            self.assertEqual(record['body_sha256'], hashlib.sha256(record['body'].encode('utf-8')).hexdigest())
            self.assertEqual(record['body_characters'], len(record['body']))
            self.assertIn(record['body'], corpus.decode('utf-8'))
        self.assertEqual(json.loads(self.meta.read_text(encoding='utf-8')), result)
        self.assertNotIn('evil.invalid', corpus.decode('utf-8'))
        self.assertEqual(json.loads((self.diagnostics / 'articles.json').read_text(encoding='utf-8'))['status'], 'success')

    def test_partial_article_failure_preserves_old_corpus_and_metadata(self):
        self.install_old_pair()
        broken = detail(102)
        broken['body'] = '<html>please login</html>'
        with mock.patch.object(module, 'fetch_json', side_effect=[feed(), detail(101), broken]):
            with self.assertRaises(ValueError):
                module.download_articles(self.out, expected_day=DAY, delay=0, diagnostics_dir=self.diagnostics)
        self.assert_old_pair()
        diagnostic = json.loads((self.diagnostics / 'articles.json').read_text(encoding='utf-8'))
        self.assertEqual(diagnostic['status'], 'failure')
        self.assertEqual(diagnostic['article_id'], '102')
        self.assertEqual(len(diagnostic['article_details']), 1)

    def test_stale_feed_failure_preserves_old_pair(self):
        self.install_old_pair()
        with mock.patch.object(module, 'fetch_json', return_value=feed(day='20261118')) as fetch:
            with self.assertRaisesRegex(ValueError, 'not for the requested day'):
                module.download_articles(self.out, expected_day=DAY, diagnostics_dir=self.diagnostics)
        self.assert_old_pair()
        self.assertEqual(fetch.call_count, 1)

    def test_missing_body_cannot_fall_back_to_title_or_summary(self):
        self.install_old_pair()
        data = detail(101)
        del data['body']
        data['summary'] = TEXT
        with mock.patch.object(module, 'fetch_json', side_effect=[feed(ids=(101,)), data]):
            with self.assertRaisesRegex(ValueError, 'no HTML body'):
                module.download_articles(self.out, expected_day=DAY, delay=0)
        self.assert_old_pair()

    def test_mismatched_detail_id_is_rejected(self):
        with mock.patch.object(module, 'fetch_json', side_effect=[feed(ids=(101,)), detail(999)]):
            with self.assertRaisesRegex(ValueError, 'does not match'):
                module.download_articles(self.out, expected_day=DAY, delay=0)
        self.assertFalse(self.out.exists())
        self.assertFalse(self.meta.exists())

    def test_successful_publication_is_not_misreported_when_diagnostic_save_fails(self):
        with mock.patch.object(module, 'fetch_json', side_effect=[feed(ids=(101,)), detail(101)]), \
                mock.patch.object(module, 'save_diagnostic', side_effect=OSError('fixture diagnostic failure')):
            result = module.download_articles(self.out, expected_day=DAY, delay=0, diagnostics_dir=self.diagnostics)
        self.assertEqual(result['articles'], 1)
        self.assertTrue(self.out.exists())
        self.assertTrue(self.meta.exists())

    def test_cli_defaults_to_github_without_calling_daily(self):
        github = mock.Mock()
        github.download_weekly.return_value = {'articles': 1, 'source_name': 'GitHub weekly fixture', 'corpus_bytes': 123}
        with mock.patch.dict(module.sys.modules, {'download_github_weekly': github}), mock.patch.object(module, 'download_articles') as daily:
            self.assertEqual(module.main(['--date', DAY.isoformat(), '--out', str(self.out)]), 0)
        github.download_weekly.assert_called_once_with(self.out, expected_day=DAY, diagnostics_dir=None)
        daily.assert_not_called()

    def test_daily_requires_explicit_source_selection(self):
        with mock.patch.object(module, 'download_articles', return_value={'articles': 1, 'source_name': 'Daily fixture', 'corpus_bytes': 123}) as daily:
            self.assertEqual(module.main(['--source', 'zhihu-daily', '--date', DAY.isoformat(), '--out', str(self.out)]), 0)
        self.assertEqual(daily.call_args.kwargs['expected_day'], DAY)

    def test_metadata_replace_failure_rolls_back_corpus(self):
        self.install_old_pair()
        real_replace = module.os.replace
        def fail_metadata(source, destination):
            if Path(destination) == self.meta:
                raise OSError('fixture metadata failure')
            return real_replace(source, destination)
        with mock.patch.object(module.os, 'replace', side_effect=fail_metadata):
            with self.assertRaisesRegex(OSError, 'fixture metadata failure'):
                module.publish_pair(self.out, b'new corpus', b'new metadata')
        self.assert_old_pair()


if __name__ == '__main__':
    unittest.main()
