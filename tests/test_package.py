import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_required_distribution_files_exist(self):
        required = (
            "SKILL.md",
            "README.md",
            "LICENSE",
            "agents/openai.yaml",
            "scripts/code_map.py",
            "scripts/init_project.py",
            "references/agents-template.md",
            ".github/workflows/validate.yml",
        )
        missing = [relative for relative in required if not (ROOT / relative).is_file()]
        self.assertEqual(missing, [])

    def test_skill_frontmatter_has_expected_name_and_description(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertIn("name: repo-architecture-guard", frontmatter)
        self.assertRegex(frontmatter, r"description:\s+\S+")

    def test_readme_documents_install_update_and_initialization(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills add", text)
        self.assertIn("npx skills update", text)
        self.assertIn("init_project.py", text)
        self.assertIn("--brief", text)
        self.assertIn("$repo-architecture-guard", text)


if __name__ == "__main__":
    unittest.main()
