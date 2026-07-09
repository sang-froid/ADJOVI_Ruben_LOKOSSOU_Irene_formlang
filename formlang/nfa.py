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

def thompson(regex: str) -> "NFA":
    """Construction de Thompson : regex -> AFN avec transitions epsilon."""
    counter = [0]

    def new_state():
        s = f"s{counter[0]}"
        counter[0] += 1
        return s

    def from_char(c):
        # Un caractère : un état initial, une transition, un état final
        s0, s1 = new_state(), new_state()
        return NFA(
            transitions={(s0, c): {s1}},
            start=s0, accept={s1}, alphabet={c}
        )

    def epsilon():
        # Mot vide : transition epsilon directe
        s0, s1 = new_state(), new_state()
        return NFA(
            transitions={(s0, ""): {s1}},
            start=s0, accept={s1}, alphabet=set()
        )

    def concat(n1, n2):
        # n1 puis n2 : relier l'état final de n1 à l'état initial de n2
        trans = {**n1.transitions, **n2.transitions}
        for f in n1.accept:
            trans.setdefault((f, ""), set()).add(n2.start)
        return NFA(
            transitions=trans,
            start=n1.start, accept=n2.accept,
            alphabet=n1.alphabet | n2.alphabet
        )

    def union(n1, n2):
        # n1 | n2 : nouvel état initial avec epsilon vers les deux
        s0, sf = new_state(), new_state()
        trans = {**n1.transitions, **n2.transitions}
        trans[(s0, "")] = {n1.start, n2.start}
        for f in n1.accept | n2.accept:
            trans.setdefault((f, ""), set()).add(sf)
        return NFA(
            transitions=trans,
            start=s0, accept={sf},
            alphabet=n1.alphabet | n2.alphabet
        )

    def star(n):
        # n* : nouvel état initial et final, epsilon vers n et retour
        s0, sf = new_state(), new_state()
        trans = {**n.transitions}
        trans[(s0, "")] = {n.start, sf}
        for f in n.accept:
            trans.setdefault((f, ""), set()).update({n.start, sf})
        return NFA(
            transitions=trans,
            start=s0, accept={sf},
            alphabet=n.alphabet
        )

    # Parser récursif descendant
    # Grammaire : expr = term ('|' term)*
    #             term = factor factor*
    #             factor = atom ('*')?
    #             atom = char | '(' expr ')'

    pos = [0]

    def peek():
        return regex[pos[0]] if pos[0] < len(regex) else None

    def consume(c=None):
        ch = regex[pos[0]]
        if c and ch != c:
            raise ValueError(f"Attendu {c}, trouvé {ch}")
        pos[0] += 1
        return ch

    def parse_expr():
        node = parse_term()
        while peek() == '|':
            consume('|')
            node = union(node, parse_term())
        return node

    def parse_term():
        node = parse_factor()
        while peek() and peek() not in ('|', ')'):
            node = concat(node, parse_factor())
        return node

    def parse_factor():
        node = parse_atom()
        if peek() == '*':
            consume('*')
            node = star(node)
        return node

    def parse_atom():
        c = peek()
        if c == '(':
            consume('(')
            node = parse_expr()
            consume(')')
            return node
        elif c and c not in ('|', ')', '*'):
            consume()
            return from_char(c)
        else:
            return epsilon()

    return parse_expr()