import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "init_project.py"
START_MARKER = "<!-- repo-architecture-guard:start -->"
END_MARKER = "<!-- repo-architecture-guard:end -->"


class ProjectInitializerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _run(self, *args):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(self.root),
                "--json",
                *args,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def _business_args(self):
        return (
            "--project-name",
            "华望知识库",
            "--target-users",
            "产品经理;实施顾问",
            "--outcome",
            "让用户快速定位可信知识",
            "--milestone",
            "完成首个可评审版本",
            "--success-criteria",
            "核心检索流程通过;关键页面可用",
            "--non-goals",
            "本阶段不接入外部计费",
            "--constraints",
            "必须支持中文;复用现有登录体系",
        )

    def test_non_interactive_initialization_creates_business_documents(self):
        result = self._run(*self._business_args(), "--no-code-map")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "initialized")
        goal = (self.root / "ProjectGoal.md").read_text(encoding="utf-8")
        self.assertIn("华望知识库", goal)
        self.assertIn("产品经理", goal)
        self.assertIn("让用户快速定位可信知识", goal)
        agents = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(START_MARKER, agents)
        self.assertIn(END_MARKER, agents)
        self.assertIn("$repo-architecture-guard", agents)
        self.assertIn("华望知识库", agents)
        self.assertTrue((self.root / "docs/ai/project-status.md").exists())
        self.assertEqual(payload["code_map"]["action"], "skipped")

    def test_existing_agents_content_is_preserved_and_block_is_idempotent(self):
        original = "# Existing Rules\n\nKeep this exact policy.\n"
        (self.root / "AGENTS.md").write_text(original, encoding="utf-8")

        first = self._run(*self._business_args(), "--no-code-map")
        second = self._run(
            *self._business_args(),
            "--outcome",
            "更新后的业务目标",
            "--no-code-map",
        )

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        agents = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(agents.startswith(original))
        self.assertEqual(agents.count(START_MARKER), 1)
        self.assertEqual(agents.count(END_MARKER), 1)
        self.assertIn("更新后的业务目标", agents)

    def test_existing_goal_and_status_are_preserved_without_force(self):
        (self.root / "ProjectGoal.md").write_text("existing goal\n", encoding="utf-8")
        status_path = self.root / "docs/ai/project-status.md"
        status_path.parent.mkdir(parents=True)
        status_path.write_text("existing status\n", encoding="utf-8")

        result = self._run(*self._business_args(), "--no-code-map")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            (self.root / "ProjectGoal.md").read_text(encoding="utf-8"),
            "existing goal\n",
        )
        self.assertEqual(status_path.read_text(encoding="utf-8"), "existing status\n")
        self.assertIn("ProjectGoal.md", payload["preserved"])
        self.assertIn("docs/ai/project-status.md", payload["preserved"])

    def test_force_flags_replace_existing_goal_and_status(self):
        (self.root / "ProjectGoal.md").write_text("existing goal\n", encoding="utf-8")
        status_path = self.root / "docs/ai/project-status.md"
        status_path.parent.mkdir(parents=True)
        status_path.write_text("existing status\n", encoding="utf-8")

        result = self._run(
            *self._business_args(),
            "--force-goal",
            "--force-status",
            "--no-code-map",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "华望知识库",
            (self.root / "ProjectGoal.md").read_text(encoding="utf-8"),
        )
        self.assertNotEqual(status_path.read_text(encoding="utf-8"), "existing status\n")

    def test_business_brief_is_retained_and_missing_fields_are_explicit(self):
        brief = self.root / "business.md"
        brief.write_text("需要让实施人员快速查询设备知识。", encoding="utf-8")

        result = self._run("--brief", str(brief), "--no-code-map")

        self.assertEqual(result.returncode, 0, result.stderr)
        goal = (self.root / "ProjectGoal.md").read_text(encoding="utf-8")
        self.assertIn("需要让实施人员快速查询设备知识。", goal)
        self.assertIn("Needs product-owner review", goal)
        self.assertIn(str(brief), goal)

    def test_missing_business_brief_fails_before_writing_files(self):
        result = self._run("--brief", "missing.md", "--no-code-map")

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertFalse((self.root / "ProjectGoal.md").exists())
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_code_map_is_bootstrapped_for_new_project(self):
        source = self.root / "src/service.py"
        source.parent.mkdir(parents=True)
        source.write_text("class SearchService:\n    pass\n", encoding="utf-8")

        result = self._run(*self._business_args())

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["code_map"]["action"], "bootstrap")
        self.assertTrue((self.root / "docs/ai/code-map.json").exists())
        self.assertTrue((self.root / "docs/ai/code-map.md").exists())


if __name__ == "__main__":
    unittest.main()
