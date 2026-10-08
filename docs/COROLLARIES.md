# Cross-family corollaries of openai/math

Source corpus: [`openai/math@adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a), 722 manuscripts in 372 families.
**Every corpus result is treated as a claim by OpenAI.** Every corollary below is conditional on the claims it cites.

"Unstated" means we grepped `CONTENTS.md`, `overview.tex`, the cited papers' text and `.tex` sources, and the Lean docs, and found nothing. It does **not** mean the result is new to the wider literature. Several items are already known once you grant the corpus input, and we say so where we know it.

## Evidence tiers

| Tier | Meaning | Count |
|---|---|---|
| **L** | **Lean-checked conditional implication.** Proved in Lean in this repo (`Corollaries/`, `Fidelity/`), taking OpenAI's comparator statement as an explicit hypothesis. The kernel checks that hypothesis is exactly OpenAI's type. Two independent audits (`#assert_standard_axioms` in Lean, and `scripts/check_axioms.py`) accept only `propext`, `Classical.choice` and `Quot.sound`. OpenAI's own proofs are **not** checked here: the vendored comparator files contain `sorry`, and the audited corollaries do not depend on them. | 7 |
| **D** | **Complete written derivation.** Premises are quoted from the corpus with their source. Every other step is either elementary and written out, or a cited classical theorem with its exact statement. Not formalized. | 4 |
| **Lead** | **Research lead.** A precise candidate statement plus a bridge sketch. Premises, citations or hypotheses have not been fully checked. Not a result. | 27 |

So the 38 entries are 7 verified conditional implications, 4 complete derivations and 27 leads.

---

## Number theory

### NT-1 · The Landau–Siegel paper is a corollary of the 7/8 paper · **L**
- **Statement.** `DirichletSevenEighths` implies OpenAI's `SiegelZeros` comparator in both of its forms, with explicit `c = log 3 / 8`. It also gives the stronger uniform gap: every real zero of every nontrivial Dirichlet `L`-function, of any modulus, satisfies `β ≤ 7/8`. No primitivity or reality is assumed.
- **Lean.** `Corollaries.real_zero_le_seven_eighths`, `Corollaries.siegel_of_sevenEighths`, `Fidelity.siegel_comparator_of_sevenEighths` and `Fidelity.siegel_comparator'_of_sevenEighths`.
- **Why it matters.** "Uniform exclusion of Landau–Siegel zeros" (Oct 1) has its own interpolation-determinant proof, does not cite the Sept 30 7/8 paper, and its Lean doc says "no explicit value of c is given". Granting the 7/8 statement, the Siegel statement adds nothing logically. This checks an implication between two claims; it does not verify the 7/8 theorem. The Oct 1 paper keeps independent value: its proof does not go through the 7/8 paper, so it would still stand if the 7/8 proof turned out to be flawed.

### NT-2 · The zeta comparator is the modulus-1 case · **L**
- **Statement.** `DirichletSevenEighths` implies `QuasiRiemannHypothesis.lean` (ζ(s) ≠ 0 for Re s > 7/8).
- **Lean.** `Corollaries.zeta_of_sevenEighths`, `Fidelity.zeta_comparator_of_sevenEighths`.

### NT-3 · A third, independent route to Siegel · **Lead**
- **Statement.** Theorem 1.2 of family 029 gives Hecke L-functions over cyclotomic `F ⊇ μ₁₂` no zeros in `Re s > 1 − 10⁻⁶`. Factoring over `Q(μ₁₂q)` (Artin formalism) makes every Dirichlet `L`-function zero-free there. So the Siegel comparator also holds with `c = 10⁻⁶·log 3`, independently of family 003.
- **Further consequence.** Via Kronecker–Weber and Aramata–Brauer, `ζ_K(s) ≠ 0` for `Re s > 1 − 10⁻⁶` uniformly, for every number field with metabelian Galois closure.
- **Unstated.** The Artin paper descends only to its Kummer fields (§9.1).

### NT-4 · Least primitive root `g(p) = p^{o(1)}`, effectively · **Lead**
- **Statement.** The 7/8 half-plane gives the following via character detection, the explicit formula (error `x^{7/8}`) and `2^{ω(p−1)} = p^{o(1)}`.
  - `g(p) ≤ exp(C log p / log log p)`.
  - The best unconditional bound in the literature is about `p^{1/4+ε}` (Burgess).
- **Unstated.** The 7/8 paper derives least quadratic nonresidues and deterministic square roots, but not primitive roots.

### NT-5 · 7/8 for Dedekind zeta of pure cubic fields · **Lead**
- **Statement.** `ζ_{Q(∛m)} = ζ · L_F(s, χ)` with `F = Q(√−3)` and `χ` cubic. Combined with OpenAI's `HeckeSevenEighths`, this gives no zeros in `Re s > 7/8`. Consequences:
  - effective Brauer–Siegel for these fields;
  - Chebotarev in `Q(ζ₃, ∛m)` with error `x^{7/8+ε}`.
- **Unchecked.** That the comparator's `Character` structure covers all ray-class characters is OpenAI's claim, not checked here.

### NT-6 · Full-reptend primes and irreducible all-one polynomials over 𝔽₂ · **D**
- **Premise (corpus).** Family 029 (`CONTENTS.md`, "Primitive roots for every admissible integer base"): for every integer `a` that is neither `−1` nor a square, at least `c_a x/(log x)²` primes in every sufficiently large interval `(x, 2x)` have primitive root `a`, with `c_a > 0`.
- **Statement.** For all large `x`, at least `c x/(log x)²` primes `p ∈ (x, 2x)` satisfy each of:
  - (a) the decimal expansion of `1/p` has period exactly `p − 1` (take `a = 10`);
  - (b) `Φ_p(X) = 1 + X + … + X^{p−1}` is irreducible over `𝔽₂`, so `𝔽_{2^{p−1}}` has a type-I optimal normal basis over `𝔽₂` (take `a = 2`).
- **Derivation.**
  1. `10` and `2` are neither `−1` nor squares, so the premise applies to both. For large `x`, the primes `2` and `5` lie outside `(x, 2x)`.
  2. (a), elementary. For a prime `p ∤ 10`, `1/p = m/(10^k − 1)` for an integer `m` exactly when `p | 10^k − 1`. So the expansion is purely periodic, and its minimal period is the least such `k`, which is `ord_p(10)`. It equals `p − 1` iff `10` is a primitive root mod `p`.
  3. (b), classical. Over `𝔽_q` with `p ∤ q`, `Φ_p` factors into `(p−1)/d` distinct irreducibles of degree `d = ord_p(q)` (Lidl–Niederreiter, *Finite Fields*, Thm 2.47(ii)). With `q = 2`, `Φ_p` is irreducible iff `ord_p(2) = p − 1`. That condition (with `p` prime) is exactly the existence criterion for a type-I optimal normal basis of `𝔽_{2^{p−1}}` (Mullin–Onyszchuk–Vanstone–Wilson, *Discrete Appl. Math.* 22 (1988/89)).
- **Unstated.** Family 029 states the general base-`a` result, and neither application appears in the corpus.

### NT-7 · Liouville sign agreement has density 1/2 · **L**
- **Statement.** Assuming family 007's `liouville_log_saving`, there is `c > 0` such that for all `a₁, a₂ > 0` with `a₁b₂ ≠ a₂b₁` there is `C > 0` with

  `|#{1 ≤ n ≤ ⌊X⌋ : λ(a₁n+b₁) = λ(a₂n+b₂)} − ⌊X⌋/2| ≤ C·X/(log X)^c` for all `X ≥ 3`.

  By `liouville_eq_iff_parity`, `λ(m) = λ(m′)` iff `Ω(m)` and `Ω(m′)` have the same parity. For example, `Ω(n)` and `Ω(n+1)` agree in parity for half of all `n`.
- **Lean.** `Fidelity.liouville_agreement_density`, `Fidelity.liouville_eq_iff_parity`.

### NT-8 · Sums of two rational cubes: at least 47.92% of integers · **Lead**
- **Statement.** Koymans–Smith (arXiv:2405.09311, Cor 1.8) assume "`r₃ = 1` ⇒ rank 1". Family 002's Selmer `p`-converse at `p = 3`, via Cassels–Tate parity, supplies that assumption.
- **Unchecked.** Their normalisations, and `dim E′(ℚ)[3] = 1` for every `n`.

### NT-9 · BSD for at least 83.75% of elliptic curves ordered by height · **Lead**
- **Statement.** Family 002's corank-≤1 converse would upgrade Bhargava–Shankar's 83.75% to the full BSD formula. The best previous proportion is 66% (Bhargava–Skinner–Zhang).
- **Narrowed (external review).** Bhargava–Shankar reach 83.75% through the proportion of curves with 5-Selmer rank 0 or 1. Since `corank_{ℤ₅} Sel_{5^∞}(E) ≤ dim_{𝔽₅} Sel₅(E)`, those curves have 5^∞-Selmer corank ≤ 1. That is the hypothesis of 002's statement with `q = 5`.
- **Remaining check.** The exact hypotheses and conclusion of 002's converse at `q = 5`: whether it really gives the full leading-term formula there, with no extra local conditions.

### NT-10 · Congruent numbers · **Lead** (known in the literature given the corpus input)
Smith's corank results plus the corpus 2-converse give the following:
- 100% of squarefree `n ≡ 5, 6, 7 (mod 8)` are congruent;
- 100% of `n ≡ 1, 2, 3 (mod 8)` are not;
- the full BSD formula holds for 100% of the curves `E_n`.

This matches Kriz + Smith in the literature, and the corpus does not state it.

### What the 7/8 half-plane does **not** improve
Primes in short intervals (Guth–Maynard `x^{17/30}`, Baker–Harman–Pintz 0.525), Bombieri–Vinogradov level, twin primes, Goldbach and Chen all stay where they are. A half-plane at 7/8 is far weaker than a density hypothesis.

**Effectivity audit.** Five families invoke ineffective Siegel–Walfisz: 011, 012, 013, 021 and 029. Those inputs become effective. None of their headline results becomes effective, for other reasons stated in each paper.

### Already in the corpus (so not listed above)
- The 11/12 paper already states an effective class-number bound `h(D) ≫ √|D| / log log |D|` and the completeness of Euler's 65 idoneal numbers.
- The 7/8 paper already states a polylog least-nonresidue bound and deterministic square roots mod `p`.

---

## Diophantine approximation

### DA-1 · `rπ + s` is not `LiouvilleWith p` for `p > 2`; `π` is not Liouville · **L**
- **Statement.** For `r, s ∈ ℚ` with `r ≠ 0` and every `p > 2`, `¬ LiouvilleWith p (π·r + s)`, and `¬ Liouville π`.
- **Lean.** `Corollaries.pi_not_liouvilleWith`, `Corollaries.rat_affine_pi_not_liouvilleWith`, `Corollaries.pi_not_liouville`.
- **Scope.** This is the upper-bound side: irrationality exponent `≤ 2`. The matching lower bound (`≥ 2`, Dirichlet's theorem, true for every irrational) is not formalized here, so `μ(rπ + s) = 2` is not claimed as a Lean theorem.
- "Not Liouville" was already known from Mahler (1953). The `p > 2` statements for `rπ + s` are consequences of the corpus claim.

### DA-2 · The Cookson Hills series converges · **Lead**
- **Statement.** `Σ sec²(n)/n³ < ∞`. More generally, `Σ n^{-a}|cos n|^{-b}` and `Σ n^{-a}|sin(rn)|^{-b}` converge iff `a > max{1, b}`.
- **Bridge.** `|cos n| ≥ ‖(2k+1)π‖/π` for the nearest half-integer multiple, then the paper's own dyadic spacing lemma.
- **Divergence for cos.** Uses Minkowski's inhomogeneous theorem.
- **Unstated.** `grep -i cookson` over the whole repo returns nothing.

### DA-3 · Discrepancy `O(N^{−1+ε})` for `n mod 2π` · **Lead**
- **Statement.** Exponent 2 means type 1, so Kuipers–Niederreiter Thm 2.3.2 and Koksma's inequality give, for example:
  - `Σ_{n≤N} sgn(sin n) = O(N^ε)`;
  - `Σ_{n≤N} |sin n| = (2/π)N + O(N^ε)`.
- **Previous bound.** The exponent bound 7.11 gave only about `N^{−0.16}`.

---

## Group rings and operator algebras

### GR-1 · Kaplansky's counterexample survives every field extension · **L**
- **Statement.** For every ring map `K →+* L` out of OpenAI's finite field, `L[G]` is not directly finite. In particular this holds for `L = 𝔽̄₂`.
- **Lean.** `Corollaries.directFiniteness_transfer`, `Fidelity.kaplansky_transfer`.
- **Extension (Lead).** Stable finiteness fails over *every* characteristic-2 field, including `𝔽₂` and `𝔽₂(t)`, via `m × m` matrices with `m = [K:𝔽₂]`. The same group is stably finite over every characteristic-0 field.

### GR-2 · The torsion-free counterexample also breaks the idempotent conjecture in characteristic 2 · **D** (ring step **L**)
- **Premise (corpus).** "A Torsion-Free Group Algebra That Is Not Directly Finite" (family 197, Oct 4), Theorem 1.1: there exist a finitely presented torsion-free group `G` and `a, b, c ∈ 𝔽₂[G]` with `ab = 1`, `ac = 0`, `c ≠ 0`. Moreover `G` admits a finite two-dimensional classifying complex.
- **Statement.** For that `G`:
  - (i) `e = ba` is an idempotent of `𝔽₂[G]` other than 0 and 1. So Kaplansky's idempotent conjecture fails for torsion-free groups over `𝔽₂` (and over every field containing `𝔽₂`, since `𝔽₂[G] ⊆ L[G]`).
  - (ii) `a ≠ 0` and `ac = 0`, so `𝔽₂[G]` has zero divisors. With the premise's topology, this is the full headline of family 196: a finitely presented torsion-free group with a finite 2-dimensional classifying complex and zero divisors in `𝔽₂[G]`.
  - (iii) Family 207 proves the idempotent conjecture for torsion-free groups over every commutative unital characteristic-0 domain. By (i), the characteristic-0 hypothesis cannot be dropped.
- **Derivation.** (i) and (ii) are the ring identities `e² = b(ab)a = e`, `e ≠ 1` (else `c = (ba)c = b(ac) = 0`), `e ≠ 0` (else `1 = (ab)(ab) = a(ba)b = 0`) and `a ≠ 0`. All four are proved in Lean for any ring (`Corollaries.idempotent_of_directFiniteness_witness`). (iii) is immediate from (i) and 207's statement.
- **Note.** This is a logical implication, not independence: the Oct 4 paper says it adapts the construction of the 196 paper.
- **Lead (not covered above).** An injective, non-surjective cellular automaton on this torsion-free group, against Gottschalk; this needs the standard group-ring/automaton dictionary.

### GR-3 · Family 196's group is not left-orderable · **L**
- **Statement.** It is not left-orderable.
- **Lean.** `Fidelity.zeroDivisor_group_not_leftOrderable`, via Mathlib's `UniqueProds ⇒ NoZeroDivisors`.
- **Classical consequences (Lead).** Not locally indicable (Burns–Hale), not bi-orderable, and not a subgroup of any right-angled Artin group.

### GR-4 · Kadison–Kaplansky counterexample vs ℓ¹: consistent · **Lead**
- **Statement.** Family 207's ℓ¹-Bass theorem gives integer traces on `K₀(ℓ¹(G))` for torsion-free `G`, so `ℓ¹(G)` has no idempotents other than 0 and 1. Family 285's projection, with trace in `(0, ½)`, therefore lies outside the image of `K₀(ℓ¹ G) → K₀(C*_r G)`.
- **Tension check.** We found no contradiction between 285 and 207. The failure sits in the ℓ¹ → C*_r comparison.

### GR-5 · Thompson's groups `F` and `T` are C*-simple · **Lead**
- **Statement.** Family 248 (F is nonamenable) plus Le Boudec–Matte Bon (2018) give that both are C*-simple with unique trace.

### GR-6 · `L(F₂)` realizes every subfactor standard invariant · **Lead**
- **Statement.** Family 287 (`L(F_∞) ≅ L(F₂)`) plus Popa–Shlyakhtenko (2003) give that every standard invariant is realized in `L(F₂)`. Also `L(F₂) ≅ L(F₂) * L(F₂)`.

### GR-7 · Connes–Shlyakhtenko L²-Betti numbers of `L(F_r)` are 0 or ∞ · **Lead**
- **Statement.** Fundamental group `ℝ>0` (family 287), with the compression formula `β_k(pMp) = β_k(M)/τ(p)²`, forces `β_k ∈ {0, ∞}`. This refutes the heuristic `β₁(L(F_n)) = n − 1`.

### GR-8 · Haagerup–Størmer for all separable type III₁ factors · **Lead**
- **Statement.** Family 290 (trivial bicentralizer) plus Marrakchi (arXiv:2309.05279, Cor B) give this.

### GR-9 · Artin groups: unconditional invariants · **Lead**
- **Statement.** Family 254 (`K(π,1)` for all finite-rank Artin groups) discharges the hypothesis of Davis–Okun and related results. This gives:
  - L²-Betti numbers;
  - `χ(A) = Σ_{T spherical} (−1)^{|T|}`;
  - `cd A = max{|T| : W_T finite}` (least checked of the three).

### GR-10 · The nonsofic group and Aldous–Lyons · **Lead**
- **Follows.** Family 197's group gives an explicit finitely presented counterexample to the marked-network Aldous–Lyons conjecture.
- **Does not follow.** Whether the group is hyperlinear. Its direct-finiteness failure in characteristic 2 says nothing over ℂ.

---

## Algebraic geometry

### AG-1 · Tate for products of curves over finite fields, and all four standard conjectures for abelian varieties · **Lead**
- **Statement.**
  - Family 032's Tate result, through Künneth motives of curves, gives Tate and `num = hom` for products of curves.
  - Tate's 1994 Thm 2.9 then gives the zeta pole-order form.
  - With the classical B and C, all four standard conjectures hold for abelian varieties.

### AG-2 · Hodge for Hilbert schemes of points on any K3 · **Lead**
- **Statement.** Family 032 (products of K3s) plus de Cataldo–Migliorini's motivic decomposition of `S^{[n]}` give the Hodge conjecture for `S^{[n]}` and their products.

### AG-3 · Compact Kähler log abundance is unconditional inside the corpus · **Lead**
- **Statement.** Assumption 1.1 of family 034's Kähler paper is word for word Corollary `spec:logarithmic` of family 033. Family 033's title and abstract still call it conditional. Two Kähler-fourfold papers are subsumed as main theorems, though they remain lemma inputs.
- **Circularity.** None found.

### AG-4 · Three projective MMP papers are special cases · **Lead**
- **Statement.** The fourfold nonvanishing and "lifting sections" papers (and probably the numerical-dimension-one paper) are special cases of "Log abundance in characteristic zero".

### AG-5 · Effective log Iitaka in every dimension · **Lead**
- **Statement.** It follows by combining the `d ≥ 5` paper, the `d = 4` paper and Chen–Han–Liu (`d ≤ 3`).

---

## Analysis, geometry and physics

### GE-1 · Bourgain–Milman with the optimal dimension-free constant (symmetric case) · **D**
- **Premise (corpus).** `ComparatorChallenges/MahlerConjecture.lean`, `OAI.SymmetricMahler.symmetric_mahler`: for `n ≥ 1` and compact convex `K ⊂ ℝⁿ`, symmetric with nonempty interior, `vol(K)·vol(K°) ≥ 4ⁿ/n!` (Lebesgue volume, coordinate polar `K° = {p : ⟨p, v⟩ ≤ 1 ∀ v ∈ K}`).
- **Statement.** Under the premise, `vol(K)·vol(K°) ≥ 2ⁿ/Γ(n/2+1)² = (2/π)ⁿ κₙ²`, where `κₙ = π^{n/2}/Γ(n/2+1)` is the volume of the Euclidean unit ball. The base `2/π` is optimal: no `c > 2/π` gives `vol(K)vol(K°) ≥ cⁿκₙ²` for all `n`.
- **Derivation.**
  1. By the premise, it suffices that `n! ≤ 2ⁿ Γ(n/2+1)²`.
  2. Legendre duplication `Γ(z)Γ(z+½) = 2^{1−2z}√π Γ(2z)` at `z = (n+1)/2` gives `n! = 2ⁿ Γ((n+1)/2) Γ(n/2+1)/√π`. So step 1 is equivalent to `Γ(x) ≤ √π Γ(x+½)` at `x = (n+1)/2 ≥ 1`.
  3. `log Γ` is convex (Bohr–Mollerup), so `x ↦ log Γ(x+½) − log Γ(x)` is nondecreasing. At `x = 1` it equals `log(√π/2)`. Hence `Γ(x) ≤ (2/√π)Γ(x+½) ≤ √π Γ(x+½)` for `x ≥ 1`, since `2/√π ≈ 1.128 < √π ≈ 1.772`.
  4. Optimality: the cube `[−1,1]ⁿ` has `vol·vol(polar) = 2ⁿ·2ⁿ/n! = 4ⁿ/n!`. By Stirling, `(4ⁿ/n!)/((2/π)ⁿκₙ²) = 2ⁿΓ(n/2+1)²/n! ~ √(πn/2)`, whose `n`-th root tends to `1`. So for `c > 2/π` the cube violates the bound for large `n`. Numerical check: the ratio is `1.571, 2.000, 4.063, 17.75` at `n = 1, 2, 10, 200`, against `√(πn/2) = 1.253, 1.772, 3.963, 17.72`.
- **In the corpus.** Bourgain–Milman appears only as history.
- **Lead (general bodies).** The analogue `(e/2π)ⁿκₙ²` from `GeneralMahler.lean` via `eⁿ n! ≤ (n+1)^{n+1}` has not been written out against that comparator's exact statement.

### GE-2 · Lattice transference `λ₁(K)λ₁(K°) ≤ (n!)^{1/n} ≈ n/e` · **Lead** (Lean target)
- **Statement.** Mahler plus Minkowski's first theorem (in Mathlib) give this. The trivial bound is `(n!)^{2/n}`.

### GE-3 · Symplectic ball rigidity · **Lead**
- **Statement.** If `int K × int K°` embeds symplectically in `B(4)`, then `K` is a linear Hanner body (Liouville volume plus Mahler's equality case).
- **In the corpus.** The symplectic paper explicitly makes no equality-case claim.

### GE-4 · Isotropic constant `L_K < 1/e` in every dimension, and `1/e` is sharp · **D**
- **Premise (corpus).** "A sharp entropy bound and the simplex inequality for isotropic constants" (family 101, Oct 5), Theorem 1.1, with `L_K = (det Σ_K / |K|²)^{1/(2n)}` as in its (1.1): every convex body `K ⊂ ℝⁿ` satisfies `L_K ≤ b(n) := (n!)^{1/n} / ((n+1)^{(n+1)/(2n)} √(n+2))`, with equality iff `K` is a simplex.
- **Statement.** Under the premise, `L_K < 1/e` for every convex body in every dimension, and `sup_n b(n) = 1/e`, approached by simplices and never attained.
- **Derivation.**
  1. `b(n)^{2n} = (n!)² / ((n+1)^{n+1}(n+2)ⁿ)`.
  2. Elementary bounds:
     - `n! ≤ e·n^{n+½}e^{−n}`: the trapezoid rule underestimates the integral of the concave `log`, so `log n! ≤ (n+½)log n − n + 1`.
     - `(n+1)^{n+1} > e·n^{n+1}`, since `(1+1/n)^{n+1} > e`.
     - `(n+2)ⁿ ≥ 3nⁿ`, by Bernoulli's inequality.
  3. Hence `b(n)^{2n} < e²n^{2n+1}e^{−2n} / (3e·n^{2n+1}) = (e/3)e^{−2n} < e^{−2n}`, so `b(n) < 1/e`.
  4. Stirling gives `b(n) → 1/e`. Numerically, `n·log(e·b(n)) → −0.581` (`b(1) = 0.2887`, `b(10) = 0.3496`, `b(10⁶) = 0.36788`).
- **Unstated.** Family 101's manuscript gives no dimension-free value.

### GE-5 · Sharp functional isotropic constant · **Lead**
- **Statement.** `‖f‖∞² det Cov f ≤ 1` for log-concave densities. It follows from family 101 and Bobkov–Madiman.

### GE-6 · Aubin's sharp Sobolev conjecture on Cartan–Hadamard manifolds · **Lead**
- **Statement.** Family 337 (κ = 0) plus Pólya–Szegő and Aubin–Talenti give it.

### GE-7 · Falconer for analytic (Borel) sets · **Lead**
- **Statement.** Family 073 is stated for compact sets. Davies–Howroyd compact-subset approximation extends it to analytic sets.

### GE-8 · Scalar Hénon–Lane–Emden Liouville theorem · **L**
- **Statement.** Assuming family 370's `main_nonexistence` (for the system), for `n ≥ 2`, `p > 0` and `n − 2 < 2(n + A)/(p + 1)` there is no positive continuous `u`, `C²` on `ℝⁿ ∖ {0}`, with `−Δu = |x|^A u^p` there. For `A = 0` this is the Gidas–Spruck range `p < (n+2)/(n−2)`.
- **Lean.** `Fidelity.scalar_henon_nonexistence` (set `v = u`, `q = p`, `B = A`).

### GE-9 · Lieb–Thirring near-sharp constants in all dimensions · **Lead**
- **Statement.** Family 262's matrix constant plus Laptev–Weidl lifting give the near-sharp constants, assuming an operator-valued extension of 262 that we have not checked.

### GE-10 · Pure-loss trade-off regions become unconditional · **Lead**
- **Statement.** Family 273's entropy photon-number inequality would make the Wilde–Hayden–Guha regions unconditional, if their conjecture is the same statement.

---

## Tensions checked

We found **no** internal contradictions. Pairs checked:
- the nesting 7/8 ⊂ 11/12 ⊂ `1 − 10⁻⁶`;
- 196/197 (characteristic 2) vs 207 (characteristic 0) vs 285 (C*_r);
- 197's nonsofic group vs Elek–Szabó;
- 046 vs 057;
- 195 vs 193/194;
- 234 vs SK/Parisi (identity predicted, not yet computed);
- Petty / Zhang–Santaló bounds vs family 088's witnesses at n = 20.

## Coverage and review

An external review of commit `77ab999` found four problems. All are fixed in this version:
- the axiom checker matched counts, not names, and could miss Lean errors;
- the `W` tier overstated sketches;
- the animation omitted conditionality;
- the π statement claimed the equality `μ = 2` but proved only the upper bound.

The review also narrowed NT-9.


Fully mined: number theory, algebraic and complex geometry, algebra, analysis, PDE, mathematical physics, group theory, operator algebras, topology, dynamics, differential and convex geometry, probability. That is 289 of 372 families.

**Not yet mined:** theoretical computer science, combinatorics and logic (83 families). The mining pass for that shard was cut off by a session limit.
