from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class UserTask:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlanStep:
    id: str
    objective: str
    tool_hint: str | None = None


@dataclass(frozen=True)
class Plan:
    goal: str
    intent: str
    steps: list[PlanStep]


@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Draft:
    title: str
    body: str
    used_context: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Evaluation:
    passed: bool
    score: float
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorkflowResult:
    task: UserTask
    plan: Plan
    tool_results: list[ToolResult]
    draft: Draft
    evaluation: Evaluation
    revision_rounds: int

