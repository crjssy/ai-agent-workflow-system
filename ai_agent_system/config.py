from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    """Runtime configuration for the Agent workflow."""

    knowledge_base_path: Path = Path("data/knowledge_base.json")
    max_revision_rounds: int = 2
    min_quality_score: float = 0.8

