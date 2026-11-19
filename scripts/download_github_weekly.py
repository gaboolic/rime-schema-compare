#!/usr/bin/env python3
"""Fetch one complete, unchanged issue of ruanyf/weekly using GitHub hosts only."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

REPOSITORY = "https://github.com/ruanyf/weekly"
API = "https://api.github.com/repos/ruanyf/weekly"
RAW = "https://raw.githubusercontent.com/ruanyf/weekly"
SOURCE_NAME = "科技爱好者周刊（GitHub原始整期正文）"
ATTRIBUTION = "阮一峰《科技爱好者周刊》，原始Markdown未改写；非商业研究评测用途；版权及许可遵循原作者声明。"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
SHANGHAI = timezone(timedelta(hours=8))
SHA = re.compile(r"[0-9a-fA-F]{40}")
HANZI = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002ebef]")


def validate_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.username or parsed.password
            or parsed.port not in (None, 443) or parsed.fragment):
        raise ValueError("Only fixed GitHub repository HTTPS endpoints are allowed")
    if parsed.hostname == "api.github.com":
        if parsed.path == "/repos/ruanyf/weekly/commits/master" and not parsed.query:
            return url
        if parsed.path == "/repos/ruanyf/weekly/commits":
            query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            if (set(query) == {"path", "sha", "per_page"}
                    and query["per_page"] == ["1"] and len(query["sha"]) == 1
                    and SHA.fullmatch(query["sha"][0])
                    and len(query["path"]) == 1
                    and re.fullmatch(r"docs/issue-[1-9][0-9]*\.md", query["path"][0])):
                return url
    elif parsed.hostname == "raw.githubusercontent.com" and not parsed.query:
        if re.fullmatch(r"/ruanyf/weekly/[0-9a-fA-F]{40}/(?:README\.md|docs/issue-[1-9][0-9]*\.md)", parsed.path):
            return url
    raise ValueError("Only pinned ruanyf/weekly GitHub endpoints are allowed")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("GitHub weekly downloads do not follow redirects")


def fetch_bytes(url: str, *, timeout: float = 30, attempts: int = 3) -> bytes:
    """GET only; TLS verification enabled; secrets never sent to the raw host."""
    validate_url(url)
    if timeout <= 0 or not 1 <= attempts <= 3:
        raise ValueError("Invalid request timeout/retry settings")
    headers = {"User-Agent": "rime-schema-compare-weekly/1.0", "Accept": "application/vnd.github+json"}
    if urllib.parse.urlsplit(url).hostname == "api.github.com":
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            if "\r" in token or "\n" in token:
                raise ValueError("Invalid GitHub credential value")
            headers["Authorization"] = "Bearer " + token
    else:
        headers["Accept"] = "text/plain"
    opener = urllib.request.build_opener(NoRedirect())
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers=headers, method="GET")
            with opener.open(request, timeout=timeout) as response:
                if response.geturl() != url:
                    raise ValueError("Unexpected GitHub response URL")
                payload = response.read(MAX_RESPONSE_BYTES + 1)
            if len(payload) > MAX_RESPONSE_BYTES:
                raise ValueError("GitHub response exceeds 2 MiB")
            return payload
        except urllib.error.HTTPError as exc:
            if exc.code not in {408, 429, 500, 502, 503, 504} or attempt + 1 == attempts:
                raise RuntimeError(f"GitHub weekly HTTP {exc.code}") from None
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            script_dir = str(Path(__file__).resolve().parent)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            from download_public_articles import network_error_description
            description = network_error_description(exc)
            if attempt + 1 == attempts:
                raise RuntimeError(f"GitHub weekly network request failed after bounded retries: {description}") from None
        if attempt + 1 < attempts:
            time.sleep(2 ** attempt)
    raise RuntimeError("GitHub weekly request failed")


def fetch_json(url: str):
    try:
        return json.loads(fetch_bytes(url).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("GitHub API did not return valid UTF-8 JSON") from None


def fetch_text(url: str) -> str:
    try:
        return fetch_bytes(url).decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Weekly source is not UTF-8 Markdown") from None


def commit_sha(value) -> str:
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise ValueError("Invalid GitHub commit SHA")
    return value.lower()


def latest_issue(readme: str, root_sha: str) -> int:
    numbers = []
    for target in re.findall(r"\[[^\]\n]*\]\(\s*([^\s)]+)(?:\s+\"[^\"]*\")?\s*\)", readme):
        match = re.fullmatch(r"(?:\./)?docs/issue-([1-9][0-9]*)\.md", target)
        if not match:
            match = re.fullmatch(r"https://github\.com/ruanyf/weekly/blob/(?:master|" + re.escape(root_sha) + r")/docs/issue-([1-9][0-9]*)\.md", target)
        if match:
            numbers.append(int(match[1]))
    if not numbers:
        raise ValueError("Pinned README contains no weekly issue links")
    return max(numbers)


def validate_updated_at(value, expected_day: date, max_age_days: int) -> str:
    if not isinstance(value, str):
        raise ValueError("Weekly source update timestamp is missing")
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Weekly source update timestamp is invalid") from None
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("Weekly source timestamp must include a timezone")
    age = (expected_day - stamp.astimezone(SHANGHAI).date()).days
    if age < 0:
        raise ValueError("Weekly source update date is in the future")
    if age > max_age_days:
        raise ValueError("Weekly source is older than the permitted age")
    return stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_body(body: str, number: int) -> str:
    if re.match(r"\s*\ufeff?\s*<(?:!doctype|html|head|body)\b", body, re.I):
        raise ValueError("Weekly source is an HTML/error page, not Markdown")
    heading = re.search(r"^\ufeff?#{1,6}[ \t]+(.+?)[ \t]*$", body, re.M)
    if not heading or not re.search(r"(?<![0-9])" + str(number) + r"(?![0-9])", heading[1]):
        raise ValueError("First Markdown heading does not identify the selected issue")
    if len(HANZI.findall(body)) < 100:
        raise ValueError("Weekly Markdown body is missing or too short")
    return heading[1].strip()


def _diagnostic_save(directory: Path | None, diagnostic: dict) -> None:
    # Lazy import allows the wrapper to import this module without a cycle.
    script_dir = str(Path(__file__).resolve().parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from download_public_articles import save_diagnostic
    try:
        save_diagnostic(directory, diagnostic)
    except OSError:
        print("Warning: unable to save weekly source diagnostics", file=sys.stderr)


def download_weekly(out: Path, *, expected_day: date, diagnostics_dir: Path | None = None,
                    max_age_days: int = 14) -> dict:
    diagnostic = {"source_kind": "public_articles", "source_id": "ruanyf_weekly", "source_url": REPOSITORY,
                  "selection_date": expected_day.isoformat(), "stage": "index"}
    try:
        if not isinstance(max_age_days, int) or isinstance(max_age_days, bool) or max_age_days < 0:
            raise ValueError("max_age_days must be a nonnegative integer")
        root = fetch_json(API + "/commits/master")
        if not isinstance(root, dict):
            raise ValueError("GitHub root commit response must be an object")
        root_sha = commit_sha(root.get("sha"))
        readme = fetch_text(f"{RAW}/{root_sha}/README.md")
        index_fetched_at = datetime.now(SHANGHAI).isoformat()
        number = latest_issue(readme, root_sha)
        diagnostic.update(stage="issue_commit", article_id=str(number), index_ref=root_sha)
        query = urllib.parse.urlencode({"path": f"docs/issue-{number}.md", "sha": root_sha, "per_page": 1})
        commits = fetch_json(API + "/commits?" + query)
        if not isinstance(commits, list) or not commits or not isinstance(commits[0], dict):
            raise ValueError("GitHub issue commit history is empty or invalid")
        issue_sha = commit_sha(commits[0].get("sha"))
        commit = commits[0].get("commit")
        committer = commit.get("committer") if isinstance(commit, dict) else None
        updated = validate_updated_at(committer.get("date") if isinstance(committer, dict) else None,
                                      expected_day, max_age_days)
        diagnostic.update(stage="body", source_ref=issue_sha, source_updated_at=updated)
        api_url = f"{RAW}/{issue_sha}/docs/issue-{number}.md"
        body = fetch_text(api_url)
        title = validate_body(body, number)
        corpus = body.encode("utf-8")
        digest = hashlib.sha256(corpus).hexdigest()
        article = {"article_id": str(number), "title": title,
                   "url": f"{REPOSITORY}/blob/{issue_sha}/docs/issue-{number}.md", "api_url": api_url,
                   "body": body, "body_sha256": digest, "body_characters": len(body)}
        metadata = {"source_kind": "public_articles", "source_id": "ruanyf_weekly", "source_name": SOURCE_NAME,
                    "source_url": REPOSITORY, "source_ref": issue_sha, "index_ref": root_sha,
                    "selection_date": expected_day.isoformat(), "source_updated_at": updated,
                    "index_fetched_at": index_fetched_at, "fetched_at": datetime.now(SHANGHAI).isoformat(),
                    "articles": 1, "articles_with_bodies": 1, "fallback_articles": 0,
                    "corpus_bytes": len(corpus), "corpus_sha256": digest, "attribution": ATTRIBUTION,
                    "article_details": [article]}
        diagnostic["stage"] = "publish"
        script_dir = str(Path(__file__).resolve().parent)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        from download_public_articles import publish_pair
        publish_pair(Path(out), corpus, (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        diagnostic.update(status="success", stage="complete", articles=1, corpus_sha256=digest)
        _diagnostic_save(diagnostics_dir, diagnostic)
        return metadata
    except (ValueError, RuntimeError, OSError) as exc:
        token = os.environ.get("GITHUB_TOKEN", "")
        message = str(exc)
        if token:
            message = message.replace(token, "[REDACTED]")
        diagnostic.update(status="failure", error_type=type(exc).__name__, error=message)
        _diagnostic_save(diagnostics_dir, diagnostic)
        if token and token in str(exc):
            raise RuntimeError(message) from None
        raise
