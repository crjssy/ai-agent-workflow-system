from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from ai_agent_system.config import AgentConfig
from ai_agent_system.models import UserTask
from ai_agent_system.orchestrator import AgentOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AI Agent workflow demo.")
    parser.add_argument("task", nargs="?", help="Task for the Agent workflow.")
    parser.add_argument("--task-file", type=Path, help="JSON file with task and metadata.")
    parser.add_argument("--knowledge-base", type=Path, default=Path("data/knowledge_base.json"))
    parser.add_argument("--json", action="store_true", help="Print the full workflow result as JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    user_task = _load_task(args.task, args.task_file)
    orchestrator = AgentOrchestrator(config=AgentConfig(knowledge_base_path=args.knowledge_base))
    result = orchestrator.run(user_task)

    if args.json:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print(_format_result(result))
    return 0


def _load_task(task_text: str | None, task_file: Path | None) -> UserTask:
    if task_file:
        raw = json.loads(task_file.read_text(encoding="utf-8"))
        metadata = {key: value for key, value in raw.items() if key != "task"}
        return UserTask(text=raw["task"], metadata=metadata)
    if not task_text:
        raise SystemExit("Provide a task string or --task-file.")
    return UserTask(text=task_text)


def _format_result(result) -> str:
    plan = "\n".join(f"- {step.objective}" for step in result.plan.steps)
    tools = "\n".join(f"- {item.tool_name}: {item.summary}" for item in result.tool_results)
    quality = (
        f"passed={result.evaluation.passed} "
        f"score={result.evaluation.score} "
        f"revision_rounds={result.revision_rounds}"
    )
    return (
        f"Goal\n{result.task.text}\n\n"
        f"Plan\n{plan}\n\n"
        f"Tools\n{tools}\n\n"
        f"Result\n{result.draft.body}\n\n"
        f"Quality\n{quality}"
    )


if __name__ == "__main__":
    raise SystemExit(main())

