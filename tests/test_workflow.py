from __future__ import annotations

import unittest
from pathlib import Path

from ai_agent_system.config import AgentConfig
from ai_agent_system.models import UserTask
from ai_agent_system.orchestrator import AgentOrchestrator
from ai_agent_system.tools.safe_math import SafeCalculator


class WorkflowTests(unittest.TestCase):
    def test_workflow_passes_quality_gate(self) -> None:
        orchestrator = AgentOrchestrator(
            config=AgentConfig(knowledge_base_path=Path("data/knowledge_base.json"))
        )
        result = orchestrator.run(
            UserTask(
                text="Create a plan for an AI Agent that reduces manual weekly reporting work",
                metadata={"manual_minutes": 45, "automated_minutes": 10, "monthly_volume": 80},
            )
        )

        self.assertTrue(result.evaluation.passed)
        self.assertGreaterEqual(result.evaluation.score, 0.8)
        self.assertIn("Operational Metrics", result.draft.body)
        self.assertTrue(result.draft.used_context)

    def test_safe_calculator_allows_basic_math(self) -> None:
        result = SafeCalculator().calculate("10 * 6 - 15")

        self.assertEqual(result.data["value"], 45)

    def test_safe_calculator_rejects_code_execution(self) -> None:
        with self.assertRaises(ValueError):
            SafeCalculator().calculate("__import__('os').system('echo nope')")


if __name__ == "__main__":
    unittest.main()

