import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_vault.py"


def load_init_module():
    spec = importlib.util.spec_from_file_location("init_vault", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TemplateIntegrityTests(unittest.TestCase):
    def test_bootstrap_templates_required_by_init_script_exist(self) -> None:
        init_vault = load_init_module()

        for template_name in (
            "AGENT_INSTRUCTIONS.md",
            "bridge_pointer.md",
            "codex_skill.md",
        ):
            with self.subTest(template_name=template_name):
                content = init_vault.load_template(template_name)
                self.assertIn("_multi-agent", content)

    def test_bridge_pointer_mentions_every_generated_entry_routine_target(self) -> None:
        bridge_pointer = (ROOT / "templates" / "bridge_pointer.md").read_text(encoding="utf-8")

        for target in (
            "_multi-agent/AGENT_INSTRUCTIONS.md",
            "_multi-agent/index.md",
            "_multi-agent/events.md",
            "_multi-agent/agents/",
            "_multi-agent/tasks/",
        ):
            self.assertIn(target, bridge_pointer)

    def test_codex_skill_points_to_canonical_protocol(self) -> None:
        codex_skill = (ROOT / "templates" / "codex_skill.md").read_text(encoding="utf-8")

        self.assertIn("Read `_multi-agent/AGENT_INSTRUCTIONS.md` first", codex_skill)
        self.assertIn("Record meaningful actions in `events.md`", codex_skill)


if __name__ == "__main__":
    unittest.main()
