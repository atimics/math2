"""CL-1 reproducer: the separability-idempotent construction, checked exactly.

Family 172's criterion (Thm 1.1; comparator EuclideanRamsey.lean `FieldCriterion`):
A = {a_1..a_s} (s >= 2, affinely spanning R^d) is Ramsey iff there is
P in Mat_{d+1}(B), B = F (x)_Q F, with
  (1)  sum_{alpha,beta} (p_i,alpha (x) 1) P_alpha,beta (1 (x) p_i,beta) = 0   for every i,
  (2)  m_F(P_alpha,beta) = delta_alpha,beta                               for spatial alpha, beta,
where p_i = (1, a_i) and m_F(x (x) y) = xy.

CL-1 claim: if F is a number field and A is spherical, P = e * (H (x) 1) works,
where H encodes the sphere and e is the separability idempotent of F/Q.

This script takes F = Q(sqrt 2), SIX points on the circle (x - sqrt2)^2 + y^2 = 1,
represents B = Q[X, Y]/(X^2 - 2, Y^2 - 2) (X = sqrt2 (x) 1, Y = 1 (x) sqrt2), and checks:
  * family 172's Prop 7.3 does NOT apply (its row-independence hypothesis fails), nor does
    Cor 7.4 (at most five points);
  * P = e*(H (x) 1) satisfies (1) and (2) exactly;
  * the naive choice P = H (x) 1, without e, violates (1).

Run: python3 scripts/review/cl1_idempotent.py   (needs sympy)
"""
import sympy as sp

s, X, Y = sp.symbols("s X Y")          # s = sqrt(2) in F; X, Y its two copies in B
SQ2 = sp.sqrt(2)


def reduce_B(expr):
    """Normal form in B = Q[X,Y]/(X^2-2, Y^2-2)."""
    return sp.reduced(sp.expand(expr), [X**2 - 2, Y**2 - 2], X, Y)[1]


def left(v):   # v in F = Q(s)  ->  v (x) 1
    return sp.expand(v).subs(s, X)


def right(v):  # v in F  ->  1 (x) v
    return sp.expand(v).subs(s, Y)


def mult(b):   # m_F : B -> F, X, Y -> s ; then reduce s^2 = 2
    return sp.expand(sp.expand(b).subs({X: s, Y: s})).subs(s**2, 2)


def main() -> None:
    # six rational parameters t -> point on the unit circle centred at (sqrt2, 0)
    ts = [sp.Integer(0), sp.Integer(1), sp.Integer(2), sp.Rational(1, 2), sp.Integer(-1), sp.Integer(3)]
    pts = [(s + (1 - t**2) / (1 + t**2), 2 * t / (1 + t**2)) for t in ts]
    # sanity: they are on the circle and distinct
    for (x, y) in pts:
        assert sp.simplify(((x - s) ** 2 + y**2 - 1).subs(s, SQ2)) == 0
    assert len({(sp.nsimplify(x.subs(s, SQ2)), y) for x, y in pts}) == 6
    p = [[sp.Integer(1), x, y] for (x, y) in pts]          # p_i = (1, a_i)

    # Prop 7.3 hypothesis: rows (p_ia p_ib)_{a,b} linearly independent over F.
    rows = sp.Matrix([[sp.expand((pi[a] * pi[b]).subs(s, SQ2)) for a in range(3) for b in range(3)] for pi in p])
    rank = rows.rank(simplify=True)
    print(f"Prop 7.3 row rank = {rank} < 6 points: neither 172's Prop 7.3 nor its Cor 7.4 (<= 5 points) applies")
    assert rank < 6

    # sphere ||a||^2 + l.a + c = 0 with l = (-2 sqrt2, 0), c = 1  ->  H (entries in F)
    H = [[sp.Integer(1), -2 * s, sp.Integer(0)],
         [sp.Integer(0), sp.Integer(1), sp.Integer(0)],
         [sp.Integer(0), sp.Integer(0), sp.Integer(1)]]
    for pi in p:
        q = sum(pi[a] * H[a][b] * pi[b] for a in range(3) for b in range(3))
        assert sp.simplify(sp.expand(q).subs(s, SQ2)) == 0

    # separability idempotent of Q(sqrt2): e = (sqrt2 (x) 1 + 1 (x) sqrt2) / (2 sqrt2 (x) 1)
    e = reduce_B((X + Y) * X / 4)                # = (2 + XY)/4
    assert mult(e) == 1
    assert reduce_B((X - Y) * e) == 0
    print(f"e = {e}:  m_F(e) = 1 and (X - Y) e = 0")

    def check(P):
        c1 = [reduce_B(sum(left(pi[a]) * P[a][b] * right(pi[b]) for a in range(3) for b in range(3))) for pi in p]
        c2 = all(sp.simplify(mult(P[a][b]) - (1 if a == b else 0)) == 0 for a in (1, 2) for b in (1, 2))
        return c1, c2

    P_e = [[reduce_B(e * left(H[a][b])) for b in range(3)] for a in range(3)]
    c1, c2 = check(P_e)
    print(f"P = e*(H(x)1): condition (1) values = {c1}; condition (2) holds = {c2}")
    assert all(v == 0 for v in c1) and c2

    P_plain = [[left(H[a][b]) for b in range(3)] for a in range(3)]
    c1n, _ = check(P_plain)
    print(f"naive P = H(x)1 (no idempotent): condition (1) values = {c1n}")
    assert any(v != 0 for v in c1n)
    print("OK: the criterion holds with the idempotent, and the naive choice fails;")
    print("so this 6-point algebraic circle set is Ramsey by 172's Theorem 1.1 itself.")


if __name__ == "__main__":
    main()
