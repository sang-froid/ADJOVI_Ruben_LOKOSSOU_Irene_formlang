
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TMResult:
    accepted: bool
    tape: str
    steps: int
    trace: list = field(default_factory=list)


@dataclass
class TuringMachine:
    transitions: dict           # (q, a) -> (q', b, d in {'L','R','S'})
    start: str
    accept: set
    blank: str = "_"
    reject: set = field(default_factory=set)

    # ----- fourni -------------------------------------------------------------
    def _read(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)

    def _window(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

    def run(self, word: str, max_steps: int = 1_000_000, trace: bool = False) -> "TMResult":
        tape = {i: c for i, c in enumerate(word)}
        head = 0
        state = self.start
        steps = 0
        history = []

        while steps < max_steps:
            symbol = tape.get(head, self.blank)

            if trace:
                history.append((self._window(tape), state, head))

            # Arrêt sur état final
            if state in self.accept:
                return TMResult(True, self._read(tape), steps, history)

            # Arrêt si pas de transition
            key = (state, symbol)
            if key not in self.transitions:
                return TMResult(False, self._read(tape), steps, history)

            # Appliquer la transition
            new_state, new_symbol, direction = self.transitions[key]
            tape[head] = new_symbol
            state = new_state
            if direction == "R":
                head += 1
            elif direction == "L":
                head -= 1
            steps += 1

        raise RuntimeError(f"Machine non arrêtée après {max_steps} pas")