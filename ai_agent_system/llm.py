from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol


class LLMClient(Protocol):
    """Minimal model interface used by all agents."""

    def complete(self, system: str, prompt: str) -> str:
        """Return a text completion for a system instruction and prompt."""


@dataclass
class MockLLM:
    """Deterministic LLM replacement for tests, demos, and GitHub reviewers."""

    seed: str = "agent-workflow"

    def complete(self, system: str, prompt: str) -> str:
        digest = hashlib.sha256(f"{self.seed}:{system}:{prompt}".encode()).hexdigest()
        marker = digest[:8]
        if "intent" in system.lower():
            return f"automation-analysis:{marker}"
        if "draft" in system.lower():
            return (
                "This workflow should define a clear outcome, collect the right "
                "context, produce a structured answer, and include measurable "
                f"success criteria. trace={marker}"
            )
        if "revise" in system.lower():
            return (
                "The revised workflow adds concrete metrics, review criteria, "
                f"operational risks, and a deployment path. trace={marker}"
            )
        return f"mock-response:{marker}"

