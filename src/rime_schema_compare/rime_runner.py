"""Thin wrapper: one RimeDllWrapper instance, switch distro dirs between vendors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from .call_librime import RimeDllWrapper
from .config import VendorConfig


@dataclass
class DecodeResult:
    prediction: str
    ok: bool
    reason: str


class RimeDistroRunner:
    """
    For each vendor directory: initialize Rime (shared + user data = that dir),
    then decode pinyin strings by creating a fresh session per sentence.
    """

    def __init__(self, dll_path: Path) -> None:
        self._dll_path = Path(dll_path)
        self._rime: Optional[RimeDllWrapper] = None
        self._data_dir: Optional[Path] = None
        self._schema_id: Optional[str] = None

    def close(self) -> None:
        if self._rime is not None:
            try:
                self._rime.finalize()
            finally:
                self._rime = None
                self._data_dir = None
                self._schema_id = None

    def switch_distro(self, vendor: VendorConfig, root: Optional[Path] = None) -> None:
        data_dir = vendor.data_dir(root)
        if not data_dir.is_dir():
            raise FileNotFoundError(f"Vendor data directory missing: {data_dir}")
        if self._rime is not None and self._data_dir == data_dir and self._schema_id == vendor.schema_id:
            return
        self.close()
        rime = RimeDllWrapper(dll_path=str(self._dll_path))
        rime.initialize(
            app_name="rime.schema.compare",
            shared_data_dir=str(data_dir),
            user_data_dir=str(data_dir),
        )
        self._rime = rime
        self._data_dir = data_dir
        self._schema_id = vendor.schema_id

    def decode_pinyin(self, pinyin: str, schema_id: Optional[str] = None) -> DecodeResult:
        if self._rime is None or self._data_dir is None:
            return DecodeResult("", False, "rime_not_initialized")
        sid = schema_id or self._schema_id or ""
        session_id = self._rime.create_session()
        if not session_id:
            return DecodeResult("", False, "create_session_failed")
        try:
            if not self._rime.select_schema(session_id, sid):
                return DecodeResult("", False, "select_schema_failed")
            if not self._rime.simulate_key_sequence(session_id, pinyin):
                return DecodeResult("", False, "simulate_key_failed")
            ctx = self._rime.get_context(session_id)
            if not ctx:
                return DecodeResult("", False, "no_context")
            preview = (ctx.get("commit_text_preview") or "").strip()
            cands: List[dict] = ctx.get("candidates") or []
            top = (cands[0].get("text") or "").strip() if cands else ""
            text = preview or top
            if not text:
                return DecodeResult("", False, "empty_prediction")
            return DecodeResult(text, True, "ok")
        finally:
            self._rime.destroy_session(session_id)
