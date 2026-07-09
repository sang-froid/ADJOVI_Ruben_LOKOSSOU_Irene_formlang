"""Bonus (Jour 5, Q3.5) : mesure du hash-consing sur un vocabulaire de
10 000 mots.

On compare deux familles de langues synthétiques :
  - agglutinante (façon turc/finnois) : préfixes/suffixes très partagés ;
  - isolante (façon anglais)          : mots libres, sans affixe productif.

Règle « gate » : ce module n'instancie que ce qui existe déjà --
CompactStore (formlang.tree via apps.hashcons.store) et
discover/segment_to_tree (apps.morpho.discover, qui repose lui-même sur
formlang.tree.TreeAutomaton). Aucune structure d'arbre ou de partage n'est
réimplémentée ici.
"""
from __future__ import annotations
from dataclasses import dataclass
import time

from apps.hashcons.store import CompactStore
from apps.morpho.discover import discover, segment_to_tree
from apps.morpho.corpora import corpus_agglutinant, corpus_isolant


@dataclass
class HashconsReport:
    label: str
    n_words: int
    n_prefixes: int
    n_suffixes: int
    total_nodes: int
    unique_nodes: int
    compression: float
    elapsed_s: float

    def __str__(self) -> str:
        return (
            f"--- {self.label} ---\n"
            f"  mots            : {self.n_words}\n"
            f"  préfixes trouvés: {self.n_prefixes}\n"
            f"  suffixes trouvés: {self.n_suffixes}\n"
            f"  noeuds total    : {self.total_nodes}\n"
            f"  noeuds uniques  : {self.unique_nodes}\n"
            f"  compression     : {self.compression:.2%}\n"
            f"  temps           : {self.elapsed_s:.3f} s"
        )


def measure(vocab: list, label: str) -> HashconsReport:
    """Segmente chaque mot en Term (discover + segment_to_tree, Jour 3) puis
    interne tous les arbres dans un CompactStore unique (hash-consing)."""
    vset = set(vocab)
    PRE = discover(vset, prefix_side=True)
    SUF = discover(vset, prefix_side=False)

    store = CompactStore()
    t0 = time.perf_counter()
    for w in vocab:
        tree = segment_to_tree(w, PRE, SUF)
        store.intern(tree)
    elapsed = time.perf_counter() - t0

    return HashconsReport(
        label=label,
        n_words=len(vocab),
        n_prefixes=len(PRE),
        n_suffixes=len(SUF),
        total_nodes=store.total_nodes(),
        unique_nodes=store.unique_nodes(),
        compression=store.compression(),
        elapsed_s=elapsed,
    )


def run_benchmark(n_words: int = 10_000) -> list:
    return [
        measure(corpus_agglutinant(n_words), "agglutinant (turc/finnois, synthétique)"),
        measure(corpus_isolant(n_words), "isolant (anglais, synthétique)"),
    ]


def main():
    for report in run_benchmark():
        print(report)
        print()


if __name__ == "__main__":
    main()
