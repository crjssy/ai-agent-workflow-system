# AI Agent Workflow System

A small, GitHub-ready AI Agent workflow that demonstrates task planning,
tool use, multi-step reasoning, result review, and automatic revision.

The project runs locally with a deterministic mock LLM, so reviewers can try
it without an API key. The LLM layer is intentionally pluggable, making it easy
to connect OpenAI, local models, or internal model gateways later.

## What It Solves

This system is designed for knowledge-work automation scenarios such as:

- requirement analysis
- document drafting
- research summary
- code-review style checklist generation
- operational task decomposition

The workflow replaces a manual process where people repeatedly search context,
split tasks, write drafts, check quality, and revise outputs.

## Core Flow

1. The user submits a task.
2. The planner agent identifies intent and decomposes the task.
3. Tool agents collect context from a local knowledge base and safe utilities.
4. The generator agent produces a structured deliverable.
5. The evaluator agent checks quality against rules.
6. The orchestrator retries and revises when the result does not pass.

## Quick Start

```bash
python -m ai_agent_system "Create a rollout plan for an internal AI writing assistant"
```

Run with JSON output:

```bash
python -m ai_agent_system "Summarize how to reduce manual review work" --json
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Example Output

```text
Goal
Create a rollout plan for an internal AI writing assistant

Plan
- Clarify the expected business outcome.
- Retrieve relevant implementation context.
- Draft the final answer with risks and metrics.

Result
...

Quality
passed=True score=0.95
```

## Project Layout

```text
ai_agent_system/
  agents/          Agent implementations
  tools/           Tool registry and local tools
  cli.py           Command line entry point
  config.py        Runtime configuration
  llm.py           Pluggable LLM interface and mock implementation
  models.py        Shared dataclasses
  orchestrator.py  End-to-end workflow coordinator
data/
  knowledge_base.json
tests/
  test_workflow.py
```

## Why This Is Useful In A Portfolio

The repository shows the engineering pieces interviewers usually look for in
Agent projects:

- clear task decomposition
- tool calling abstraction
- review and retry loop
- deterministic tests
- no hard-coded vendor dependency
- measurable workflow outputs

## GitHub Description Suggestion

> A pluggable AI Agent workflow for task decomposition, tool-assisted context
> retrieval, structured generation, quality evaluation, and automatic revision.
