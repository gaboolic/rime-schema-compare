# rime-schema-compare

Compare **whole-sentence decoding accuracy** of several Rime distributions (雾凇 / 薄荷 / 万象) using **Python + librime** (`rime.dll` on Windows).

## What it does

1. Split text on `，,。.` into segments.
2. Turn each segment’s **Hanzi** into a **continuous lowercase pinyin** string (`pypinyin`, reproducible baseline).
3. For each vendor checkout under `vendor/`, initialize librime with **`shared_data_dir` = [`vendor/data`](vendor/data)** (created if missing) and **`user_data_dir` = that vendor’s submodule tree**, select the main schema, feed the pinyin, and read **`commit_text_preview` or the first candidate**. Put any shared Rime assets you want all schemes to see under `vendor/data` (e.g. symlink or copy from a Weasel install).
4. Report **sentence exact match rate** and **macro CER** (total edit distance over total gold Hanzi length).

## Prerequisites

- **Windows** with a working **Weasel** (小狼毫) or other install that provides **`rime.dll`** and its dependencies in the same folder.
- **Python 3.10+** recommended.
- **Git submodules** checked out (large downloads on first run):

```bash
git submodule update --init --recursive --depth 1
```

The **万象** submodule tracks branch `wanxiang` (see [.gitmodules](.gitmodules)).

## Rime deploy (required once per vendor)

Submodule trees are mostly **source YAML**. Before librime can build candidates, deploy / compile for **each** `vendor/*` directory you want to test (e.g. copy that folder as a Rime user directory and use Weasel’s **部署**, or run `rime_deployer` with that path). If you skip this, you will see many `empty_prediction` / `no_context` rows in the output.

## Setup

```bash
pip install -r requirements.txt
```

Optional: create a `.env` file in the repo root:

```env
RIME_DLL=C:\Program Files\Rime\weasel-0.16.3\rime.dll
```

If you copy **`rime.dll` (and keep its companion DLLs next to it if required)** into the **repository root**, it is picked up automatically before scanning `Program Files\Rime\...`.

## Run

From the repo root:

```bash
set RIME_DLL=C:\Program Files\Rime\weasel-0.16.3\rime.dll
python scripts\smoke_rime.py
python scripts\benchmark_sentences.py
```

With no `--corpus` argument, **all `*.txt` files under `data/corpus/`** are evaluated in one run. Typical artifacts under `artifacts/`:

| File | Content |
|------|---------|
| `benchmark_all_corpus_<ts>.csv` | **按句一行**：`corpus,index,gold,pinyin`，其后各方案依次为 `*_sentence_correct`(0/1)、`*_character_accuracy_percent`(该句)、`*_prediction`、`*_error` |
| `benchmark_all_corpus_<ts>_long.csv` | 窄表：每句 × 每方案一行（旧版明细） |
| `benchmark_all_corpus_<ts>_summary.csv` | 汇总：语料 × 方案 |
| `benchmark_all_corpus_<ts>_report.txt` | 中文摘要：各方案句子正确率、文字正确率 |
| `benchmark_all_corpus_<ts>.json` | 完整 JSON（含 `per_sentence` 窄表数据） |

进度日志打在 **stderr**（在简体中文 Windows 上跟随控制台默认编码，一般为 GBK，避免乱码）。阶段前缀：`[启动]`、`[语料列表]`、`[分句]`、`[pypinyin]`、`[librime:加载方案 x]`、`[librime:解码 x]`、`[汇总]`、`[写出结果]`、`[聚合]` / `[结束]`。若你使用 UTF-8 终端（`chcp 65001`），stderr 一般也能正确显示中文。

单语料时文件名前缀为 `benchmark_<语料>_<ts>`，规则相同。

Single file or explicit list:

```bash
python scripts\benchmark_sentences.py --corpus data\corpus\prose.txt
python scripts\benchmark_sentences.py --corpus data\corpus\prose.txt data\corpus\tech.txt
```

Options:

- `--vendors rime_frost rime_ice wanxiang` — subset of vendors (see defaults in `src/rime_schema_compare/config.py`).
- `--out-dir artifacts` — JSON + CSV with per-sentence rows and aggregate summary.
- `--progress-every N` — stderr progress for long corpora.

## Layout

| Path | Role |
|------|------|
| [vendor/rime-frost](vendor/rime-frost) | 雾凇拼音，schema `rime_frost` |
| [vendor/rime-ice](vendor/rime-ice) | 薄荷方案，schema `rime_ice` |
| [vendor/rime_wanxiang](vendor/rime_wanxiang) | 万象拼音，schema `wanxiang` |
| [src/rime_schema_compare/call_librime.py](src/rime_schema_compare/call_librime.py) | ctypes wrapper for `rime.dll` |
| [scripts/benchmark_sentences.py](scripts/benchmark_sentences.py) | CLI benchmark |
| [data/corpus/](data/corpus/) | Sample prose / tech / novel UTF-8 snippets (replace with your own) |

## Troubleshooting

- **`FileNotFoundError` for `rime.dll`** — set `RIME_DLL` to the full path of `rime.dll` next to Weasel’s binaries.
- **`Vendor data directory missing`** — run `git submodule update --init --recursive`.
- **Mostly `empty_prediction`** — deploy Rime for that `vendor/*` directory so `.bin` / build artifacts exist.
- **SSL errors when cloning submodules** — fix Git HTTPS / proxy settings, then re-run submodule init.

## License

This repo’s own scripts and packaging are provided as-is. Third-party pieces are credited in [NOTICE](NOTICE). Each `vendor/*` submodule remains under its upstream license.
