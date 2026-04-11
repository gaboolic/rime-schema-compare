# rime-schema-compare

Compare **whole-sentence decoding accuracy** of several Rime distributions (雾凇 / 薄荷 / 万象) using **Python + librime** (`rime.dll` on Windows).

## What it does

1. Split text on `，,。.` into segments.
2. Turn each segment’s **Hanzi** into a **continuous lowercase pinyin** string (`pypinyin`, reproducible baseline).
3. For each vendor checkout under `vendor/`, initialize librime with that directory as both `shared_data_dir` and `user_data_dir`, select the main schema, feed the pinyin, and read **`commit_text_preview` or the first candidate**.
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

## Run

From the repo root:

```bash
set RIME_DLL=C:\Program Files\Rime\weasel-0.16.3\rime.dll
python scripts\smoke_rime.py
python scripts\benchmark_sentences.py --corpus data\corpus\prose.txt
python scripts\benchmark_sentences.py --corpus data\corpus\tech.txt
python scripts\benchmark_sentences.py --corpus data\corpus\novel.txt
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
