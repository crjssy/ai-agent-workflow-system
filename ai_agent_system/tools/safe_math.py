from __future__ import annotations

import ast
import operator
from dataclasses import dataclass

from ai_agent_system.models import ToolResult


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


@dataclass
class SafeCalculator:
    """Evaluate simple arithmetic expressions without executing code."""

    max_expression_length: int = 80

    def calculate(self, expression: str) -> ToolResult:
        if len(expression) > self.max_expression_length:
            raise ValueError("Expression is too long.")
        tree = ast.parse(expression, mode="eval")
        value = self._eval(tree.body)
        return ToolResult(
            tool_name="safe_calculator",
            summary=f"{expression} = {value}",
            data={"value": value},
        )

    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](self._eval(node.operand))
        raise ValueError("Only basic arithmetic is supported.")

