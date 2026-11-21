#!/usr/bin/env python3
"""Public GitHub repository lead discovery; no third-party dependencies.

Run from the skill directory:
    python scripts/github_search.py -q "multi agent browser" -q "authenticated Chrome agent" --format markdown

This is not semantic search and does not verify capabilities.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.github.com/search/repositories"
TIMEOUT_SECONDS = 20


class SearchError(Exception):
    """GitHub API or network error, without leaking credentials."""


def fetch_items(
    query: str, per_query: int, sort: str, token: str | None
) -> list[dict[str, Any]]:
    """Fetch one page. The public GitHub API returns best-match by default."""
    params: dict[str, str | int] = {"q": query, "per_page": per_query}
    if sort != "best-match":
        params["sort"] = sort
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "find-anything/0.1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(f"{API}?{urlencode(params)}", headers=headers)
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = json.load(response)
    except HTTPError as exc:
        if exc.code in (403, 429):
            raise SearchError(
                f"GitHub API returned HTTP {exc.code} (possibly rate limited). "
                "Try GITHUB_TOKEN or retry later."
            ) from exc
        if exc.code == 422:
            raise SearchError(f"GitHub rejected query {query!r} (HTTP 422).") from exc
        raise SearchError(f"GitHub API returned HTTP {exc.code}.") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise SearchError(f"Unable to contact GitHub: {type(exc).__name__}.") from exc
    except (ValueError, TypeError) as exc:
        raise SearchError("GitHub returned invalid JSON.") from exc

    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise SearchError("GitHub response did not contain an items list.")
    return [item for item in payload["items"] if isinstance(item, dict)]


def normalize(item: dict[str, Any], query: str) -> dict[str, Any] | None:
    """Normalize only the fields used for discovery and audit."""
    full_name = item.get("full_name")
    url = item.get("html_url")
    if not isinstance(full_name, str) or not full_name or not isinstance(url, str):
        return None
    lic = item.get("license") or {}
    return {
        "full_name": full_name,
        "url": url,
        "description": item.get("description") or "",
        "stars": item.get("stargazers_count"),
        "updated_at": item.get("updated_at"),
        "archived": bool(item.get("archived", False)),
        "fork": bool(item.get("fork", False)),
        "topics": item.get("topics") or [],
        "license": lic.get("spdx_id") if isinstance(lic, dict) else None,
        "found_by": [query],
    }


def merge_results(batches: list[tuple[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    """Deduplicate canonical repositories and record query provenance."""
    merged: dict[str, dict[str, Any]] = {}
    for query, items in batches:
        for raw in items:
            candidate = normalize(raw, query)
            if candidate is None:
                continue
            key = candidate["full_name"].casefold()
            if key in merged:
                if query not in merged[key]["found_by"]:
                    merged[key]["found_by"].append(query)
            else:
                merged[key] = candidate
    # Repeated query matches boost visibility, not stars or an invented fit score.
    return sorted(merged.values(), key=lambda item: -len(item["found_by"]))


def collect(
    queries: list[str],
    per_query: int = 20,
    max_total: int = 50,
    sort: str = "best-match",
    fetch: Callable[[str, int, str, str | None], list[dict[str, Any]]] = fetch_items,
    token: str | None = None,
) -> dict[str, Any]:
    """Search independent queries; return partial results and errors explicitly."""
    batches: list[tuple[str, list[dict[str, Any]]]] = []
    errors: list[dict[str, str]] = []
    for query in dict.fromkeys(query.strip() for query in queries if query.strip()):
        try:
            batches.append((query, fetch(query, per_query, sort, token)))
        except SearchError as exc:
            errors.append({"query": query, "error": str(exc)})
    results = merge_results(batches)
    return {
        "searched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "GitHub public repository search API only",
        "queries": list(dict.fromkeys(query.strip() for query in queries if query.strip())),
        "sort": sort,
        "successful_queries": len(batches),
        "errors": errors,
        "unique_candidates_before_limit": len(results),
        "results": results[:max_total],
    }


def render_markdown(report: dict[str, Any]) -> str:
    def clean(value: Any) -> str:
        return str(value or "").replace("|", "\\|").replace("\n", " ").replace("\r", " ")

    lines = [
        "# GitHub candidate leads (not verified)",
        "",
        f"Source: {report['source']}. Searched: {report['searched_at_utc']}.",
        f"Queries succeeded: {report['successful_queries']}/{len(report['queries'])}. "
        f"Unique repositories: {report['unique_candidates_before_limit']}.",
        "",
        "| Repository | Description | Stars | Updated | Query matches | Flags |",
        "|---|---|---:|---|---:|---|",
    ]
    for item in report["results"]:
        flags = ", ".join(
            label for name, label in (("archived", "archived"), ("fork", "fork"))
            if item.get(name)
        )
        title = clean(item["full_name"])
        desc = clean(item["description"])[:140]
        stars = item["stars"] if item["stars"] is not None else "?"
        lines.append(
            f"| [{title}]({item['url']}) | {desc} | {stars} | "
            f"{clean(item['updated_at'])[:10]} | {len(item['found_by'])} | {flags} |"
        )
    if report["errors"]:
        lines.extend(["", "## Incomplete queries"])
        for item in report["errors"]:
            lines.append(f"- {clean(item['query'])}: {clean(item['error'])}")
    lines.extend([
        "",
        "Results are discovery leads, not evidence of supported functionality. "
        "Read official docs and relevant code for finalists; search other ecosystems separately.",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Discover public GitHub repo leads from multiple independent queries."
    )
    parser.add_argument("-q", "--query", action="append", required=True, help="Repeatable query.")
    parser.add_argument("--per-query", type=int, default=20, help="Results per query (1–100).")
    parser.add_argument("--max-total", type=int, default=50, help="Maximum unique output (1–1000).")
    parser.add_argument("--sort", choices=["best-match", "updated", "stars"], default="best-match")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    if not 1 <= args.per_query <= 100:
        parser.error("--per-query must be in 1..100")
    if not 1 <= args.max_total <= 1000:
        parser.error("--max-total must be in 1..1000")
    if not any(q.strip() for q in args.query):
        parser.error("Provide at least one non-empty --query.")

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    report = collect(
        args.query, per_query=args.per_query, max_total=args.max_total,
        sort=args.sort, token=token,
    )
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))

    if report["successful_queries"] == 0:
        print("All GitHub searches failed; no coverage claim is justified.", file=sys.stderr)
        return 2
    if report["errors"]:
        print(f"{len(report['errors'])} GitHub queries failed; results are partial.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
