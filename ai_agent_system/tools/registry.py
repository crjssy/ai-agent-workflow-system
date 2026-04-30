from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_agent_system.models import ToolResult
from ai_agent_system.tools.knowledge_base import LocalKnowledgeBase
from ai_agent_system.tools.safe_math import SafeCalculator


@dataclass
class ToolRegistry:
    """Central place where agents discover and call tools."""

    knowledge_base_path: Path

    def __post_init__(self) -> None:
        self.knowledge_base = LocalKnowledgeBase(self.knowledge_base_path)
        self.calculator = SafeCalculator()

    def retrieve_context(self, query: str) -> ToolResult:
        return self.knowledge_base.search(query)

    def estimate_savings(self, manual_minutes: int, automated_minutes: int, volume: int) -> ToolResult:
        saved_minutes = max(manual_minutes - automated_minutes, 0) * volume
        saved_hours = round(saved_minutes / 60, 2)
        return ToolResult(
            tool_name="savings_estimator",
            summary=f"Estimated monthly savings: {saved_hours} hours",
            data={
                "manual_minutes": manual_minutes,
                "automated_minutes": automated_minutes,
                "monthly_volume": volume,
                "saved_hours": saved_hours,
            },
        )

