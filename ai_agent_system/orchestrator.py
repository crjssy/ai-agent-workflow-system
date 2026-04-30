from __future__ import annotations

from ai_agent_system.agents import EvaluatorAgent, GeneratorAgent, PlannerAgent, ResearcherAgent
from ai_agent_system.config import AgentConfig
from ai_agent_system.llm import LLMClient, MockLLM
from ai_agent_system.models import UserTask, WorkflowResult
from ai_agent_system.tools import ToolRegistry


class AgentOrchestrator:
    """Coordinate planner, researcher, generator, and evaluator agents."""

    def __init__(self, config: AgentConfig | None = None, llm: LLMClient | None = None) -> None:
        self.config = config or AgentConfig()
        self.llm = llm or MockLLM()
        self.tools = ToolRegistry(self.config.knowledge_base_path)
        self.planner = PlannerAgent(self.llm)
        self.researcher = ResearcherAgent(self.tools)
        self.generator = GeneratorAgent(self.llm)
        self.evaluator = EvaluatorAgent()

    def run(self, task: UserTask | str) -> WorkflowResult:
        user_task = task if isinstance(task, UserTask) else UserTask(text=task)
        plan = self.planner.create_plan(user_task)
        tool_results = self.researcher.collect(user_task, plan)
        draft = self.generator.generate(user_task, plan, tool_results)
        evaluation = self.evaluator.evaluate(user_task, draft)

        revision_rounds = 0
        while not evaluation.passed and revision_rounds < self.config.max_revision_rounds:
            draft = self.generator.revise(draft, evaluation.issues, evaluation.suggestions)
            evaluation = self.evaluator.evaluate(user_task, draft)
            revision_rounds += 1

        return WorkflowResult(
            task=user_task,
            plan=plan,
            tool_results=tool_results,
            draft=draft,
            evaluation=evaluation,
            revision_rounds=revision_rounds,
        )

