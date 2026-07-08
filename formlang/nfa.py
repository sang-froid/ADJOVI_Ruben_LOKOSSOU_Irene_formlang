"""AFN (eps = ''). À COMPLÉTER : to_dfa par sous-ensembles.  -> Jour 1 (E1.3)."""
from __future__ import annotations
from dataclasses import dataclass, field
from .dfa import DFA


@dataclass
class NFA:
    transitions: dict            # (state, sym|'') -> set(states)
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions if a != ""}

    # ----- fourni -------------------------------------------------------------
    def _eps_closure(self, states: frozenset) -> frozenset:
        stack, clos = list(states), set(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, ""), ()):
                if t not in clos:
                    clos.add(t)
                    stack.append(t)
        return frozenset(clos)

    def _move(self, states: frozenset, a: str) -> frozenset:
        out = set()
        for s in states:
            out |= self.transitions.get((s, a), set())
        return frozenset(out)

    def accepts(self, w: str) -> bool:
        cur = self._eps_closure(frozenset({self.start}))
        for c in w:
            cur = self._eps_closure(self._move(cur, c))
        return any(s in self.accept for s in cur)

    def to_dfa(self) -> DFA:
        start_set = self._eps_closure(frozenset({self.start}))
        
        def name(fs): return str(sorted(fs))

        queue = [start_set]
        visited = {start_set}
        trans = {}
        accept = set()

        while queue:
            current = queue.pop(0)
            if any(s in self.accept for s in current):
                accept.add(name(current))
            for a in self.alphabet:
                nxt = self._eps_closure(self._move(current, a))
                trans[(name(current), a)] = name(nxt)
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)

        return DFA(trans, name(start_set), accept, self.alphabet)
