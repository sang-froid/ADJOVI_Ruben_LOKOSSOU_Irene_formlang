"""Automate morphologique (instancie formlang.tree). À COMPLÉTER : règles Delta.
-> Jour 3 (E3.2). Constructeurs et classify FOURNIS."""
from formlang.tree import Term, TreeAutomaton


# ----- constructeurs FOURNIS ------------------------------------------------
def prefix(s): return Term("prefix", label=s)
def root(s):   return Term("root",   label=s)
def suffix(s): return Term("suffix", label=s)
def nil():     return Term("nil")
def prefixes(h, t): return Term("prefixes", (h, t))
def suffixes(h, t): return Term("suffixes", (h, t))
def rest(r, s):     return Term("rest", (r, s))
def word(p, r):     return Term("word", (p, r))


def build_word(pres, root_str, sufs) -> Term:
    pc = nil()
    for p in reversed(pres):
        pc = prefixes(prefix(p), pc)
    sc = nil()
    for s in reversed(sufs):
        sc = suffixes(suffix(s), sc)
    return word(pc, rest(root(root_str), sc))


def morpho_automaton() -> TreeAutomaton:
    A = TreeAutomaton(final_states={"WORD"})

    # Feuilles
    A.add_rule("nil",    (),          "NIL")
    A.add_rule("prefix", (),          "PRE")
    A.add_rule("root",   (),          "ROOT")
    A.add_rule("suffix", (),          "SUF")

    # Chaînes de préfixes et suffixes
    A.add_rule("prefixes", ("PRE", "NIL"),   "PREFS")
    A.add_rule("prefixes", ("PRE", "PREFS"), "PREFS")
    A.add_rule("suffixes", ("SUF", "NIL"),   "SUFS")
    A.add_rule("suffixes", ("SUF", "SUFS"),  "SUFS")

    # rest et word
    A.add_rule("rest", ("ROOT", "NIL"),  "REST")
    A.add_rule("rest", ("ROOT", "SUFS"), "REST")
    A.add_rule("word", ("NIL",  "REST"), "WORD")
    A.add_rule("word", ("PREFS","REST"), "WORD")

    return A


# ----- FOURNI ---------------------------------------------------------------
def _contains(t: Term, sym: str) -> bool:
    if t.symbol == sym:
        return True
    return any(_contains(c, sym) for c in t.children)


def classify(A: TreeAutomaton, t: Term) -> str:
    if not A.accepts(t):
        return "INVALID"
    p  = _contains(t, "prefix")
    s  = _contains(t, "suffix")
    i  = _contains(t, "infix")
    if i:
        return "INFIXED"
    if p and s:
        return "CIRCUMFIXED"
    if s:
        return "SUFFIXED"
    if p:
        return "PREFIXED"
    return "BARE"

# ----- constructeurs infixation (bonus) -------------------------------------
def infix(s):      return Term("infix", label=s)
def infixes(h, t): return Term("infixes", (h, t))
def root_split(left, inf, right): return Term("root_split", (left, inf, right))
def word_infix(p, r): return Term("word_infix", (p, r))


def build_word_infix(pres, root_left, inf, root_right, sufs) -> Term:
    pc = nil()
    for p in reversed(pres):
        pc = prefixes(prefix(p), pc)
    sc = nil()
    for s in reversed(sufs):
        sc = suffixes(suffix(s), sc)
    rs = root_split(root(root_left), infix(inf), root(root_right))
    return word_infix(pc, rest(rs, sc))


def morpho_automaton_with_infix() -> TreeAutomaton:
    A = morpho_automaton()   # récupérer toutes les règles existantes

    # Nouvelles feuilles
    A.add_rule("infix", (), "INF")

    # Chaîne d'infixes
    A.add_rule("infixes", ("INF", "NIL"),   "INFS")
    A.add_rule("infixes", ("INF", "INFS"),  "INFS")

    # root_split : racine coupée avec infixe au milieu
    A.add_rule("root_split", ("ROOT", "INF", "ROOT"), "ROOT_INF")

    # rest et word_infix
    A.add_rule("rest",       ("ROOT_INF", "NIL"),   "REST")
    A.add_rule("rest",       ("ROOT_INF", "SUFS"),  "REST")
    A.add_rule("word_infix", ("NIL",   "REST"),     "WORD")
    A.add_rule("word_infix", ("PREFS", "REST"),     "WORD")

    return A