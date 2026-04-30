from __future__ import annotations

from ai_agent_system.llm import LLMClient
from ai_agent_system.models import Plan, PlanStep, UserTask


class PlannerAgent:
    """Identify user intent and turn a request into executable steps."""

    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def create_plan(self, task: UserTask) -> Plan:
        intent = self.llm.complete(
            system="Classify intent for an automation Agent task.",
            prompt=task.text,
        )
        steps = [
            PlanStep("clarify", "Clarify target outcome and audience."),
            PlanStep("retrieve", "Retrieve relevant context.", "knowledge_base"),
            PlanStep("draft", "Generate a structured deliverable."),
            PlanStep("evaluate", "Evaluate quality and revise if needed."),
        ]
        return Plan(goal=task.text, intent=intent, steps=steps)

