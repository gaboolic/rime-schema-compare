#!/usr/bin/env python3
"""Install upstream Luna Pinyin + original hant Octagram, without modifying other vendors."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
# Branches are recorded along with resolved commits in upstream_versions.json.
SOURCES = (
    ("luna-pinyin", "rime/rime-luna-pinyin", "master"),
    ("prelude", "rime/rime-prelude", "master"),
    ("essay", "rime/rime-essay", "master"),
    ("stroke", "rime/rime-stroke", "master"),
    ("octagram", "lotem/rime-octagram-data", "master"),
    ("octagram-hant", "lotem/rime-octagram-data", "hant"),
)


def git(*args: str) -> None:
    subprocess.run(["git", *args], check=True)


def install(root: Path, *, update: bool = False) -> Path:
    cache = root / ".cache" / "luna-octagram"
    target = root / "vendor" / "luna_pinyin_with_octagram"
    target.mkdir(parents=True, exist_ok=True)
    snapshots = []
    for name, repository, branch in SOURCES:
        checkout = cache / name
        url = f"https://github.com/{repository}.git"
        if not checkout.exists():
            checkout.parent.mkdir(parents=True, exist_ok=True)
            git("clone", "--depth", "1", "--branch", branch, url, str(checkout))
        elif update:
            git("-C", str(checkout), "fetch", "--depth", "1", "origin", branch)
            git("-C", str(checkout), "checkout", "--detach", "FETCH_HEAD")
        # Use a file rather than a pipe so this also works in confined Windows hosts.
        revision_file = cache / f"{name}.revision"
        with revision_file.open("w", encoding="utf-8") as stream:
            subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                           check=True, stdout=stream)
        snapshots.append({"repository": repository, "branch": branch,
                          "commit": revision_file.read_text(encoding="utf-8").strip()})
        for source in checkout.iterdir():
            if source.is_file() and (source.suffix in {".yaml", ".txt", ".gram"}
                                     or source.name in {"LICENSE", "AUTHORS"}):
                if source.suffix == ".gram" and source.name != "zh-hant-t-essay-bgw.gram":
                    continue
                if source.name in {"LICENSE", "AUTHORS"}:
                    destination = target / "licenses" / name / source.name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                else:
                    destination = target / source.name
                shutil.copy2(source, destination)
    # Luna already includes grammar:/hant. Explicitly retain that upstream preset;
    # simp only changes output conversion, NOT the traditional dictionary/model.
    (target / "luna_pinyin.custom.yaml").write_text(
        "patch:\n  __include: grammar:/hant\n  translator/enable_user_dict: false\n",
        encoding="utf-8",
    )
    (target / "luna_pinyin_simp.custom.yaml").write_text(
        "patch:\n  translator/enable_user_dict: false\n", encoding="utf-8",
    )
    # Maintenance deploys default's schema_list, which upstream prelude does not
    # include the simp variant in. Explicitly deploy the benchmark schema.
    (target / "default.custom.yaml").write_text(
        "patch:\n  schema_list:\n    - schema: luna_pinyin_simp\n", encoding="utf-8",
    )
    model = target / "zh-hant-t-essay-bgw.gram"
    if not model.is_file() or model.stat().st_size == 0:
        raise RuntimeError(f"Missing or empty Octagram model: {model}")
    manifest = target / "upstream_versions.json"
    manifest.write_text(json.dumps(snapshots, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Installed Luna Pinyin + hant Octagram: {target}\nUpstream versions: {manifest}")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="Fetch latest upstream commits (otherwise reuse cached snapshots)")
    args = parser.parse_args()
    install(ROOT, update=args.update)


if __name__ == "__main__":
    main()
