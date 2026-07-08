"""Grammaire hors-contexte : génération bornée. À COMPLÉTER.  -> Jour 2 (E2.2)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        max_nt = 2 * max_len + 2
        agenda = {("S",)}
        terminaux = set()
        vus = {("S",)}
        while agenda:
            nouveau = set()
            for forme in agenda:
                nb_nt = sum(1 for s in forme if s in self.nonterminals)
                for i, sym in enumerate(forme):
                    if sym in self.nonterminals:
                        for regle in self.rules[sym]:
                            nouvelle_forme = forme[:i] + regle + forme[i+1:]
                            
                            nb_t = sum(1 for s in nouvelle_forme 
                                    if s not in self.nonterminals)
                            nb_nt_new = sum(1 for s in nouvelle_forme 
                                            if s in self.nonterminals)
                            
                            if nb_t > max_len or nb_nt_new > max_nt:
                                continue
                            
                            if nouvelle_forme not in vus:
                                vus.add(nouvelle_forme)
                                if nb_nt_new == 0:
                                    mot = "".join(nouvelle_forme)
                                    if len(mot) <= max_len:
                                        terminaux.add(mot)
                                else:
                                    nouveau.add(nouvelle_forme)
                        break  
            agenda = nouveau
        return terminaux


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )
