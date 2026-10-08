# TC-4 · Directed APSP with small integer weights in `O(n^2.5082)` — review packet

**Reviewer profile:** fast matrix multiplication (rectangular exponents) or fine-grained
complexity. **Time:** 30–60 minutes.
**Catalogue entry:** [TC-4](../COROLLARIES.md#tc-4).
**Tier:** D (complete written derivation; not formalized).

## The claim

*Assume* OpenAI family 107's rectangular bounds `α > 0.465` and `ω(1, 0.709, 1) < 2.092`
in characteristic zero.

All-pairs shortest paths in a **directed** graph on `n` vertices with integer edge weights
in `{−M, …, M}`, `M = O(1)`, and no negative cycles, can then be solved in
`Õ(n^{2+μ*}) ⊂ O(n^{2.5082})`, where

```
μ* = 10061/19800 = 0.5081313…
```

The best previously published exponent we found is `2 + 0.5275` (Alman, Duan,
Vassilevska Williams, Xu, Xu, Zhou, arXiv:2404.16349, SODA 2025).

## Questions for you

1. **Zwick's theorem.** Does Zwick's algorithm (*JACM* 49 (2002) 289–317; arXiv:cs/0008011)
   run in `Õ(n^{2+μ})` for every `μ` with `ω(1,μ,1) ≤ 1 + 2μ`, when `M = O(1)`? His
   abstract says "Õ(n^{2+μ}) time, where μ satisfies the equation ω(1, μ, 1) = 1 + 2μ".
2. **Convexity.** We use convexity of `k ↦ ω(1,k,1)` on `[0.465, 0.709]` (Lotti–Romani;
   107 §2). Do you agree it applies here?
3. **The computational model.** 107's bounds are in the arithmetic-operation model, which
   excludes coefficient bit size. Its Cors 14.1–14.2 move them to every field of
   characteristic zero by realizing the schemes over a number field. Zwick's distance
   products run the algebraic algorithm on integer encodings of about `M·log n` bits. Is
   the usual passage from arithmetic count to bit complexity sound here, with fixed
   rational constants for each fixed `ε`, as for every other `ω`-based bound?
4. **Novelty.** Is any published `μ` below `0.5275`? Dupont et al. (arXiv:2608.16884)
   improve only the square `ω`.
5. **A possible improvement (lead).** 107 §12.2 derives a one-parameter curve (eq. 12.12)
   but records only its `t = 2/3` point. If (12.12) holds for every `t > 0`, the curve
   meets Zwick's line at `μ ≈ 0.50339`, giving `O(n^{2.5035})`. Is (12.12) valid at
   `t ≈ 0.2128` over ℂ? If so, does the classical field invariance of rectangular exponents
   (Schönhage) carry it to ℚ without repeating 107's descent?

## Premises, verbatim

**P1. OpenAI family 107.** *Complex Matrix Multiplication Below 2.258 and Rectangular
Bounds*. Source:
`preprints/Complex-Matrix-Multiplication-Below-2.258-and-Rectangular-Bounds-September-24-2026/…pdf`.

> **Abstract.** Over every field of characteristic zero, we prove that the square
> matrix-multiplication exponent satisfies ω < 2.258, the dual exponent satisfies α > 0.465,
> and ω(1, 0.709, 1) < 2.092.
>
> **Theorem 1.1.** Over C, the arithmetic matrix-multiplication exponents satisfy
> ω < 1129/500 = 2.258, α > 0.465, w(0.709) < 2.092.
>
> **Corollary 14.1** (Finite-exception field bounds). There is a finite set S of positive
> primes such that, for every field F with char F = 0 or char F = p ∉ S, ω_F < 1129/500
> [and w_F(709/1000) < 523/250].
>
> **Corollary 14.2** (Characteristic-zero dual bound). For every field F of characteristic
> zero, α_F > 0.465.
>
> §2: "The properties in Theorem 2.1 imply that w is convex."

Here `w(k) = ω(1,k,1)`, and `α = sup{k : w(k) = 2}`, so `α > 0.465` gives `w(0.465) = 2`.

The 2.258 paper is family 107's *secondary* write-up. The family's headline result is
`ω ≤ 9/4` over ℂ (*An Upper Bound of 9/4 for the Matrix Multiplication Exponent*,
Oct 2), and that paper gives no rectangular bounds. The square bound does not help here:
a chord through `(0.465, 2)` and `(1, 9/4)` gives only `μ < 0.5107`.

**OpenAI's formalization.** OpenAI's Lean project proves the ℂ versions:
`OAI.MatrixMultiplication.complex_alpha_gt_93_div_200` and
`OAI.MatrixMultiplication.complex_rectangular_omega_lt_523_div_250`, in
`lean/OAI/LinearAlgebra/MatrixMultiplication/Main.lean` (with
`complex_omega_le_nine_quarters`), against the comparator
`lean/ComparatorChallenges/MatrixMultiplication.lean`. The comparator's model is finite
division-free straight-line programs over ℂ with arbitrary constants. Note that
93/200 = 0.465 and 523/250 = 2.092. We have **not** rebuilt that proof here: it needs
external dependencies beyond Mathlib. The transfer to ℚ (Cors 14.1–14.2) is paper-only.

**P2. Zwick**, *All pairs shortest paths using bridging sets and rectangular matrix
multiplication*, *JACM* 49(3) (2002). From the abstract: the first algorithm handles graphs
whose "edge weights are integers of small absolute value" in "Õ(n^{2+μ}) time, where μ
satisfies the equation ω(1, μ, 1) = 1 + 2μ".

## The bridge, step by step

1. **Two points on the curve.** `w(0.465) = 2` (from `α > 0.465` and monotonicity) and
   `w(0.709) < 523/250`.
2. **Chord.** By convexity, for `0.465 ≤ μ ≤ 0.709`:
   `w(μ) ≤ 2 + (23/61)(μ − 0.465)`, strictly for `μ > 0.465`. The slope is
   `(523/250 − 2)/(0.709 − 0.465) = 0.092/0.244 = 23/61`.
3. **Crossing.** The chord meets `1 + 2μ` at `μ* = (1 − (23/61)·0.465)/(2 − 23/61) = 10061/19800`,
   which lies inside `[0.465, 0.709]`. So `w(μ*) < 1 + 2μ*`.
4. **Zwick.** `w(μ) − 2μ` is strictly decreasing, since padding gives
   `w(μ′) ≤ w(μ) + (μ′ − μ)`. So Zwick's `μ` is at most `μ*`, and the running time is
   `Õ(n^{2+μ*}) ⊂ O(n^{2.5082})`.

## How it could fail, most likely first

1. **107's rectangular bounds are wrong.** OpenAI's Lean formalization over ℂ makes this
   less likely; we did not rebuild it.
2. **The arithmetic-to-word-RAM passage (Q3) has a subtlety** specific to 107's
   accuracy-dependent number fields (Cor 14.2 picks a field `K_ε` for each `ε`). We
   expect the standard argument to apply: constants are fixed for each fixed `ε`.
3. **The result is already published (Q4).** That would affect novelty only.
4. **Misreading Zwick's `M`-dependence (Q1).** Irrelevant for `M = O(1)`.

For **undirected** graphs this is not an improvement: Shoshan–Zwick's `Õ(M n^ω)` is
already better.

## Reproduce

```sh
python3 scripts/review/tc4_apsp.py
```

Expected output:

```
slope = 23/61  (expected 23/61)
mu*   = 10061/19800 = 0.5081313  (expected 10061/19800)
APSP exponent 2 + mu* = 2.5081313 < 2.5082
previous best published mu < 0.5275: improvement 0.01937
OK
LEAD (not a result): (12.12) at t = 0.212797 gives w(0.503389) <= 2.006778 = 1 + 2*mu, i.e. mu < 0.50346 if (12.12) holds at that t
```

The main computation uses exact rationals. The lead uses 30-digit mpmath and also checks
that the curve reproduces 107's recorded point (`k > 0.709`, `w < 2.092` at `t = 2/3`).

## Status

- **Formal.** The bridge is not formalized. It would need convexity of `rectangularOmega`
  from OpenAI's program model, which is a substantial development.
- **Literature.** ADVXXZ (2404.16349) give `μ < 0.5275`. 107 cites an updated table with
  `ω(1, 0.5, 1) ≤ 2.042776` and `ω(1, 0.6, 1) ≤ 2.092351`; a chord through those gives
  only `μ < 0.5285`.
