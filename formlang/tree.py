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

def minimize_buta(a: "TreeAutomaton") -> "TreeAutomaton":
    """Minimisation d'un BUTA par raffinement de partition."""

    # Collecter tous les états
    states = set(a.final)
    for (sym, kids), res in a.delta.items():
        states.add(res)
        for k in kids:
            states.add(k)

    # Partition initiale : finaux vs non-finaux
    finals     = frozenset(s for s in states if s in a.final)
    non_finals = frozenset(s for s in states if s not in a.final)
    partition  = []
    if finals:     partition.append(finals)
    if non_finals: partition.append(non_finals)

    def block_id(s):
        for i, b in enumerate(partition):
            if s in b:
                return i
        return -1

    # Raffinement
    changed = True
    while changed:
        changed = False
        new_partition = []
        for block in partition:
            groups = {}
            for s in block:
                # Signature : pour chaque règle où s apparaît comme enfant,
                # quel symbole et quels blocs des autres enfants
                sig = []
                for (sym, kids), res in a.delta.items():
                    for pos, k in enumerate(kids):
                        if k == s:
                            other_blocks = tuple(
                                block_id(kids[j]) for j in range(len(kids)) if j != pos
                            )
                            sig.append((sym, pos, other_blocks, block_id(res)))
                sig = tuple(sorted(sig))
                groups.setdefault(sig, set()).add(s)
            for grp in groups.values():
                new_partition.append(frozenset(grp))
            if len(groups) > 1:
                changed = True
        partition = new_partition

    # Représentants : prendre le min de chaque bloc
    rep = {s: min(b) for b in partition for s in b}

    # Reconstruire
    new_a = TreeAutomaton(final_states={rep[s] for s in a.final})
    for (sym, kids), res in a.delta.items():
        new_a.add_rule(sym, tuple(rep[k] for k in kids), rep[res])

    return new_a