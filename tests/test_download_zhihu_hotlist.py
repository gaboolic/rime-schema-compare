"""Offline tests for hot-list fallback excerpts."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('download_hotlist', Path(__file__).resolve().parents[1] / 'scripts/download_zhihu_hotlist.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HotlistDescriptionTests(unittest.TestCase):
    def test_legacy_description_has_priority(self):
        self.assertEqual(module.hotlist_description({'extra': {'desc': '<b>正文</b>', 'info': ['另一个摘要']}}), '正文')

    def test_current_info_excludes_heat_and_media_markers(self):
        self.assertEqual(module.hotlist_description({'extra': {'info': ['热度: 390 万热度', '[视频]', '真实摘要', '[图片]', '第二段']}}), '真实摘要 第二段')

    def test_missing_or_invalid_info_is_empty(self):
        for item in ({}, {'extra': None}, {'extra': {'info': 'not a list'}}):
            self.assertEqual(module.hotlist_description(item), '')

    def test_write_corpus_uses_real_excerpt_without_answers(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'corpus.txt'
            module.write_corpus([{'title': '问题标题', 'url': 'https://www.zhihu.com/question/1', 'extra': {'info': ['热度：100', '接口摘要']}}], path, delay=0)
            self.assertIn('接口摘要', path.read_text(encoding='utf-8'))
            self.assertNotIn('热度', path.read_text(encoding='utf-8'))


class BodyDownloadTests(unittest.TestCase):
    def test_dom_plain_text_preserves_inequalities_and_literal_entities(self):
        self.assertEqual(module._plain_text(' 若 a < b 且 c > d，\n则成立 &amp; <code>示例</code> '),
                         '若 a < b 且 c > d， 则成立 &amp; <code>示例</code>')

    def test_require_bodies_does_not_replace_existing_corpus(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'corpus.txt'
            path.write_text('keep previous corpus', encoding='utf-8')
            with self.assertRaisesRegex(RuntimeError, 'No answer bodies fetched'):
                module.write_corpus([{'title': '标题', 'url': 'https://www.zhihu.com/question/1'}], path, delay=0, require_bodies=True)
            self.assertEqual(path.read_text(encoding='utf-8'), 'keep previous corpus')

    def test_rendered_bodies_override_excerpt_and_record_provenance(self):
        import json
        class FakeBrowser:
            last_fetch = {'question_id': '1', 'initial_http_status': 403,
                          'answers': [{'text': '实际回答正文', 'answer_url': 'https://www.zhihu.com/question/1/answer/2'}]}
            def fetch_top_answers(self, qid, max_answers):
                return ['实际回答正文', '第二个回答']
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'corpus.txt'
            module.write_corpus([{'title': '问题', 'url': 'https://www.zhihu.com/question/1',
                                  'extra': {'desc': '不应混入的问题摘要'}}], path,
                                browser=FakeBrowser(), delay=0, require_bodies=True)
            text = path.read_text(encoding='utf-8')
            self.assertIn('实际回答正文', text)
            self.assertNotIn('不应混入', text)
            meta = json.loads(path.with_suffix('.meta.json').read_text(encoding='utf-8'))
            self.assertEqual(meta['answer_bodies'], 2)
            self.assertEqual(meta['questions_with_answer_bodies'], 1)
            self.assertEqual(meta['fallback_questions'], 0)
            self.assertEqual(meta['question_details'][0]['initial_http_status'], 403)


if __name__ == '__main__':
    unittest.main()
