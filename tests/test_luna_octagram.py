"""Offline regression tests for upstream Luna Pinyin + hant Octagram.

Run with: python -m unittest discover -s tests -p test_luna_octagram.py -v
Only the standard-library unittest runner and mocks are used; importing the
application still requires its normal runtime dependencies.
"""

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from rime_schema_compare import benchmark_env, rime_runner
from rime_schema_compare.config import DEFAULT_VENDORS, VendorConfig


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


setup_luna_octagram = load_script("setup_luna_octagram")
benchmark_sentences = load_script("benchmark_sentences")
LUNA = next(v for v in DEFAULT_VENDORS if v.key == "luna_pinyin_with_octagram")
MODEL = "zh-hant-t-essay-bgw.gram"


class TemporaryRootTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write_file(self, relative, content="fixture\n"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def read_yaml(self, path):
        # Reuse the application's existing YAML dependency, not a test framework.
        return benchmark_env.yaml.safe_load(path.read_text(encoding="utf-8"))


class VendorConfigTests(TemporaryRootTest):
    def test_original_luna_entry_is_unique_and_requires_hant_assets(self):
        self.assertEqual(sum(v.key == LUNA.key for v in DEFAULT_VENDORS), 1)
        self.assertEqual(LUNA.rel_path, "vendor/luna_pinyin_with_octagram")
        self.assertEqual(LUNA.schema_id, "luna_pinyin_simp")
        self.assertEqual(LUNA.input_mode, "pinyin")
        self.assertTrue(LUNA.preserve_translator_defaults)
        self.assertEqual(LUNA.required_rime_modules, ("octagram",))
        self.assertEqual(set(LUNA.required_files), {
            "luna_pinyin.schema.yaml", "luna_pinyin_simp.schema.yaml",
            "luna_pinyin.dict.yaml", "grammar.yaml", MODEL,
            "upstream_versions.json",
        })
        self.assertEqual(LUNA.data_dir(self.root),
                         (self.root / LUNA.rel_path).resolve())

    def test_legacy_vendor_defaults_are_backward_compatible(self):
        vendor = VendorConfig("legacy", "vendor/legacy", "legacy")
        self.assertFalse(vendor.preserve_translator_defaults)
        self.assertEqual(vendor.required_files, ())
        for key in ("mingyuepinyin", "mingyuepinyin_with_gram"):
            with self.subTest(key=key):
                legacy = next(v for v in DEFAULT_VENDORS if v.key == key)
                self.assertFalse(legacy.preserve_translator_defaults)
                self.assertEqual(legacy.required_files, ())


class BenchmarkEnvironmentTests(TemporaryRootTest):
    def test_preserving_mode_keeps_upstream_include_and_unrelated_settings(self):
        custom = self.write_file("luna_pinyin.custom.yaml", """metadata: original
patch:
  __include: grammar:/hant
  translator/enable_user_dict: true
  translator/dictionary: luna_pinyin
  translator/contextual_suggestions: true
  menu/page_size: 9
""")
        benchmark_env.merge_disable_user_dict_patch(
            custom, preserve_translator_defaults=True)
        self.assertEqual(self.read_yaml(custom), {
            "metadata": "original",
            "patch": {"__include": "grammar:/hant",
                      "translator/enable_user_dict": False,
                      "translator/dictionary": "luna_pinyin",
                      "translator/contextual_suggestions": True,
                      "menu/page_size": 9},
        })

    def test_preserving_mode_removes_stale_benchmark_overrides_idempotently(self):
        custom = self.write_file("luna_pinyin_simp.custom.yaml", """patch:
  __include: grammar:/hant
  translator/max_sentences: 999
  translator/max_homophones: 999
  translator/enable_user_dict: true
  translator/initial_quality: 1.2
""")
        for _ in range(2):
            benchmark_env.merge_disable_user_dict_patch(
                custom, preserve_translator_defaults=True)
            patch = self.read_yaml(custom)["patch"]
            self.assertNotIn("translator/max_sentences", patch)
            self.assertNotIn("translator/max_homophones", patch)
            self.assertFalse(patch["translator/enable_user_dict"])
            self.assertEqual(patch["__include"], "grammar:/hant")
            self.assertEqual(patch["translator/initial_quality"], 1.2)

    def test_preserving_mode_creates_only_user_dictionary_override(self):
        custom = self.root / "nested" / "luna.custom.yaml"
        benchmark_env.merge_disable_user_dict_patch(
            custom, preserve_translator_defaults=True)
        self.assertEqual(self.read_yaml(custom), {
            "patch": {"translator/enable_user_dict": False}})

    def test_legacy_mode_still_injects_all_benchmark_translator_settings(self):
        custom = self.write_file("legacy.custom.yaml", """metadata: keep
patch:
  __include: grammar:/hant
  translator/max_sentences: 999
  translator/max_homophones: 999
  translator/enable_user_dict: true
  menu/page_size: 5
""")
        benchmark_env.merge_disable_user_dict_patch(custom)
        data = self.read_yaml(custom)
        self.assertEqual(data["metadata"], "keep")
        self.assertEqual(data["patch"], {
            "__include": "grammar:/hant", "menu/page_size": 5,
            **benchmark_env.PATCH_TRANSLATOR_SETTINGS,
        })

    def test_prepare_removes_userdbs_but_preserves_schema_dictionary_and_model(self):
        user_dir = self.root / "user"
        originals = {
            "luna_pinyin.schema.yaml": "schema: original\n",
            "luna_pinyin.dict.yaml": "dictionary: original\n",
            "grammar.yaml": "hant: original\n",
            MODEL: "original model bytes",
        }
        for name, content in originals.items():
            self.write_file(f"user/{name}", content)
        db_dir = user_dir / "nested" / "luna.userdb"
        db_dir.mkdir(parents=True)
        (db_dir / "data").write_bytes(b"learned")
        db_file = self.write_file("user/old.userdb", "learned")
        keep = self.write_file("user/keep.txt", "keep")
        self.write_file("user/luna_pinyin_simp.custom.yaml", """patch:
  __include: grammar:/hant
  translator/max_homophones: 8
""")
        result = benchmark_env.prepare_vendor_for_benchmark(
            user_dir, LUNA.schema_id,
            preserve_translator_defaults=LUNA.preserve_translator_defaults)
        self.assertEqual(set(result["userdb_paths_removed"]), {str(db_dir), str(db_file)})
        self.assertFalse(db_dir.exists())
        self.assertFalse(db_file.exists())
        self.assertEqual(keep.read_text(encoding="utf-8"), "keep")
        for name, content in originals.items():
            self.assertEqual((user_dir / name).read_text(encoding="utf-8"), content)
        custom = user_dir / "luna_pinyin_simp.custom.yaml"
        self.assertEqual(result["custom_yaml"], str(custom.resolve()))
        self.assertEqual(self.read_yaml(custom)["patch"], {
            "__include": "grammar:/hant", "translator/enable_user_dict": False})


class InstallerTests(TemporaryRootTest):
    def setUp(self):
        super().setUp()
        self.fixtures = self.root / "fixtures"
        for name, _, _ in setup_luna_octagram.SOURCES:
            self.write_file(f"fixtures/{name}/LICENSE", f"license {name}")
            self.write_file(f"fixtures/{name}/AUTHORS", f"authors {name}")
        self.originals = {
            "luna-pinyin/luna_pinyin.schema.yaml": "schema: upstream luna\n",
            "luna-pinyin/luna_pinyin_simp.schema.yaml": "schema: upstream simp\n",
            "luna-pinyin/luna_pinyin.dict.yaml": "dictionary: traditional upstream\n",
            "prelude/default.yaml": "config_version: upstream\n",
            "essay/essay.txt": "upstream essay\n",
            "stroke/stroke.schema.yaml": "schema: stroke\n",
            "octagram/grammar.yaml": "hant:\n  translator/max_homophones: 7\n",
            f"octagram-hant/{MODEL}": "nonempty traditional model",
        }
        for relative, content in self.originals.items():
            self.write_file(f"fixtures/{relative}", content)
        self.write_file("fixtures/octagram-hant/zh-hans-t-essay-bgw.gram", "wrong model")
        self.write_file("fixtures/luna-pinyin/ignored.bin", "ignore")
        self.write_file("fixtures/luna-pinyin/nested/ignored.yaml", "ignore")

    def run_install(self, *, update=False):
        def fake_git(*args):
            if args[0] == "clone":
                self.assertEqual(args[:4], ("clone", "--depth", "1", "--branch"))
                destination = Path(args[-1])
                source = next(s for s in setup_luna_octagram.SOURCES
                              if s[0] == destination.name)
                self.assertEqual(args[4], source[2])
                self.assertEqual(args[5], f"https://github.com/{source[1]}.git")
                shutil.copytree(self.fixtures / destination.name, destination)
            else:
                self.assertIn(args[2], ("fetch", "checkout"))

        def fake_run(args, **kwargs):
            self.assertEqual(args[:2], ["git", "-C"])
            self.assertEqual(args[3:], ["rev-parse", "HEAD"])
            self.assertTrue(kwargs["check"])
            kwargs["stdout"].write("a" * 40 + "\n")
            return subprocess.CompletedProcess(args, 0)

        with mock.patch.object(setup_luna_octagram, "git", side_effect=fake_git) as git_mock, \
                mock.patch.object(setup_luna_octagram.subprocess, "run", side_effect=fake_run) as run_mock, \
                redirect_stdout(io.StringIO()):
            target = setup_luna_octagram.install(self.root, update=update)
        return target, git_mock, run_mock

    def test_install_copies_original_assets_model_licenses_and_manifest(self):
        unrelated = self.write_file("vendor/mingyuepinyin/untouched.yaml", "untouched")
        target, git_mock, run_mock = self.run_install()
        self.assertEqual(target, self.root / LUNA.rel_path)
        self.assertEqual(git_mock.call_count, len(setup_luna_octagram.SOURCES))
        self.assertEqual(run_mock.call_count, len(setup_luna_octagram.SOURCES))
        for relative, content in self.originals.items():
            self.assertEqual((target / Path(relative).name).read_text(encoding="utf-8"), content)
        self.assertFalse((target / "zh-hans-t-essay-bgw.gram").exists())
        self.assertFalse((target / "ignored.bin").exists())
        self.assertFalse((target / "nested").exists())
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "untouched")
        for name, _, _ in setup_luna_octagram.SOURCES:
            self.assertEqual((target / "licenses" / name / "LICENSE").read_text(encoding="utf-8"),
                             f"license {name}")
            self.assertEqual((target / "licenses" / name / "AUTHORS").read_text(encoding="utf-8"),
                             f"authors {name}")
        self.assertEqual(self.read_yaml(target / "luna_pinyin.custom.yaml"), {
            "patch": {"__include": "grammar:/hant", "translator/enable_user_dict": False}})
        self.assertEqual(self.read_yaml(target / "luna_pinyin_simp.custom.yaml"), {
            "patch": {"translator/enable_user_dict": False}})
        self.assertEqual(self.read_yaml(target / "default.custom.yaml"), {
            "patch": {"schema_list": [{"schema": "luna_pinyin_simp"}]}})
        manifest = json.loads((target / "upstream_versions.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest, [
            {"repository": repository, "branch": branch, "commit": "a" * 40}
            for _, repository, branch in setup_luna_octagram.SOURCES])
        self.assertEqual(benchmark_sentences._filter_unavailable_vendors(self.root, [LUNA]), [LUNA])

    def test_cached_install_does_not_clone_or_fetch_without_update(self):
        self.run_install()
        _, git_mock, run_mock = self.run_install()
        git_mock.assert_not_called()
        self.assertEqual(run_mock.call_count, len(setup_luna_octagram.SOURCES))

    def test_update_fetches_each_cached_branch_and_checks_out_fetch_head(self):
        self.run_install()
        _, git_mock, _ = self.run_install(update=True)
        expected = []
        for name, _, branch in setup_luna_octagram.SOURCES:
            checkout = str(self.root / ".cache" / "luna-octagram" / name)
            expected.extend([
                mock.call("-C", checkout, "fetch", "--depth", "1", "origin", branch),
                mock.call("-C", checkout, "checkout", "--detach", "FETCH_HEAD"),
            ])
        self.assertEqual(git_mock.call_args_list, expected)

    def test_install_rejects_missing_model(self):
        (self.fixtures / "octagram-hant" / MODEL).unlink()
        with self.assertRaisesRegex(RuntimeError, "Missing or empty Octagram model"):
            self.run_install()
        self.assertFalse((LUNA.data_dir(self.root) / "upstream_versions.json").exists())

    def test_install_rejects_empty_model(self):
        (self.fixtures / "octagram-hant" / MODEL).write_bytes(b"")
        with self.assertRaisesRegex(RuntimeError, "Missing or empty Octagram model"):
            self.run_install()


class VendorAvailabilityTests(TemporaryRootTest):
    def populate_required_files(self):
        for name in LUNA.required_files:
            self.write_file(f"{LUNA.rel_path}/{name}")

    def test_missing_model_fails_fast_even_with_available_legacy_vendor(self):
        self.populate_required_files()
        (LUNA.data_dir(self.root) / MODEL).unlink()
        legacy = VendorConfig("legacy", "vendor/legacy", "legacy")
        legacy.data_dir(self.root).mkdir(parents=True)
        with self.assertRaises(SystemExit) as raised:
            benchmark_sentences._filter_unavailable_vendors(self.root, [legacy, LUNA])
        self.assertIn(LUNA.key, str(raised.exception))
        self.assertIn(MODEL, str(raised.exception))
        self.assertIn("python scripts/setup_luna_octagram.py", str(raised.exception))

    def test_missing_install_directory_has_actionable_setup_hint(self):
        with self.assertRaises(SystemExit) as raised:
            benchmark_sentences._filter_unavailable_vendors(self.root, [LUNA])
        self.assertIn("python scripts/setup_luna_octagram.py", str(raised.exception))

    def test_complete_install_is_available(self):
        self.populate_required_files()
        self.assertEqual(benchmark_sentences._filter_unavailable_vendors(self.root, [LUNA]), [LUNA])

    def test_legacy_optional_with_gram_vendor_remains_skippable(self):
        legacy = VendorConfig("legacy", "vendor/legacy", "legacy")
        optional = VendorConfig("legacy_with_gram", "vendor/optional", "legacy")
        legacy.data_dir(self.root).mkdir(parents=True)
        with self.assertLogs(benchmark_sentences.logger, level="WARNING"):
            actual = benchmark_sentences._filter_unavailable_vendors(self.root, [legacy, optional])
        self.assertEqual(actual, [legacy])


class RequiredModuleTests(TemporaryRootTest):
    def run_switch(self, dll):
        LUNA.data_dir(self.root).mkdir(parents=True)
        wrapper = mock.Mock(dll=dll)
        runner = rime_runner.RimeDistroRunner(Path("unused.dll"))
        with mock.patch.object(rime_runner, "RimeDllWrapper", return_value=wrapper):
            runner.switch_distro(LUNA, self.root)
        return wrapper, runner

    def test_missing_module_export_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "RimeFindModule is unavailable"):
            self.run_switch(object())

    def test_missing_octagram_is_rejected(self):
        dll = mock.Mock()
        dll.RimeFindModule.return_value = None
        with self.assertRaisesRegex(RuntimeError, "requires librime-octagram"):
            self.run_switch(dll)

    def test_registered_octagram_allows_initialization(self):
        dll = mock.Mock()
        dll.RimeFindModule.return_value = 123
        wrapper, runner = self.run_switch(dll)
        dll.RimeFindModule.assert_called_once_with(b"octagram")
        wrapper.initialize.assert_called_once()
        runner.close()


if __name__ == "__main__":
    unittest.main()
