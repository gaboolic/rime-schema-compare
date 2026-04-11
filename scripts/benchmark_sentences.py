#!/usr/bin/env python3
"""
Benchmark whole-sentence decoding: split corpus → pinyin → Rime → metrics.

Run from repository root, after `pip install -r requirements.txt` and submodule init:

  set RIME_DLL=C:\\Program Files\\Rime\\weasel-x.y.z\\rime.dll
  python scripts/benchmark_sentences.py --corpus data/corpus/prose.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

try:
    from dotenv import load_dotenv

    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass

from rime_schema_compare.config import DEFAULT_VENDORS, VendorConfig, resolve_rime_dll, repo_root
from rime_schema_compare.metrics import cer_sentence, levenshtein, sentence_exact_match
from rime_schema_compare.rime_runner import RimeDistroRunner
from rime_schema_compare.text_pipeline import extract_hanzi, sentence_to_continuous_pinyin, split_sentences


def _pick_vendors(keys: Optional[List[str]]) -> List[VendorConfig]:
    if not keys:
        return list(DEFAULT_VENDORS)
    keyset = {k.strip().lower() for k in keys}
    out = [v for v in DEFAULT_VENDORS if v.key.lower() in keyset]
    if len(out) != len(keyset):
        found = {v.key.lower() for v in out}
        missing = keyset - found
        raise SystemExit(f"Unknown vendor key(s): {sorted(missing)}. Known: {[v.key for v in DEFAULT_VENDORS]}")
    return out


def run_benchmark(
    corpus_path: Path,
    out_dir: Path,
    rime_dll: Path,
    vendors: List[VendorConfig],
    corpus_label: str,
    progress_every: int,
) -> Dict[str, Any]:
    text = corpus_path.read_text(encoding="utf-8")
    raw_sents = split_sentences(text)

    rows: List[Dict[str, Any]] = []
    stats: Dict[str, Dict[str, Any]] = {}

    runner = RimeDistroRunner(rime_dll)

    for v in vendors:
        stats[v.key] = {
            "sentences_total": 0,
            "skipped_no_hanzi": 0,
            "skipped_no_pinyin": 0,
            "decode_failed": 0,
            "exact_matches": 0,
            "cer_char_total_edits": 0,
            "cer_char_total_gold_len": 0,
        }

    prepared: List[Optional[Dict[str, Any]]] = []
    for i, seg in enumerate(raw_sents):
        gold = extract_hanzi(seg)
        if not gold:
            prepared.append(None)
            for v in vendors:
                stats[v.key]["skipped_no_hanzi"] += 1
            continue
        py = sentence_to_continuous_pinyin(seg)
        if not py:
            prepared.append(None)
            for v in vendors:
                stats[v.key]["skipped_no_pinyin"] += 1
            continue
        prepared.append({"index": i, "gold": gold, "pinyin": py})

    try:
        for v in vendors:
            st = stats[v.key]
            try:
                runner.switch_distro(v)
            except FileNotFoundError as e:
                for slot in prepared:
                    if slot is None:
                        continue
                    rows.append(
                        {
                            "corpus": corpus_label,
                            "index": slot["index"],
                            "vendor": v.key,
                            "gold": slot["gold"],
                            "pinyin": slot["pinyin"],
                            "prediction": "",
                            "exact": False,
                            "cer": None,
                            "error": str(e),
                        }
                    )
                    st["sentences_total"] += 1
                    st["decode_failed"] += 1
                continue

            done = 0
            for slot in prepared:
                if slot is None:
                    continue
                st["sentences_total"] += 1
                res = runner.decode_pinyin(slot["pinyin"])
                pred = res.prediction if res.ok else ""
                gold = slot["gold"]
                if not res.ok:
                    st["decode_failed"] += 1
                exact = res.ok and sentence_exact_match(pred, gold)
                if exact:
                    st["exact_matches"] += 1
                if res.ok and gold:
                    dist = levenshtein(pred, gold)
                    st["cer_char_total_edits"] += dist
                    st["cer_char_total_gold_len"] += len(gold)
                    cer = cer_sentence(pred, gold)
                else:
                    cer = None

                rows.append(
                    {
                        "corpus": corpus_label,
                        "index": slot["index"],
                        "vendor": v.key,
                        "gold": gold,
                        "pinyin": slot["pinyin"],
                        "prediction": pred,
                        "exact": exact,
                        "cer": cer,
                        "error": "" if res.ok else res.reason,
                    }
                )
                done += 1
                if progress_every and done % progress_every == 0:
                    print(
                        f"[{v.key}] decoded {done} sentences",
                        file=sys.stderr,
                    )
    finally:
        runner.close()

    summary: Dict[str, Any] = {}
    for v in vendors:
        st = stats[v.key]
        n = st["sentences_total"]
        exact_rate = (st["exact_matches"] / n) if n else 0.0
        denom = st["cer_char_total_gold_len"]
        macro_cer = (st["cer_char_total_edits"] / denom) if denom else None
        summary[v.key] = {
            **st,
            "sentence_exact_rate": exact_rate,
            "macro_cer_over_gold_chars": macro_cer,
        }

    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = f"benchmark_{corpus_label}_{stamp}"
    json_path = out_dir / f"{base}.json"
    csv_path = out_dir / f"{base}.csv"

    payload = {
        "generated_at_utc": stamp,
        "corpus_file": str(corpus_path),
        "corpus_label": corpus_label,
        "rime_dll": str(rime_dll),
        "vendors": [asdict(v) for v in vendors],
        "summary": summary,
        "per_sentence": rows,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "corpus",
                "index",
                "vendor",
                "gold",
                "pinyin",
                "prediction",
                "exact",
                "cer",
                "error",
            ],
        )
        w.writeheader()
        for row in rows:
            w.writerow(row)

    return payload


def main() -> None:
    p = argparse.ArgumentParser(description="Rime whole-sentence decoding benchmark")
    p.add_argument("--corpus", type=Path, required=True, help="UTF-8 text file")
    p.add_argument(
        "--label",
        type=str,
        default="",
        help="Tag for results (default: corpus file stem)",
    )
    p.add_argument("--out-dir", type=Path, default=Path("artifacts"), help="Output directory")
    p.add_argument("--rime-dll", type=str, default="", help="Override rime.dll path")
    p.add_argument(
        "--vendors",
        nargs="*",
        default=None,
        help="Subset of vendor keys: rime_frost rime_ice wanxiang",
    )
    p.add_argument("--progress-every", type=int, default=50, help="Print progress every N raw segments (0=off)")
    args = p.parse_args()

    root = repo_root()
    corpus = args.corpus if args.corpus.is_absolute() else root / args.corpus
    if not corpus.is_file():
        raise SystemExit(f"Corpus not found: {corpus}")

    dll = resolve_rime_dll(args.rime_dll or None)
    vendors = _pick_vendors(args.vendors)
    label = args.label or corpus.stem
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir

    payload = run_benchmark(
        corpus_path=corpus,
        out_dir=out_dir,
        rime_dll=dll,
        vendors=vendors,
        corpus_label=label,
        progress_every=args.progress_every,
    )

    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
