#!/usr/bin/env python3
"""Fail closed before publishing a weekly corpus and all-vendor benchmark report."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from rime_schema_compare.config import DEFAULT_VENDORS

SHANGHAI = timezone(timedelta(hours=8))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def local_day(value: str) -> date:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Provenance timestamps must include a timezone")
    return parsed.astimezone(SHANGHAI).date()


def verify_git_source(directory: Path) -> None:
    """Ensure a publishable submodule gitlink matches its evaluated snapshot."""
    if not (directory / ".git").exists():
        return  # Non-submodule generated variants record sources in the report.
    def git_value(*args: str) -> str:
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as output:
            subprocess.run(["git", "-C", str(directory), *args], check=True, stdout=output)
            output.seek(0)
            return output.read().strip()
    require(Path(git_value("rev-parse", "--show-toplevel")).resolve() == directory.resolve(),
            f"Wrong submodule Git pointer: {directory}")
    versions = json.loads((directory / "upstream_versions.json").read_text(encoding="utf-8"))
    require(len(versions) == 1 and git_value("rev-parse", "HEAD") == versions[0]["commit"],
            f"Submodule HEAD differs from evaluated source: {directory}")


def validate(corpus: Path, artifacts: Path, expected_day: date, *, root: Path = ROOT,
             min_sentences: int = 1) -> tuple[dict, dict]:
    corpus = corpus.resolve()
    meta = json.loads(corpus.with_suffix(".meta.json").read_text(encoding="utf-8"))
    contents = corpus.read_bytes()
    require(local_day(meta["fetched_at"]) == expected_day, "Corpus was not fetched on the requested Shanghai date")
    require(local_day(meta["hotlist_updated_at"]) == expected_day, "Hot-list API data is stale or has no current-day timestamp")
    require(local_day(meta["hotlist_fetched_at"]) == expected_day, "Hot-list API was not fetched today")
    require(hashlib.sha256(contents).hexdigest() == meta["corpus_sha256"], "Corpus SHA256 mismatch")
    require(len(contents) == meta["corpus_bytes"], "Corpus size mismatch")
    questions = meta["questions"]
    require(questions > 0 and meta["questions_with_answer_bodies"] == questions,
            "Every hot-list question must have a rendered answer body")
    require(meta["fallback_questions"] == 0, "Excerpt/title fallback is not publishable")
    details = meta["question_details"]
    require(len(details) == questions, "Question provenance count mismatch")
    seen_questions: set[str] = set()
    seen_answers: set[str] = set()
    answer_count = 0
    text = contents.decode("utf-8")
    for question in details:
        qid = question["question_id"]
        require(qid not in seen_questions, "Duplicate question provenance")
        seen_questions.add(qid)
        require(bool(question["answers"]), f"No answer provenance for {qid}")
        for answer in question["answers"]:
            url = answer["answer_url"]
            require(re.fullmatch(rf"https://www\.zhihu\.com/question/{re.escape(qid)}/answer/\d+", url) is not None,
                    f"Invalid answer source URL: {url}")
            require(url not in seen_answers, f"Duplicate answer source: {url}")
            seen_answers.add(url)
            require(bool(answer["text"].strip()) and answer["text"] in text, f"Answer body missing from corpus: {url}")
            answer_count += 1
    require(answer_count == meta["answer_bodies"], "Answer count mismatch")

    results = list(artifacts.glob("benchmark*.json"))
    require(len(results) == 1, "Use an isolated output directory containing exactly one benchmark JSON")
    payload = json.loads(results[0].read_text(encoding="utf-8"))
    require(Path(payload["corpus_file"]).resolve() == corpus, "Benchmark used the wrong corpus")
    summary = payload["summary"]
    require(set(summary) == {v.key for v in DEFAULT_VENDORS}, "Not all default vendors were benchmarked")
    totals = set()
    shared_model_hashes = set()
    verified_models = []
    for vendor in DEFAULT_VENDORS:
        verify_git_source(vendor.data_dir(root))
        row = summary[vendor.key]
        require(row["sentence_total"] >= min_sentences, f"Too few evaluated sentences: {vendor.key}")
        require(row["decode_failed"] == 0, f"Decode failures: {vendor.key}")
        require(row["skipped_no_input"] == 0, f"Missing input codes: {vendor.key}")
        totals.add((row["sentence_total"], row["gold_character_total"]))
        compiled = yaml.safe_load((vendor.data_dir(root) / "build" / f"{vendor.schema_id}.schema.yaml").read_text(encoding="utf-8"))
        expected_model = ("zh-hant-t-essay-bgw" if vendor.key == "luna_pinyin_with_octagram"
                          else "wanxiang-lts-zh-hans" if "_with_gram" in vendor.key else "")
        language = (compiled.get("grammar") or {}).get("language")
        require(language == expected_model, f"Wrong compiled model for {vendor.key}: {language}")
        translator = compiled["translator"]
        require(translator["enable_user_dict"] is False, f"User dictionary enabled: {vendor.key}")
        if expected_model:
            model = vendor.data_dir(root) / f"{expected_model}.gram"
            require(model.is_file() and model.stat().st_size > 0, f"Missing model: {vendor.key}")
            versions = json.loads((vendor.data_dir(root) / "model_versions.json").read_text(encoding="utf-8"))["models"]
            require(len(versions) == 1 and versions[0]["name"] == model.name, f"Missing model provenance: {vendor.key}")
            info = versions[0]
            digest = hashlib.sha256()
            with model.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            require(model.stat().st_size == info["size"] and digest.hexdigest() == info["sha256"],
                    f"Model size/SHA256 mismatch: {vendor.key}")
            verified_models.append({"vendor": vendor.key, **info})
            if expected_model == "wanxiang-lts-zh-hans":
                shared_model_hashes.add(info["sha256"])
        if vendor.preserve_translator_defaults:
            require(translator.get("max_homophones") == 7 and translator.get("max_homographs") == 7
                    and "max_sentences" not in translator, "Original Octagram translator defaults were overridden")
    require(len(totals) == 1, "Vendors were not evaluated on identical sentence/character totals")
    require(len(shared_model_hashes) == 1, "with_gram vendors used different model versions")
    payload["verified_models"] = verified_models
    return payload, meta


def annotate_reports(report_dir: Path, corpus: Path, payload: dict, meta: dict, day: date) -> None:
    """Annotate staging reports only, after validation succeeds."""
    summary = payload["summary"]
    first = next(iter(summary.values()))
    context = ["## 自动采集与验证", "",
               f"- 语料日期（北京时间）：{day.isoformat()}；采集：{meta['fetched_at']}。",
               f"- 热榜 API 更新时间：{meta['hotlist_updated_at']}。",
               f"- 实际正文：{meta['questions']} 个问题、{meta['answer_bodies']} 条回答；摘要回退 0。",
               f"- 评测：{len(summary)} 个方案、每方案 {first['sentence_total']} 句；解码失败 0。",
               f"- [正文语料](../data/corpus/{corpus.name}) / [来源元数据](../data/corpus/{corpus.with_suffix('.meta.json').name})。",
               f"- 语料 SHA-256：`{meta['corpus_sha256']}`。", "",
               "| 方案 | 整句正确率 | 文字正确率 |", "|------|-----------:|-----------:|"]
    for vendor in DEFAULT_VENDORS:
        row = summary[vendor.key]
        context.append(f"| `{vendor.key}` | {row['sentence_accuracy_percent']:.2f}% | {row['character_accuracy_percent']:.2f}% |")
    context += ["", "### 已验证的语言模型", ""]
    for model in payload["verified_models"]:
        context.append(f"- `{model['vendor']}`：`{model['name']}`，{model['size']} 字节，SHA-256 `{model['sha256']}`。")
    context += ["", "公开网页、上游方案和词库随时间变化；以本次保存的语料、来源和提交版本为准。", ""]
    for name in ("latest.md", f"{day.isoformat()}.md"):
        path = report_dir / name
        report = path.read_text(encoding="utf-8")
        require(report.startswith("# Rime 评测结果\n"), f"Unexpected report format: {path}")
        report = report.replace("## Vendor 子模块版本", "\n".join(context) + "\n## Vendor 子模块版本", 1)
        path.write_text(report.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--date", type=date.fromisoformat, required=True)
    parser.add_argument("--min-sentences", type=int, default=1)
    parser.add_argument("--report-dir", type=Path, help="Annotate validated staging reports")
    args = parser.parse_args()
    payload, meta = validate(args.corpus, args.artifacts, args.date, min_sentences=args.min_sentences)
    if args.report_dir:
        annotate_reports(args.report_dir, args.corpus, payload, meta, args.date)
    print(f"Validated {len(payload['summary'])} vendors, {meta['answer_bodies']} answer bodies; no fallback/decode failures")


if __name__ == "__main__":
    main()
