"""Paths and defaults for Rime DLL and vendor distributions."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class VendorConfig:
    """One Rime distribution checkout (git submodule path)."""

    key: str
    rel_path: str
    schema_id: str

    def data_dir(self, root: Optional[Path] = None) -> Path:
        base = root or repo_root()
        return (base / self.rel_path).resolve()


# Default schema ids match each distro's main full-pinyin schema file names.
DEFAULT_VENDORS: List[VendorConfig] = [
    VendorConfig("rime_frost", "vendor/rime-frost", "rime_frost"),
    VendorConfig("rime_ice", "vendor/rime-ice", "rime_ice"),
    VendorConfig("wanxiang", "vendor/rime_wanxiang", "wanxiang"),
]


def default_rime_dll_candidates() -> List[Path]:
    """Common Weasel install locations on Windows."""
    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    roots = [Path(program_files), Path(program_files_x86)]
    out: List[Path] = []
    for root in roots:
        weasel = root / "Rime"
        if weasel.is_dir():
            for sub in weasel.glob("weasel-*"):
                dll = sub / "rime.dll"
                if dll.is_file():
                    out.append(dll)
        dll_flat = root / "Rime" / "rime.dll"
        if dll_flat.is_file():
            out.append(dll_flat)
    return out


def resolve_rime_dll(explicit: Optional[str] = None) -> Path:
    if explicit:
        p = Path(explicit)
        if p.is_file():
            return p.resolve()
        raise FileNotFoundError(f"RIME_DLL path is not a file: {explicit}")
    env = os.environ.get("RIME_DLL", "").strip()
    if env:
        return resolve_rime_dll(env)
    for c in default_rime_dll_candidates():
        if c.is_file():
            return c.resolve()
    raise FileNotFoundError(
        "Could not find rime.dll. Set environment variable RIME_DLL to the full path "
        "(e.g. Weasel install folder)."
    )
