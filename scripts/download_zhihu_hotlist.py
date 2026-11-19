"""Download today's Zhihu hot list and save it as a benchmark corpus file.

Writes entries in the same layout as ``data/corpus/news.txt``: a ``链接：``
line with the question URL, then the question title and the top answer's
body text.

The hot list comes from a third-party aggregation API (no login needed).
The full answer bodies are read by rendering each ``/question/<id>`` page in a
real Chromium (Playwright). Zhihu gates its detail pages behind a JS challenge
(``__zse_ck`` / ``x-zse-96``) that flags plain HTTP clients *and* detectable
automation (e.g. ``navigator.webdriver``), returning HTTP 403 / ``40362``.
Use a real browser with its native user agent/client hints, optionally with a
dedicated persistent profile. An initial HTTP 403 may resolve after page JS runs;
only rendered answer nodes count as success. Login/verification may still be
required by Zhihu; this script does not bypass either.

Usage (from repository root):

  python scripts/download_zhihu_hotlist.py
  python scripts/download_zhihu_hotlist.py --limit 30 --delay 1
  python scripts/download_zhihu_hotlist.py --answers 3        # top-N answers per question (default: 3)
  python scripts/download_zhihu_hotlist.py --headed          # visible browser, for debugging
  python scripts/download_zhihu_hotlist.py --headed --browser-channel chrome --profile-dir .cache/zhihu-browser --require-bodies

Requires: pip install playwright && playwright install chromium
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

DEFAULT_API = "https://uapis.cn/api/v1/misc/hotboard?type=zhihu"
ROOT = Path(__file__).resolve().parent.parent

_TAG_RE = re.compile(r"<[^>]+>")
_QID_RE = re.compile(r"/question/(\d+)")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def _ssl_context():
    ctx = __import__("ssl").create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = __import__("ssl").CERT_NONE
    return ctx


def _fetch_json(url: str, proxy: str = "", timeout: int = 30) -> dict:
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    handlers.append(urllib.request.HTTPSHandler(context=_ssl_context()))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.build_opener(*handlers).open(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _clean(text: str) -> str:
    text = html.unescape(_TAG_RE.sub("", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def _plain_text(text: str) -> str:
    """DOM innerText is already decoded text; preserve literal <, > and entities."""
    return re.sub(r"\s+", " ", text or "").strip()


def hotlist_description(item: dict) -> str:
    """Support both legacy desc and the current API's info[] excerpts."""
    extra = item.get("extra") or {}
    desc = _clean(extra.get("desc", ""))
    if desc:
        return desc
    info = extra.get("info", [])
    if not isinstance(info, list):
        return ""
    return " ".join(
        cleaned for text in info if isinstance(text, str)
        if (cleaned := _clean(text))
        and not re.match(r"^热度\s*[:：]", cleaned)
        and cleaned not in {"[视频]", "[图片]"}
    )


def download(limit: int = 30, api: str = DEFAULT_API, proxy: str = "", *, provenance: dict | None = None) -> list:
    payload = _fetch_json(api, proxy=proxy)
    if provenance is not None:
        from datetime import datetime, timezone
        provenance.update(source_url=api, hotlist_updated_at=payload.get("update_time"),
                          hotlist_fetched_at=datetime.now(timezone.utc).isoformat())
    rows = payload.get("list", [])
    if not isinstance(rows, list):
        raise RuntimeError("unexpected payload from API: missing 'list'")
    return rows[:limit]


class _ZhihuBrowser:
    """Native Chromium-family session for rendered, publicly accessible answers."""

    def __init__(self, proxy: str = "", headed: bool = False,
                 channel: str = "chromium", profile_dir: Path | None = None):
        from playwright.sync_api import sync_playwright

        self._pw = sync_playwright()
        self._playwright = self._pw.start()
        self.last_fetch = {}
        launch_kwargs = {
            "headless": not headed,
            "args": ["--disable-blink-features=AutomationControlled"],
            "ignore_default_args": ["--enable-automation"],
        }
        if channel != "chromium":
            launch_kwargs["channel"] = channel
        if proxy:
            launch_kwargs["proxy"] = {"server": proxy}
        # Keep the browser's real UA, client hints, plugins and permissions in
        # agreement. A fixed Chrome/126 UA and fabricated JS properties are
        # inconsistent with current browser versions and can fail challenges.
        context_kwargs = dict(locale="zh-CN", timezone_id="Asia/Shanghai",
                              viewport={"width": 1440, "height": 1000})
        self._browser = None
        if profile_dir is not None:
            self._context = self._playwright.chromium.launch_persistent_context(
                str(profile_dir.resolve()), **launch_kwargs, **context_kwargs)
        else:
            self._browser = self._playwright.chromium.launch(**launch_kwargs)
            self._context = self._browser.new_context(**context_kwargs)
        # Establish normal session/challenge cookies before question navigation.
        warmup = self._context.new_page()
        try:
            warmup.goto("https://www.zhihu.com/", wait_until="domcontentloaded", timeout=45000)
            warmup.wait_for_timeout(4000)
        except Exception as exc:
            print(f"[browser warmup] {exc}", file=sys.stderr)
        finally:
            warmup.close()

    def fetch_top_answers(self, qid: str, max_answers: int = 3) -> list:
        page = self._context.new_page()
        self.last_fetch = {"question_id": qid, "url": f"https://www.zhihu.com/question/{qid}",
                           "initial_http_status": None, "answers": []}
        try:
            response = page.goto(self.last_fetch["url"], timeout=45000, wait_until="domcontentloaded")
            self.last_fetch["initial_http_status"] = response.status if response else None
            # An initial 403 can be a JS challenge, not the final page. Judge
            # success by rendered answer DOM, never by response.status alone.
            try:
                page.wait_for_selector(".List-item .RichContent-inner", timeout=30000)
            except Exception:
                self.last_fetch["error"] = page.locator("body").inner_text()[:500]
                print(f"[no answers] {qid}: HTTP {self.last_fetch['initial_http_status']}", file=sys.stderr)
                return []
            count_js = "() => document.querySelectorAll('.List-item .RichContent-inner').length"
            last = 0
            stall = 0
            for _ in range(8):
                n = page.evaluate(count_js)
                if n >= max_answers:
                    break
                if n == last:
                    stall += 1
                    if stall >= 2:
                        break
                else:
                    stall = 0
                last = n
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1500)
            records = page.evaluate(r"""() => Array.from(document.querySelectorAll('.List-item'))
                .map(item => {
                    const rich = item.querySelector('.RichContent-inner');
                    if (!rich || !rich.innerText.trim()) return null;
                    const meta = item.querySelector('meta[itemprop="url"][content*="/answer/"]');
                    const link = item.querySelector('a[href*="/answer/"]');
                    const answer = item.querySelector('.AnswerItem');
                    let id = '';
                    try { id = JSON.parse(answer?.getAttribute('data-zop') || '{}').itemId || ''; } catch {}
                    return {text: rich.innerText.trim(),
                            answer_url: meta?.content || link?.href || (id ? location.origin + location.pathname + '/answer/' + id : ''),
                            answer_id: String(id)};
                }).filter(Boolean)""")
            records = records[:max_answers]
            for record in records:
                if record["answer_id"].isdigit():
                    record["answer_url"] = f"https://www.zhihu.com/question/{qid}/answer/{record['answer_id']}"
                record["text"] = _plain_text(record["text"])
                record["characters"] = len(record["text"])
            self.last_fetch["answers"] = records
            self.last_fetch["final_url"] = page.url
            print(f"[answers] {qid}: {len(records)} answers, {sum(r['characters'] for r in records)} chars", file=sys.stderr)
            return [record["text"] for record in records]
        except Exception as e:
            self.last_fetch["error"] = str(e)
            print(f"  [skip] {qid}: {e}", file=sys.stderr)
            return []
        finally:
            page.close()

    def close(self) -> None:
        try:
            self._context.close()
        finally:
            self._playwright.stop()


def write_corpus(rows: list, out: Path, browser: "_ZhihuBrowser | None" = None, delay: float = 1.0, max_answers: int = 3,
                 require_bodies: bool = False, require_all_bodies: bool = False) -> int:
    lines = []
    fetched = 0
    answer_count = 0
    details = []
    for i, item in enumerate(rows):
        url = item.get("url", "")
        title = _clean(item.get("title", ""))
        desc = hotlist_description(item)
        lines.append(f"链接：{url}")
        if title:
            lines.append(title)
        answers = []
        if browser:
            m = _QID_RE.search(url)
            if m:
                answers = browser.fetch_top_answers(m.group(1), max_answers=max_answers)
                details.append(dict(browser.last_fetch))
        if answers:
            fetched += 1
            answer_count += len(answers)
            lines.extend(answers)
        elif desc:
            lines.append(desc)
        if i < len(rows) - 1 and delay:
            time.sleep(delay)
        lines.append("")
    if require_bodies and fetched == 0:
        raise RuntimeError("No answer bodies fetched; refusing to overwrite corpus with excerpts/titles")
    if require_all_bodies and (not rows or fetched != len(rows)):
        raise RuntimeError(f"Answer bodies missing for {len(rows) - fetched}/{len(rows)} questions; refusing to overwrite corpus")
    out.write_text("\n".join(lines), encoding="utf-8")
    from datetime import datetime
    import hashlib
    metadata = {"fetched_at": datetime.now().astimezone().isoformat(),
                "questions": len(rows), "questions_with_answer_bodies": fetched,
                "answer_bodies": answer_count, "fallback_questions": len(rows) - fetched,
                "actual_content": "question titles + rendered answer bodies; failed questions use available excerpts/titles",
                "corpus_bytes": out.stat().st_size,
                "corpus_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                "question_details": details}
    out.with_suffix(".meta.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"fetched {answer_count} answer bodies for {fetched}/{len(rows)} items (others use available hot-list excerpts or titles only)")
    return len(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Download today's Zhihu hot list as a corpus file")
    parser.add_argument("--limit", type=int, default=30, help="how many hot-list items to fetch (default: 30)")
    parser.add_argument("--out", type=Path, default=None, help="output .txt path (default: data/corpus/zhihu_hotlist_YYYY-MM-DD.txt)")
    parser.add_argument("--api", default=DEFAULT_API, help="hot-list API URL (default: %(default)s)")
    parser.add_argument("--proxy", default=None, help="proxy for all requests, e.g. http://127.0.0.1:7890 (or set ALL_PROXY)")
    parser.add_argument("--headed", action="store_true", help="run the browser with a visible window")
    parser.add_argument("--browser-channel", choices=["chromium", "chrome", "msedge"], default="chromium", help="Browser installation to use")
    parser.add_argument("--profile-dir", type=Path, default=None, help="Dedicated persistent browser profile (do not use your regular browser profile)")
    parser.add_argument("--require-bodies", action="store_true", help="Fail without overwriting the corpus if no actual answer bodies are fetched")
    parser.add_argument("--require-all-bodies", action="store_true", help="Fail without overwriting if any hot-list question has no actual answer body")
    parser.add_argument("--answers", type=int, default=3, help="top-N answers to fetch per question (default: 3)")
    parser.add_argument("--delay", type=float, default=1.0, help="extra seconds to wait between questions (default: 1)")
    args = parser.parse_args(argv)

    proxy = args.proxy or os.environ.get("ALL_PROXY") or os.environ.get("HTTPS_PROXY") or ""
    if args.out is None:
        args.out = ROOT / "data" / "corpus" / f"zhihu_hotlist_{date.today().isoformat()}.txt"

    provenance = {}
    rows = download(limit=args.limit, api=args.api, proxy=proxy, provenance=provenance)
    if not rows:
        print("no items returned by API", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)

    browser = None
    try:
        browser = _ZhihuBrowser(proxy=proxy, headed=args.headed,
                                channel=args.browser_channel, profile_dir=args.profile_dir)
    except ImportError:
        print("warning: playwright is not installed (pip install playwright && playwright install chromium); "
              "hot-list excerpt only", file=sys.stderr)

    try:
        n_lines = write_corpus(rows, args.out, browser=browser, delay=args.delay,
                               max_answers=args.answers, require_bodies=args.require_bodies,
                               require_all_bodies=args.require_all_bodies)
        meta_path = args.out.with_suffix(".meta.json")
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        metadata.update(provenance)
        metadata["browser_channel"] = args.browser_channel
        meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    finally:
        if browser:
            browser.close()
    print(f"wrote {len(rows)} hot-list items ({n_lines} lines) -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())