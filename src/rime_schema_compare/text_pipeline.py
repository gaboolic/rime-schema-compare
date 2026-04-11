"""Split corpus text and build pinyin strings for Rime."""

from __future__ import annotations

import re
from typing import List

from pypinyin import Style, lazy_pinyin

# Chinese and ASCII comma / full stop / period
_SPLIT_RE = re.compile(r"[，,。.]+")

# Remove common punctuation and whitespace; keep Hanzi, Latin, digits as needed
_PUNCT_RE = re.compile(
    r"[\s·…！!？?；;：:\"\"''「」『』（）()\[\]【】《》<>、．·—\-—]+"
)


def split_sentences(text: str) -> List[str]:
    parts = _SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


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
