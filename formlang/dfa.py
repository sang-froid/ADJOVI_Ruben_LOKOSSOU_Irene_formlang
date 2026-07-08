"""AFD. À COMPLÉTER : run, accepts, minimize (Moore).  -> Jour 1 (E1.1, E1.2)."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class DFA:
    transitions: dict            # (state, sym) -> state
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions}

    def run(self, w: str):
        state = self.start
        for c in w:
            state = self.transitions.get((state, c))
            if state is None:
                return None
        return state

    def accepts(self, w: str) -> bool:
        return self.run(w) in self.accept

    # ----- fourni : utilitaires pour la minimisation --------------------------
    def _reachable(self) -> set:
        seen, todo = {self.start}, deque([self.start])
        while todo:
            s = todo.popleft()
            for a in self.alphabet:
                t = self.transitions.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    def _completed(self):
        SINK = "__sink__"
        trans = dict(self.transitions)
        states = self._reachable()
        need = False
        for s in states:
            for a in self.alphabet:
                if (s, a) not in trans:
                    trans[(s, a)] = SINK
                    need = True
        if need:
            states = states | {SINK}
            for a in self.alphabet:
                trans[(SINK, a)] = SINK
        return states, trans

    def minimize(self) -> "DFA":
        states, trans = self._completed()

        # Partition initiale : finaux vs non-finaux
        finals = frozenset(s for s in states if s in self.accept)
        non_finals = frozenset(states - finals)
        partition = set()
        if finals:
            partition.add(finals)
        if non_finals:
            partition.add(non_finals)

        changed = True
        while changed:
            changed = False
            new_partition = set()
            for block in partition:
                groups = {}
                for s in block:
                    sig = tuple(
                        next((i for i, b in enumerate(partition) if trans.get((s, a)) in b), -1)
                        for a in sorted(self.alphabet)
                    )
                    groups.setdefault(sig, set()).add(s)
                for grp in groups.values():
                    new_partition.add(frozenset(grp))
                if len(groups) > 1:
                    changed = True
            partition = new_partition

        rep = {s: min(block) for block in partition for s in block}

        new_trans = {}
        for (s, a), t in trans.items():
            rs, rt = rep[s], rep[t]
            if rs != "__sink__" and rt != "__sink__":
                new_trans[(rs, a)] = rt
            elif rs != "__sink__":
                new_trans[(rs, a)] = rt  

        new_trans = {(rep[s], a): rep[t]
                    for (s, a), t in trans.items()
                    if rep[s] != "__sink__"}

        new_accept = {rep[s] for s in self.accept if s in rep}
        return DFA(new_trans, rep[self.start], new_accept, self.alphabet)

    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
