from apps.mtu.calculator import Calculatrice
from apps.mtu.machines import ADD, SUB


def test_add_sub_machines_directes():
    assert ADD.run("111+11").tape.count("1") == 5
    assert SUB.run("111-11").tape.count("1") == 1
    assert SUB.run("11-11").tape == ""


def test_calculatrice_exhaustif():
    c = Calculatrice()
    for n in range(7):
        for m in range(7):
            assert c.addition(n, m) == n + m
            assert c.soustraction(n, m) == max(0, n - m)
            assert c.multiplication(n, m) == n * m
            if m:
                assert c.division(n, m) == divmod(n, m)


def test_chainage():
    assert Calculatrice().chainer(2, [("+", 1), ("*", 2), ("-", 1), ("/", 2)]) == 2


def test_division_par_zero():
    import pytest
    with pytest.raises(ZeroDivisionError):
        Calculatrice().division(3, 0)

def test_mul_monolithique():
    from apps.mtu.machines import MUL
    assert MUL.run("11*111=").tape.count("1") == 6
    assert MUL.run("111*11=").tape.count("1") == 6
    assert MUL.run("1*1111=").tape.count("1") == 4
    assert MUL.run("11111*11=").tape.count("1") == 10


def test_mul_monolithique_via_utm():
    """Bonus : la MÊME table MUL, non ré-exécutée en Python mais simulée par la
    machine universelle (formlang.utm.UniversalTM), comme addition_via_utm."""
    from apps.mtu.interpreter import multiplication_via_utm
    assert multiplication_via_utm(2, 3) == 6
    assert multiplication_via_utm(5, 2) == 10
    assert multiplication_via_utm(0, 4) == 0
    assert multiplication_via_utm(4, 4) == 16