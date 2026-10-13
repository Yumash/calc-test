import pytest

from calculator.core import CalculationError, evaluate_expression


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("6 * 7", 42),
        ("8 / 2", 4),
        ("0.1 + 0.2", pytest.approx(0.3)),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("-5 + 2", -3),
    ],
)
def test_evaluate_expression(expression: str, expected: object) -> None:
    assert evaluate_expression(expression) == expected


@pytest.mark.parametrize(
    ("expression", "message"),
    [
        ("1 / 0", "Деление на ноль"),
        ("", "Введите выражение"),
        ("2 +", "Некорректное выражение"),
        ("__import__('os').getcwd()", "Некорректное выражение"),
        ("2 ** 8", "Поддерживаются только"),
    ],
)
def test_invalid_expression(expression: str, message: str) -> None:
    with pytest.raises(CalculationError, match=message):
        evaluate_expression(expression)
