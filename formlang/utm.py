"""Machine universelle.  COMPLÉTER : encode/decode et run.  -> Jour 4 (E4.2)."""
from __future__ import annotations
import json
from .turing import TuringMachine, TMResult


def encode(machine: "TuringMachine") -> str:
    data = {
        "transitions": {
            json.dumps([q, a]): [q2, b, d]
            for (q, a), (q2, b, d) in machine.transitions.items()
        },
        "start":  machine.start,
        "accept": sorted(machine.accept),
        "blank":  machine.blank,
    }
    return json.dumps(data, sort_keys=True)


def decode(desc: str) -> "TuringMachine":
    data = json.loads(desc)
    transitions = {
        tuple(json.loads(k)): tuple(v)
        for k, v in data["transitions"].items()
    }
    return TuringMachine(
        transitions=transitions,
        start=data["start"],
        accept=set(data["accept"]),
        blank=data["blank"],
    )

class UniversalTM:
    def run(self, encoded_machine: str, word: str, **kw) -> "TMResult":
        machine = decode(encoded_machine)
        return machine.run(word, **kw)