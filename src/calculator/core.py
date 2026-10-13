"""Safe arithmetic expression evaluation."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable


class CalculationError(ValueError):
    """Raised when an expression cannot be calculated safely."""


BinaryOperation = Callable[[float, float], float]

_BINARY_OPERATIONS: dict[type[ast.operator], BinaryOperation] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_UNARY_OPERATIONS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(expression: str) -> int | float:
    """Evaluate a basic arithmetic expression without using ``eval``.

    Only decimal numbers, parentheses, +, -, *, and / are accepted.
    """
    if not expression.strip():
        raise CalculationError("Введите выражение")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate_node(tree.body)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
        if isinstance(error, CalculationError):
            raise
        if isinstance(error, ZeroDivisionError):
            raise CalculationError("Деление на ноль") from error
        raise CalculationError("Некорректное выражение") from error

    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def _evaluate_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return float(node.value)

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATIONS.get(type(node.op))
        if operation is None:
            raise CalculationError("Поддерживаются только +, -, × и ÷")
        return operation(_evaluate_node(node.left), _evaluate_node(node.right))

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATIONS.get(type(node.op))
        if operation is None:
            raise CalculationError("Некорректная операция")
        return operation(_evaluate_node(node.operand))

    raise CalculationError("Некорректное выражение")
