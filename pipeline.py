"""Pipeline intégrateur. À COMPLÉTER : assemblage.  -> Jour 5 (E5.1)."""
from __future__ import annotations
import argparse

from apps.shield.normalizer import leet_normalize
from apps.shield.detector import contains_or
from apps.shield.delimiters import well_parenthesized
from apps.morpho.automaton import morpho_automaton, classify
from apps.morpho.discover import discover, segment_to_tree
from apps.shield.decomposer import (
    shield_automaton, is_blocked, txt, ovr, role, seq, frame, sys,
)


def analyze_word(raw: str) -> dict:
    normalise = leet_normalize(raw)
    or_detecte = contains_or(normalise)
    delimiteurs = well_parenthesized(normalise)
    return {
        "normalisé(FST)":      normalise,
        "facteur_or(AFD)":     or_detecte,
        "délimiteurs_ok(PDA)": delimiteurs,
    }


def analyze_morpho(word: str, vocab: set) -> dict:
    PRE = discover(vocab, prefix_side=True)
    SUF = discover(vocab, prefix_side=False)
    tree = segment_to_tree(word, PRE, SUF)
    A = morpho_automaton()
    classe = classify(A, tree)
    return {
        "prefixes":     PRE,
        "suffixes":     SUF,
        "classe(BUTA)": classe,
    }


def demo_shield() -> list:
    # FOURNI
    A = shield_automaton()
    cases = {
        "seq(txt,txt)": seq(txt(), txt()),
        "role (isolé)": role(),
        "sys(role)": sys(role()),
        "seq(frame(ovr),txt)": seq(frame(ovr()), txt()),
        "sys(seq(txt,frame(role)))": sys(seq(txt(), frame(role()))),
    }
    return [(name, is_blocked(A, t)) for name, t in cases.items()]


def main(argv=None):
    p = argparse.ArgumentParser(description="Pipeline formlang")
    p.add_argument("--word")
    p.add_argument("--morpho")
    p.add_argument("--hashcons-bench", action="store_true",
                    help="Bonus Jour 5 : mesure hash-consing sur 10 000 mots (agglutinant vs isolant)")
    p.add_argument("--mul-utm", nargs=2, type=int, metavar=("M", "N"),
                    help="Bonus Jour 4 : m*n via la table MUL exécutée par la machine universelle")
    args = p.parse_args(argv)
    if args.word:
        for k, v in analyze_word(args.word).items():
            print(f"{k:>22} : {v}")
    if args.morpho:
        from apps.morpho.corpora import corpus_A
        print(analyze_morpho(args.morpho, set(corpus_A())))
    if args.mul_utm:
        from apps.mtu.interpreter import multiplication_via_utm
        m, n = args.mul_utm
        print(f"{m} * {n} (MUL via UTM) = {multiplication_via_utm(m, n)}")
    if args.hashcons_bench:
        from apps.hashcons.benchmark import run_benchmark
        for report in run_benchmark():
            print(report)
            print()
    if not any([args.word, args.morpho, args.hashcons_bench, args.mul_utm]):
        print("== démo Shield (AttackDecomposer) ==")
        for name, blocked in demo_shield():
            print(f"  {'BLOQUÉ ' if blocked else 'OK     '} {name}")


if __name__ == "__main__":
    main()
