"""Real Git regression: preserve raw corpus bytes without weakening report checks."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('git'), 'Git is required')
class PublicationAttributesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.git('init', '-q')
        self.git('config', 'core.autocrlf', 'true')
        self.git('config', 'core.whitespace', 'blank-at-eof,blank-at-eol,space-before-tab')
        shutil.copyfile(ROOT / '.gitattributes', self.root / '.gitattributes')

    def git(self, *args, check=True):
        with tempfile.TemporaryFile() as output:
            result = subprocess.run(['git', '-C', str(self.root), *args], stdout=output,
                                    stderr=subprocess.STDOUT, check=False)
            output.seek(0)
            data = output.read()
        if check:
            self.assertEqual(result.returncode, 0, data.decode('utf-8', errors='replace'))
        return result.returncode, data

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def assert_raw_body_is_preserved_and_publishable(self, body):
        corpus = 'data/corpus/public_articles_2026-11-19.txt'
        self.write(corpus, body)
        self.write('data/corpus/public_articles_2026-11-19.meta.json', b'{"source_id":"fixture"}\n')
        self.write('report/latest.md', b'# Valid report\n')
        _, output = self.git('add', '--', '.gitattributes', 'data/corpus', 'report')
        self.assertNotIn(b'LF will be replaced by CRLF', output)
        self.git('diff', '--cached', '--check')
        _, staged = self.git('show', ':' + corpus)
        self.assertEqual(staged, body)

    def test_original_blank_eof_and_trailing_spaces_are_not_publication_errors(self):
        self.assert_raw_body_is_preserved_and_publishable('原始正文保留末尾空行。  \n\n'.encode('utf-8'))

    def test_original_crlf_bytes_are_not_normalized_in_the_index(self):
        self.assert_raw_body_is_preserved_and_publishable('原始正文使用CRLF。\r\n\r\n'.encode('utf-8'))

    def test_generated_report_whitespace_errors_are_still_rejected(self):
        self.write('report/latest.md', b'# Invalid report  \n\n')
        self.git('add', '--', '.gitattributes', 'report')
        code, output = self.git('diff', '--cached', '--check', check=False)
        self.assertNotEqual(code, 0)
        self.assertIn(b'report/latest.md', output)


if __name__ == '__main__':
    unittest.main()
