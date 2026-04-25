#!/usr/bin/env python3
"""
Benchmark fengyun_qiaoma whole-sentence decoding with shape-code inputs.

The input generation follows the wubi sentence benchmark: split corpus into
Hanzi-only segments, read the single-character shape dictionary, take each
character's code before the first semicolon, concatenate those codes, then feed
the full string to librime.

Usage (repo root):

  python scripts/benchmark_fengyun_qiaoma.py
  python scripts/benchmark_fengyun_qiaoma.py --corpus data/corpus/news.txt
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import benchmark_sentences as bench
from rime_schema_compare.config import VendorConfig, repo_root, resolve_rime_dll, shared_data_dir


logger = logging.getLogger("benchmark_fengyun_qiaoma")


def fengyun_qiaoma_vendor() -> VendorConfig:
    return VendorConfig(
        "fengyun_qiaoma",
        "vendor/fengyun_qiaoma",
        "fyzj",
        input_mode="shape_code_head",
        input_dict_rel_path="fyzjgy2.dict.yaml",
    )


def _setup_logging() -> None:
    bench._setup_logging()
    if logger.handlers:
        return
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _corpus_files(root: Path, corpus_args: List[Path] | None) -> List[Tuple[Path, str]]:
    if not corpus_args:
        corpora = bench.default_corpus_files(root)
        if not corpora:
            raise SystemExit(f"No *.txt found under {root / 'data' / 'corpus'}")
        return corpora

    corpora: List[Tuple[Path, str]] = []
    for corpus in corpus_args:
        path = corpus if corpus.is_absolute() else root / corpus
        if not path.is_file():
            raise SystemExit(f"Corpus not found: {path}")
        corpora.append((path.resolve(), path.stem))
    return corpora


def main() -> None:
    _setup_logging()
    p = argparse.ArgumentParser(description="fengyun_qiaoma whole-sentence benchmark")
    p.add_argument(
        "--corpus",
        type=Path,
        nargs="*",
        default=None,
        help="UTF-8 text file(s). Omit to run all *.txt under data/corpus/.",
    )
    p.add_argument(
        "--label",
        type=str,
        default="",
        help="Tag for results when a single --corpus is given; ignored for multi-corpus runs.",
    )
    p.add_argument("--out-dir", type=Path, default=Path("artifacts"), help="Output directory")
    p.add_argument("--rime-dll", type=str, default="", help="Override rime.dll path")
    p.add_argument("--progress-every", type=int, default=50, help="Print progress every N raw segments (0=off)")
    p.add_argument(
        "--eval-synonyms",
        type=Path,
        default=None,
        help="同义词评测 JSON（默认 data/eval_synonyms.json；文件不存在则用内置规则）",
    )
    args = p.parse_args()

    root = repo_root()
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    dll = resolve_rime_dll(args.rime_dll or None)
    vendor = fengyun_qiaoma_vendor()
    vendors = bench._filter_unavailable_vendors(root, [vendor])
    syn_cfg, syn_path = bench._init_eval_synonyms(root, args.eval_synonyms)
    corpora = _corpus_files(root, args.corpus)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    logger.info("[启动] 仓库根目录: %s", root)
    logger.info("[启动] rime.dll: %s", dll)
    logger.info("[启动] shared_data_dir: %s", shared_data_dir(root))
    logger.info(
        "[启动] 方案: %s(schema=%s), 单字码表=%s, 每字取第一个分号前编码",
        vendor.key,
        vendor.schema_id,
        vendor.input_dict_rel_path,
    )
    logger.info("[评测] 同义词归一化: %s", syn_cfg.summary_line())

    if len(corpora) == 1:
        corpus_path, stem = corpora[0]
        label = args.label or stem
        base = f"benchmark_fengyun_qiaoma_{label}_{stamp}"
        payload = bench.run_benchmark(
            corpus_path=corpus_path,
            out_dir=out_dir,
            rime_dll=dll,
            vendors=vendors,
            corpus_label=label,
            progress_every=args.progress_every,
            eval_synonyms=syn_cfg,
            eval_synonyms_path=syn_path,
            write_artifacts=True,
            stamp=stamp,
            artifact_base=base,
        )
        print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
        logger.info("[结束] 单语料评测完成 | 输出前缀: %s | 输出目录: %s", base, out_dir.resolve())
        return

    if args.label:
        logger.warning("[启动] --label 在多语料模式下会被忽略")

    logger.info("[流程] 多语料模式: 共 %d 个语料，逐个运行 fengyun_qiaoma", len(corpora))
    all_rows: List[Dict[str, Any]] = []
    summary_by_corpus: Dict[str, Dict[str, Any]] = {}
    corpus_files: Dict[str, str] = {}
    timings_by_corpus: Dict[str, Dict[str, Any]] = {}
    t_wall = time.perf_counter()

    for idx, (corpus_path, stem) in enumerate(corpora, start=1):
        logger.info("[大步骤 %d/%d] 语料 «%s»", idx, len(corpora), stem)
        part = bench.run_benchmark(
            corpus_path=corpus_path,
            out_dir=out_dir,
            rime_dll=dll,
            vendors=vendors,
            corpus_label=stem,
            progress_every=args.progress_every,
            eval_synonyms=syn_cfg,
            eval_synonyms_path=syn_path,
            write_artifacts=False,
            stamp=stamp,
        )
        all_rows.extend(part["per_sentence"])
        summary_by_corpus[stem] = part["summary"]
        corpus_files[stem] = str(corpus_path)
        timings_by_corpus[stem] = part.get("timings") or {}

    summary_overall = bench._aggregate_summaries(summary_by_corpus, vendors)
    base = f"benchmark_fengyun_qiaoma_all_corpus_{stamp}"
    payload = {
        "generated_at_utc": stamp,
        "corpus_mode": "all",
        "corpus_files": corpus_files,
        "rime_dll": str(dll),
        "vendors": [asdict(v) for v in vendors],
        "summary_by_corpus": summary_by_corpus,
        "summary_overall": summary_overall,
        "per_sentence": all_rows,
        "timings_by_corpus": timings_by_corpus,
        "eval_synonyms": {
            "config_path": str(syn_path.resolve()) if syn_path.is_file() else None,
            "rules_summary": syn_cfg.summary_line(),
        },
    }
    bench._write_combined_artifacts(out_dir, stamp, base, payload, vendors, wall_clock_start=t_wall)
    logger.info("[结束] 多语料评测完成 | 输出前缀: %s | 输出目录: %s", base, out_dir.resolve())


if __name__ == "__main__":
    main()
