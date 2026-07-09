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
        
        # Chaque forme est un tuple de symboles (terminaux et non-terminaux)
        agenda = {("S",)}
        terminaux = set()
        vus = {("S",)}

        while agenda:
            nouveau = set()
            for forme in agenda:
                # Compter les non-terminaux dans la forme
                nb_nt = sum(1 for s in forme if s in self.nonterminals)
                
                # Trouver le premier non-terminal à réécrire
                for i, sym in enumerate(forme):
                    if sym in self.nonterminals:
                        for regle in self.rules[sym]:
                            nouvelle_forme = forme[:i] + regle + forme[i+1:]
                            
                            # Calculer terminaux et non-terminaux
                            nb_t = sum(1 for s in nouvelle_forme 
                                    if s not in self.nonterminals)
                            nb_nt_new = sum(1 for s in nouvelle_forme 
                                            if s in self.nonterminals)
                            
                            # Élaguer si trop long ou trop de non-terminaux
                            if nb_t > max_len or nb_nt_new > max_nt:
                                continue
                            
                            if nouvelle_forme not in vus:
                                vus.add(nouvelle_forme)
                                # Si entièrement terminal → ajouter au résultat
                                if nb_nt_new == 0:
                                    mot = "".join(nouvelle_forme)
                                    if len(mot) <= max_len:
                                        terminaux.add(mot)
                                else:
                                    nouveau.add(nouvelle_forme)
                        break  # on ne réécrit qu'un seul NT à la fois
            agenda = nouveau

        return terminaux


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )

def to_cnf(cfg: "CFG") -> "CFG":
    """Convertit une CFG en Forme Normale de Chomsky (CNF)."""
    rules = {}
    nonterminals = set(cfg.nonterminals)
    counter = [0]

    def new_nt():
        s = f"X{counter[0]}"
        counter[0] += 1
        nonterminals.add(s)
        return s

    # Étape 1 : remplacer les terminaux dans les règles longues
    term_map = {}
    for nt, prods in cfg.rules.items():
        rules[nt] = []
        for prod in prods:
            if len(prod) >= 2:
                new_prod = []
                for sym in prod:
                    if sym not in cfg.nonterminals:
                        if sym not in term_map:
                            t = new_nt()
                            term_map[sym] = t
                            rules[t] = [(sym,)]
                        new_prod.append(term_map[sym])
                    else:
                        new_prod.append(sym)
                rules[nt].append(tuple(new_prod))
            else:
                rules[nt].append(prod)

    # Étape 2 : binariser les règles longues (A -> B C D => A -> B X, X -> C D)
    final_rules = {}
    for nt, prods in rules.items():
        final_rules[nt] = []
        for prod in prods:
            while len(prod) > 2:
                x = new_nt()
                final_rules[x] = [prod[1:]]
                prod = (prod[0], x)
            final_rules.setdefault(nt, []).append(prod) if nt not in final_rules else None
            if nt in final_rules:
                final_rules[nt].append(prod)

    # Nettoyer doublons
    for nt in final_rules:
        final_rules[nt] = list(set(final_rules[nt]))

    return CFG(rules=final_rules, start=cfg.start, nonterminals=nonterminals)


def cyk(word: str, cfg: "CFG") -> bool:
    """Algorithme CYK : décide si word ∈ L(cfg). La grammaire doit être en CNF."""
    n = len(word)
    if n == 0:
        # Cas mot vide : vérifier si S -> eps existe
        return any(prod == () for prod in cfg.rules.get(cfg.start, []))

    # table[i][j] = ensemble des non-terminaux qui génèrent word[i:j+1]
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Remplir la diagonale : règles unitaires (A -> a)
    for i, c in enumerate(word):
        for nt, prods in cfg.rules.items():
            if (c,) in prods:
                table[i][i].add(nt)

    # Remplir le reste de la table
    for length in range(2, n + 1):          # longueur du sous-mot
        for i in range(n - length + 1):     # début
            j = i + length - 1              # fin
            for k in range(i, j):           # point de coupure
                for nt, prods in cfg.rules.items():
                    for prod in prods:
                        if len(prod) == 2:
                            B, C = prod
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].add(nt)

    return cfg.start in table[0][n - 1]