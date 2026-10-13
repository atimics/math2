"""Exact finite controls for the NT-4 note; no analytic theorem is computed.

Runtime: Python 3.10+ standard library. The fixed domain is deliberate; it is
finite supporting evidence, not a configurable asymptotic search.
"""

from collections.abc import Callable
from fractions import Fraction
from functools import cache
import json
from math import comb, gcd, lcm


@cache
def divisors(n: int) -> tuple[int, ...]:
    """Positive divisors, for a positive integer in the fixed test domain."""
    return tuple(d for d in range(1, n + 1) if n % d == 0)


@cache
def mobius(n: int) -> int:
    sign = 1
    prime = 2
    while prime * prime <= n:
        if n % prime == 0:
            n //= prime
            sign = -sign
            if n % prime == 0:
                return 0
        prime += 1
    return -sign if n > 1 else sign


@cache
def totient(n: int) -> int:
    return sum(gcd(k, n) == 1 for k in range(1, n + 1))


def ramanujan(d: int, k: int) -> int:
    # Integer divisor identity avoids floating-point roots of unity.
    return sum(e * mobius(d // e) for e in divisors(gcd(d, k)))


def character_indicator(order: int, exponent: int) -> Fraction:
    return Fraction(totient(order), order) * sum(
        Fraction(mobius(d), totient(d)) * ramanujan(d, exponent)
        for d in divisors(order)
    )


def require(condition: bool, explanation: str) -> None:
    # Explicit raising preserves failure detection under python -O.
    if not condition:
        raise AssertionError(explanation)


def verify_indicator(
    evaluator: Callable[[int, int], Fraction], limit: int
) -> int:
    checked = 0
    for order in range(1, limit + 1):
        for exponent in range(order):
            observed = evaluator(order, exponent)
            expected = int(gcd(order, exponent) == 1)
            require(observed == expected,
                    f"indicator: order={order}, exponent={exponent}, "
                    f"observed={observed}, expected={expected}")
            checked += 1
    return checked


def verify_binomial(limit: int) -> int:
    # log(lcm(1,...,n)) is Psi(n); all comparisons are integer-exact.
    lcms = [1]
    for n in range(1, 2 * limit + 1):
        lcms.append(lcm(lcms[-1], n))
    for m in range(1, limit + 1):
        central = comb(2 * m, m)
        require(lcms[2 * m] % central == 0, f"binomial divides lcm: m={m}")
        require(central % (lcms[2 * m] // lcms[m]) == 0,
                f"prime-power interval divides binomial: m={m}")
        require(central <= 4 ** m, f"binomial upper bound: m={m}")
        require(central * (2 * m + 1) >= 4 ** m,
                f"binomial lower bound: m={m}")
    return limit


def expect_rejection(check: Callable[[], object]) -> str:
    try:
        check()
    except AssertionError as error:
        return str(error)
    raise AssertionError("negative control unexpectedly passed")


def run() -> dict[str, object]:
    indicator_cases = verify_indicator(character_indicator, 256)
    binomial_cases = verify_binomial(256)

    def missing_normalization(order: int, exponent: int) -> Fraction:
        return character_indicator(order, exponent) * Fraction(order, totient(order))

    def unsigned_mobius(order: int, exponent: int) -> Fraction:
        return Fraction(totient(order), order) * sum(
            Fraction(abs(mobius(d)), totient(d)) * ramanujan(d, exponent)
            for d in divisors(order)
        )

    controls = []
    for name, mutation in [
        ("missing_indicator_normalization", missing_normalization),
        ("unsigned_mobius_coefficients", unsigned_mobius),
    ]:
        failure = expect_rejection(lambda: verify_indicator(mutation, 32))
        controls.append({"name": name, "rejected": True, "counterexample": failure})

    # At x=2, Lambda(1)=0, and the only possible nonzero Mangoldt term is
    # log(2) times w(1)=0. This exactly disproves a positive bound at x=2.
    w_at_one = Fraction(2, 2) * (1 - Fraction(2, 2))
    failure = expect_rejection(
        lambda: require(w_at_one >= Fraction(2, 512), "W(2)=0 < 2/512")
    )
    controls.append({"name": "lower_bound_extended_to_x_2",
                     "rejected": True, "counterexample": failure})
    return {
        "status": "passed",
        "arithmetic": "exact integers and fractions; no floating point",
        "indicator_domain": {"order_min": 1, "order_max": 256,
                             "exponents": "every 0 <= k < order"},
        "indicator_cases": indicator_cases,
        "binomial_domain": {"m_min": 1, "m_max": 256},
        "binomial_cases": binomial_cases,
        "binomial_relations_per_case": 4,
        "negative_controls": controls,
        "random_seed": None,
        "stopping_rule": "complete the stated finite domains",
        "analytic_theorem_verified_by_computation": False,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
