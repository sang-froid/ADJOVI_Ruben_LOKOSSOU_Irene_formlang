from apps.morpho.automaton import build_word
from apps.hashcons.store import CompactStore


def test_round_trip_exact():
    t = build_word(["re"], "structur", ["ation"])
    s = CompactStore()
    nid = s.intern(t)
    assert s.get(nid) == t


def test_sous_arbres_identiques_partages():
    s = CompactStore()
    a = build_word([], "structur", ["ation"])
    b = build_word([], "structur", ["ation"])
    assert s.intern(a) == s.intern(b)


def test_compression_positive():
    s = CompactStore()
    s.intern(build_word([], "structur", ["ation"]))
    s.intern(build_word(["re"], "structur", ["ation"]))
    assert s.unique_nodes() < s.total_nodes()
    assert s.compression() > 0.0


def test_hashcons_benchmark_10000_mots():
    """Bonus (Jour 5, Q3.5) : sur 10 000 mots, un vocabulaire agglutinant
    (affixes très partagés) doit se compresser nettement mieux qu'un
    vocabulaire isolant (mots libres, sans affixe productif)."""
    from apps.hashcons.benchmark import run_benchmark

    aggl, isol = run_benchmark(10_000)

    assert aggl.n_words == 10_000 and isol.n_words == 10_000
    assert aggl.n_prefixes > 0 and aggl.n_suffixes > 0
    assert isol.n_prefixes == 0 and isol.n_suffixes == 0
    assert aggl.compression > isol.compression
    assert aggl.elapsed_s < 5.0 and isol.elapsed_s < 5.0
