#!/usr/bin/env python3
"""Benchmark a Windows Pinyin IME via foreground Notepad automation."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

try:
    from dotenv import load_dotenv

    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass

from rime_schema_compare.benchmark_common import (
    accumulate_char_metrics,
    aggregate_summaries,
    default_corpus_files,
    finalize_summary,
    init_eval_synonyms,
    init_stats,
    prepare_corpus_segments,
)
from rime_schema_compare.eval_synonyms import EvalSynonymConfig
from rime_schema_compare.metrics import sentence_exact_match
from rime_schema_compare.ms_pinyin_harness import WindowsPinyinImeHarness
from rime_schema_compare.reporting import (
    summary_csv_rows_for_block,
    write_long_csv,
    write_long_csv_by_sentence,
    write_multi_summary_csv,
    write_report_txt,
    write_scheme_compare_txt,
    write_sentence_grouped_csv,
    write_summary_csv,
)
from rime_schema_compare.text_pipeline import MIN_EVAL_HANZI_CHARS, sentence_to_continuous_pinyin, split_sentences

logger = logging.getLogger("benchmark_windows_ime")


@dataclass(frozen=True)
class BlackboxVendor:
    key: str
    display_name: str
    input_mode: str = "pinyin"


@dataclass(frozen=True)
class ImeProfile:
    ime_key: str
    display_name: str
    engine_display_name: str

    @property
    def vendor(self) -> BlackboxVendor:
        return BlackboxVendor(self.ime_key, self.display_name)

    @property
    def artifact_prefix(self) -> str:
        return f"benchmark_{self.ime_key}"

    @property
    def report_title(self) -> str:
        return f"{self.display_name}黑盒整句评测 — 摘要报告"

    @property
    def compare_title(self) -> str:
        return f"{self.display_name}黑盒整句判对对比"

    @property
    def engine_value(self) -> str:
        return f"{self.engine_display_name} via Notepad automation"

    @property
    def footer_note(self) -> str:
        return (
            f"黑盒口径: 宿主 = Notepad；目标输入法 = {self.display_name}；输入串 = 连续全拼；提交键 = Space；"
            "结果来自 GUI 自动化上屏文本，受系统版本、IME 状态、个性化词频与联网状态影响。"
        )


IME_PROFILES: Dict[str, ImeProfile] = {
    "microsoft_pinyin": ImeProfile("microsoft_pinyin", "微软拼音", "Microsoft Pinyin"),
    "sogou_pinyin": ImeProfile("sogou_pinyin", "搜狗拼音", "Sogou Pinyin"),
}


def _ime_profile(ime_key: str) -> ImeProfile:
    profile = IME_PROFILES.get(ime_key.strip().lower())
    if profile is None:
        known = ", ".join(sorted(IME_PROFILES))
        raise SystemExit(f"Unknown --ime {ime_key!r}. Known values: {known}")
    return profile


def _setup_logging() -> None:
    if logger.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _corpus_inputs(root: Path, explicit_paths: Optional[Sequence[str]]) -> List[Tuple[Path, str]]:
    if explicit_paths:
        out: List[Tuple[Path, str]] = []
        for raw in explicit_paths:
            p = Path(raw)
            if not p.is_absolute():
                p = root / p
            if not p.is_file():
                raise SystemExit(f"Corpus file not found: {raw}")
            out.append((p.resolve(), p.stem))
        return out
    out = default_corpus_files(root)
    if not out:
        raise SystemExit(f"No corpus files under {root / 'data' / 'corpus'}")
    return out


def _write_single_artifacts(
    out_dir: Path,
    base: str,
    payload: Dict[str, Any],
    vendors: Sequence[BlackboxVendor],
    *,
    profile: ImeProfile,
    corpus_label: str,
    corpus_path: Path,
    eval_synonyms: EvalSynonymConfig,
) -> None:
    rows = payload["per_sentence"]
    summary = payload["summary"]
    timings = payload["timings"]
    stamp = payload["generated_at_utc"]
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{base}.json"
    csv_grouped = out_dir / f"{base}.csv"
    csv_long = out_dir / f"{base}_long.csv"
    csv_long_by_sentence = out_dir / f"{base}_long_by_sentence.csv"
    write_sentence_grouped_csv(csv_grouped, rows, vendors)
    write_long_csv(csv_long, rows)
    write_long_csv_by_sentence(csv_long_by_sentence, rows, vendors)
    write_scheme_compare_txt(
        out_dir / f"{base}_scheme_compare.txt",
        generated_utc=stamp,
        mode=f"单语料 ({corpus_label})",
        per_sentence=rows,
        vendors=vendors,
        title=profile.compare_title,
    )
    write_summary_csv(out_dir / f"{base}_summary.csv", summary_csv_rows_for_block(corpus_label, summary, vendors))
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report_txt(
        out_dir / f"{base}_report.txt",
        generated_utc=stamp,
        title=profile.report_title,
        engine_label="黑盒引擎",
        engine_value=profile.engine_value,
        corpus_files={corpus_label: str(corpus_path)},
        summary_by_corpus=None,
        summary_overall=summary,
        vendors=vendors,
        mode=f"单语料 ({corpus_label})",
        timings_one_corpus=timings,
        eval_synonyms_summary=eval_synonyms.summary_line(),
        footer_note=profile.footer_note,
    )


def _write_combined_artifacts(
    out_dir: Path,
    base: str,
    payload: Dict[str, Any],
    vendors: Sequence[BlackboxVendor],
    profile: ImeProfile,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = payload["generated_at_utc"]
    json_path = out_dir / f"{base}.json"
    csv_grouped = out_dir / f"{base}.csv"
    csv_long = out_dir / f"{base}_long.csv"
    csv_long_by_sentence = out_dir / f"{base}_long_by_sentence.csv"
    write_sentence_grouped_csv(csv_grouped, payload["per_sentence"], vendors)
    write_long_csv(csv_long, payload["per_sentence"])
    write_long_csv_by_sentence(csv_long_by_sentence, payload["per_sentence"], vendors)
    write_scheme_compare_txt(
        out_dir / f"{base}_scheme_compare.txt",
        generated_utc=stamp,
        mode="全部语料 (data/corpus/*.txt)",
        per_sentence=payload["per_sentence"],
        vendors=vendors,
        title=profile.compare_title,
    )
    write_multi_summary_csv(
        out_dir / f"{base}_summary.csv",
        payload["summary_by_corpus"],
        payload["summary_overall"],
        vendors,
    )
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report_txt(
        out_dir / f"{base}_report.txt",
        generated_utc=stamp,
        title=profile.report_title,
        engine_label="黑盒引擎",
        engine_value=profile.engine_value,
        corpus_files=payload.get("corpus_files"),
        summary_by_corpus=payload["summary_by_corpus"],
        summary_overall=payload["summary_overall"],
        vendors=vendors,
        mode="全部语料 (data/corpus/*.txt)",
        timings_by_corpus=payload.get("timings_by_corpus"),
        timings_wall_total_ms=payload.get("timings_wall_total_ms"),
        eval_synonyms_summary=(payload.get("eval_synonyms") or {}).get("rules_summary"),
        footer_note=profile.footer_note,
    )


def run_blackbox_benchmark(
    corpus_path: Path,
    out_dir: Path,
    profile: ImeProfile,
    corpus_label: str,
    progress_every: int,
    *,
    eval_synonyms: EvalSynonymConfig,
    eval_synonyms_path: Path,
    harness_kwargs: Dict[str, Any],
    write_artifacts: bool = True,
    stamp: Optional[str] = None,
    artifact_base: Optional[str] = None,
) -> Dict[str, Any]:
    vendor = profile.vendor
    norm = eval_synonyms.normalize
    timings: Dict[str, Any] = {"vendors": {}}
    vendor_keys = [vendor.key]
    stats = init_stats(vendor_keys)

    logger.info("[语料:%s] 读取 UTF-8: %s", corpus_label, corpus_path)
    t0 = time.perf_counter()
    text = corpus_path.read_text(encoding="utf-8")
    timings["read_text_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    logger.info("[语料:%s] 读取完成，耗时 %.2f ms", corpus_label, timings["read_text_ms"])

    t1 = time.perf_counter()
    raw_sents = split_sentences(text)
    timings["split_ms"] = round((time.perf_counter() - t1) * 1000, 2)
    logger.info(
        "[分句] 完成，共 %d 个片段，耗时 %.2f ms",
        len(raw_sents),
        timings["split_ms"],
    )

    logger.info("[预过滤] 开始: 纯汉字、无 ASCII 数字/字母、至少 %d 字", MIN_EVAL_HANZI_CHARS)
    t_prep0 = time.perf_counter()
    prepared_base = prepare_corpus_segments(raw_sents, stats)
    timings["prepare_segments_ms"] = round((time.perf_counter() - t_prep0) * 1000, 2)
    n_prepared = sum(1 for x in prepared_base if x is not None)
    n_skip = len(prepared_base) - n_prepared
    st0 = stats[vendor.key]
    logger.info(
        "[预过滤] 完成: 耗时 %.2f ms | 候选 %d 句 | 跳过 %d 段（混合/非纯汉字或含 ASCII 数字字母: %d，纯汉字但不足 %d 字: %d，无汉字: %d）",
        timings["prepare_segments_ms"],
        n_prepared,
        n_skip,
        st0["skipped_mixed_content"],
        MIN_EVAL_HANZI_CHARS,
        st0["skipped_too_short"],
        st0["skipped_no_hanzi"],
    )

    logger.info("[输入串 %s] 开始: 连续全拼，共 %d 句", vendor.key, n_prepared)
    t_input0 = time.perf_counter()
    prepared_vendor: List[Dict[str, Any]] = []
    for slot in prepared_base:
        if slot is None:
            continue
        raw_input = sentence_to_continuous_pinyin(slot["text"])
        if not raw_input:
            stats[vendor.key]["skipped_no_input"] += 1
            continue
        prepared_vendor.append({"index": slot["index"], "gold": slot["gold"], "input": raw_input})
    input_ms = round((time.perf_counter() - t_input0) * 1000, 2)
    logger.info(
        "[输入串 %s] 完成: 耗时 %.2f ms | 可解码 %d 句 | 缺少输入串 %d 句",
        vendor.key,
        input_ms,
        len(prepared_vendor),
        stats[vendor.key]["skipped_no_input"],
    )

    rows: List[Dict[str, Any]] = []
    harness = WindowsPinyinImeHarness(**harness_kwargs)
    launch_ms = 0.0
    self_check_ms = 0.0
    decode_ms = 0.0
    t_launch = time.perf_counter()
    try:
        logger.info("[黑盒宿主 %s] 启动 Notepad 并定位文本框", vendor.key)
        harness.start()
        launch_ms = round((time.perf_counter() - t_launch) * 1000, 2)
        t_check = time.perf_counter()
        logger.info("[黑盒宿主 %s] 自检 %s 与宿主焦点", vendor.key, profile.display_name)
        harness.self_check()
        self_check_ms = round((time.perf_counter() - t_check) * 1000, 2)
        logger.info("[黑盒解码 %s] 开始: 前台按键 + Space 上屏，共 %d 句", vendor.key, len(prepared_vendor))
        t_dec = time.perf_counter()
        done = 0
        for slot in prepared_vendor:
            stats[vendor.key]["sentences_total"] += 1
            res = harness.decode(slot["input"])
            pred = res.prediction if res.ok else ""
            if not res.ok:
                stats[vendor.key]["decode_failed"] += 1
            exact = res.ok and sentence_exact_match(norm(pred), norm(slot["gold"]))
            if exact:
                stats[vendor.key]["exact_matches"] += 1
            _, cer = accumulate_char_metrics(stats[vendor.key], slot["gold"], pred, res.ok, norm)
            rows.append(
                {
                    "corpus": corpus_label,
                    "index": slot["index"],
                    "vendor": vendor.key,
                    "gold": slot["gold"],
                    "input": slot["input"],
                    "prediction": pred,
                    "exact": exact,
                    "cer": cer,
                    "error": "" if res.ok else res.reason,
                }
            )
            done += 1
            if progress_every and done % progress_every == 0:
                logger.info("[黑盒解码 %s] 进度 %d / %d 句", vendor.key, done, len(prepared_vendor))
        decode_ms = round((time.perf_counter() - t_dec) * 1000, 2)
        logger.info("[黑盒解码 %s] 完成，本方案 %d 句，逐句黑盒输入 %.2f ms", vendor.key, done, decode_ms)
    except Exception as exc:
        logger.warning("[黑盒宿主 %s] 启动或自检失败: %s", vendor.key, exc)
        for slot in prepared_vendor:
            stats[vendor.key]["sentences_total"] += 1
            stats[vendor.key]["decode_failed"] += 1
            _, cer = accumulate_char_metrics(stats[vendor.key], slot["gold"], "", False, norm)
            rows.append(
                {
                    "corpus": corpus_label,
                    "index": slot["index"],
                    "vendor": vendor.key,
                    "gold": slot["gold"],
                    "input": slot["input"],
                    "prediction": "",
                    "exact": False,
                    "cer": cer,
                    "error": str(exc),
                }
            )
    finally:
        try:
            harness.close()
        except Exception:
            pass

    timings["vendors"][vendor.key] = {
        "input_ms": input_ms,
        "launch_ms": launch_ms,
        "self_check_ms": self_check_ms,
        "decode_ms": decode_ms,
        "decode_label": "逐句黑盒输入",
    }

    summary = finalize_summary(stats, vendor_keys)
    stamp = stamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "generated_at_utc": stamp,
        "engine": {
            "type": "windows_ime_blackbox",
            "name": profile.engine_display_name,
            "ime_key": profile.ime_key,
            "host": "Notepad",
            "submit_key": "Space",
        },
        "corpus_file": str(corpus_path),
        "corpus_label": corpus_label,
        "vendors": [asdict(vendor)],
        "summary": summary,
        "per_sentence": rows,
        "timings": timings,
        "eval_synonyms": {
            "config_path": str(eval_synonyms_path.resolve()) if eval_synonyms_path.is_file() else None,
            "rules_summary": eval_synonyms.summary_line(),
        },
    }

    if write_artifacts:
        t_write = time.perf_counter()
        base = artifact_base or f"{profile.artifact_prefix}_{corpus_label}_{stamp}"
        _write_single_artifacts(
            out_dir,
            base,
            payload,
            [vendor],
            profile=profile,
            corpus_label=corpus_label,
            corpus_path=corpus_path,
            eval_synonyms=eval_synonyms,
        )
        timings["write_artifacts_ms"] = round((time.perf_counter() - t_write) * 1000, 2)
        payload["timings"] = timings
        (out_dir / f"{base}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def main(argv: Optional[Sequence[str]] = None) -> int:
    _setup_logging()
    if sys.platform != "win32":
        raise SystemExit("benchmark_microsoft_pinyin.py only supports Windows.")

    parser = argparse.ArgumentParser(description="Benchmark a Windows Pinyin IME via Notepad black-box automation.")
    parser.add_argument(
        "--ime",
        default="microsoft_pinyin",
        help="Target IME profile (default: microsoft_pinyin). Supported: microsoft_pinyin, sogou_pinyin",
    )
    parser.add_argument("--corpus", nargs="*", help="UTF-8 corpus file(s). Default: all data/corpus/*.txt")
    parser.add_argument("--out-dir", default="artifacts", help="Output directory (default: artifacts)")
    parser.add_argument("--label", help="Single-corpus artifact label override")
    parser.add_argument("--progress-every", type=int, default=20, help="Log progress every N decoded sentences")
    parser.add_argument("--eval-synonyms", type=Path, help="Override eval synonyms JSON")
    parser.add_argument("--stamp", help="UTC timestamp override, e.g. 20260421T120000Z")
    parser.add_argument("--launch-timeout-s", type=float, default=10.0, help="Seconds to wait for Notepad window")
    parser.add_argument("--settle-timeout-s", type=float, default=3.0, help="Seconds to wait for committed text to settle")
    parser.add_argument("--inter-key-delay-ms", type=float, default=12.0, help="Delay between simulated key presses")
    parser.add_argument("--commit-delay-ms", type=float, default=120.0, help="Delay before sending Space")
    args = parser.parse_args(argv)

    root = _REPO_ROOT
    out_dir = (root / args.out_dir).resolve()
    corpora = _corpus_inputs(root, args.corpus)
    eval_synonyms, eval_synonyms_path = init_eval_synonyms(root, args.eval_synonyms)
    profile = _ime_profile(args.ime)
    stamp = args.stamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    harness_kwargs = {
        "launch_timeout_s": args.launch_timeout_s,
        "settle_timeout_s": args.settle_timeout_s,
        "inter_key_delay_s": max(0.0, args.inter_key_delay_ms / 1000.0),
        "commit_delay_s": max(0.0, args.commit_delay_ms / 1000.0),
    }
    logger.info(
        "[启动] 通用 Windows 拼音输入法黑盒评测 | 目标输入法: %s (%s) | 宿主: Notepad",
        profile.display_name,
        profile.ime_key,
    )
    if profile.ime_key == "sogou_pinyin":
        logger.info("[启动] 请先确保前台可切换到搜狗拼音；脚本当前不会强制选择特定第三方 IME。")

    if len(corpora) == 1:
        corpus_path, stem = corpora[0]
        label = args.label or stem
        run_blackbox_benchmark(
            corpus_path,
            out_dir,
            profile,
            label,
            args.progress_every,
            eval_synonyms=eval_synonyms,
            eval_synonyms_path=eval_synonyms_path,
            harness_kwargs=harness_kwargs,
            write_artifacts=True,
            stamp=stamp,
            artifact_base=f"{profile.artifact_prefix}_{label}_{stamp}",
        )
        logger.info("[结束] 单语料黑盒评测完成 | 输入法: %s | 输出目录: %s", profile.display_name, out_dir)
        return 0

    wall_clock_start = time.perf_counter()
    summary_by_corpus: Dict[str, Dict[str, Any]] = {}
    timings_by_corpus: Dict[str, Dict[str, Any]] = {}
    corpus_files: Dict[str, str] = {}
    all_rows: List[Dict[str, Any]] = []
    for corpus_path, stem in corpora:
        payload = run_blackbox_benchmark(
            corpus_path,
            out_dir,
            profile,
            stem,
            args.progress_every,
            eval_synonyms=eval_synonyms,
            eval_synonyms_path=eval_synonyms_path,
            harness_kwargs=harness_kwargs,
            write_artifacts=False,
            stamp=stamp,
        )
        summary_by_corpus[stem] = payload["summary"]
        timings_by_corpus[stem] = payload["timings"]
        corpus_files[stem] = str(corpus_path)
        all_rows.extend(payload["per_sentence"])

    vendor = profile.vendor
    summary_overall = aggregate_summaries(summary_by_corpus, [vendor.key])
    combined_payload = {
        "generated_at_utc": stamp,
        "engine": {
            "type": "windows_ime_blackbox",
            "name": profile.engine_display_name,
            "ime_key": profile.ime_key,
            "host": "Notepad",
            "submit_key": "Space",
        },
        "corpus_files": corpus_files,
        "vendors": [asdict(vendor)],
        "summary_by_corpus": summary_by_corpus,
        "summary_overall": summary_overall,
        "per_sentence": all_rows,
        "timings_by_corpus": timings_by_corpus,
        "timings_wall_total_ms": round((time.perf_counter() - wall_clock_start) * 1000, 2),
        "eval_synonyms": {
            "config_path": str(eval_synonyms_path.resolve()) if eval_synonyms_path.is_file() else None,
            "rules_summary": eval_synonyms.summary_line(),
        },
    }
    base = f"{profile.artifact_prefix}_all_corpus_{stamp}"
    _write_combined_artifacts(out_dir, base, combined_payload, [vendor], profile)
    logger.info("[结束] 多语料黑盒评测完成 | 输入法: %s | 输出目录: %s", profile.display_name, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
