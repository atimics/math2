"""TC-4 reproducer: the APSP exponent from family 107's rectangular bounds, exactly.

Premises (family 107, "Complex Matrix Multiplication Below 2.258 and Rectangular
Bounds", Thm 1.1 and Cors 14.1–14.2): over every field of characteristic zero
    alpha > 0.465            (so w(0.465) = 2, where w(k) = omega(1, k, 1))
    w(0.709) < 523/250 = 2.092.
Convexity of k -> w(k) (107 §2; classical, Lotti–Romani) gives, for
0.465 <= mu <= 0.709,   w(mu) < 2 + (23/61)(mu - 0.465)   (strict for mu > 0.465).
Zwick (JACM 49, 2002): directed APSP with integer weights in {-M..M}, M = O(1),
runs in O~(n^{2+mu}) whenever w(mu) <= 1 + 2 mu.

The second part is a LEAD, not a result: 107 §12.2 derives, for a parameter t,
    w(2 g(t)/h(t)) <= 6 log 3 / h(t)                                  (12.12)
with Z(t) = 8 + 12*2^t + 6*4^t + 19^t, g = (log Z)', h = log Z - t g, but its
Theorem 1.1 and Corollaries 14.1-14.2 record only t = 2/3. If (12.12) holds for
every t > 0, the curve meets Zwick's line w(mu) = 1 + 2 mu at mu ~ 0.50339.

Run: python3 scripts/review/tc4_apsp.py   (the lead part needs mpmath, which sympy installs)
"""
from fractions import Fraction as Fr

K0, W0 = Fr(465, 1000), Fr(2)          # alpha > 0.465  =>  w(0.465) = 2
K1, W1 = Fr(709, 1000), Fr(523, 250)   # w(0.709) < 2.092
PREVIOUS_BEST = Fr(5275, 10000)        # Alman–Duan–Vassilevska Williams–Xu–Xu–Zhou, arXiv:2404.16349


def chord(mu: Fr) -> Fr:
    return W0 + (W1 - W0) / (K1 - K0) * (mu - K0)


def main() -> None:
    slope = (W1 - W0) / (K1 - K0)
    # solve chord(mu) = 1 + 2 mu
    mu_star = (W0 - slope * K0 - 1) / (2 - slope)
    print(f"slope = {slope}  (expected 23/61)")
    print(f"mu*   = {mu_star} = {float(mu_star):.7f}  (expected 10061/19800)")
    assert slope == Fr(23, 61) and mu_star == Fr(10061, 19800)
    assert K0 < mu_star < K1, "crossing must lie inside the interpolation interval"
    assert chord(mu_star) == 1 + 2 * mu_star
    # every mu slightly above mu* satisfies the strict Zwick condition
    mu = mu_star + Fr(1, 10**6)
    assert chord(mu) < 1 + 2 * mu
    print(f"APSP exponent 2 + mu* = {float(2 + mu_star):.7f} < 2.5082")
    assert 2 + mu_star < Fr(25082, 10000)
    print(f"previous best published mu < {float(PREVIOUS_BEST)}: improvement {float(PREVIOUS_BEST - mu_star):.5f}")
    assert mu_star < PREVIOUS_BEST
    print("OK")
    lead()


def lead() -> None:
    try:
        from mpmath import mp, mpf, log, diff, findroot
    except ImportError:
        print("(lead skipped: mpmath not installed)")
        return
    mp.dps = 30
    Z = lambda t: 8 + 12 * mpf(2) ** t + 6 * mpf(4) ** t + mpf(19) ** t
    g = lambda t: diff(lambda u: log(Z(u)), t)
    h = lambda t: log(Z(t)) - t * g(t)
    k = lambda t: 2 * g(t) / h(t)
    w = lambda t: 6 * log(3) / h(t)
    t23 = mpf(2) / 3
    assert k(t23) > mpf("0.709") and w(t23) < mpf("2.092")   # 107's recorded point
    t0 = findroot(lambda t: w(t) - 1 - 2 * k(t), 0.2)
    print(f"LEAD (not a result): (12.12) at t = {float(t0):.6f} gives w({float(k(t0)):.6f}) <= "
          f"{float(w(t0)):.6f} = 1 + 2*mu, i.e. mu < 0.50346 if (12.12) holds at that t")
    assert k(t0) < mpf("0.50346")


if __name__ == "__main__":
    main()
