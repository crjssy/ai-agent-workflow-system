# AI Agent 工作流系统

这是一个可以直接上传到 GitHub 的 AI Agent 项目示例，用来展示任务拆解、工具调用、多步推理、结果评审和自动修正等核心能力。

项目默认使用确定性的 `MockLLM`，因此不需要 API Key 也能本地运行和测试。后续如果要接入 OpenAI、国产大模型、本地模型或公司内部模型网关，只需要替换 LLM 接口实现即可。

## 项目解决的问题

这个系统适用于知识工作自动化场景，例如：

- 需求分析
- 文档生成
- 资料检索与总结
- 代码评审清单生成
- 运营或项目管理任务拆解

传统流程通常需要人工完成信息检索、任务拆解、初稿撰写、质量检查和结果修改，容易出现耗时长、上下文遗漏、输出不稳定等问题。本项目把这些步骤拆成多个 Agent 模块，并通过统一编排流程自动执行。

## 核心流程

1. 用户输入任务或需求。
2. `PlannerAgent` 识别意图，并把任务拆成可执行步骤。
3. `ResearcherAgent` 调用工具获取上下文，例如本地知识库和收益估算工具。
4. `GeneratorAgent` 根据计划和上下文生成结构化结果。
5. `EvaluatorAgent` 根据规则检查结果质量。
6. 如果结果不达标，系统自动进入修正流程，直到通过质量门槛或达到最大重试次数。

## 架构特点

- 多 Agent 分工：规划、检索、生成、评审职责清晰。
- 工具调用抽象：工具统一注册，便于继续扩展搜索、数据库、RAG、代码执行等能力。
- 质量评审闭环：不是一次性生成，而是带有检查与修正机制。
- 可测试：默认 Mock LLM，测试结果稳定，不依赖外部模型服务。
- 可扩展：LLM、工具和评审规则都可以独立替换。

## 快速开始

运行一个任务：

```bash
python -m ai_agent_system "Create a launch plan for an internal AI Agent"
```

输出完整 JSON：

```bash
python -m ai_agent_system "Summarize how to reduce manual review work" --json
```

使用示例任务文件：

```bash
python -m ai_agent_system --task-file examples/task.json
```

运行测试：

```bash
python -m unittest discover -s tests
```

## 项目结构

```text
ai_agent_system/
  agents/          Agent 实现
  tools/           工具注册与本地工具
  cli.py           命令行入口
  config.py        运行配置
  llm.py           可替换的 LLM 接口与 Mock 实现
  models.py        共享数据结构
  orchestrator.py  工作流编排器
data/
  knowledge_base.json
examples/
  task.json
tests/
  test_workflow.py
```

## 主要模块说明

### PlannerAgent

负责识别用户任务意图，并生成执行计划。当前实现会拆出目标澄清、上下文检索、结果生成和质量评估等步骤。

### ResearcherAgent

负责调用工具获取上下文。当前项目包含本地知识库检索和自动化收益估算工具，后续可以扩展为联网搜索、向量数据库、SQL 查询、内部系统 API 等。

### GeneratorAgent

负责根据任务、计划和工具结果生成最终内容。如果评审失败，它也会根据评审意见进行修正。

### EvaluatorAgent

负责检查生成结果是否包含必要结构，例如目标、执行计划、工具上下文、运营指标、风险控制等。这个模块可以替换为更复杂的规则引擎或评审 Agent。

### AgentOrchestrator

负责串联完整流程，是系统的主入口。它会控制任务执行、工具调用、质量评审和自动重试。

## 示例输出

```text
Goal
Create a launch plan for an internal AI Agent

Plan
- Clarify target outcome and audience.
- Retrieve relevant context.
- Generate a structured deliverable.
- Evaluate quality and revise if needed.

Quality
passed=True score=1.0 revision_rounds=0
```

## 如何接入真实大模型

当前的模型接口定义在 `ai_agent_system/llm.py`：

```python
class LLMClient(Protocol):
    def complete(self, system: str, prompt: str) -> str:
        ...
```

你可以新增一个实现类，例如 `OpenAILLM`、`LocalLLM` 或 `CompanyGatewayLLM`，只要实现 `complete()` 方法即可。然后在创建 `AgentOrchestrator` 时传入新的 LLM 实例。

## 可以写进简历或项目描述的版本

我构建了一个用于知识工作自动化的 AI Agent 工作流系统，主要解决人工任务拆解、资料检索、文档生成和质量检查耗时较长、输出不稳定的问题。系统由 Planner、Researcher、Generator、Evaluator 多个 Agent 协作完成任务，支持工具调用、上下文检索、结构化生成、规则评审和自动修正。

该项目默认提供可运行的 Mock LLM、命令行入口、知识库工具、收益估算工具和单元测试，方便在没有外部 API Key 的情况下完成演示。整体架构可扩展到 RAG、搜索、数据库查询、代码执行和真实大模型服务。

## GitHub 仓库描述建议

> 一个可扩展的 AI Agent 工作流系统，支持任务拆解、工具调用、上下文检索、结构化生成、质量评审和自动修正。

