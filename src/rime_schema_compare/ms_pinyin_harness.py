"""Black-box Windows Pinyin IME automation via Windows APIs."""

from __future__ import annotations

import ctypes
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set


if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

user32 = ctypes.WinDLL("user32", use_last_error=True)
imm32 = ctypes.WinDLL("imm32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

SW_RESTORE = 9
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
WM_SETTEXT = 0x000C
WM_CLOSE = 0x0010
WM_INPUTLANGCHANGEREQUEST = 0x0050
WM_CHAR = 0x0102
KEYEVENTF_KEYUP = 0x0002
KLF_ACTIVATE = 0x00000001
VK_SPACE = 0x20
VK_ESCAPE = 0x1B

PREFERRED_EDIT_CLASSES = {
    "Edit",
    "RichEdit20W",
    "RichEdit50W",
    "RichEditD2DPT",
    "TextInputHostWindow",
}


LPARAM = ctypes.c_longlong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_long


@dataclass
class BlackboxDecodeResult:
    prediction: str
    ok: bool
    reason: str


def _wait_until(predicate, timeout_s: float, poll_s: float = 0.05) -> bool:
    deadline = time.perf_counter() + timeout_s
    while time.perf_counter() < deadline:
        if predicate():
            return True
        time.sleep(poll_s)
    return False


class WindowsPinyinImeHarness:
    """Drive a foreground Windows Pinyin IME in a Notepad window."""

    def __init__(
        self,
        *,
        host_command: Optional[List[str]] = None,
        launch_timeout_s: float = 10.0,
        settle_timeout_s: float = 3.0,
        inter_key_delay_s: float = 0.012,
        commit_delay_s: float = 0.12,
        probe_input: str = "a",
        max_prepare_attempts: int = 2,
    ) -> None:
        self.host_command = host_command or ["notepad.exe"]
        self.launch_timeout_s = launch_timeout_s
        self.settle_timeout_s = settle_timeout_s
        self.inter_key_delay_s = inter_key_delay_s
        self.commit_delay_s = commit_delay_s
        self.probe_input = probe_input
        self.max_prepare_attempts = max(1, max_prepare_attempts)
        self._proc: Optional[subprocess.Popen[str]] = None
        self._window_hwnd: Optional[int] = None
        self._edit_hwnd: Optional[int] = None
        self._window_pid: Optional[int] = None
        self._layout_hkl: Optional[int] = None

    @property
    def process_pid(self) -> Optional[int]:
        return self._proc.pid if self._proc is not None else None

    def start(self) -> None:
        if self._proc is not None and self._window_hwnd and self._edit_hwnd:
            return
        baseline = set(self._candidate_top_windows())
        self._proc = subprocess.Popen(self.host_command)
        ok = _wait_until(lambda: self._refresh_window_handles(baseline), timeout_s=self.launch_timeout_s)
        if not ok:
            raise RuntimeError("notepad_window_not_found")
        self.reset_host()

    def close(self) -> None:
        if self._edit_hwnd:
            try:
                user32.SendMessageW(self._edit_hwnd, WM_SETTEXT, 0, "")
            except Exception:
                pass
        if self._window_hwnd:
            try:
                user32.PostMessageW(self._window_hwnd, WM_CLOSE, 0, 0)
            except Exception:
                pass
        if self._proc is not None:
            try:
                self._proc.wait(timeout=0.5)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
        self._proc = None
        self._window_hwnd = None
        self._edit_hwnd = None
        self._window_pid = None

    def reset_host(self) -> None:
        if not self._refresh_window_handles():
            raise RuntimeError("host_window_unavailable")
        self._focus_host()
        self._press_escape()
        user32.SendMessageW(self._edit_hwnd, WM_SETTEXT, 0, "")
        time.sleep(0.05)

    def self_check(self) -> None:
        if not self._refresh_window_handles():
            raise RuntimeError("host_window_unavailable")
        self.reset_host()
        if not self._ensure_chinese_mode():
            raise RuntimeError("ime_not_ready")
        user32.SendMessageW(self._edit_hwnd, WM_SETTEXT, 0, "abc")
        time.sleep(0.05)
        committed = self._read_host_text().strip()
        if committed != "abc":
            raise RuntimeError(f"host_ascii_probe_failed:{committed!r}")
        self.reset_host()

    def decode(self, raw_input: str) -> BlackboxDecodeResult:
        if not raw_input:
            return BlackboxDecodeResult("", False, "empty_input")
        try:
            self.reset_host()
        except Exception as exc:
            return BlackboxDecodeResult("", False, f"reset_failed:{exc}")
        if not self._ensure_chinese_mode():
            return BlackboxDecodeResult("", False, "ime_not_ready")
        self.reset_host()
        self._focus_host()
        try:
            self._send_ascii_keys(raw_input)
            time.sleep(self.commit_delay_s)
            self._press_space()
            committed = self._wait_for_committed_text().strip()
        except Exception as exc:
            return BlackboxDecodeResult("", False, f"send_keys_failed:{exc}")
        if not committed:
            return BlackboxDecodeResult("", False, "empty_committed_text")
        lowered = committed.lower().strip()
        if lowered == raw_input.lower() or lowered == (raw_input.lower() + " "):
            return BlackboxDecodeResult(committed, False, "ime_not_in_chinese_mode")
        return BlackboxDecodeResult(committed, True, "ok")

    def _refresh_window_handles(self, baseline_hwnds: Optional[Set[int]] = None) -> bool:
        if self._window_hwnd and user32.IsWindow(self._window_hwnd):
            hwnd = self._window_hwnd
        else:
            hwnd = None
        if not hwnd and self._proc is not None and self._proc.poll() is None:
            hwnd = self._find_main_window_for_pid(self._proc.pid)
        if not hwnd:
            hwnd = self._find_new_top_window(baseline_hwnds or set())
        if not hwnd:
            return False
        edit_hwnd = self._find_text_control(hwnd)
        if not edit_hwnd:
            return False
        proc_id = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
        self._window_hwnd = hwnd
        self._edit_hwnd = edit_hwnd
        self._window_pid = int(proc_id.value) if proc_id.value else None
        return True

    def _find_main_window_for_pid(self, pid: int) -> Optional[int]:
        found: List[int] = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, LPARAM)
        def enum_proc(hwnd, _lparam):
            if not user32.IsWindowVisible(hwnd):
                return True
            proc_id = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
            if proc_id.value != pid:
                return True
            if user32.GetWindow(hwnd, 4):  # GW_OWNER
                return True
            found.append(int(hwnd))
            return False

        user32.EnumWindows(enum_proc, 0)
        return found[0] if found else None

    def _candidate_top_windows(self) -> List[int]:
        found: List[int] = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, LPARAM)
        def enum_proc(hwnd, _lparam):
            if not user32.IsWindowVisible(hwnd):
                return True
            class_name = self._class_name(int(hwnd))
            if class_name != "Notepad":
                return True
            found.append(int(hwnd))
            return True

        user32.EnumWindows(enum_proc, 0)
        return found

    def _find_new_top_window(self, baseline_hwnds: Set[int]) -> Optional[int]:
        current = self._candidate_top_windows()
        for hwnd in current:
            if hwnd not in baseline_hwnds:
                return hwnd
        fg = int(user32.GetForegroundWindow() or 0)
        if fg and self._class_name(fg) == "Notepad":
            return fg
        return current[0] if current else None

    def _find_text_control(self, parent_hwnd: int) -> Optional[int]:
        matches: List[int] = []

        def scan(hwnd: int) -> None:
            children: List[int] = []

            @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, LPARAM)
            def enum_proc(child_hwnd, _lparam):
                children.append(int(child_hwnd))
                return True

            user32.EnumChildWindows(hwnd, enum_proc, 0)
            for child in children:
                class_name = self._class_name(child)
                if class_name in PREFERRED_EDIT_CLASSES:
                    matches.append(child)
                scan(child)

        scan(parent_hwnd)
        if matches:
            return matches[0]
        return None

    def _class_name(self, hwnd: int) -> str:
        buf = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, buf, len(buf))
        return buf.value

    def _focus_host(self) -> None:
        if not self._window_hwnd or not self._edit_hwnd:
            raise RuntimeError("host_window_unavailable")
        user32.ShowWindow(self._window_hwnd, SW_RESTORE)
        user32.SetForegroundWindow(self._window_hwnd)
        time.sleep(0.05)
        user32.SetForegroundWindow(self._edit_hwnd)
        time.sleep(0.05)

    def _ensure_chinese_mode(self) -> bool:
        for _ in range(self.max_prepare_attempts):
            try:
                self._focus_host()
                self._activate_chinese_layout()
                self._open_ime()
                time.sleep(0.08)
                if self._probe_hanzi_commit():
                    return True
            finally:
                try:
                    self.reset_host()
                except Exception:
                    pass
        return False

    def _activate_chinese_layout(self) -> None:
        if not self._window_hwnd:
            raise RuntimeError("host_window_unavailable")
        hkl = user32.LoadKeyboardLayoutW("00000804", KLF_ACTIVATE)
        if not hkl:
            raise RuntimeError("load_zh_cn_layout_failed")
        self._layout_hkl = int(hkl)
        user32.PostMessageW(self._window_hwnd, WM_INPUTLANGCHANGEREQUEST, 0, self._layout_hkl)
        if self._edit_hwnd:
            user32.PostMessageW(self._edit_hwnd, WM_INPUTLANGCHANGEREQUEST, 0, self._layout_hkl)

    def _open_ime(self) -> None:
        if not self._edit_hwnd:
            return
        himc = imm32.ImmGetContext(self._edit_hwnd)
        if not himc:
            return
        try:
            imm32.ImmSetOpenStatus(himc, True)
        finally:
            imm32.ImmReleaseContext(self._edit_hwnd, himc)

    def _probe_hanzi_commit(self) -> bool:
        self.reset_host()
        self._focus_host()
        self._send_ascii_keys(self.probe_input)
        time.sleep(self.commit_delay_s)
        self._press_space()
        committed = self._wait_for_committed_text().strip()
        if not committed:
            return False
        if committed.lower() == self.probe_input.lower():
            return False
        return any("\u4e00" <= ch <= "\u9fff" for ch in committed)

    def _send_ascii_keys(self, text: str) -> None:
        for ch in text:
            if not ch.isascii() or not ch.isprintable():
                raise ValueError(f"unsupported_key:{ch!r}")
            vk = ord(ch.upper())
            self._send_vk(vk)
            time.sleep(self.inter_key_delay_s)

    def _press_space(self) -> None:
        self._send_vk(VK_SPACE)

    def _press_escape(self) -> None:
        self._send_vk(VK_ESCAPE)

    def _send_vk(self, vk: int) -> None:
        user32.keybd_event(vk, 0, 0, 0)
        time.sleep(0.005)
        user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

    def _wait_for_committed_text(self) -> str:
        stable = ""
        stable_count = 0
        deadline = time.perf_counter() + self.settle_timeout_s
        while time.perf_counter() < deadline:
            current = self._read_host_text().strip()
            if current and current == stable:
                stable_count += 1
                if stable_count >= 2:
                    return current
            else:
                stable = current
                stable_count = 0
            time.sleep(0.05)
        return self._read_host_text()

    def _read_host_text(self) -> str:
        if not self._edit_hwnd:
            raise RuntimeError("host_window_unavailable")
        length = int(user32.SendMessageW(self._edit_hwnd, WM_GETTEXTLENGTH, 0, 0))
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.SendMessageW(self._edit_hwnd, WM_GETTEXT, length + 1, buf)
        return buf.value


# Backward-compatible alias for older imports.
MicrosoftPinyinHarness = WindowsPinyinImeHarness
