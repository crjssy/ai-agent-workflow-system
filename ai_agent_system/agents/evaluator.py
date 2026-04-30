from __future__ import annotations

from ai_agent_system.models import Draft, Evaluation, UserTask


class EvaluatorAgent:
    """Rule-based evaluator that keeps the demo deterministic."""

    REQUIRED_SECTIONS = [
        "Goal",
        "Execution Plan",
        "Tool Context",
        "Operational Metrics",
        "Risks And Controls",
    ]

    def evaluate(self, task: UserTask, draft: Draft) -> Evaluation:
        issues: list[str] = []
        suggestions: list[str] = []

        if task.text.lower().split()[0] not in draft.body.lower():
            issues.append("The draft may not directly reference the original task.")
            suggestions.append("Restate the user's goal in the final answer.")

        for section in self.REQUIRED_SECTIONS:
            if section not in draft.body:
                issues.append(f"Missing section: {section}.")
                suggestions.append(f"Add a concise {section} section.")

        if not draft.used_context:
            issues.append("No retrieved context was attached to the draft.")
            suggestions.append("Include the knowledge-base document ids used by the workflow.")

        score = max(0.0, 1.0 - (len(issues) * 0.18))
        return Evaluation(
            passed=score >= 0.8 and not issues,
            score=round(score, 2),
            issues=issues,
            suggestions=suggestions,
        )

