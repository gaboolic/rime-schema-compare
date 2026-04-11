"""Split corpus text and build pinyin strings for Rime."""

from __future__ import annotations

import re
from typing import List

from pypinyin import Style, lazy_pinyin

# Chinese and ASCII comma / full stop / period
_SPLIT_RE = re.compile(r"[，,。.]+")

# 片段在去掉首尾空白后须「全部为汉字」才参与评测（含数字、拉丁字母、符号则丢弃）
_HANZI_ONLY_RE = re.compile(r"^[\u4e00-\u9fff]+$")

# 分句后：含 ASCII 数字或英文字母的片段不参与评测（与「纯汉字」规则一致，单独检测便于统计）
_ASCII_DIGIT_OR_LETTER_RE = re.compile(r"[0-9A-Za-z]")

# 纯汉字片段至少含多少个字才参与评测
MIN_EVAL_HANZI_CHARS = 5

# Remove common punctuation and whitespace; keep Hanzi, Latin, digits as needed
_PUNCT_RE = re.compile(
    r"[\s·…！!？?；;：:\"\"''「」『』（）()\[\]【】《》<>、．·—\-—]+"
)


def split_sentences(text: str) -> List[str]:
    parts = _SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def is_pure_hanzi_segment(s: str) -> bool:
    """True iff non-empty and every codepoint is a CJK unified ideograph (no digit/letter/symbol)."""
    t = s.strip()
    return bool(t) and bool(_HANZI_ONLY_RE.fullmatch(t))


def segment_has_ascii_digit_or_letter(s: str) -> bool:
    """True if segment contains ASCII digit or Latin letter (after strip, any position)."""
    return bool(_ASCII_DIGIT_OR_LETTER_RE.search(s.strip()))


def extract_hanzi(s: str) -> str:
    return "".join(re.findall(r"[\u4e00-\u9fff]", s))


def strip_inner_punct(s: str) -> str:
    return _PUNCT_RE.sub("", s)


def sentence_to_continuous_pinyin(s: str) -> str:
    """Lowercase contiguous pinyin, Hanzi only (reproducible baseline)."""
    hz = extract_hanzi(s)
    if not hz:
        return ""
    syllables = lazy_pinyin(hz, style=Style.NORMAL, errors="ignore")
    return "".join(syllables).lower()
