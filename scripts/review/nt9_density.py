"""NT-9 reproducer: where 83.75% comes from, in exact arithmetic.

Bhargava–Shankar (arXiv:1312.7859) prove that the average size of Sel_5(E)
is 6 in every "large" family of elliptic curves defined by local conditions,
ordered by height (their Props 38(b), 40(b); proof of Thms 3–5, pp. 27–29).
On a family of density > 0.5501 root numbers are equidistributed, so by
p-parity (Dokchitser–Dokchitser) dim Sel_5 is even/odd half the time each.

This script recomputes the two resulting lower bounds on P(dim Sel_5 <= 1)
as tiny linear programs over the distribution of d = dim Sel_5, with
#Sel_5 = 5^d, and then the combined density. It also records the bridge
corank_{Z_5} Sel_{5^oo} <= dim Sel_5 - dim E(Q)[5] <= dim Sel_5.

Run: python3 scripts/review/nt9_density.py
"""
from fractions import Fraction as Fr
from itertools import product

AVG = Fr(6)            # Bhargava–Shankar: average #Sel_5 = 6 in large families
DMAX = 6               # truncation for the brute-force check (higher d only costs more)


def worst_case(parity_split: bool) -> Fr:
    """Max of P(d >= 2) subject to E[5^d] <= AVG (and, if parity_split,
    P(d even) = P(d odd) = 1/2). Solved exactly by enumerating the LP's
    vertices, which put mass on at most two (resp. four) support points."""
    best = Fr(0)
    ds = range(DMAX + 1)
    if not parity_split:
        for d1, d2 in product(ds, ds):
            if d1 >= d2:
                continue
            # mass p at d2, 1-p at d1, cost constraint p*5^d2 + (1-p)*5^d1 <= AVG
            c1, c2 = Fr(5) ** d1, Fr(5) ** d2
            if c1 > AVG:
                continue
            p = min(Fr(1), (AVG - c1) / (c2 - c1))
            bad = (p if d2 >= 2 else 0) + ((1 - p) if d1 >= 2 else 0)
            best = max(best, bad)
        return best
    evens = [d for d in ds if d % 2 == 0]
    odds = [d for d in ds if d % 2 == 1]
    # half the mass on evens, half on odds; each half is a two-point mixture
    for e1, e2, o1, o2 in product(evens, evens, odds, odds):
        if e1 > e2 or o1 > o2:
            continue
        # grid over the mixing weights (vertices lie at 0, 1 or the budget boundary)
        for a in [Fr(k, 96) for k in range(97)]:
            for b in [Fr(k, 96) for k in range(97)]:
                cost = Fr(1, 2) * ((1 - a) * 5 ** e1 + a * 5 ** e2) + Fr(1, 2) * ((1 - b) * 5 ** o1 + b * 5 ** o2)
                if cost > AVG:
                    continue
                bad = Fr(1, 2) * ((a if e2 >= 2 else 0) + ((1 - a) if e1 >= 2 else 0)) \
                    + Fr(1, 2) * ((b if o2 >= 2 else 0) + ((1 - b) if o1 >= 2 else 0))
                best = max(best, bad)
    return best


def main() -> None:
    bad_parity = worst_case(parity_split=True)     # expect 1/8   -> good >= 7/8
    bad_free = worst_case(parity_split=False)      # expect 5/24  -> good >= 19/24
    good_parity, good_free = 1 - bad_parity, 1 - bad_free
    share = Fr(5501, 10000)                         # BS: equidistributed-root-number family
    total = share * good_parity + (1 - share) * good_free
    print(f"P(dim Sel5 <= 1) on the equidistributed family  >= {good_parity}  (expected 7/8)")
    print(f"P(dim Sel5 <= 1) on the complement               >= {good_free}  (expected 19/24)")
    print(f"combined lower density = 0.5501*{good_parity} + 0.4499*{good_free} = {total} = {float(total):.8f}")
    assert good_parity == Fr(7, 8), good_parity
    assert good_free == Fr(19, 24), good_free
    assert total > Fr(8375, 10000)
    print("OK: lower density > 0.8375 with 5-Selmer dimension <= 1.")
    print("Bridge: corank Sel_{5^oo} <= dim Sel_5 - dim E(Q)[5] <= dim Sel_5, so these curves")
    print("satisfy s_5(E) in {0,1}, the hypothesis of family 002's Theorem 1.1 at q = 5.")


if __name__ == "__main__":
    main()
