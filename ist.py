"""A small desktop calculator built with Tkinter."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> float:
    """Evaluate the calculator's supported arithmetic expression safely."""
    tree = ast.parse(expression, mode="eval")

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)

        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return _BINARY_OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Only arithmetic expressions are supported")

    return evaluate(tree.body)


class CalculatorApp:
    """Tkinter user interface for the calculator."""

    def __init__(self, root: tk.Tk) -> None:
        import tkinter as tk
        from tkinter import ttk

        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.expression = tk.StringVar()
        self.display = ttk.Entry(
            root,
            textvariable=self.expression,
            justify="right",
            font=("TkDefaultFont", 20),
            state="readonly",
            width=16,
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=8)

        buttons = (
            ("C", self.clear),
            ("⌫", self.backspace),
            ("(", lambda: self.append("(")),
            (")", lambda: self.append(")")),
            ("7", lambda: self.append("7")),
            ("8", lambda: self.append("8")),
            ("9", lambda: self.append("9")),
            ("÷", lambda: self.append("/")),
            ("4", lambda: self.append("4")),
            ("5", lambda: self.append("5")),
            ("6", lambda: self.append("6")),
            ("×", lambda: self.append("*")),
            ("1", lambda: self.append("1")),
            ("2", lambda: self.append("2")),
            ("3", lambda: self.append("3")),
            ("−", lambda: self.append("-")),
            ("0", lambda: self.append("0")),
            (".", lambda: self.append(".")),
            ("+", lambda: self.append("+")),
            ("=", self.solve),
        )

        for index, (label, command) in enumerate(buttons):
            row, column = divmod(index, 4)
            ttk.Button(root, text=label, command=command, width=5).grid(
                row=row + 1,
                column=column,
                padx=4,
                pady=4,
                ipady=6,
                sticky="nsew",
            )

        root.bind("<Return>", lambda _event: self.solve())
        root.bind("<Escape>", lambda _event: self.clear())

    def append(self, value: str) -> None:
        self.expression.set(self.expression.get() + value)

    def clear(self) -> None:
        self.expression.set("")

    def backspace(self) -> None:
        self.expression.set(self.expression.get()[:-1])

    def solve(self) -> None:
        expression = self.expression.get()
        if not expression:
            return
        try:
            result = calculate(expression)
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            self.expression.set("Error")
            return
        self.expression.set(str(int(result)) if result.is_integer() else str(result))


def main() -> None:
    import tkinter as tk

    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()