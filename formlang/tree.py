"""Automate d'arbres ascendant (BUTA) générique. À COMPLÉTER : run, accepts,
product.  -> Jour 3 (E3.1, E3.4)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Hashable


@dataclass(frozen=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()
    label: Optional[str] = None


class _Reject:
    __slots__ = ()
    def __repr__(self):
        return "REJECT"


REJECT = _Reject()


class TreeAutomaton:
    def __init__(self, final_states):
        self.delta: dict[tuple[str, tuple], Hashable] = {}
        self.final: set = set(final_states)

    def add_rule(self, symbol: str, child_states, result) -> None:
        # FOURNI
        self.delta[(symbol, tuple(child_states))] = result

    def run(self, t: "Term"):
        child_states = []
        for child in t.children:
            state = self.run(child)
            if isinstance(state, _Reject):
                return REJECT
            child_states.append(state)
        
        # Chercher la règle correspondante
        key = (t.symbol, tuple(child_states))
        if key not in self.delta:
            return REJECT
        return self.delta[key]

    def accepts(self, t: "Term") -> bool:
        return self.run(t) in self.final


def product(a1: "TreeAutomaton", a2: "TreeAutomaton") -> "TreeAutomaton":
    final_pairs = {(f1, f2) for f1 in a1.final for f2 in a2.final}
    P = TreeAutomaton(final_states=final_pairs)

    for (sym1, kids1), r1 in a1.delta.items():
        for (sym2, kids2), r2 in a2.delta.items():
            if sym1 == sym2 and len(kids1) == len(kids2):
                paired_kids = tuple(zip(kids1, kids2))
                P.add_rule(sym1, paired_kids, (r1, r2))

    return P
