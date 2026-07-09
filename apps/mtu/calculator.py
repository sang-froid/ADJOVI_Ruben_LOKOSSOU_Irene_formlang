"""Calculatrice unaire. À COMPLÉTER.  -> Jour 4 (E4.3)."""
from .machines import ADD, SUB


def _ones(s: str) -> int:
    return s.count("1")


class Calculatrice:
    def addition(self, n: int, m: int) -> int:
        tape = "1" * n + "+" + "1" * m
        return ADD.run(tape).tape.count("1")

    def soustraction(self, n: int, m: int) -> int:
        if m == 0:
            return n
        if m >= n:
            return 0
        tape = "1" * n + "-" + "1" * m
        return SUB.run(tape).tape.count("1")

    def multiplication(self, n: int, m: int) -> int:
        result = 0
        for _ in range(m):
            result = self.addition(result, n)
        return result

    def division(self, n: int, m: int):
        if m == 0:
            raise ZeroDivisionError("division par zéro")
        quotient, reste = 0, n
        while reste >= m:
            reste = self.soustraction(reste, m)
            quotient = self.addition(quotient, 1)
        return quotient, reste

    def chainer(self, v0: int, ops: list) -> int:
        result = v0
        for op, val in ops:
            if op == "+":
                result = self.addition(result, val)
            elif op == "-":
                result = self.soustraction(result, val)
            elif op == "*":
                result = self.multiplication(result, val)
            elif op == "/":
                result, _ = self.division(result, val)
        return result
