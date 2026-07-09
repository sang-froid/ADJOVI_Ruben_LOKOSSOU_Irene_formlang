"""Corpus synthétiques (FOURNI)."""
PREFIXES_A = ["mu", "ba", "ki", "vi", "li", "ma", "wa", "tu"]
SUFFIXES_B = ["lar", "ler", "im", "in", "de", "den", "si", "ya"]
CONS = "fghjzcdnrs"
VOW = "aeiou"


def roots(n: int):
    out = []
    for c1 in CONS:
        for v1 in VOW:
            for c2 in CONS:
                for v2 in VOW:
                    out.append(c1 + v1 + c2 + v2 + "k")
                    if len(out) >= n:
                        return out
    return out


def corpus_A(n_roots: int = 150) -> list:
    A = []
    for r in roots(n_roots):
        A.append(r)
        A += [p + r for p in PREFIXES_A]
    return A


def corpus_B(n_roots: int = 150) -> list:
    B = []
    for r in roots(n_roots):
        B.append(r)
        B += [r + s for s in SUFFIXES_B]
    return B


# ----- Bonus (Jour 5) : vocabulaires 10 000 mots pour la mesure hash-consing ---
# roots() ne peut produire que 10*5*10*5 = 2500 racines distinctes (c1 v1 c2 v2 "k").

def corpus_agglutinant(n_words: int = 10_000) -> list:
    """Vocabulaire synthétique de type agglutinant (façon turc/finnois) : pour
    chaque racine on ajoute la racine nue, la racine préfixée (8 préfixes) et
    la racine suffixée (8 suffixes) -- comme corpus_A/corpus_B, mais assez de
    racines pour atteindre n_words. discover() retrouve alors les 8 préfixes
    et les 8 suffixes (la racine « pelée » est bien présente dans le
    vocabulaire), et segment_to_tree peut ensuite produire de nombreux
    sous-arbres 'prefixes(...)'/'suffixes(...)' identiques -- un fort partage
    par hash-consing."""
    forms_per_root = 1 + len(PREFIXES_A) + len(SUFFIXES_B)  # bare + préfixées + suffixées
    n_roots = -(-n_words // forms_per_root)  # ceil
    out = []
    for r in roots(n_roots):
        out.append(r)
        out += [p + r for p in PREFIXES_A]
        out += [r + s for s in SUFFIXES_B]
        if len(out) >= n_words:
            break
    return out[:n_words]


def corpus_isolant(n_words: int = 10_000) -> list:
    """Vocabulaire synthétique de type isolant (façon anglais) : chaque mot est
    la concaténation de deux racines choisies pour rester quasi toutes
    distinctes, sans affixe productif partagé -> aucun préfixe/suffixe n'est
    (re)découvert par discover(), donc un partage par hash-consing minimal
    (seuls les nœuds-squelette communs, ex. nil(), sont réutilisés)."""
    rs = roots(2500)
    n = len(rs)
    out, seen = [], set()
    i, j = 0, 0
    while len(out) < n_words:
        w = rs[i % n] + rs[j % n]
        if w not in seen:
            seen.add(w)
            out.append(w)
        i += 1
        j += 7
        if i % n == 0:
            j += 1
    return out[:n_words]
