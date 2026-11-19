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


def validate_public_article_source(meta: dict, text: str, expected_day: date) -> None:
    """Verify pinned public full-text provenance; never confuse selection and publication dates."""
    source = meta["source_id"]
    if source == "zhihu_daily":
        require(meta["source_url"] == "https://news-at.zhihu.com/api/4/news/latest", "Wrong public article feed URL")
        require(date.fromisoformat(meta["feed_date"]) == expected_day, "Public article feed date is stale")
        require(local_day(meta["feed_fetched_at"]) == expected_day, "Public article feed was not fetched today")
    elif source == "ruanyf_weekly":
        require(meta["source_url"] == "https://github.com/ruanyf/weekly", "Wrong weekly repository URL")
        for field in ("source_ref", "index_ref"):
            require(re.fullmatch(r"[0-9a-f]{40}", meta[field]) is not None, "Weekly source must use immutable commit IDs")
        require(date.fromisoformat(meta["selection_date"]) == expected_day, "Weekly selection date mismatch")
        require(local_day(meta["index_fetched_at"]) == expected_day, "Weekly index was not fetched today")
        age = (expected_day - local_day(meta["source_updated_at"])).days
        require(0 <= age <= 14, "Weekly source update date is future or stale (over 14 days)")
        require(meta["articles"] == 1, "Select exactly one complete latest weekly issue")
    else:
        raise ValueError(f"Unsupported public article source: {source}")
    count = meta["articles"]
    require(count > 0 and meta["articles_with_bodies"] == count, "Every selected article must have a body")
    require(meta["fallback_articles"] == 0, "Article summary/title fallback is not publishable")
    details = meta["article_details"]
    require(len(details) == count, "Article provenance count mismatch")
    seen: set[str] = set()
    for article in details:
        identity = article["article_id"]
        require(isinstance(identity, str) and re.fullmatch(r"\d+", identity) is not None, "Invalid article ID")
        require(identity not in seen, "Duplicate article provenance")
        seen.add(identity)
        if source == "zhihu_daily":
            require(article["url"] == f"https://daily.zhihu.com/story/{identity}", "Invalid article source URL")
            require(article["api_url"] == f"https://news-at.zhihu.com/api/4/news/{identity}", "Invalid article body API URL")
        else:
            reference = meta["source_ref"]
            require(article["url"] == f"https://github.com/ruanyf/weekly/blob/{reference}/docs/issue-{identity}.md", "Invalid pinned weekly source URL")
            require(article["api_url"] == f"https://raw.githubusercontent.com/ruanyf/weekly/{reference}/docs/issue-{identity}.md", "Invalid pinned weekly raw URL")
            require(text == article["body"], "Weekly corpus must preserve the complete original Markdown exactly")
        body = article["body"]
        require(bool(body.strip()) and body in text, "Article body missing from corpus")
        require(len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002ebef]", body)) >= 30, "Article body is too short to verify")
        require(article["body_characters"] == len(body), "Article body length mismatch")
        require(article["body_sha256"] == hashlib.sha256(body.encode("utf-8")).hexdigest(), "Article body SHA256 mismatch")


def validate(corpus: Path, artifacts: Path, expected_day: date, *, root: Path = ROOT,
             min_sentences: int = 1) -> tuple[dict, dict]:
    corpus = corpus.resolve()
    meta = json.loads(corpus.with_suffix(".meta.json").read_text(encoding="utf-8"))
    contents = corpus.read_bytes()
    require(local_day(meta["fetched_at"]) == expected_day, "Corpus was not fetched on the requested Shanghai date")
    require(hashlib.sha256(contents).hexdigest() == meta["corpus_sha256"], "Corpus SHA256 mismatch")
    require(len(contents) == meta["corpus_bytes"], "Corpus size mismatch")
    text = contents.decode("utf-8")
    kind = meta.get("source_kind", "zhihu_hotlist")
    if kind == "public_articles":
        validate_public_article_source(meta, text, expected_day)
    elif kind == "zhihu_hotlist":
        # Keep explicit legacy support for historical question/answer corpora.
        require(local_day(meta["hotlist_updated_at"]) == expected_day, "Hot-list API data is stale or has no current-day timestamp")
        require(local_day(meta["hotlist_fetched_at"]) == expected_day, "Hot-list API was not fetched today")
        questions = meta["questions"]
        require(questions > 0 and meta["questions_with_answer_bodies"] == questions,
                "Every hot-list question must have a rendered answer body")
        require(meta["fallback_questions"] == 0, "Excerpt/title fallback is not publishable")
        details = meta["question_details"]
        require(len(details) == questions, "Question provenance count mismatch")
        seen_questions: set[str] = set()
        seen_answers: set[str] = set()
        answer_count = 0
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
    else:
        raise ValueError(f"Unsupported corpus source kind: {kind}")

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
    if meta.get("source_id") == "ruanyf_weekly":
        source_lines = [f"- 来源：{meta['source_name']}；选择日期：{meta['selection_date']}。",
                        f"- 源码最近更新时间：{meta['source_updated_at']}（不冒充当日发表；最多允许 14 天）。",
                        f"- 固定源码提交：`{meta['source_ref']}`。",
                        "- 实际正文：1 期完整原始 Markdown；包含原刊自带的资讯摘编，不代表外链文章全文；摘要回退 0。",
                        f"- 署名及使用声明：{meta['attribution']}"]
    elif meta.get("source_kind") == "public_articles":
        source_lines = [f"- 来源：{meta['source_name']}（公开文章，不是知乎热榜回答）；日报日期：{meta['feed_date']}。",
                        f"- 实际正文：{meta['articles']} 篇文章；摘要回退 0；无需网页登录、Cookie 或 Access Secret。"]
    else:
        source_lines = [f"- 热榜 API 更新时间：{meta['hotlist_updated_at']}。",
                        f"- 实际正文：{meta['questions']} 个问题、{meta['answer_bodies']} 条回答；摘要回退 0。"]
    context = ["## 自动采集与验证", "",
               f"- 语料日期（北京时间）：{day.isoformat()}；采集：{meta['fetched_at']}。",
               *source_lines,
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
    units = (f"{meta['articles']} public article bodies" if meta.get("source_kind") == "public_articles"
             else f"{meta['answer_bodies']} answer bodies")
    print(f"Validated {len(payload['summary'])} vendors, {units}; no fallback/decode failures")


if __name__ == "__main__":
    main()
