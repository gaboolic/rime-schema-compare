"""Offline vendor-preparation tests: temporary fixtures only, no real Git/network."""
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

import yaml

SPEC = importlib.util.spec_from_file_location("setup_benchmark_vendors", Path(__file__).resolve().parents[1] / "scripts/setup_benchmark_vendors.py")
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)
MODEL_BYTES = b"verified model fixture\x00\x01"


def asset():
    return {"name": setup.MODEL_NAME, "id": 123, "size": len(MODEL_BYTES),
            "digest": "sha256:" + hashlib.sha256(MODEL_BYTES).hexdigest(),
            "state": "uploaded", "updated_at": "2026-11-14T15:43:32Z"}


def metadata():
    source = asset()
    return {"name": setup.MODEL_NAME, "repository": setup.MODEL_REPOSITORY,
            "release_tag": "LTS", "asset_id": source["id"], "size": source["size"],
            "sha256": source["digest"][7:], "updated_at": source["updated_at"],
            "release_api_url": setup.MODEL_RELEASE_API,
            "asset_api_url": f"https://api.github.com/repos/{setup.MODEL_REPOSITORY}/releases/assets/123"}


class TemporaryRoot(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def write(self, relative, content="fixture"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def yaml(self, path):
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def archive(self, entries):
        path = self.root / "snapshot.zip"
        with zipfile.ZipFile(path, "w") as bundle:
            for name, content in entries.items():
                bundle.writestr(name, content)
        return path


class SnapshotTests(TemporaryRoot):
    def test_only_upstream_runtime_files_are_copied_and_unrelated_files_survive(self):
        target = self.root / "target"
        unrelated = self.write("target/personal-notes.txt", "untouched")
        local_git = self.write("target/.git", "local git pointer")
        local_db = self.write("target/personal.userdb/000003.log", "learned")
        archive = self.archive({
            "main.schema.yaml": "schema: upstream", "lua/data/table.txt": "runtime data",
            "opencc/map.ocd2": b"opencc", "LICENSE": "license",
            ".git": "bad pointer", ".git/config": "bad config", "build/main.table.bin": "old",
            "artifacts/report.txt": "local", "main.userdb/data": "learned",
            "main.userdb.old/file": "old learned", "nested/user.yaml": "state",
            "installation.yaml": "state", "grammar.gram": "old model",
            "other.custom.yaml": "old patch", "lua/__pycache__/x.pyc": "bytecode",
            "upstream_versions.json": "old provenance", "model_versions.json": "old model metadata",
        })
        copied = setup.extract_snapshot(archive, target)
        self.assertEqual(set(copied), {"main.schema.yaml", "lua/data/table.txt", "opencc/map.ocd2", "LICENSE"})
        self.assertEqual(unrelated.read_text(), "untouched")
        self.assertEqual(local_git.read_text(), "local git pointer")
        self.assertEqual(local_db.read_text(), "learned")
        self.assertFalse((target / "grammar.gram").exists())

    def test_path_traversal_absolute_drive_and_backslash_paths_are_rejected(self):
        for name in ("../escape.txt", "/absolute.txt", "C:/escape.txt", "dir\\..\\escape.txt", "dir/file:stream", "dir./file", "NUL.txt", "dir/COM1", "dir/bad|name"):
            with self.subTest(name=name):
                archive = self.archive({"safe.txt": "must not be copied", name: "bad"})
                target = self.root / "target"
                with self.assertRaises(ValueError):
                    setup.extract_snapshot(archive, target)
                self.assertFalse((target / "safe.txt").exists())

    def test_archive_symlinks_are_rejected_before_any_writes(self):
        archive = self.root / "symlink.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("safe.txt", "safe")
            info = zipfile.ZipInfo("linked")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            bundle.writestr(info, "../outside")
        with self.assertRaisesRegex(ValueError, "Non-regular"):
            setup.extract_snapshot(archive, self.root / "target")
        self.assertFalse((self.root / "target/safe.txt").exists())

    def test_existing_destination_link_is_rejected(self):
        archive = self.archive({"linked/file.txt": "bad"})
        target = self.root / "target"
        target.mkdir()
        outside = self.root / "outside"
        outside.mkdir()
        try:
            (target / "linked").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Host does not permit directory symlinks")
        with self.assertRaisesRegex(ValueError, "linked"):
            setup.extract_snapshot(archive, target)
        self.assertFalse((outside / "file.txt").exists())

    def test_git_archive_uses_exact_source_commit_and_no_checkout_copy(self):
        source = self.root / "vendor/base"
        source.mkdir(parents=True)
        target = self.root / "vendor/variant"
        fixture = self.archive({"main.schema.yaml": "upstream", ".git": "exclude"})
        commit = "a" * 40
        def fake_run(arguments, **kwargs):
            output_path = Path(arguments[arguments.index("--output") + 1])
            shutil.copy2(fixture, output_path)
            self.assertEqual(arguments[-1], commit)
        with mock.patch.object(setup, "git_text", side_effect=[str(source), commit]), \
                mock.patch.object(setup.subprocess, "run", side_effect=fake_run) as run:
            self.assertEqual(setup.copy_git_snapshot(source, target, self.root / "cache"), commit)
        self.assertEqual(run.call_args.args[0][3:5], ["archive", "--format=zip"])
        self.assertFalse((target / ".git").exists())
        self.assertEqual((target / "main.schema.yaml").read_text(), "upstream")

    def test_variant_head_is_aligned_to_exact_base_commit_before_archive(self):
        source = self.root / 'base'
        target = self.root / 'variant'
        source.mkdir()
        self.write('variant/.git', 'gitdir: fixture')
        commit = 'a' * 40
        archive = self.archive({'main.schema.yaml': 'upstream'})
        def fake_run(arguments, **kwargs):
            if 'archive' in arguments:
                shutil.copy2(archive, Path(arguments[arguments.index('--output') + 1]))
        with mock.patch.object(setup, 'git_text', side_effect=[str(source), commit, str(target), 'b' * 40, commit]), \
                mock.patch.object(setup.subprocess, 'run', side_effect=fake_run) as run:
            self.assertEqual(setup.copy_git_snapshot(source, target, self.root / 'cache'), commit)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(commands[0], ['git', '-C', str(target), 'fetch', '--no-tags', str(source), commit])
        self.assertEqual(commands[1], ['git', '-C', str(target), 'checkout', '--detach', commit])
        self.assertIn('archive', commands[2])

    def test_real_git_variant_tracks_evaluated_commit_and_removes_newer_only_files(self):
        source = self.root / 'base'
        target = self.root / 'variant'
        def git(directory, *args):
            subprocess.run(['git', '-C', str(directory), *args], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        source.mkdir()
        git(source, 'init')
        git(source, 'config', 'user.name', 'Offline Test')
        git(source, 'config', 'user.email', 'test@example.invalid')
        path = source / 'main.schema.yaml'
        path.write_text('version A\n', encoding='utf-8')
        git(source, 'add', '.')
        git(source, '-c', 'commit.gpgsign=false', 'commit', '-m', 'A')
        commit_a = setup.git_text(source, 'rev-parse', 'HEAD')
        path.write_text('version B\n', encoding='utf-8')
        (source / 'newer-only.txt').write_text('B only', encoding='utf-8')
        git(source, 'add', '.')
        git(source, '-c', 'commit.gpgsign=false', 'commit', '-m', 'B')
        subprocess.run(['git', 'clone', '--no-hardlinks', str(source), str(target)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        git(source, 'checkout', '--detach', commit_a)
        notes = target / 'personal-notes.txt'
        notes.write_text('keep', encoding='utf-8')
        self.assertEqual(setup.copy_git_snapshot(source, target, self.root / 'cache'), commit_a)
        self.assertEqual(setup.git_text(target, 'rev-parse', 'HEAD'), commit_a)
        self.assertEqual((target / 'main.schema.yaml').read_text(encoding='utf-8'), 'version A\n')
        self.assertFalse((target / 'newer-only.txt').exists())
        self.assertEqual(notes.read_text(encoding='utf-8'), 'keep')

    def test_shared_variant_git_pointer_is_rejected_without_mutation(self):
        source = self.root / 'base'
        target = self.root / 'variant'
        source.mkdir()
        self.write('variant/.git', 'gitdir: wrong shared pointer')
        with mock.patch.object(setup, 'git_text', side_effect=[str(source), 'a' * 40, str(source)]), \
                mock.patch.object(setup.subprocess, 'run') as run:
            with self.assertRaisesRegex(RuntimeError, 'different checkout'):
                setup.copy_git_snapshot(source, target, self.root / 'cache')
        run.assert_not_called()

    def test_missing_submodule_cannot_fall_back_to_parent_repository(self):
        source = self.root / "vendor/empty"
        source.mkdir(parents=True)
        with mock.patch.object(setup, "git_text", return_value=str(self.root)):
            with self.assertRaisesRegex(RuntimeError, "initialized Git checkout"):
                setup.copy_git_snapshot(source, self.root / "variant", self.root / "cache")


class PatchTests(TemporaryRoot):
    def test_base_profiles_have_no_language_model_and_no_user_dictionary(self):
        for schema in ("rime_frost", "rime_ice", "wanxiang", "wubi86", "luna_pinyin_simp"):
            with self.subTest(schema=schema):
                patch = setup.benchmark_patch(schema, with_model=False)
                self.assertEqual(patch, {"translator/enable_user_dict": False,
                    "translator/max_sentences": 3, "translator/max_homophones": 8, "grammar/language": ""})

    def test_frost_and_wubi_use_exact_current_penalties(self):
        for schema in ("rime_frost", "wubi86"):
            patch = setup.benchmark_patch(schema, with_model=True)
            self.assertEqual(patch["grammar"], {"language": "wanxiang-lts-zh-hans",
                "collocation_max_length": 5, "collocation_min_length": 2,
                "non_collocation_penalty": -4, "collocation_penalty": -14})
            self.assertEqual(patch["translator/max_homographs"], 2)
            self.assertTrue(patch["translator/contextual_suggestions"])

    def test_ice_and_mingyue_do_not_inject_extra_penalties(self):
        for schema, homographs in (("rime_ice", 2), ("luna_pinyin_simp", 7)):
            patch = setup.benchmark_patch(schema, with_model=True)
            self.assertEqual(patch["grammar"], {"language": "wanxiang-lts-zh-hans",
                                              "collocation_max_length": 5, "collocation_min_length": 2})
            self.assertEqual(patch["translator/max_homographs"], homographs)

    def test_wanxiang_preserves_all_upstream_model_and_contextual_settings(self):
        patch = setup.benchmark_patch("wanxiang", with_model=True)
        self.assertEqual(patch, {"translator/enable_user_dict": False,
                               "translator/max_sentences": 3, "translator/max_homophones": 8})

    def test_managed_patches_remove_stale_settings_and_deploy_selected_schema(self):
        directory = self.root / "copy"
        self.write("copy/rime_ice.custom.yaml", "patch:\n  grammar/language: old\n  stale: true\n")
        unrelated = self.write("copy/my-personal.custom.yaml", "keep")
        setup.prepare_patches(directory, "rime_ice", with_model=True)
        self.assertEqual(self.yaml(directory / "rime_ice.custom.yaml")["patch"], setup.benchmark_patch("rime_ice", with_model=True))
        self.assertEqual(self.yaml(directory / "default.custom.yaml"), {"patch": {"schema_list": [{"schema": "rime_ice"}]}})
        self.assertEqual(unrelated.read_text(), "keep")

    def test_original_luna_preserves_upstream_translator_parameters(self):
        target = self.root / "original"
        setup.prepare_patches(target, "luna_pinyin_simp", original_luna=True)
        self.assertEqual(self.yaml(target / "luna_pinyin_simp.custom.yaml"), {"patch": {"translator/enable_user_dict": False}})


class ModelTests(TemporaryRoot):
    def test_metadata_uses_official_api_and_whitelists_no_credentials(self):
        release = {"assets": [dict(asset(), uploader={"token": "never-save"})]}
        with mock.patch.object(setup, "request", return_value=io.BytesIO(json.dumps(release).encode())) as request:
            result = setup.model_asset_metadata()
        request.assert_called_once_with(setup.MODEL_RELEASE_API)
        self.assertEqual(result, metadata())
        self.assertNotIn("never-save", json.dumps(result))

    def test_missing_digest_incomplete_upload_bad_size_or_wrong_asset_fail(self):
        invalid_assets = [dict(asset(), digest=None), dict(asset(), digest="md5:bad"),
                          dict(asset(), size=0), dict(asset(), state="new"), dict(asset(), name="other.gram")]
        for invalid in invalid_assets:
            with self.subTest(asset=invalid), mock.patch.object(setup, "request", side_effect=lambda *a, **k: io.BytesIO(json.dumps({"assets": [invalid]}).encode())), mock.patch.object(setup.time, "sleep"):
                with self.assertRaisesRegex(RuntimeError, "valid current LTS model metadata"):
                    setup.model_asset_metadata()

    def test_metadata_network_errors_retry_three_times_and_sanitize_errors(self):
        with mock.patch.object(setup, "request", side_effect=OSError("https://secret?token=DO-NOT-LOG")) as request, mock.patch.object(setup.time, "sleep"):
            with self.assertRaises(RuntimeError) as raised:
                setup.model_asset_metadata()
        self.assertEqual(request.call_count, 4)
        self.assertNotIn("DO-NOT-LOG", str(raised.exception))

    def test_download_streams_official_asset_and_checks_digest(self):
        with mock.patch.object(setup, "request", return_value=io.BytesIO(MODEL_BYTES)) as request:
            path = setup.download_model(self.root, metadata())
        request.assert_called_once_with(metadata()["asset_api_url"], binary=True)
        self.assertTrue(setup.valid_model(path, metadata()))
        self.assertIn("benchmark-models", path.parts)
        self.assertIn(metadata()["sha256"], path.name)
        self.assertFalse(list(path.parent.glob("*.part")))

    def test_valid_content_addressed_cache_avoids_repeated_asset_download(self):
        with mock.patch.object(setup, "request", return_value=io.BytesIO(MODEL_BYTES)):
            path = setup.download_model(self.root, metadata())
        with mock.patch.object(setup, "request", side_effect=AssertionError("No asset network expected")):
            self.assertEqual(setup.download_model(self.root, metadata()), path)

    def test_invalid_cache_is_not_returned_and_download_failure_does_not_use_old_model(self):
        with mock.patch.object(setup, "request", return_value=io.BytesIO(MODEL_BYTES)):
            path = setup.download_model(self.root, metadata())
        path.write_bytes(b"bad")
        unrelated = self.write(".cache/benchmark-models/personal.txt", "keep")
        with mock.patch.object(setup, "request", side_effect=OSError("failed")) as request, mock.patch.object(setup.time, "sleep"):
            with self.assertRaisesRegex(RuntimeError, "download and verify current LTS"):
                setup.download_model(self.root, metadata())
        self.assertEqual(request.call_count, 4)
        self.assertFalse(setup.valid_model(path, metadata()))
        self.assertEqual(unrelated.read_text(), "keep")
        self.assertFalse(list(path.parent.glob("*.part")))

    def test_truncated_wrong_hash_html_and_oversized_downloads_all_fail(self):
        for content in (MODEL_BYTES[:-1], b"x" * len(MODEL_BYTES), b"<html>error</html>", MODEL_BYTES + b"extra"):
            with self.subTest(content=content), mock.patch.object(setup, "request", side_effect=lambda *a, **k: io.BytesIO(content)), mock.patch.object(setup.time, "sleep"):
                with self.assertRaisesRegex(RuntimeError, "download and verify"):
                    setup.download_model(self.root, metadata())
        self.assertFalse(list((self.root / ".cache/benchmark-models").glob("*.gram")))
        self.assertFalse(list((self.root / ".cache/benchmark-models").glob("*.part")))

    def test_incomplete_http_stream_retries_and_removes_partial_files(self):
        from http.client import IncompleteRead
        class BrokenResponse(io.BytesIO):
            def read(self, *args):
                raise IncompleteRead(b"partial", 99)
        with mock.patch.object(setup, "request", side_effect=lambda *a, **k: BrokenResponse()) as request, mock.patch.object(setup.time, "sleep"):
            with self.assertRaisesRegex(RuntimeError, "download and verify"):
                setup.download_model(self.root, metadata())
        self.assertEqual(request.call_count, 4)
        self.assertFalse(list((self.root / ".cache/benchmark-models").glob("*.part")))

    def test_hash_validation_checks_both_size_and_content(self):
        path = self.root / "model"
        path.write_bytes(MODEL_BYTES)
        self.assertTrue(setup.valid_model(path, metadata()))
        path.write_bytes(b"x" * len(MODEL_BYTES))
        self.assertFalse(setup.valid_model(path, metadata()))
        path.write_bytes(MODEL_BYTES[:-1])
        self.assertFalse(setup.valid_model(path, metadata()))

    def test_request_uses_binary_accept_header_and_finite_timeout(self):
        with mock.patch.object(setup.urllib.request, "urlopen") as open_url:
            setup.request(metadata()["asset_api_url"], binary=True)
        request = open_url.call_args.args[0]
        self.assertEqual(request.get_header("Accept"), "application/octet-stream")
        self.assertEqual(open_url.call_args.kwargs["timeout"], setup.HTTP_TIMEOUT)
        self.assertNotIn("Authorization", dict(request.header_items()))


class InstallationTests(TemporaryRoot):
    def fake_luna_install(self, root, *, update):
        self.assertTrue(update)
        originals = root / "vendor/luna_pinyin_with_octagram"
        originals.mkdir(parents=True, exist_ok=True)
        for name in setup.LUNA_SOURCES:
            self.write(f".cache/luna-octagram/{name}/LICENSE", f"license {name}")
            self.write(f".cache/luna-octagram/{name}/AUTHORS", f"authors {name}")
        for filename in ("luna_pinyin.schema.yaml", "luna_pinyin_simp.schema.yaml", "luna_pinyin.dict.yaml"):
            self.write(f".cache/luna-octagram/luna-pinyin/{filename}", "original upstream")
            self.write(f"vendor/luna_pinyin_with_octagram/{filename}", "original upstream")
        self.write(".cache/luna-octagram/prelude/default.yaml", "upstream defaults")
        self.write(".cache/luna-octagram/essay/essay.txt", "original essay")
        self.write(".cache/luna-octagram/stroke/stroke.dict.yaml", "original stroke")
        self.write(".cache/luna-octagram/luna-pinyin/old.gram", "must not copy")
        self.write(".cache/luna-octagram/luna-pinyin/user.yaml", "must not copy")
        self.write("vendor/luna_pinyin_with_octagram/luna_pinyin.custom.yaml", "patch:\n  __include: grammar:/hant\n")
        self.write("vendor/luna_pinyin_with_octagram/zh-hant-t-essay-bgw.gram", "original hant bytes")
        versions = [{"repository": repo, "branch": branch, "commit": "a" * 40}
                    for _, repo, branch in setup.setup_luna_octagram.SOURCES]
        setup.write_json(originals / "upstream_versions.json", versions)
        return originals

    def fake_snapshot(self, source, target, cache):
        self.assertIn(self.root, source.parents)
        pair = next(pair for pair in setup.PAIRS if pair[0] == source.name)
        schema = pair[2]
        self.write(f"vendor/{source.name}/{schema}.schema.yaml", "upstream schema unchanged")
        self.write(f"vendor/{target.name}/{schema}.schema.yaml", "upstream schema unchanged")
        if schema == "wubi86":
            self.write(f"vendor/{source.name}/program/wubi86.dict.yaml", "input table")
            self.write(f"vendor/{target.name}/program/wubi86.dict.yaml", "input table")
        return "b" * 40

    def test_full_preparation_covers_all_eleven_vendors_and_all_five_model_copies(self):
        model = self.root / "model.gram"
        model.write_bytes(MODEL_BYTES)
        with mock.patch.object(setup, "model_asset_metadata", return_value=metadata()) as fetch_metadata, \
                mock.patch.object(setup, "download_model", return_value=model), \
                mock.patch.object(setup.setup_luna_octagram, "install", side_effect=self.fake_luna_install) as install_luna, \
                mock.patch.object(setup, "copy_git_snapshot", side_effect=self.fake_snapshot) as snapshot, \
                redirect_stdout(io.StringIO()):
            setup.install(self.root)
        fetch_metadata.assert_called_once()
        install_luna.assert_called_once_with(self.root.resolve(), update=True)
        self.assertEqual(snapshot.call_count, 4)
        with_models = []
        for vendor in setup.DEFAULT_VENDORS:
            directory = vendor.data_dir(self.root)
            self.assertTrue((directory / "upstream_versions.json").is_file())
            self.assertTrue((directory / "model_versions.json").is_file())
            self.assertEqual(self.yaml(directory / "default.custom.yaml"), {"patch": {"schema_list": [{"schema": vendor.schema_id}]}})
            patch = self.yaml(directory / f"{vendor.schema_id}.custom.yaml")["patch"]
            self.assertFalse(patch["translator/enable_user_dict"])
            if "_with_gram" in vendor.key:
                self.assertEqual((directory / setup.MODEL_NAME).read_bytes(), MODEL_BYTES)
                self.assertEqual(json.loads((directory / "model_versions.json").read_text())["models"], [metadata()])
                with_models.append(vendor.key)
            elif vendor.key == "luna_pinyin_with_octagram":
                self.assertEqual(patch, {"translator/enable_user_dict": False})
                self.assertIn("grammar:/hant", (directory / "luna_pinyin.custom.yaml").read_text())
                self.assertEqual(json.loads((directory / "model_versions.json").read_text())["models"][0]["commit"], "a" * 40)
            else:
                self.assertEqual(patch["grammar/language"], "")
                self.assertEqual(json.loads((directory / "model_versions.json").read_text()), {"models": []})
        self.assertEqual(len(with_models), 5)
        for name in ("mingyuepinyin", "mingyuepinyin_with_gram"):
            directory = self.root / "vendor" / name
            for source in setup.LUNA_SOURCES:
                self.assertEqual((directory / "licenses" / source / "LICENSE").read_text(), f"license {source}")
            self.assertFalse((directory / "old.gram").exists())
            self.assertFalse((directory / "user.yaml").exists())
            self.assertEqual((directory / "luna_pinyin.dict.yaml").read_text(), "original upstream")

    def test_metadata_network_failure_stops_before_any_luna_or_vendor_preparation(self):
        with mock.patch.object(setup, "model_asset_metadata", side_effect=RuntimeError("network unavailable")), \
                mock.patch.object(setup.setup_luna_octagram, "install") as install_luna:
            with self.assertRaisesRegex(RuntimeError, "network unavailable"):
                setup.install(self.root)
        install_luna.assert_not_called()
        self.assertFalse((self.root / "vendor").exists())

    def test_luna_resources_require_original_license(self):
        for name in setup.LUNA_SOURCES:
            (self.root / ".cache/luna-octagram" / name).mkdir(parents=True)
        with self.assertRaisesRegex(RuntimeError, "license"):
            setup.copy_luna_resources(self.root, self.root / "target")

    def test_cli_accepts_explicit_root_without_running_live_setup(self):
        with mock.patch.object(setup, "install") as install:
            setup.main(["--root", str(self.root)])
        install.assert_called_once_with(self.root)


if __name__ == "__main__":
    unittest.main()
