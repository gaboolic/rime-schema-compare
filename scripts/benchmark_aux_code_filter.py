#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmark rime-frost with and without lua_filter@*aux_code.

The script creates two temporary user data dirs from a source rime-frost checkout:
one unchanged, and one with the aux_code filter line removed from
rime_frost.schema.yaml. It then feeds the same input prefixes into librime and
measures feed_input + get_context time on a reused session.
"""

from __future__ import annotations

import argparse
import shutil
import statistics
import sys
import time
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from rime_schema_compare.call_librime import RimeDllWrapper
from rime_schema_compare.config import resolve_rime_dll, shared_data_dir


DEFAULT_INPUTS = [
    "nihao",
    "women",
    "zhongguo",
    "rimefrost",
    "jinxiantianqibucuo",
    "xinxingchanyedefazhan",
    "wojintianxiangceshishurufadexingneng",
    "zhegeshurufanganzaizhengchangdazishihoudekaliangan",
]

DEFAULT_AUX_INPUTS = [
    "hao`n",
    "shi`o",
    "zhong`k",
    "ceshi`u",
    "zhongguo`k",
]


def copy_case(src: Path, dst: Path, *, remove_aux_filter: bool, tag_gated: bool = False) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    ignore = shutil.ignore_patterns(".git", ".git*", "__pycache__", "*.pyc", "build")
    shutil.copytree(src, dst, ignore=ignore)
    schema = dst / "rime_frost.schema.yaml"
    text = schema.read_text(encoding="utf-8")
    needle = "    - lua_filter@*aux_code                 # 墨奇辅助码\n"
    if needle not in text:
        raise RuntimeError(f"aux_code filter line not found in {schema}")
    if remove_aux_filter:
        text = text.replace(needle, "")
    if tag_gated:
        if "aux_code:\n  tags: [ aux_code ]\n" not in text:
            text = text.replace(
                "corrector: \"{comment}\"\n",
                "corrector: \"{comment}\"\n\n\n# Lua 配置：辅助码滤镜只处理含辅助码引导符的 segment\n"
                "aux_code:\n"
                "  tags: [ aux_code ]\n",
            )
        if '    aux_code: "^.+`[A-Za-z]*$"' not in text:
            text = text.replace(
                '    radical_lookup: "^uU[a-z]+$"        # 响应部件拆字的反查，与 radical_lookup/prefix 匹配\n',
                '    radical_lookup: "^uU[a-z]+$"        # 响应部件拆字的反查，与 radical_lookup/prefix 匹配\n'
                '    aux_code: "^.+`[A-Za-z]*$"          # 只在输入辅助码引导符时启用 aux_code filter\n',
            )
    schema.write_text(text, encoding="utf-8", newline="\n")


def expanded_prefixes(inputs: list[str], repeat: int) -> list[str]:
    prefixes: list[str] = []
    for raw in inputs:
        for i in range(1, len(raw) + 1):
            prefixes.append(raw[:i])
    return prefixes * repeat


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * pct)))
    return ordered[index]


def bench_case(
    *,
    dll: Path,
    user_dir: Path,
    label: str,
    inputs: list[str],
    repeat: int,
    warmup: int,
) -> dict[str, float | int | str]:
    rime = RimeDllWrapper(dll_path=str(dll))
    try:
        t0 = time.perf_counter()
        rime.initialize(
            app_name=f"rime.aux.benchmark.{label}",
            shared_data_dir=str(shared_data_dir(_ROOT)),
            user_data_dir=str(user_dir),
        )
        load_ms = (time.perf_counter() - t0) * 1000.0

        session_id = rime.create_session()
        if not session_id:
            raise RuntimeError(f"{label}: create_session failed")
        if not rime.select_schema(session_id, "rime_frost"):
            raise RuntimeError(f"{label}: select_schema failed")

        feed_mode = "set_input" if rime.uses_set_input() else "simulate_key_sequence"
        samples = expanded_prefixes(inputs, repeat)

        # Warm up schema caches and Python ctypes paths.
        for raw in samples[:warmup]:
            rime.feed_input(session_id, raw)
            rime.get_context(session_id)

        timings: list[float] = []
        candidates_seen = 0
        for raw in samples:
            t = time.perf_counter()
            ok = rime.feed_input(session_id, raw)
            ctx = rime.get_context(session_id)
            elapsed = (time.perf_counter() - t) * 1000.0
            if not ok:
                raise RuntimeError(f"{label}: feed_input failed for {raw!r}")
            if ctx:
                candidates_seen += len(ctx.get("candidates") or [])
            timings.append(elapsed)

        rime.destroy_session(session_id)
        return {
            "label": label,
            "feed_mode": feed_mode,
            "load_ms": load_ms,
            "n": len(timings),
            "mean": statistics.mean(timings),
            "median": statistics.median(timings),
            "p95": percentile(timings, 0.95),
            "min": min(timings),
            "max": max(timings),
            "stdev": statistics.pstdev(timings),
            "candidates_seen": candidates_seen,
        }
    finally:
        rime.finalize()


def print_row(row: dict[str, float | int | str]) -> None:
    print(
        f"{row['label']:14s} n={row['n']:5d} mode={row['feed_mode']} "
        f"load={row['load_ms']:8.2f} ms "
        f"mean={row['mean']:8.4f} median={row['median']:8.4f} "
        f"p95={row['p95']:8.4f} min={row['min']:8.4f} max={row['max']:8.4f} "
        f"stdev={row['stdev']:8.4f}"
    )


def compare(with_aux: dict[str, float | int | str], no_aux: dict[str, float | int | str]) -> None:
    delta = float(with_aux["mean"]) - float(no_aux["mean"])
    pct = delta / float(no_aux["mean"]) * 100.0 if float(no_aux["mean"]) else 0.0
    print(f"mean delta (with_aux - no_aux): {delta:.4f} ms / prefix ({pct:+.2f}%)")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", default=r"D:\vscode\rime-frost", help="Source rime-frost checkout")
    p.add_argument("--workdir", default=str(_ROOT / ".tmp_aux_code_bench"), help="Temporary work directory")
    p.add_argument("--repeat", type=int, default=80, help="Repeat count for all input prefixes")
    p.add_argument("--warmup", type=int, default=80, help="Warmup prefix count")
    p.add_argument("--rime-dll", default="", help="Override rime.dll path")
    p.add_argument("--skip-copy", action="store_true", help="Reuse existing temporary copies")
    args = p.parse_args()

    source = Path(args.source).resolve()
    workdir = Path(args.workdir).resolve()
    with_aux_dir = workdir / "with_aux_filter"
    no_aux_dir = workdir / "without_aux_filter"
    tagged_aux_dir = workdir / "tagged_aux_filter"
    dll = resolve_rime_dll(args.rime_dll or None)

    if not args.skip_copy:
        workdir.mkdir(parents=True, exist_ok=True)
        copy_case(source, with_aux_dir, remove_aux_filter=False)
        copy_case(source, no_aux_dir, remove_aux_filter=True)
        copy_case(source, tagged_aux_dir, remove_aux_filter=False, tag_gated=True)

    print(f"dll: {dll}")
    print(f"source: {source}")
    print(f"workdir: {workdir}")
    print(f"normal inputs: {len(DEFAULT_INPUTS)} strings, repeat={args.repeat}")
    print()

    print("[normal typing: no aux trigger]")
    normal_with = bench_case(
        dll=dll,
        user_dir=with_aux_dir,
        label="with_aux",
        inputs=DEFAULT_INPUTS,
        repeat=args.repeat,
        warmup=args.warmup,
    )
    normal_without = bench_case(
        dll=dll,
        user_dir=no_aux_dir,
        label="without_aux",
        inputs=DEFAULT_INPUTS,
        repeat=args.repeat,
        warmup=args.warmup,
    )
    normal_tagged = bench_case(
        dll=dll,
        user_dir=tagged_aux_dir,
        label="tagged_aux",
        inputs=DEFAULT_INPUTS,
        repeat=args.repeat,
        warmup=args.warmup,
    )
    print_row(normal_with)
    print_row(normal_without)
    print_row(normal_tagged)
    compare(normal_with, normal_without)
    compare(normal_tagged, normal_without)
    print()

    print("[aux trigger inputs: contains `]")
    aux_with = bench_case(
        dll=dll,
        user_dir=with_aux_dir,
        label="with_aux",
        inputs=DEFAULT_AUX_INPUTS,
        repeat=args.repeat,
        warmup=args.warmup,
    )
    aux_without = bench_case(
        dll=dll,
        user_dir=no_aux_dir,
        label="without_aux",
        inputs=DEFAULT_AUX_INPUTS,
        repeat=args.repeat,
        warmup=args.warmup,
    )
    aux_tagged = bench_case(
        dll=dll,
        user_dir=tagged_aux_dir,
        label="tagged_aux",
        inputs=DEFAULT_AUX_INPUTS,
        repeat=args.repeat,
        warmup=args.warmup,
    )
    print_row(aux_with)
    print_row(aux_without)
    print_row(aux_tagged)
    compare(aux_with, aux_without)
    compare(aux_tagged, aux_without)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
