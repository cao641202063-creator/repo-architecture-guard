import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "code_map.py"


class CodeMapWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._write(
            "package.json",
            json.dumps(
                {
                    "name": "sample-orders",
                    "scripts": {"test": "vitest", "build": "tsc"},
                    "dependencies": {"react": "^19.0.0"},
                }
            ),
        )
        self._write(
            "src/index.ts",
            "import { OrderService } from './orders/order.service';\n"
            "export const orderService = new OrderService();\n",
        )
        self._write(
            "src/orders/order.service.ts",
            "export class OrderService {\n"
            "  createOrder(id: string): string { return id; }\n"
            "}\n",
        )
        self._write(
            "src/components/Pagination.tsx",
            "export function Pagination() { return <button>Next</button>; }\n",
        )
        self._write(
            "tests/order.service.test.ts",
            "import { OrderService } from '../src/orders/order.service';\n"
            "test('creates an order', () => expect(new OrderService()).toBeTruthy());\n",
        )
        self._write(
            "README.md",
            "# Sample Orders\n\n"
            "```ts\n"
            "import { Phantom } from './ghost';\n"
            "export class DocumentationExample {}\n"
            "```\n",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write(self, relative_path, content):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--root", str(self.root), "--json"],
            text=True,
            capture_output=True,
            check=False,
        )

    def _map(self):
        return json.loads((self.root / "docs/ai/code-map.json").read_text(encoding="utf-8"))

    def _node(self, suffix):
        return next(node for node in self._map()["nodes"] if node["id"].endswith(suffix))

    def test_bootstrap_builds_typed_nodes_and_markdown(self):
        result = self._run("bootstrap")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "created")
        node_types = {node["type"] for node in self._map()["nodes"]}
        self.assertTrue({"entry", "service", "component", "test"}.issubset(node_types))
        self.assertIn("typescript", self._map()["meta"]["stacks"])
        markdown = (self.root / "docs/ai/code-map.md").read_text(encoding="utf-8")
        self.assertIn("# Code Map", markdown)
        self.assertIn("OrderService", markdown)
        documentation_nodes = [
            node for node in self._map()["nodes"] if node["type"] == "documentation"
        ]
        self.assertTrue(documentation_nodes)
        self.assertTrue(all(not node["symbols"] for node in documentation_nodes))
        self.assertTrue(all(not node["imports"] for node in documentation_nodes))

    def test_check_detects_source_change_and_update_preserves_semantics(self):
        self.assertEqual(self._run("bootstrap").returncode, 0)
        map_path = self.root / "docs/ai/code-map.json"
        stored = self._map()
        service = next(node for node in stored["nodes"] if node["type"] == "service")
        service["responsibility"] = "Owns order creation and state transitions."
        service["reuse_guidance"] = "Extend this service for order commands."
        service["needs_ai_review"] = False
        map_path.write_text(json.dumps(stored, indent=2), encoding="utf-8")

        self._write(
            "src/orders/order.service.ts",
            "export class OrderService {\n"
            "  createOrder(id: string): string { return id; }\n"
            "  cancelOrder(id: string): string { return id; }\n"
            "}\n",
        )

        stale = self._run("check")
        self.assertEqual(stale.returncode, 1)
        stale_payload = json.loads(stale.stdout)
        self.assertEqual(stale_payload["status"], "stale")
        self.assertTrue(stale_payload["changed_nodes"])

        updated = self._run("update")
        self.assertEqual(updated.returncode, 0, updated.stderr)
        updated_service = next(node for node in self._map()["nodes"] if node["type"] == "service")
        self.assertEqual(
            updated_service["responsibility"],
            "Owns order creation and state transitions.",
        )
        self.assertEqual(
            updated_service["reuse_guidance"],
            "Extend this service for order commands.",
        )
        self.assertFalse(updated_service["needs_ai_review"])
        self.assertEqual(self._run("check").returncode, 0)

    def test_check_and_update_detect_added_and_removed_nodes(self):
        self.assertEqual(self._run("bootstrap").returncode, 0)
        self._write(
            "src/integrations/payment.client.ts",
            "export class PaymentClient { charge(): boolean { return true; } }\n",
        )
        (self.root / "src/components/Pagination.tsx").unlink()

        stale = self._run("check")
        self.assertEqual(stale.returncode, 1)
        payload = json.loads(stale.stdout)
        self.assertTrue(payload["added_nodes"])
        self.assertTrue(payload["removed_nodes"])

        updated = self._run("update")
        self.assertEqual(updated.returncode, 0, updated.stderr)
        node_types = {node["type"] for node in self._map()["nodes"]}
        self.assertIn("integration", node_types)
        self.assertNotIn(
            "src.components.pagination",
            {node["id"] for node in self._map()["nodes"]},
        )

    def test_render_uses_enriched_json(self):
        self.assertEqual(self._run("bootstrap").returncode, 0)
        map_path = self.root / "docs/ai/code-map.json"
        stored = self._map()
        service = next(node for node in stored["nodes"] if node["type"] == "service")
        service["product_capability"] = "Order management"
        service["responsibility"] = "Creates and cancels orders."
        map_path.write_text(json.dumps(stored, indent=2), encoding="utf-8")

        rendered = self._run("render")

        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        markdown = (self.root / "docs/ai/code-map.md").read_text(encoding="utf-8")
        self.assertIn("Order management", markdown)
        self.assertIn("Creates and cancels orders.", markdown)


if __name__ == "__main__":
    unittest.main()
