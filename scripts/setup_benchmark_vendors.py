#!/usr/bin/env python3
"""Prepare all default benchmark vendors from updated submodules and verified models.

Run after git submodule update. This does not fetch/change base submodule commits.
It overwrites upstream snapshot files and managed benchmark custom patches only;
unrelated files, browser sessions and user databases are never deleted.
"""
from __future__ import annotations

import argparse
import hashlib
from http.client import HTTPException
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
from rime_schema_compare.config import DEFAULT_VENDORS

# Import by path so both direct CLI execution and importlib-based tests work.
_spec = importlib.util.spec_from_file_location("benchmark_setup_luna", Path(__file__).with_name("setup_luna_octagram.py"))
setup_luna_octagram = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(setup_luna_octagram)

MODEL_NAME = "wanxiang-lts-zh-hans.gram"
MODEL_REPOSITORY = "amzxyz/rime-wanxiang-data"
MODEL_RELEASE_API = f"https://api.github.com/repos/{MODEL_REPOSITORY}/releases/tags/LTS"
HTTP_TIMEOUT = 60
HTTP_RETRIES = 3
CHUNK_SIZE = 1024 * 1024
# Base directory, derived directory, schema, repository, branch.
PAIRS = (
    ("rime-frost", "rime-frost_with_gram", "rime_frost", "gaboolic/rime-frost", "master"),
    ("rime-ice", "rime-ice_with_gram", "rime_ice", "iDvel/rime-ice", "main"),
    ("rime_wanxiang", "rime_wanxiang_with_gram", "wanxiang", "amzxyz/rime_wanxiang", "wanxiang"),
    ("rime-wubi-sentence", "rime-wubi-sentence_with_gram", "wubi86", "gaboolic/rime-wubi-sentence", "master"),
)
LUNA_SOURCES = ("luna-pinyin", "prelude", "essay", "stroke")
EXCLUDED_PARTS = {".git", ".cache", ".venv", "build", "artifacts", "__pycache__", "sync", "logs", "downloads"}
EXCLUDED_FILES = {"installation.yaml", "user.yaml", "upstream_versions.json", "model_versions.json"}
EXCLUDED_SUFFIXES = {".gram", ".bin", ".log", ".pyc", ".zip", ".7z", ".exe", ".dll", ".dylib", ".so"}


def write_json(path: Path, data) -> None:
    path = safe_destination(path.parent, PurePosixPath(path.name))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_member_path(name: str) -> PurePosixPath:
    """Validate archive paths using Windows-safe rules on every host."""
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    reserved = {"CON", "PRN", "AUX", "NUL"} | {f"{prefix}{n}" for prefix in ("COM", "LPT") for n in range(1, 10)}
    if (not normalized or path.is_absolute() or ":" in normalized
            or any(ord(char) < 32 or char in '<>"|?*' for char in normalized)
            or any(part in {"..", "."} or part.endswith((" ", "."))
                   or part.split(".")[0].upper() in reserved for part in path.parts)):
        raise ValueError(f"Unsafe archive member: {name!r}")
    return path


def snapshot_file_selected(path: PurePosixPath) -> bool:
    parts = [part.lower() for part in path.parts]
    return not (
        any(part in EXCLUDED_PARTS or ".userdb" in part for part in parts)
        or path.name.lower() in EXCLUDED_FILES
        or path.name.lower().endswith(".custom.yaml")
        or path.suffix.lower() in EXCLUDED_SUFFIXES
    )


def safe_destination(target: Path, relative: PurePosixPath) -> Path:
    if target.is_symlink():
        raise ValueError(f"Refusing symlink snapshot target: {target}")
    destination = target.joinpath(*relative.parts)
    # Existing directory/file links and Windows junctions must not redirect writes.
    cursor = destination
    while True:
        if cursor.is_symlink() or getattr(cursor, "is_junction", lambda: False)():
            raise ValueError(f"Refusing linked snapshot destination: {destination}")
        if cursor == target:
            break
        if cursor == cursor.parent:
            raise ValueError(f"Snapshot destination escapes target: {destination}")
        cursor = cursor.parent
    if not destination.resolve().is_relative_to(target.resolve()):
        raise ValueError(f"Snapshot destination escapes target: {destination}")
    return destination


def extract_snapshot(archive: Path, target: Path) -> list[str]:
    """Copy selected regular files; never use ZipFile.extract/extractall."""
    selected = []
    with zipfile.ZipFile(archive) as bundle:
        # Validate the complete archive before overwriting any snapshot files.
        entries = []
        for member in bundle.infolist():
            relative = safe_member_path(member.filename)
            mode = member.external_attr >> 16
            if stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError(f"Non-regular archive member: {member.filename!r}")
            if member.is_dir() or not snapshot_file_selected(relative):
                continue
            entries.append((member, safe_destination(target, relative)))
        for member, destination in entries:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(member) as source, destination.open("wb") as output:
                shutil.copyfileobj(source, output)
            selected.append(member.filename)
    return selected


def git_text(source: Path, *arguments: str) -> str:
    # File-backed stdout works on Windows hosts that disallow piped child stdio.
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as output:
        subprocess.run(["git", "-C", str(source), *arguments], check=True, stdout=output)
        output.seek(0)
        return output.read().strip()


def copy_git_snapshot(source: Path, target: Path, cache: Path) -> str:
    if not source.is_dir() or Path(git_text(source, "rev-parse", "--show-toplevel")).resolve() != source.resolve():
        raise RuntimeError(f"Base vendor is not an initialized Git checkout: {source}")
    commit = git_text(source, "rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise RuntimeError(f"Invalid source commit for {source}")
    if (target / ".git").exists():
        # A tracked variant is a real submodule on a clean Actions checkout.
        # Its gitlink must identify the same source actually copied/evaluated.
        if Path(git_text(target, "rev-parse", "--show-toplevel")).resolve() != target.resolve():
            raise RuntimeError(f"Variant Git pointer refers to a different checkout: {target}")
        if git_text(target, "rev-parse", "HEAD") != commit:
            subprocess.run(["git", "-C", str(target), "fetch", "--no-tags", str(source), commit], check=True)
            # Never force away local tracked edits: a conflicting checkout fails.
            subprocess.run(["git", "-C", str(target), "checkout", "--detach", commit], check=True)
        if git_text(target, "rev-parse", "HEAD") != commit:
            raise RuntimeError(f"Variant HEAD does not match benchmark source: {target}")
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / f"{source.name}-{commit}.zip"
    subprocess.run(["git", "-C", str(source), "archive", "--format=zip", "--output", str(archive), commit], check=True)
    extract_snapshot(archive, target)
    return commit


def benchmark_patch(schema: str, *, with_model: bool) -> dict:
    patch = {"translator/enable_user_dict": False,
             "translator/max_sentences": 3, "translator/max_homophones": 8}
    if not with_model:
        patch["grammar/language"] = ""
    elif schema != "wanxiang":
        grammar = {"language": "wanxiang-lts-zh-hans", "collocation_max_length": 5, "collocation_min_length": 2}
        if schema in {"rime_frost", "wubi86"}:
            grammar.update(non_collocation_penalty=-4, collocation_penalty=-14)
        patch.update(grammar=grammar)
        patch["translator/contextual_suggestions"] = True
        patch["translator/max_homographs"] = 7 if schema == "luna_pinyin_simp" else 2
    # Wanxiang's language, contextual_suggestions and grammar weights are
    # deliberately inherited unchanged from the exact upstream schema.
    return patch


def prepare_patches(directory: Path, schema: str, *, with_model: bool = False, original_luna: bool = False) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    patch = {"translator/enable_user_dict": False} if original_luna else benchmark_patch(schema, with_model=with_model)
    custom = safe_destination(directory, PurePosixPath(f"{schema}.custom.yaml"))
    default = safe_destination(directory, PurePosixPath("default.custom.yaml"))
    custom.write_text(yaml.safe_dump({"patch": patch}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    default.write_text(yaml.safe_dump({"patch": {"schema_list": [{"schema": schema}]}}, sort_keys=False), encoding="utf-8")


def request(url: str, *, binary: bool = False):
    headers = {"User-Agent": "rime-schema-compare-benchmark-setup", "Accept": "application/octet-stream" if binary else "application/vnd.github+json"}
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=HTTP_TIMEOUT)


def model_asset_metadata() -> dict:
    for attempt in range(HTTP_RETRIES + 1):
        try:
            with request(MODEL_RELEASE_API) as response:
                payload = response.read(4 * CHUNK_SIZE + 1)
            if len(payload) > 4 * CHUNK_SIZE:
                raise ValueError("Oversized release metadata")
            release = json.loads(payload)
            if not isinstance(release, dict) or not isinstance(release.get("assets"), list):
                raise ValueError("Invalid release metadata shape")
            assets = [asset for asset in release["assets"] if isinstance(asset, dict) and asset.get("name") == MODEL_NAME]
            if len(assets) != 1:
                raise ValueError("LTS release must contain exactly one requested model")
            asset = assets[0]
            digest = asset.get("digest", "")
            if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", digest):
                raise ValueError("LTS asset has no valid SHA-256 digest")
            if type(asset.get("size")) is not int or asset["size"] <= 0 or type(asset.get("id")) is not int or asset["id"] <= 0:
                raise ValueError("LTS asset has invalid size or id")
            if asset.get("state", "uploaded") != "uploaded":
                raise ValueError("LTS asset upload is incomplete")
            return {"name": MODEL_NAME, "repository": MODEL_REPOSITORY, "release_tag": "LTS",
                    "asset_id": asset["id"], "size": asset["size"], "sha256": digest[7:].lower(),
                    "updated_at": asset.get("updated_at"), "release_api_url": MODEL_RELEASE_API,
                    "asset_api_url": f"https://api.github.com/repos/{MODEL_REPOSITORY}/releases/assets/{asset['id']}"}
        except (OSError, HTTPException, ValueError, KeyError, TypeError):
            if attempt == HTTP_RETRIES:
                raise RuntimeError("Unable to obtain valid current LTS model metadata from official GitHub API") from None
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


def valid_model(path: Path, metadata: dict) -> bool:
    return path.is_file() and path.stat().st_size == metadata["size"] and file_sha256(path) == metadata["sha256"]


def download_model(root: Path, metadata: dict) -> Path:
    cache = root / ".cache" / "benchmark-models"
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / f"{Path(MODEL_NAME).stem}-{metadata['sha256']}.gram"
    if valid_model(destination, metadata):
        return destination
    for attempt in range(HTTP_RETRIES + 1):
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=cache, prefix="model-", suffix=".part", delete=False) as output:
                temporary = Path(output.name)
                size = 0
                with request(metadata["asset_api_url"], binary=True) as response:
                    while block := response.read(CHUNK_SIZE):
                        size += len(block)
                        if size > metadata["size"]:
                            raise ValueError("Downloaded model exceeds expected size")
                        output.write(block)
            if not valid_model(temporary, metadata):
                raise ValueError("Downloaded model failed size/SHA-256 verification")
            temporary.replace(destination)
            return destination
        except (OSError, HTTPException, ValueError):
            if attempt == HTTP_RETRIES:
                raise RuntimeError("Unable to download and verify current LTS model from official GitHub asset API") from None
            time.sleep(2 ** attempt)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    raise AssertionError("unreachable")


def copy_model(source: Path, target: Path, metadata: dict) -> None:
    destination = safe_destination(target, PurePosixPath(MODEL_NAME))
    shutil.copy2(source, destination)
    if not valid_model(destination, metadata):
        raise RuntimeError(f"Installed model failed size/SHA-256 verification: {target.name}")


def copy_luna_resources(root: Path, target: Path) -> None:
    for name in LUNA_SOURCES:
        checkout = root / ".cache" / "luna-octagram" / name
        if not checkout.is_dir() or not (checkout / "LICENSE").is_file():
            raise RuntimeError(f"Missing official Luna source cache or license: {checkout}")
        for source in checkout.iterdir():
            if not source.is_file() or source.is_symlink():
                continue
            if source.name in {"LICENSE", "AUTHORS"}:
                relative = PurePosixPath("licenses", name, source.name)
            elif source.suffix in {".yaml", ".txt"} and snapshot_file_selected(PurePosixPath(source.name)):
                relative = PurePosixPath(source.name)
            else:
                continue
            destination = safe_destination(target, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def install(root: Path = ROOT) -> None:
    root = root.resolve()
    # Always refresh metadata, even when a verified content-addressed cache exists.
    # Network/metadata errors must stop preparation, never select an older model.
    metadata = model_asset_metadata()
    model = download_model(root, metadata)
    original = setup_luna_octagram.install(root, update=True)
    prepare_patches(original, "luna_pinyin_simp", original_luna=True)
    original_versions = json.loads((original / "upstream_versions.json").read_text(encoding="utf-8"))
    luna_versions = [item for item in original_versions if item["repository"] in {
        "rime/rime-luna-pinyin", "rime/rime-prelude", "rime/rime-essay", "rime/rime-stroke"}]
    if len(luna_versions) != 4:
        raise RuntimeError("Incomplete official Luna source manifest")
    hant = original / "zh-hant-t-essay-bgw.gram"
    hant_sources = [item for item in original_versions if item["repository"] == "lotem/rime-octagram-data" and item["branch"] == "hant"]
    if len(hant_sources) != 1 or not hant.is_file() or hant.stat().st_size == 0:
        raise RuntimeError("Incomplete original hant model or provenance")
    write_json(original / "model_versions.json", {"models": [{"name": hant.name, "size": hant.stat().st_size,
               "sha256": file_sha256(hant), "repository": "lotem/rime-octagram-data", "branch": "hant",
               "commit": hant_sources[0]["commit"]}]})
    prepared = {"luna_pinyin_with_octagram"}
    for name, with_model in (("mingyuepinyin", False), ("mingyuepinyin_with_gram", True)):
        target = root / "vendor" / name
        copy_luna_resources(root, target)
        prepare_patches(target, "luna_pinyin_simp", with_model=with_model)
        write_json(target / "upstream_versions.json", luna_versions)
        write_json(target / "model_versions.json", {"models": [metadata] if with_model else []})
        if with_model:
            copy_model(model, target, metadata)
        prepared.add(name)
    for base_name, variant_name, schema, repository, branch in PAIRS:
        base, variant = root / "vendor" / base_name, root / "vendor" / variant_name
        commit = copy_git_snapshot(base, variant, root / ".cache" / "benchmark-snapshots")
        versions = [{"repository": repository, "branch": branch, "commit": commit}]
        for directory, with_model in ((base, False), (variant, True)):
            if not (directory / f"{schema}.schema.yaml").is_file():
                raise RuntimeError(f"Missing benchmark schema: {directory / (schema + '.schema.yaml')}")
            prepare_patches(directory, schema, with_model=with_model)
            write_json(directory / "upstream_versions.json", versions)
            write_json(directory / "model_versions.json", {"models": [metadata] if with_model else []})
            if with_model:
                copy_model(model, directory, metadata)
        prepared.update(v.key for v in DEFAULT_VENDORS if Path(v.rel_path).name in {base_name, variant_name})
    if prepared != {v.key for v in DEFAULT_VENDORS}:
        raise RuntimeError("Setup profiles do not cover all DEFAULT_VENDORS")
    for vendor in DEFAULT_VENDORS:
        directory = vendor.data_dir(root)
        if not (directory / f"{vendor.schema_id}.schema.yaml").is_file():
            raise RuntimeError(f"Missing schema for {vendor.key}")
        dictionary = vendor.input_dict_path(root)
        if dictionary is not None and not dictionary.is_file():
            raise RuntimeError(f"Missing input dictionary for {vendor.key}: {dictionary}")
    print(f"Prepared {len(prepared)} benchmark vendors; verified LTS model SHA-256: {metadata['sha256']}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository checkout root (default: this repository)")
    args = parser.parse_args(argv)
    install(args.root)


if __name__ == "__main__":
    main()
