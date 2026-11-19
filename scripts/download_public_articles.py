#!/usr/bin/env python3
"""Fetch complete public Chinese text without login or browser.

Default: latest GitHub-hosted technology weekly, pinned to its source commit.
Optional: current-day Zhihu Daily. No title or feed summary substitutes a body.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import http.client
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import socket
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from public_source_transport import DailyHTTPSHandler

SHANGHAI = timezone(timedelta(hours=8))
API_HOST = "news-at.zhihu.com"
FEED_URL = f"https://{API_HOST}/api/4/news/latest"
DETAIL_BASE = f"https://{API_HOST}/api/4/news/"
SOURCE_NAME = "知乎日报公开文章"
MAX_RESPONSE_BYTES = 10 * 1024 * 1024
HANZI = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002ebef]")


def shanghai_today() -> date:
    return datetime.now(SHANGHAI).date()


def validate_api_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname != API_HOST
            or parsed.port not in (None, 443) or parsed.username or parsed.password
            or parsed.query or parsed.fragment
            or re.fullmatch(r"/api/4/news/(?:latest|[0-9]+)", parsed.path) is None):
        raise ValueError("Only fixed-host HTTPS Daily feed/detail URLs are allowed")
    return url


class FixedHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_api_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def network_error_description(exc: BaseException) -> str:
    """Retain actionable causes without exposing proxy credentials or query secrets."""
    reason = getattr(exc, "reason", exc)
    if isinstance(reason, ssl.SSLCertVerificationError):
        category = "TLS_CERTIFICATE_VERIFY_FAILED"
    elif isinstance(reason, ssl.SSLError):
        category = "TLS_ERROR"
    elif isinstance(reason, socket.gaierror):
        category = "DNS_ERROR"
    elif isinstance(reason, TimeoutError):
        category = "TIMEOUT"
    else:
        category = type(reason).__name__
    # Arbitrary URLError strings can contain an entire private proxy config.
    # Typed OS/TLS exceptions retain their actionable, sanitized reason below.
    message = ("unclassified network failure" if isinstance(reason, str) else str(reason))
    message = message.replace("\r", " ").replace("\n", " ")
    message = re.sub(r"(?i)(https?://)[^/\s@]+@", r"\1[redacted]@", message)
    message = re.sub(r"(?i)((?:access_secret|token|password|api_key)=)[^&\s]+", r"\1[redacted]", message)
    return f"{category}: {message[:500]}"


def fetch_json(url: str, *, timeout: float = 30, attempts: int = 3) -> dict:
    """Bounded, read-only GET retries. TLS certificate verification stays enabled."""
    validate_api_url(url)
    if timeout <= 0 or attempts < 1 or attempts > 5:
        raise ValueError("Invalid HTTP timeout/retry settings")
    opener = urllib.request.build_opener(FixedHostRedirect(), DailyHTTPSHandler())
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={
                "Accept": "application/json", "User-Agent": "rime-schema-compare-public-articles/1.0"}, method="GET")
            with opener.open(request, timeout=timeout) as response:
                validate_api_url(response.geturl())
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise ValueError("Daily API response exceeds the size limit")
            try:
                result = json.loads(raw.decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError("Daily API did not return valid JSON (possibly an HTML error page)") from exc
            if not isinstance(result, dict):
                raise ValueError("Daily API JSON must be an object")
            return result
        except urllib.error.HTTPError as exc:
            if exc.code not in {408, 429, 500, 502, 503, 504} or attempt + 1 == attempts:
                raise RuntimeError(f"Daily API HTTP {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as exc:
            description = network_error_description(exc)
            print(f"[Daily API attempt {attempt + 1}/{attempts}] {description}", file=sys.stderr)
            if attempt + 1 == attempts:
                raise RuntimeError(f"Daily API network request failed after bounded retries: {description}") from None
        if attempt + 1 < attempts:
            time.sleep(2 ** attempt)
    raise RuntimeError("Daily API request failed")


def article_id(value) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("Daily article ID must be a positive numeric identifier")
    result = str(value)
    if not re.fullmatch(r"[0-9]+", result) or int(result) <= 0:
        raise ValueError("Daily article ID must be a positive numeric identifier")
    return result


class ContentParser(HTMLParser):
    """Extract only .content containers, excluding metadata and executable text."""
    BLOCKS = {"p", "div", "br", "li", "ul", "ol", "blockquote", "pre", "h1", "h2", "h3", "h4", "hr", "figcaption"}
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    BLOCKED_TAGS = {"script", "style", "noscript", "iframe", "svg", "nav", "button"}
    BLOCKED_CLASSES = {"meta", "author", "bio", "avatar", "view-more", "share", "share-box", "navigation", "originUrl"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.frames: list[tuple[str, bool, bool]] = []
        self.parts: list[str] = []
        self.containers = 0

    def newline(self):
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        is_content = tag == "div" and "content" in classes
        parent_active = self.frames[-1][1] if self.frames else False
        parent_blocked = self.frames[-1][2] if self.frames else False
        blocked = parent_blocked or tag in self.BLOCKED_TAGS or bool(classes & self.BLOCKED_CLASSES)
        active = parent_active or is_content
        if is_content and not blocked:
            self.containers += 1
        if active and not blocked and tag in self.BLOCKS:
            self.newline()
        if tag not in self.VOID:
            self.frames.append((tag, active, blocked))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.frames) - 1, -1, -1):
            current, active, blocked = self.frames[index]
            if current == tag:
                if active and not blocked and tag in self.BLOCKS:
                    self.newline()
                del self.frames[index:]
                break

    def handle_data(self, data):
        if self.frames and self.frames[-1][1] and not self.frames[-1][2]:
            if data.strip() not in {"查看知乎原文", "查看原文"}:
                self.parts.append(data)

    def text(self) -> str:
        paragraphs = [re.sub(r"\s+", " ", line).strip() for line in "".join(self.parts).splitlines()]
        return "\n\n".join(line for line in paragraphs if line)


def extract_body(html: str, *, min_hanzi: int = 30) -> str:
    if not isinstance(html, str) or not html.strip():
        raise ValueError("Daily article has no HTML body")
    if min_hanzi < 1:
        raise ValueError("min_hanzi must be positive")
    parser = ContentParser()
    parser.feed(html)
    parser.close()
    text = parser.text()
    if parser.containers == 0:
        raise ValueError("Daily article has no central content container")
    if re.search(r"^(?:请先?登录|登录后(?:查看|继续)|请完成.{0,20}验证|访问过于频繁|请求存在异常|access denied|403 forbidden)", text, re.I):
        raise ValueError("Daily article body is a login/verification/error message")
    if len(HANZI.findall(text)) < min_hanzi:
        raise ValueError("Daily article body is empty or below the minimum Hanzi count")
    return text


def select_stories(feed: dict, expected_day: date, limit: int) -> list[dict]:
    if limit < 1:
        raise ValueError("limit must be positive")
    raw_date = feed.get("date")
    if not isinstance(raw_date, str) or not re.fullmatch(r"[0-9]{8}", raw_date):
        raise ValueError("Daily feed date is missing or invalid")
    actual_day = datetime.strptime(raw_date, "%Y%m%d").date()
    if actual_day != expected_day:
        raise ValueError(f"Daily feed is not for the requested day: {actual_day.isoformat()}")
    stories = feed.get("stories")
    if not isinstance(stories, list) or not stories:
        raise ValueError("Daily feed has no current-day stories")
    selected = stories[:limit]
    ids = []
    for story in selected:
        if not isinstance(story, dict):
            raise ValueError("Daily feed story must be an object")
        ids.append(article_id(story.get("id")))
    if len(set(ids)) != len(ids):
        raise ValueError("Daily feed contains duplicate selected article IDs")
    return selected


def publish_pair(out: Path, corpus: bytes, metadata: bytes) -> None:
    """Stage both files first and roll back already-replaced outputs on errors."""
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = out.with_suffix(".meta.json")
    if out.is_symlink() or meta.is_symlink():
        raise ValueError("Refusing symlink corpus/metadata outputs")
    with tempfile.TemporaryDirectory(prefix="public-articles-", dir=out.parent) as stage_name:
        stage = Path(stage_name)
        targets = ((out, corpus), (meta, metadata))
        backups = {}
        staged = {}
        for index, (target, data) in enumerate(targets):
            temporary = stage / f"new-{index}"
            temporary.write_bytes(data)
            staged[target] = temporary
            if target.exists():
                backup = stage / f"old-{index}"
                shutil.copyfile(target, backup)
                backups[target] = backup
        replaced = []
        try:
            for target, _ in targets:
                os.replace(staged[target], target)
                replaced.append(target)
        except OSError:
            for target in reversed(replaced):
                if target in backups:
                    os.replace(backups[target], target)
                else:
                    target.unlink()
            raise


def save_diagnostic(directory: Path | None, diagnostic: dict) -> None:
    if directory is not None:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "articles.json").write_text(json.dumps(diagnostic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def download_articles(out: Path, *, expected_day: date | None = None, limit: int = 5,
                      delay: float = 5, min_hanzi: int = 30,
                      diagnostics_dir: Path | None = None) -> dict:
    expected_day = expected_day or shanghai_today()
    if delay < 0 or min_hanzi < 1 or limit < 1:
        raise ValueError("Invalid article count, delay or minimum Hanzi setting")
    diagnostic = {"source_kind": "public_articles", "source_id": "zhihu_daily", "source_url": FEED_URL,
                  "expected_date": expected_day.isoformat(), "article_details": [], "stage": "feed"}
    try:
        feed = fetch_json(FEED_URL)
        feed_fetched_at = datetime.now(SHANGHAI).isoformat()
        stories = select_stories(feed, expected_day, limit)
        details = []
        lines = []
        for index, story in enumerate(stories):
            identifier = article_id(story["id"])
            api_url = DETAIL_BASE + identifier
            diagnostic.update(stage="article", article_id=identifier)
            data = fetch_json(api_url)
            if "id" in data and article_id(data["id"]) != identifier:
                raise ValueError("Daily detail ID does not match its feed story")
            body = extract_body(data.get("body"), min_hanzi=min_hanzi)
            title = data.get("title") or story.get("title")
            if not isinstance(title, str) or not title.strip():
                raise ValueError("Daily article has no title")
            title = re.sub(r"\s+", " ", title).strip()
            url = f"https://daily.zhihu.com/story/{identifier}"
            detail = {"article_id": identifier, "title": title, "url": url, "api_url": api_url,
                      "body": body, "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                      "body_characters": len(body)}
            details.append(detail)
            diagnostic["article_details"].append({"article_id": identifier, "url": url,
                                                 "api_url": api_url, "body_characters": len(body)})
            lines.extend((f"链接：{url}", title, body, ""))
            if index + 1 < len(stories) and delay:
                time.sleep(delay)
        corpus = ("\n".join(lines).rstrip() + "\n").encode("utf-8")
        metadata = {"source_kind": "public_articles", "source_id": "zhihu_daily", "source_name": SOURCE_NAME,
                    "source_url": FEED_URL, "feed_date": expected_day.isoformat(),
                    "fetched_at": datetime.now(SHANGHAI).isoformat(), "feed_fetched_at": feed_fetched_at,
                    "articles": len(details), "articles_with_bodies": len(details), "fallback_articles": 0,
                    "corpus_bytes": len(corpus), "corpus_sha256": hashlib.sha256(corpus).hexdigest(),
                    "article_details": details}
        diagnostic["stage"] = "publish"
        encoded_metadata = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        publish_pair(out, corpus, encoded_metadata)
        diagnostic.update(status="success", stage="complete", articles=len(details), corpus_sha256=metadata["corpus_sha256"])
        try:
            save_diagnostic(diagnostics_dir, diagnostic)
        except OSError:
            # Successful corpus publication must not be misreported as failed
            # solely because a nonessential diagnostic update could not be saved.
            print("Warning: unable to save public-article diagnostics", file=sys.stderr)
        return metadata
    except (ValueError, OSError, RuntimeError) as exc:
        diagnostic.update(status="failure", error_type=type(exc).__name__, error=str(exc))
        try:
            save_diagnostic(diagnostics_dir, diagnostic)
        except OSError:
            print("Warning: unable to save public-article diagnostics", file=sys.stderr)
        raise


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("github-weekly", "zhihu-daily"), default="github-weekly", help="Public text source (default: GitHub-hosted weekly; Daily is opt-in)")
    parser.add_argument("--date", type=date.fromisoformat, default=None, help="Selection date, ISO YYYY-MM-DD (default: today in Asia/Shanghai)")
    parser.add_argument("--out", type=Path, default=None, help="Output corpus path")
    parser.add_argument("--limit", type=int, default=5, help="Maximum Daily stories; GitHub always selects one complete latest issue")
    parser.add_argument("--delay", type=float, default=5, help="Seconds between Daily article requests (default: 5)")
    parser.add_argument("--min-hanzi", type=int, default=30, help="Minimum Hanzi in each real body (default: 30)")
    parser.add_argument("--diagnostics-dir", type=Path, default=None)
    args = parser.parse_args(argv)
    day = args.date or shanghai_today()
    out = args.out or ROOT / "data" / "corpus" / f"public_articles_{day.isoformat()}.txt"
    try:
        if args.source == "github-weekly":
            from download_github_weekly import download_weekly
            metadata = download_weekly(out, expected_day=day, diagnostics_dir=args.diagnostics_dir)
        else:
            metadata = download_articles(out, expected_day=day, limit=args.limit, delay=args.delay,
                                         min_hanzi=args.min_hanzi, diagnostics_dir=args.diagnostics_dir)
    except (ValueError, OSError, RuntimeError) as exc:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            message = str(exc).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::error title=Public article download failed::{message}", flush=True)
        raise
    print(f"Downloaded {metadata['articles']} complete public text unit(s) from {metadata['source_name']}, "
          f"selected on {day.isoformat()}, {metadata['corpus_bytes']} bytes -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
