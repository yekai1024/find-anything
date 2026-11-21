"""Offline unit tests: python -m unittest discover -s tests -v."""

from __future__ import annotations

import importlib.util
import pathlib
import unittest
from unittest import mock

PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "github_search.py"
SPEC = importlib.util.spec_from_file_location("github_search", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def item(name: str, stars: int = 0, description: str = "candidate") -> dict:
    return {
        "full_name": name,
        "html_url": "https://github.com/" + name,
        "description": description,
        "stargazers_count": stars,
        "archived": False,
        "updated_at": "2026-11-21T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "topics": [],
    }


class GitHubSearchTests(unittest.TestCase):
    def test_deduplicates_and_records_query_origins(self) -> None:
        def fake(query, per_query, sort, token):
            if query == "browser agent":
                return [item("org/A", 2), item("org/B", 50000)]
            return [item("org/a", 2), item("org/C", 1)]

        report = MODULE.collect(["browser agent", "persistent profile"], fetch=fake)
        self.assertEqual(report["successful_queries"], 2)
        self.assertEqual(report["unique_candidates_before_limit"], 3)
        self.assertEqual(report["results"][0]["full_name"], "org/A")
        self.assertEqual(len(report["results"][0]["found_by"]), 2)
        self.assertNotEqual(report["results"][0]["full_name"], "org/B")

    def test_repeated_queries_are_not_issued_twice(self) -> None:
        queries = []
        def fake(query, per_query, sort, token):
            queries.append(query)
            return []

        MODULE.collect([" x ", "x", "y"], fetch=fake)
        self.assertEqual(queries, ["x", "y"])

    def test_keeps_partial_results_and_explicit_errors(self) -> None:
        def fake(query, per_query, sort, token):
            if query == "broken":
                raise MODULE.SearchError("rate limited")
            return [item("org/good")]

        report = MODULE.collect(["works", "broken"], fetch=fake)
        self.assertEqual(report["successful_queries"], 1)
        self.assertEqual(len(report["results"]), 1)
        self.assertEqual(report["errors"][0]["query"], "broken")

    def test_malformed_records_are_skipped(self) -> None:
        report = MODULE.collect(["x"], fetch=lambda *args: [{}, item("org/good"), {"full_name": ""}])
        self.assertEqual(len(report["results"]), 1)

    def test_markdown_escapes_pipes_and_discloses_limits(self) -> None:
        report = MODULE.collect(["x"], fetch=lambda *args: [item("org/a", description="a | b")])
        output = MODULE.render_markdown(report)
        self.assertIn("a \\| b", output)
        self.assertIn("not verified", output)
        self.assertIn("GitHub", output)

    def test_invalid_cli_limit_fails_without_network(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            MODULE.main(["-q", "anything", "--per-query", "0"])
        self.assertEqual(caught.exception.code, 2)

    def test_cli_json_output_is_parseable(self) -> None:
        from io import StringIO
        with mock.patch.object(MODULE, "collect", return_value={
            "successful_queries": 1, "errors": [], "results": [], "queries": ["x"],
        }):
            with mock.patch("sys.stdout", new_callable=StringIO) as out:
                result = MODULE.main(["-q", "x", "--format", "json"])
        self.assertEqual(result, 0)
        self.assertEqual(__import__("json").loads(out.getvalue())["queries"], ["x"])


if __name__ == "__main__":
    unittest.main()
