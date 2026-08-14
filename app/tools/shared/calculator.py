from langchain_core.tools import tool
import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            evaluate(node.left),
            evaluate(node.right),
        )

    if isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Examples:
    - 10 + 20
    - 5 * (7 + 3)
    - 2 ** 8
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        return str(result)

    except Exception as e:
        return f"Calculation Error: {e}"