"""Offline publication guards; no network, browsers, or real vendor mutation."""
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('weekly_validation', ROOT / 'scripts/validate_weekly_benchmark.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.corpus = self.root / 'today.txt'
        self.corpus.write_text('问题标题\n这是实际回答正文\n', encoding='utf-8')
        self.meta = {
            'fetched_at': '2026-11-18T08:30:00+08:00',
            'hotlist_updated_at': '2026-11-17T20:00:00Z',
            'hotlist_fetched_at': '2026-11-18T00:00:00Z',
            'corpus_sha256': hashlib.sha256(self.corpus.read_bytes()).hexdigest(),
            'corpus_bytes': self.corpus.stat().st_size,
            'questions': 1, 'questions_with_answer_bodies': 1,
            'answer_bodies': 1, 'fallback_questions': 0,
            'question_details': [{'question_id': '1', 'answers': [
                {'text': '这是实际回答正文', 'answer_url': 'https://www.zhihu.com/question/1/answer/2'}]}],
        }
        self.artifacts = self.root / 'results'
        self.artifacts.mkdir()
        self.result = {'corpus_file': str(self.corpus), 'summary': {}}
        for vendor in module.DEFAULT_VENDORS:
            folder = vendor.data_dir(self.root)
            (folder / 'build').mkdir(parents=True)
            language = ('zh-hant-t-essay-bgw' if vendor.preserve_translator_defaults
                        else 'wanxiang-lts-zh-hans' if '_with_gram' in vendor.key else '')
            translator = {'enable_user_dict': False}
            if vendor.preserve_translator_defaults:
                translator.update(max_homophones=7, max_homographs=7)
            (folder / 'build' / f'{vendor.schema_id}.schema.yaml').write_text(
                yaml.safe_dump({'grammar': {'language': language}, 'translator': translator}), encoding='utf-8')
            if language:
                data = b'verified model fixture'
                (folder / f'{language}.gram').write_bytes(data)
                (folder / 'model_versions.json').write_text(json.dumps({'models': [
                    {'name': f'{language}.gram', 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}]}), encoding='utf-8')
            self.result['summary'][vendor.key] = {'sentence_total': 150, 'gold_character_total': 1500,
                'decode_failed': 0, 'skipped_no_input': 0,
                'sentence_accuracy_percent': 70.0, 'character_accuracy_percent': 95.0}

    def validate(self):
        self.corpus.with_suffix('.meta.json').write_text(json.dumps(self.meta), encoding='utf-8')
        (self.artifacts / 'benchmark_today.json').write_text(json.dumps(self.result), encoding='utf-8')
        return module.validate(self.corpus, self.artifacts, date(2026, 11, 18), root=self.root, min_sentences=100)

    def test_valid_full_body_all_vendor_result(self):
        payload, _ = self.validate()
        self.assertEqual(len(payload['summary']), 11)
        self.assertEqual(len(payload['verified_models']), 6)

    def test_stale_api_data_is_not_today_even_when_download_is_today(self):
        self.meta['hotlist_updated_at'] = '2026-11-16T20:00:00Z'
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.validate()

    def test_shanghai_day_not_utc_day(self):
        self.assertEqual(module.local_day('2026-11-17T20:00:00Z'), date(2026, 11, 18))

    def test_excerpt_fallback_rejected(self):
        self.meta['fallback_questions'] = 1
        with self.assertRaisesRegex(ValueError, 'fallback'):
            self.validate()

    def test_missing_vendor_rejected(self):
        del self.result['summary']['rime_ice']
        with self.assertRaisesRegex(ValueError, 'all default vendors'):
            self.validate()

    def test_decode_failure_rejected(self):
        self.result['summary']['rime_frost']['decode_failed'] = 1
        with self.assertRaisesRegex(ValueError, 'Decode failures'):
            self.validate()

    def test_small_corpus_rejected(self):
        self.result['summary']['rime_frost']['sentence_total'] = 5
        with self.assertRaisesRegex(ValueError, 'Too few'):
            self.validate()

    def test_corpus_hash_mismatch_rejected(self):
        self.corpus.write_text('被意外替换的文本', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            self.validate()

    def test_wrong_corpus_rejected(self):
        self.result['corpus_file'] = str(self.root / 'old.txt')
        with self.assertRaisesRegex(ValueError, 'wrong corpus'):
            self.validate()

    def test_corrupted_model_rejected(self):
        vendor = next(v for v in module.DEFAULT_VENDORS if v.key == 'rime_frost_with_gram')
        (vendor.data_dir(self.root) / 'wanxiang-lts-zh-hans.gram').write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'Model size/SHA256'):
            self.validate()

    def test_wrong_compiled_model_rejected(self):
        vendor = module.DEFAULT_VENDORS[0]
        path = vendor.data_dir(self.root) / 'build' / f'{vendor.schema_id}.schema.yaml'
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        data['grammar']['language'] = 'unexpected-model'
        path.write_text(yaml.safe_dump(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Wrong compiled model'):
            self.validate()

    def test_staging_reports_annotated_identically(self):
        payload, meta = self.validate()
        report = self.root / 'reports'
        report.mkdir()
        for name in ('latest.md', '2026-11-18.md'):
            (report / name).write_text('# Rime 评测结果\n\n## Vendor 子模块版本\n\nversions\n', encoding='utf-8')
        module.annotate_reports(report, self.corpus, payload, meta, date(2026, 11, 18))
        latest = (report / 'latest.md').read_text(encoding='utf-8')
        self.assertIn('11 个方案', latest)
        self.assertIn('已验证的语言模型', latest)
        self.assertEqual(latest, (report / '2026-11-18.md').read_text(encoding='utf-8'))


class SourceProvenanceTests(unittest.TestCase):
    def test_git_head_must_match_evaluated_source_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / '.git').write_text('gitdir: fixture', encoding='utf-8')
            (folder / 'upstream_versions.json').write_text(json.dumps([{'commit': 'a' * 40}]), encoding='utf-8')
            def fake_run(arguments, **kwargs):
                kwargs['stdout'].write(str(folder) if arguments[-1] == '--show-toplevel' else 'b' * 40)
            with mock.patch.object(module.subprocess, 'run', side_effect=fake_run):
                with self.assertRaisesRegex(ValueError, 'HEAD differs'):
                    module.verify_git_source(folder)

    def test_generated_non_git_variant_is_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            module.verify_git_source(Path(temp))


class WorkflowTests(unittest.TestCase):
    def test_official_standard_windows_runner_needs_no_personal_desktop(self):
        workflow = yaml.load((ROOT / '.github/workflows/weekly-report.yml').read_text(encoding='utf-8'), Loader=yaml.BaseLoader)
        job = workflow['jobs']['benchmark']
        self.assertEqual(job['runs-on'], 'windows-latest')
        steps = job['steps']
        checkout = next(s for s in steps if s.get('uses', '').startswith('actions/checkout'))
        self.assertEqual(checkout['with']['fetch-depth'], '1')
        text = '\n'.join(s.get('run', '') for s in steps)
        self.assertNotIn('[Environment]::UserInteractive', text)
        self.assertNotIn('run.cmd', text)
        self.assertIn('p.chromium.launch(channel="chrome", headless=False)', text)
        self.assertIn('find_module(b"octagram")', text)
        self.assertIn('page.title()', text)
        self.assertIn('git submodule update --init --recursive --depth 1 --remote', text)

    def test_monday_schedule_and_publication_guards(self):
        workflow = yaml.load((ROOT / '.github/workflows/weekly-report.yml').read_text(encoding='utf-8'), Loader=yaml.BaseLoader)
        self.assertEqual(workflow['on']['schedule'][0]['cron'], '0 0 * * 1')
        self.assertNotIn('pull_request', workflow['on'])
        steps = workflow['jobs']['benchmark']['steps']
        text = '\n'.join(s.get('run', '') for s in steps)
        self.assertIn('--require-all-bodies', text)
        self.assertIn('--limit 5 --answers 1 --delay 5', text)
        self.assertIn('--diagnostics-dir', text)
        self.assertIn('--min-sentences 20', text)
        self.assertIn('validate_weekly_benchmark.py', text)
        regression = next(s['run'] for s in steps if s['name'].startswith('Install dependencies'))
        self.assertLess(regression.index('New-Item'), regression.index('python -m pip'))
        for filename in ('dependencies.log', 'regression-tests.log', 'shell-tests.log'):
            self.assertIn(filename, regression)
        upload = next(s for s in steps if s.get('uses', '').startswith('actions/upload-artifact'))
        self.assertEqual(upload['if'], 'always()')
        self.assertNotIn('.cache', upload['with']['path'])
        commit = next(s for s in steps if s['name'].startswith('Commit and push'))
        self.assertNotIn('uses', commit)
        self.assertIn('git push origin HEAD:main', commit['run'])
        self.assertIn('git add -- @paths', commit['run'])
        self.assertNotIn('--force', commit['run'])
        self.assertNotIn('.cache', commit['run'])
        self.assertNotIn('RUNNER_TEMP', commit['run'])


if __name__ == '__main__':
    unittest.main()
