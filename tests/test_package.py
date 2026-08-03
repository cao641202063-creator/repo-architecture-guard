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

    def test_governance_policy_requires_product_readiness_and_proportional_testing(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        policy = (ROOT / "references" / "agents-template.md").read_text(encoding="utf-8")
        artifacts = (ROOT / "references" / "artifact-contract.md").read_text(encoding="utf-8")

        for text in (skill, policy):
            self.assertIn("Requirement Readiness and Product Challenge", text)
            self.assertIn("Complexity and Regression Decision", text)
            self.assertIn("full regression", text)
            self.assertIn("reversible assumption", text)

        self.assertIn("Solution Review Artifact", artifacts)
        self.assertIn("non-UI", artifacts)

    def test_governance_policy_requires_scale_aware_impact_and_independent_audit(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        policy = (ROOT / "references" / "agents-template.md").read_text(encoding="utf-8")
        map_contract = (ROOT / "references" / "code-map-contract.md").read_text(encoding="utf-8")
        artifacts = (ROOT / "references" / "artifact-contract.md").read_text(encoding="utf-8")

        for text in (skill, policy):
            self.assertIn("Scope-First Global Logic", text)
            self.assertIn("Documentation Impact Analysis", text)
            self.assertIn("Independent Delivery Audit", text)

        self.assertIn("Global Logic Navigation", map_contract)
        self.assertIn("scope hypothesis", map_contract)
        self.assertIn("data or event boundaries", map_contract)
        self.assertIn("Documentation Impact Analysis", artifacts)
        self.assertIn("Independent Agent Audit", artifacts)
        self.assertIn("fresh context", artifacts)
        self.assertIn("at most one revision pass", artifacts)
        self.assertIn("self-review", artifacts)

    def test_human_facing_artifacts_default_to_simplified_chinese(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        policy = (ROOT / "references" / "agents-template.md").read_text(encoding="utf-8")
        artifacts = (ROOT / "references" / "artifact-contract.md").read_text(encoding="utf-8")
        review = (ROOT / "references" / "html-review-contract.md").read_text(encoding="utf-8")

        for text in (skill, policy, artifacts, review):
            self.assertIn("简体中文", text)


if __name__ == "__main__":
    unittest.main()
