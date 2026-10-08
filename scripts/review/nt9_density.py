"""NT-9 reproducer: where 83.75% comes from, in exact arithmetic.

Bhargava–Shankar (arXiv:1312.7859) prove that the average size of Sel_5(E) is 6
when elliptic curves over Q are ordered by height (their Thm 1), and that a family
F of density > 55.01% has equidistributed root numbers (their Thm 6). By p-parity
(Dokchitser–Dokchitser) and Cassels–Tate, d = dim_F5 Sel_5(E) has the parity of the
root number outside the density-zero set of curves with a rational 5-torsion point,
so on F, d is even for half the curves and odd for the other half.

This script proves, for EVERY distribution of d (no truncation), the two bounds
    on F:            P(d <= 1) >= 7/8     given E[5^d] <= 6 and P(d odd) = 1/2,
    on F's complement: P(d <= 1) >= 19/24  given E[5^d] <= 6,
via a pointwise dual certificate, shows both are tight for these inputs, and then
combines them. It also states the bridge to family 002 at q = 5:
    corank_{Z_5} Sel_{5^oo}(E) <= dim Sel_5(E) - dim E(Q)[5] <= dim Sel_5(E).

Run: python3 scripts/review/nt9_density.py
"""
from fractions import Fraction as Fr

AVG = Fr(6)                 # Bhargava–Shankar Thm 1: average #Sel_5 = 6
SHARE_F = Fr(5501, 10000)   # Bhargava–Shankar Thm 6: density of F is > 0.5501


def certificate_holds(c_big: Fr, c_odd: Fr, upto: int = 60) -> bool:
    """5^d >= 1 + c_big*[d >= 2] + c_odd*[d odd] for all d >= 0.

    Checked for d <= upto; for d >= 3 the left side is >= 125 and increasing while
    the right side is constant, so checking up to any upto >= 3 covers all d."""
    return all(Fr(5) ** d >= 1 + c_big * (d >= 2) + c_odd * (d % 2) for d in range(upto + 1))


def mean(dist: dict) -> Fr:
    return sum(p * Fr(5) ** d for d, p in dist.items())


def show(dist: dict) -> str:
    return ", ".join(f"d={d}: {p}" for d, p in sorted(dist.items()))


def main() -> None:
    # --- On F: averaging the certificate 5^d >= 1 + 24[d>=2] + 4[d odd] gives
    #     AVG >= 1 + 24 P(d>=2) + 4 * 1/2, so P(d>=2) <= (AVG - 3)/24 = 1/8.
    assert certificate_holds(Fr(24), Fr(4))
    bad_F = (AVG - 1 - Fr(4) * Fr(1, 2)) / 24
    tight_F = {0: Fr(3, 8), 1: Fr(1, 2), 2: Fr(1, 8)}   # BS §1 extremal law (#Sel5 = 1, 5, 25)
    assert sum(tight_F.values()) == 1 and mean(tight_F) == AVG
    assert sum(p for d, p in tight_F.items() if d % 2) == Fr(1, 2)
    assert sum(p for d, p in tight_F.items() if d >= 2) == bad_F
    good_F = 1 - bad_F

    # --- On the complement: 5^d >= 1 + 24[d>=2] gives P(d>=2) <= (AVG - 1)/24 = 5/24.
    assert certificate_holds(Fr(24), Fr(0))
    bad_C = (AVG - 1) / 24
    tight_C = {0: Fr(19, 24), 2: Fr(5, 24)}
    assert sum(tight_C.values()) == 1 and mean(tight_C) == AVG
    good_C = 1 - bad_C

    total = SHARE_F * good_F + (1 - SHARE_F) * good_C
    print(f"P(dim Sel5 <= 1) on the equidistributed family F >= {good_F}  (tight: {show(tight_F)})")
    print(f"P(dim Sel5 <= 1) on the complement of F          >= {good_C}  (tight: {show(tight_C)})")
    print(f"combined lower density = 0.5501*{good_F} + 0.4499*{good_C} = {total} = {float(total):.8f}")
    assert good_F == Fr(7, 8) and good_C == Fr(19, 24)
    assert total == Fr(100501, 120000) and total > Fr(8375, 10000)
    # A larger share for F only helps, since 7/8 > 19/24.
    assert good_F > good_C
    print("OK: lower density > 0.8375 with 5-Selmer dimension <= 1.")
    print("Bridge: corank Sel_{5^oo} <= dim Sel_5 - dim E(Q)[5] <= dim Sel_5, so these curves")
    print("satisfy s_5(E) in {0,1}, the hypothesis of family 002's Theorem 1.1 at q = 5.")


if __name__ == "__main__":
    main()
