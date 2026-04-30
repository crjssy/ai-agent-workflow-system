from __future__ import annotations

from ai_agent_system.models import Plan, ToolResult, UserTask
from ai_agent_system.tools import ToolRegistry


class ResearcherAgent:
    """Collect context through registered tools."""

    def __init__(self, tools: ToolRegistry) -> None:
        self.tools = tools

    def collect(self, task: UserTask, plan: Plan) -> list[ToolResult]:
        context = self.tools.retrieve_context(f"{task.text} {plan.intent}")
        savings = self.tools.estimate_savings(
            manual_minutes=int(task.metadata.get("manual_minutes", 30)),
            automated_minutes=int(task.metadata.get("automated_minutes", 8)),
            volume=int(task.metadata.get("monthly_volume", 120)),
        )
        return [context, savings]

