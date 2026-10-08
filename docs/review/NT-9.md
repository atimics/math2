# NT-9 · Full BSD for at least 83.75% of elliptic curves — review packet

**Reviewer profile:** arithmetic statistics (Bhargava–Shankar averages) or Selmer and Iwasawa
theory. **Time:** about an hour if you know Bhargava–Shankar's 5-Selmer paper.
**Catalogue entry:** [NT-9](../COROLLARIES.md#nt-9). The longer write-up is
[RP-4](../RESEARCH_PRIORITIES.md#rp-4-full-bsd-in-analytic-low-rank-and-a-height-density-consequence).
**Tier:** D (complete written derivation; not formalized).

## The claim

*Assume* OpenAI family 002's Theorem 1.1 (quoted below). Order elliptic curves `E/ℚ` by
naive height `H(E_{A,B}) = max(4|A|³, 27B²)`. Then the full Birch–Swinnerton-Dyer formula

```
L^(r)(E,1) / r!  =  Ω_E · Reg_E · #Ш(E/ℚ) · ∏_ℓ c_ℓ(E)  /  #E(ℚ)_tors²,      r = rank E(ℚ) = ord_{s=1} L(E,s),
```

with `Ш` finite, holds on a set of curves of **lower density at least
`0.5501·7/8 + 0.4499·19/24 = 100501/120000 = 0.83750…`**.

The new step is small. Bhargava–Shankar's inputs bound the density of curves with
5-Selmer dimension at most 1, and 002 accepts low 5-Selmer corank as its hypothesis.
Steps 4–7 below re-derive that density directly from Bhargava–Shankar's Theorems 1, 2
and 6. They do not rely on how Bhargava–Shankar phrase their 83.75%. For comparison,
Bhargava–Skinner–Zhang's 66.48% is for the *rank* part of BSD with finite Ш, not the
leading-term formula.

## Questions for you

1. **The crux: averages on `F` and on its complement.** Steps 5–6 need
   `avg #Sel₅ ≤ 6` both on the equidistributed family `F` (Thm 6) and on its complement.
   For the complement this needs the average on `F` to be **exactly** 6, a lower bound
   and not only an upper bound. Thm 2 is stated for families defined by *finitely many*
   congruence conditions, while Thm 6 says only that `F` is "defined by congruence
   conditions". Is the complement bound justified? Bhargava–Shankar use the same split
   themselves, for their 0.885 average-rank bound (`0.5501 × 0.75 + 0.4499 × 1.05`) and,
   in our reading, for 83.75% and 20.62%. So whatever justifies theirs justifies ours.
2. **Corroboration.** Are Bhargava–Shankar's 83.75% (Thm 4) and 20.62% (Thm 5) obtained
   as lower densities of curves with `dim_{𝔽₅} Sel₅ ≤ 1` and `= 0`? Our script reproduces
   both figures from the Selmer constraints alone: `0.5501·7/8 + 0.4499·19/24 = 0.837508`
   and `0.5501·3/8 = 0.206288`. Our external reviewer located the argument at Props 38(b)
   and 40(b) and the proof of Thms 3–5, printed pp. 27–29. We could not re-open those
   pages for this packet, so this is supporting evidence, not a dependency.
3. **The bridge inequality.** Is `corank_{ℤ₅} Sel_{5^∞}(E) ≤ dim Sel₅(E) − dim E(ℚ)[5]`
   with equal parity correct, as derived in step 2 below?
4. **Normalizations.** 002 defines `Sel_{q^∞}` with the local Kummer images at every
   place. It takes `Ω_E = ∫_{E(ℝ)} |ω_E|` over all of `E(ℝ)`, and its height pairing has
   `B(P,P) = lim 4^{-n} h_x(2^n P)`. Is this the standard BSD normalization, with no
   factor 2 lost?
5. **Novelty.** Do you know of any published positive-proportion result *by height* for
   the full leading-term formula, as opposed to its rank part or its `p`-parts? The corpus
   itself claims full BSD for a density-one set of quadratic twists of every `E/ℚ`
   (families 002 and 006, per `CONTENTS.md`). That is a statement within twist
   families, not over all curves by height.

## Premises, verbatim

**P1. OpenAI family 002**, Theorem 1.1. Source:
`preprints/Exact-Birch-Swinnerton-Dyer-Formula-from-Low-Selmer-Corank-October-3-2026/exact-bsd-low-selmer-corank.pdf`, §1.1.

> For a prime p, let Sel_{p^∞}(E/Q) denote the full p-power Selmer group, defined using the
> local Kummer images at every place, and write s_p(E) = corank_{Z_p} Sel_{p^∞}(E/Q),
> a(E) = ord_{s=1} L(E,s), r(E) = rank E(Q). Here L(E,s) is the uncompleted Hasse–Weil
> L-function with all its finite Euler factors.
>
> **Theorem 1.1.** Let E/Q be an elliptic curve and let q be any prime. If s_q(E) ∈ {0,1},
> then #Sha(E/Q) < ∞, r(E) = a(E) = s_q(E), and, with r = r(E) and the preceding
> normalizations, [the leading-term formula displayed above] (1.2).
> There are no additional hypotheses on reduction, rational torsion, isogenies, complex
> multiplication, or residual Galois representations.

The normalizations, also from §1.1:

> Ω_E = ∫_{E(R)} |ω_E|, c_ℓ(E) = [E(Q_ℓ) : E_0(Q_ℓ)]. Thus the real period includes both
> connected components when there are two. … If x(P) = a/b in lowest terms, b > 0, put
> h_x(P) = log max{|a|, b} … H(P) = lim 4^{−n} h_x([2^n]P), B(P,Q) = (H(P+Q) − H(P) − H(Q))/2 …
> Reg_E = det(B(P_i, P_j)).

002 depends on two other corpus papers:

- [23], *The Selmer converse for elliptic curves at every prime* (Sept 24), which gives
  the rank and finiteness conclusions;
- [24], *The two-primary BSD formula in Selmer corank at most one* (Sept 24), which gives
  the 2-part.

002 itself proves the odd-primary part.

**P2. Bhargava–Shankar**, *The average size of the 5-Selmer group of elliptic curves is 6,
and the average rank is less than 1*, arXiv:1312.7859. From §1:

- **Thm 1:** "When elliptic curves E/Q are ordered by height, the average size of the
  5-Selmer group S₅(E) is equal to 6."
- **Thm 2:** the same holds for any family defined by finitely many congruence conditions
  on `A, B`.
- **Thm 4:** "a density of at least 83.75% have rank 0 or 1."
- **Thm 6:** a family `F` of "density greater than 55.01% among all elliptic curves" in
  which "the root number of elliptic curves in F is equidistributed."
- **§1, average-rank bound:** on `F` the extremal Selmer law is 37.5% size 1, 50% size 5
  and 12.5% size 25. The final combination is `0.5501 × 0.75 + 0.4499 × 1.05 < 0.885`.

**P3. Classical inputs.**

- **Cassels–Tate.** `Ш[p^∞]/div` carries a nondegenerate alternating pairing, so for odd
  `p` its `𝔽_p`-dimension of `p`-torsion is even.
- **`p`-parity** (T. and V. Dokchitser, *Ann. of Math.* 172 (2010)).
  `(−1)^{s_p(E)} = w(E)` for every `E/ℚ` and every prime `p`.
- **Torsion.** Curves with a rational point of order 5 have density zero by height
  (`X₁(5)` has genus 0; Harron–Snowden, *J. reine angew. Math.* 729 (2017), give the
  count `≍ X^{1/6}` against `≍ X^{5/6}` for all curves).

## The bridge, step by step

Write `d(E) = dim_{𝔽₅} Sel₅(E)`, `t(E) = d(E) − dim E(ℚ)[5]`, and `s(E) = s₅(E)`.

1. **Finite-level Kummer.** `0 → E(ℚ)/5 → Sel₅ → Ш[5] → 0` gives
   `d = r + dim E(ℚ)[5] + dim Ш[5]`. So `t = r + dim Ш[5]`.
2. **`s ≤ t`, with the same parity.** By 002's sequence (2.1), `s = r + c`, where `c` is the
   `ℤ₅`-corank of `Ш[5^∞]`. Write `Ш[5^∞] ≅ (ℚ₅/ℤ₅)^c ⊕ T` with `T` finite. Then
   `dim Ш[5] = c + dim T[5] ≥ c`, so `s ≤ t`. Also `T ≅ Ш[5^∞]/div`, so Cassels–Tate makes
   `dim T[5]` even and `t ≡ s (mod 2)`.
3. **Outside a density-zero set, `d = t`.** This uses the torsion input in P3.
4. **Parity on `F`.** By `p`-parity, `(−1)^s = w(E)`. Root numbers are equidistributed on
   `F`, so on `F` the dimension `d` is even for half the curves and odd for the other half,
   in density.
5. **Linear program on `F`.** For every integer `d ≥ 0`,
   `5^d ≥ 1 + 24·[d ≥ 2] + 4·[d odd]` (check `d = 0,1,2,3`; beyond that the left side
   only grows). Averaging over `F` gives `6 ≥ 1 + 24·P(d ≥ 2) + 4·½`, so `P_F(d ≤ 1) ≥ 7/8`.
   The bound is tight: Bhargava–Shankar's §1 law (3/8, 1/2, 1/8 on `d = 0, 1, 2`) attains it.
6. **Linear program on the complement.** `5^d ≥ 1 + 24·[d ≥ 2]` gives
   `P(d ≤ 1) ≥ 19/24`. The law (19/24, 5/24 on `d = 0, 2`) attains it.
7. **Combine.** `0.5501·7/8 + 0.4499·19/24 = 100501/120000 > 0.8375`. Because
   `7/8 > 19/24`, a larger density for `F` only helps.
8. **Apply 002 at `q = 5`.** On this set, `s ≤ t = d ≤ 1`, so `s₅(E) ∈ {0,1}`. Theorem 1.1
   then gives the full formula, with `Ш` finite and `r = ord_{s=1} L(E,s)`.

## How it could fail, most likely first

1. **002 is wrong.** This is the premise, an unrefereed OpenAI preprint that also leans on
   corpus papers [23] and [24]. If 002 falls, NT-9 falls with it. Nothing here tests 002.
2. **The complement averaging (Q1) needs more than Bhargava–Shankar prove.** We consider
   this unlikely, since their own 0.885, 83.75% and 20.62% figures use the same split.
3. **Bhargava–Shankar is itself wrong.** It is an arXiv preprint (2013) whose method is
   widely used. We treat it as a premise, not as classical.
4. **A normalization mismatch (Q4).** This would affect the formula's constant, not the
   density.

## Reproduce

```sh
python3 scripts/review/nt9_density.py
```

Expected output:

```
P(dim Sel5 <= 1) on the equidistributed family F >= 7/8  (tight: d=0: 3/8, d=1: 1/2, d=2: 1/8)
P(dim Sel5 <= 1) on the complement of F          >= 19/24  (tight: d=0: 19/24, d=2: 5/24)
combined lower density = 0.5501*7/8 + 0.4499*19/24 = 100501/120000 = 0.83750833
OK: lower density > 0.8375 with 5-Selmer dimension <= 1.
corroboration: P(dim Sel5 = 0) >= 0.5501*3/8 = 0.20629, Bhargava-Shankar's 20.62% (Thm 5)
Bridge: corank Sel_{5^oo} <= dim Sel_5 - dim E(Q)[5] <= dim Sel_5, so these curves
satisfy s_5(E) in {0,1}, the hypothesis of family 002's Theorem 1.1 at q = 5.
```

The script works in exact rationals. It checks the dual certificates for `d ≤ 60`; for
`d ≥ 3` the left side is at least 125 and only grows, while the right side is constant,
so this covers every `d`. It also checks that the two extremal laws have mean exactly 6.

## Status

- **Formal.** Not formalized. Mathlib has no Selmer groups or BSD, and OpenAI's Lean
  project has no formalization of 002 (its `formalization.yaml` has no entry for it).
- **Literature.** Bhargava–Skinner–Zhang (2014) give 66.48% for the rank part with finite
  Ш. Full-formula results that we know of are curve-by-curve or `p`-part-by-`p`-part. We
  found no positive-proportion statement for the full formula.
- **What changes if a reviewer confirms Q1 and Q3.** NT-9 becomes "conditional on 002 and
  on Bhargava–Shankar", with every other step classical.
