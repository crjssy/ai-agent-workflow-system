from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ai_agent_system.models import ToolResult


@dataclass(frozen=True)
class KnowledgeDocument:
    id: str
    title: str
    content: str


class LocalKnowledgeBase:
    """Small JSON-backed retrieval tool used by the Agent workflow."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._documents = self._load(path)

    def search(self, query: str, limit: int = 3) -> ToolResult:
        terms = {term.lower() for term in query.split() if len(term) > 2}
        scored: list[tuple[int, KnowledgeDocument]] = []
        for document in self._documents:
            haystack = f"{document.title} {document.content}".lower()
            score = sum(1 for term in terms if term in haystack)
            if score:
                scored.append((score, document))

        if not scored:
            scored = [(0, document) for document in self._documents[:limit]]

        matches = [doc for _, doc in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]
        summary = "\n".join(f"- {doc.title}: {doc.content}" for doc in matches)
        return ToolResult(
            tool_name="local_knowledge_base",
            summary=summary,
            data={"document_ids": [doc.id for doc in matches]},
        )

    @staticmethod
    def _load(path: Path) -> list[KnowledgeDocument]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [KnowledgeDocument(**item) for item in raw]

