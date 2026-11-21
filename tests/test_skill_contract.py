"""Check that the Skill entry point and bundled references are internally coherent."""

from __future__ import annotations

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_header(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        header = skill.split("---\n", 2)[1]
        self.assertRegex(header, r"(?m)^name: find-anything$")
        description = re.search(r"(?m)^description:\s*(.+)$", header)
        self.assertIsNotNone(description)
        assert description is not None
        self.assertLessEqual(len(description.group(1)), 1024)
        self.assertGreater(len(description.group(1)), 20)

    def test_relative_references_exist(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"\]\(((?:references|tests)/[^)]+)\)", skill)
        self.assertGreaterEqual(len(references), 3)
        for relative in references:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_discovery_instructions_are_not_single_path(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for term in ("Wave A", "Wave B", "Wave C", "Unknown", "Adopt", "Build"):
            with self.subTest(term=term):
                self.assertIn(term, skill)


if __name__ == "__main__":
    unittest.main()
