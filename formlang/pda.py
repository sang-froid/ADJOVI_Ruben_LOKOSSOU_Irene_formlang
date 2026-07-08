"""Automate à pile (acceptation pile vide). À COMPLÉTER.  -> Jour 2 (E2.1)."""
from __future__ import annotations


class DelimiterPDA:
    def __init__(self, pairs=(("[", "]"), ("(", ")")), ignore=("a", "o", "r", "e")):
        self.open = {o for o, _ in pairs}
        self.match = {c: o for o, c in pairs}     # fermant -> ouvrant attendu
        self.ignore = set(ignore)

    def accepts(self, w: str) -> bool:
        pile = []
        for c in w:
            if c in self.open:
                pile.append(c)
            elif c in self.match:
                if not pile or pile[-1] != self.match[c]:
                    return False
                pile.pop()
            elif c in self.ignore:
                continue
            else:
                return False
        return len(pile) == 0
