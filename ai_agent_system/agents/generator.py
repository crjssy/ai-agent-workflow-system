from __future__ import annotations

from ai_agent_system.llm import LLMClient
from ai_agent_system.models import Draft, Plan, ToolResult, UserTask


class GeneratorAgent:
    """Generate and revise final user-facing content."""

    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def generate(self, task: UserTask, plan: Plan, tool_results: list[ToolResult]) -> Draft:
        context = self._format_context(tool_results)
        model_text = self.llm.complete(
            system="Draft a structured answer using the Agent plan and context.",
            prompt=f"Task: {task.text}\nPlan: {plan}\nContext:\n{context}",
        )
        body = self._compose_body(task, plan, tool_results, model_text)
        return Draft(title="AI Agent Workflow Proposal", body=body, used_context=self._context_ids(tool_results))

    def revise(self, draft: Draft, issues: list[str], suggestions: list[str]) -> Draft:
        revision = self.llm.complete(
            system="Revise the draft to fix evaluation issues.",
            prompt=f"Draft:\n{draft.body}\nIssues: {issues}\nSuggestions: {suggestions}",
        )
        additions = "\n\nRevision Notes\n" + "\n".join(f"- {item}" for item in suggestions)
        additions += f"\n- Model revision: {revision}"
        return Draft(title=draft.title, body=draft.body + additions, used_context=draft.used_context)

    @staticmethod
    def _format_context(tool_results: list[ToolResult]) -> str:
        return "\n".join(f"[{result.tool_name}]\n{result.summary}" for result in tool_results)

    @staticmethod
    def _context_ids(tool_results: list[ToolResult]) -> list[str]:
        ids: list[str] = []
        for result in tool_results:
            ids.extend(result.data.get("document_ids", []))
        return ids

    @staticmethod
    def _compose_body(
        task: UserTask,
        plan: Plan,
        tool_results: list[ToolResult],
        model_text: str,
    ) -> str:
        context_summary = "\n".join(f"- {result.summary}" for result in tool_results)
        plan_summary = "\n".join(f"- {step.objective}" for step in plan.steps)
        return (
            f"Goal\n{task.text}\n\n"
            f"Detected Intent\n{plan.intent}\n\n"
            f"Execution Plan\n{plan_summary}\n\n"
            f"Tool Context\n{context_summary}\n\n"
            "Recommended Output\n"
            f"{model_text}\n\n"
            "Operational Metrics\n"
            "- Average handling time\n"
            "- Human review pass rate\n"
            "- Retry count\n"
            "- Cost per completed task\n\n"
            "Risks And Controls\n"
            "- Keep human approval for external publishing.\n"
            "- Log tool calls for observability.\n"
            "- Use evaluation checks before final delivery.\n"
        )

