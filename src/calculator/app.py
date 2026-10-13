"""Tkinter user interface for the calculator."""

from __future__ import annotations

import tkinter as tk

from calculator.core import CalculationError, evaluate_expression


class CalculatorApp:
    """A compact desktop calculator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Калькулятор")
        self.root.resizable(False, False)
        self.expression = tk.StringVar()
        self._showing_error = False
        self._build_interface()
        self._bind_keyboard()

    def _build_interface(self) -> None:
        frame = tk.Frame(self.root, padx=12, pady=12, bg="#20242b")
        frame.pack()

        display = tk.Entry(
            frame,
            textvariable=self.expression,
            justify="right",
            font=("Segoe UI", 22),
            width=16,
            bd=0,
            relief="flat",
        )
        display.grid(row=0, column=0, columnspan=4, padx=2, pady=(0, 10), ipady=10)
        display.focus_set()

        buttons = [
            ("C", 1, 0, self.clear, "#d65a5a"),
            ("(", 1, 1, lambda: self.append("("), "#4b5563"),
            (")", 1, 2, lambda: self.append(")"), "#4b5563"),
            ("÷", 1, 3, lambda: self.append("/"), "#e09145"),
            ("7", 2, 0, lambda: self.append("7"), "#3a404a"),
            ("8", 2, 1, lambda: self.append("8"), "#3a404a"),
            ("9", 2, 2, lambda: self.append("9"), "#3a404a"),
            ("×", 2, 3, lambda: self.append("*"), "#e09145"),
            ("4", 3, 0, lambda: self.append("4"), "#3a404a"),
            ("5", 3, 1, lambda: self.append("5"), "#3a404a"),
            ("6", 3, 2, lambda: self.append("6"), "#3a404a"),
            ("−", 3, 3, lambda: self.append("-"), "#e09145"),
            ("1", 4, 0, lambda: self.append("1"), "#3a404a"),
            ("2", 4, 1, lambda: self.append("2"), "#3a404a"),
            ("3", 4, 2, lambda: self.append("3"), "#3a404a"),
            ("+", 4, 3, lambda: self.append("+"), "#e09145"),
            ("0", 5, 0, lambda: self.append("0"), "#3a404a"),
            (".", 5, 1, lambda: self.append("."), "#3a404a"),
            ("⌫", 5, 2, self.backspace, "#4b5563"),
            ("=", 5, 3, self.calculate, "#4f9d69"),
        ]

        for text, row, column, command, color in buttons:
            tk.Button(
                frame,
                text=text,
                command=command,
                font=("Segoe UI", 14),
                width=5,
                height=2,
                bd=0,
                bg=color,
                fg="white",
                activebackground="#687180",
                activeforeground="white",
            ).grid(row=row, column=column, padx=2, pady=2)

    def _bind_keyboard(self) -> None:
        self.root.bind("<Return>", lambda _event: self.calculate())
        self.root.bind("<KP_Enter>", lambda _event: self.calculate())
        self.root.bind("<Escape>", lambda _event: self.clear())

    def append(self, value: str) -> None:
        if self._showing_error:
            self.clear()
        self.expression.set(self.expression.get() + value)

    def clear(self) -> None:
        self.expression.set("")
        self._showing_error = False

    def backspace(self) -> None:
        if self._showing_error:
            self.clear()
            return
        self.expression.set(self.expression.get()[:-1])

    def calculate(self) -> None:
        try:
            result = evaluate_expression(self.expression.get())
        except CalculationError as error:
            self.expression.set(str(error))
            self._showing_error = True
            return

        self.expression.set(str(result))
        self._showing_error = False


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
