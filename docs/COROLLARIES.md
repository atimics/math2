# Cross-family corollaries of openai/math

Source corpus: [`openai/math@adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a), 722 manuscripts in 372 families. All 372 families have now been mined.

**Every corpus result is treated as a claim by OpenAI.** Every entry below is conditional on the claims it cites.

"Unstated" means we grepped `CONTENTS.md`, `overview.tex`, the cited papers' text and `.tex` sources, and the Lean docs, and found nothing. It does **not** mean the result is new to the wider literature. Entries that are already known once the corpus input is granted say so.

<a id="evidence-tiers"></a>

## Evidence tiers and review status

| Tier | Meaning |
|---|---|
| **L** | **Lean-checked conditional implication.** Proved in Lean in this repo (`Corollaries/`, `Fidelity/`), taking OpenAI's comparator statement as an explicit hypothesis. The kernel checks that the hypothesis has exactly OpenAI's type. Two independent audits (`#assert_standard_axioms` in Lean; `scripts/check_axioms.py`) accept only `propext`, `Classical.choice` and `Quot.sound`. OpenAI's own proofs are **not** checked here: the vendored comparator files contain `sorry`, and no audited declaration depends on them. |
| **D** | **Complete written derivation.** Premises are quoted from the corpus with their source. Every other step is either elementary and written out, or a cited classical theorem. Not formalized. |
| **Lead** | **Research lead.** A precise candidate statement with a bridge sketch. Not a result. |

**Refereed** means two independent agents, who had not seen how the entries were produced, re-checked every premise, citation and number against the sources. That pass covered every entry in the first edition of this file (NT, DA, GR, AG, GE). They confirmed all of them, found none wrong, corrected two citations, and recommended the tier changes made here. A second referee pass then checked the entries from the final mining pass (theoretical computer science, combinatorics, logic) the same way, so **every entry in this file has now been refereed**.

A summary table with counts is at the end.

---

## Number theory

### NT-1 · OpenAI's Landau–Siegel statement follows from its 7/8 statement · **L** · refereed
- **Statement.** `DirichletSevenEighths` implies OpenAI's `SiegelZeros` comparator, in both forms, with explicit `c = log 3 / 8`. It also gives a stronger uniform gap: every real zero of every nontrivial Dirichlet `L`-function of any modulus has `β ≤ 7/8`. No primitivity or reality condition is assumed.
- **Lean.** `Corollaries.real_zero_le_seven_eighths`, `Corollaries.siegel_of_sevenEighths`, `Fidelity.siegel_comparator_of_sevenEighths`, `Fidelity.siegel_comparator'_of_sevenEighths`.
- **Scope.** This checks an implication between two claims, not the 7/8 theorem itself. The Oct 1 paper keeps independent value: neither paper cites the other, so the Siegel result would survive a flaw in the 7/8 proof. The referee found no circularity.

### NT-2 · OpenAI's zeta statement is the modulus-1 case · **L** · refereed
- `DirichletSevenEighths` implies `QuasiRiemannHypothesis.lean`, i.e. `ζ(s) ≠ 0` for `Re s > 7/8`.
- **Lean.** `Corollaries.zeta_of_sevenEighths`, `Fidelity.zeta_comparator_of_sevenEighths`.

### NT-3 · A third route to the Siegel statement, through family 029 · **D** · refereed
- **Premise.** 029, Theorem 1.2: "Let F be a cyclotomic number field containing µ12. For every finite-order Hecke character η of F, the meromorphic continuation of L_F(s, η) has no zeros in Re s > 1 − 10⁻⁶. The principal character is included, with its pole at s = 1 permitted. The width is common to all fields and characters."
- **Statement.**
  - Every Dirichlet `L`-function, `ζ` included, has no zero in `Re s > 1 − 10⁻⁶`. So the Siegel comparator also holds with `c = 10⁻⁶·log 3`.
  - More generally, `ζ_K(s) ≠ 0` for `Re s > 1 − 10⁻⁶`, uniformly, for every number field `K` whose Galois closure is metabelian.
- **Derivation.**
  1. Let `χ` mod `q` be induced by the primitive character `χ*`, and let `F = ℚ(μ_{12q})`. Then `ζ_F = ∏_{ψ mod 12q} L(s, ψ*)` (Washington, *Cyclotomic Fields*, Thm 4.3), and `L(s, χ*)` is one of the factors.
  2. The premise with `η` trivial makes `ζ_F` zero-free there. Every factor is holomorphic away from `s = 1`, and `L(1, χ*) ≠ 0`. So `L(s, χ*)` is zero-free there too.
  3. `L(s, χ)` differs from `L(s, χ*)` by Euler factors that vanish only on `Re s = 0`.
  4. Metabelian case: `E = L^{G′}` is abelian, so it lies in a cyclotomic field (Kronecker–Weber). Then `M = L·ℚ(μ_{lcm(12,n)})` is abelian over that cyclotomic field. So `ζ_M` is a product of Hecke `L_F`'s (Neukirch VII (10.5)–(10.6)) and is zero-free. Since `ζ_M/ζ_K` is entire (Aramata–Brauer), `ζ_K` is zero-free as well.
- **Qualification.** This route does not use 003's theorem, but it does use 003's method: 029 §§6–7 follow "the reflection method of [23]", which is the 7/8 paper.
- **Unstated.** 029 descends only to its Kummer fields (§9.1).

### NT-4 · Small ℓ-th power nonresidues and primitive roots from 7/8 · **Lead** · refereed
*(Merges the first edition's NT-4 with candidate DT-04 from the TCS pass.)*
- **Claim.** Assume 003's Theorem 1.1.
  - For `p ≥ p₀` and every prime `ℓ | p − 1`, some `a ≤ C(log p)⁸` is not an `ℓ`-th power mod `p`.
  - Hence `g(p) ≤ exp(C log p / log log p)`, effectively. The best unconditional bound is about `p^{1/4+ε}` (Burgess).
  - Given the factorization of `p − 1`, a primitive root can be found deterministically in `poly(log p)`.
  - With family 279 (exact quantum factoring), a primitive root can be found in exact quantum polynomial time.
- **Argument.** Ankeny's GRH argument, with the 7/8 half-plane in place of GRH. The smoothed explicit formula gives `ψ(x, χ) ≪ x^{7/8} log p` for characters of order `ℓ`. If every `n < 2x` were an `ℓ`-th power, this would force `x ≪ (log p)⁸`. Vinogradov's indicator and `ω(n) ≤ (1+o(1)) log n / log log n` then give the bound on `g(p)`.
- **Why still a Lead.** The explicit-formula step must hold for `x < q`, and needs a citation pinned to an exact statement (Montgomery–Vaughan Thm 12.10; Davenport Ch. 19–20). The 11/12 paper's Cor 1.2 needs `q ≤ x`, so it does not apply.
- **Unstated.** Neither 003 paper mentions primitive roots, or `ℓ`-th powers for `ℓ > 2`.

### NT-5 · Pure cubic fields: `ζ_{ℚ(∛m)}(s) ≠ 0` for `Re s > 7/8` · **D** for the zero-free claim · refereed
- **Premise.** 003, Thm 1.1 (Sept 30): "Every finite-order Hecke L-function over F = ℚ(√−3) has no zero in ℜs > 7/8. The same holds for every Dirichlet L-function, including ζ(s)."
- **Derivation.**
  1. Let `m` be a non-cube and `L = ℚ(∛m, ζ₃)`. Then `Gal(L/ℚ) = S₃`, and `L/F` is cyclic of degree 3.
  2. A nontrivial `χ` of `Gal(L/F)` is a finite-order Hecke character of `F`.
  3. `Ind_{C₂}^{S₃} 1 = 1 ⊕ Ind_{A₃}^{S₃} χ`. So `ζ_K = ζ · L_F(s, χ)` (Neukirch VII (10.4)(iv), (10.6)), and both factors are zero-free.
  4. The same argument, with Aramata–Brauer, covers every `K` inside an abelian extension of `ℚ(√−3)`.
- **Referee check.** The comparator's `Character` structure is exactly the set of ray-class characters (`ℤ[ω]` is a PID with unit group `μ₆`, and `F` has no real place).
- **Lead.** Chebotarev in `ℚ(ζ₃, ∛m)` with error `x^{7/8+ε}`.
- **Not new.** Effective Brauer–Siegel for non-Galois cubic fields is already known unconditionally (arXiv:2510.02309, building on Stark 1974).

### NT-6 · Full-reptend primes; irreducible all-one polynomials over 𝔽₂ · **D** · refereed
- **Premise.** 029 (`CONTENTS.md`): for every integer `a` that is neither `−1` nor a square, at least `c_a x/(log x)²` primes in every sufficiently large interval `(x, 2x)` have primitive root `a`.
- **Statement.** Each of the following holds **separately** for at least `c·x/(log x)²` primes `p ∈ (x, 2x)` once `x` is large. (The two together are not covered.)
  - (a) `1/p` has decimal period exactly `p − 1` (`a = 10`).
  - (b) `Φ_p = 1 + X + … + X^{p−1}` is irreducible over `𝔽₂`, so `𝔽_{2^{p−1}}` has a type-I optimal normal basis (`a = 2`).
- **Derivation.**
  1. Neither 10 nor 2 is `−1` or a square, and `2, 5 ∉ (x, 2x)` for large `x`.
  2. (a): for `p ∤ 10`, `1/p = m/(10^k − 1)` exactly when `p | 10^k − 1`. So the period is `ord_p(10)`.
  3. (b): `Φ_p` splits over `𝔽_q` into factors of degree `ord_p(q)` (Lidl–Niederreiter, Thm 2.47(ii)).
  4. The type-I optimal normal basis exists when `n + 1` is prime and `q` is primitive mod `n + 1` (Mullin–Onyszchuk–Vanstone–Wilson, *Discrete Appl. Math.* 22 (1988/89)).
- **Unstated.** No "reptend", "optimal normal basis" or "all-one" anywhere in the corpus.

### NT-7 · Liouville sign agreement has density 1/2 · **L** · refereed
- **Statement.** Assume 007's `liouville_log_saving`. Then there is `c > 0` such that, for all `a₁, a₂ > 0` with `a₁b₂ ≠ a₂b₁`, there is `C > 0` with
  `|#{1 ≤ n ≤ ⌊X⌋ : λ(a₁n+b₁) = λ(a₂n+b₂)} − ⌊X⌋/2| ≤ C·X/(log X)^c` for all `X ≥ 3`.
- **Equivalently**, `Ω(a₁n+b₁)` and `Ω(a₂n+b₂)` agree in parity for half of all `n`.
- **Lean.** `Fidelity.liouville_agreement_density`, `Fidelity.liouville_eq_iff_parity`.

### NT-8 · At least 47.92% of positive integers are sums of two rational cubes · **D** · refereed
- **Premises.**
  - 002 Selmer-converse Thm 1.1: "For every elliptic curve A0/Q, every prime p, and r ∈ {0,1}, s_p(A0) = r ⟹ a(A0) = rank A0(Q) = r, # Sha(A0/Q) < ∞."
  - Koymans–Smith (arXiv:2405.09311), Cor 1.8: if `r₃(E_{−432,n}) = 1 ⟹ rank E_{−432,n} = 1` holds for all positive `n`, then at least 47.92% of positive integers are sums of two rational cubes.
  - Koymans–Smith, Def 1.4: `r₃ = −1 + dim Sel³ E_{−27d,n}` when `−27d` is a square.
- **Derivation.**
  1. `−27·(−432) = 108²`, so `r₃ = dim Sel³(E′) − 1` with `E′ : y² = x³ + (108n)²`.
  2. `(0, ±108n)` are 3-torsion. `E′[3]` is not fully rational, since the Weil pairing would then force `μ₃ ⊂ ℚ`. So `dim E′(ℚ)[3] = 1`.
  3. By the Kummer sequence and Cassels–Tate, `r₃ = s₃ + (even)`. So `r₃ = 1` forces `s₃ = 1`.
  4. 002 at `p = 3` gives rank 1.
  5. The 3-isogeny `(x, y) ↦ ((x³+4k)/x², y(x³−8k)/x³)` and a rescaling carry this to `E_{−432,n}`.

<a id="nt-9"></a>

### NT-9 · Full BSD formula for at least 83.75% of elliptic curves ordered by height · **D** · refereed
- **Premises.**
  - 002 Exact-BSD Thm 1.1: "Let E/Q be an elliptic curve and let q be any prime. If s_q(E) ∈ {0,1}, then # Sha(E/Q) < ∞, r(E) = a(E) = s_q(E), and [the full leading-term formula] … There are no additional hypotheses on reduction, rational torsion, isogenies, complex multiplication, or residual Galois representations."
  - Bhargava–Shankar (arXiv:1312.7859): at least 83.75% of curves have rank 0 or 1. Their method bounds "not just the rank but the 5-Selmer rank". Concretely, Propositions 38(b) and 40(b), with the proof of Theorems 3–5 (printed pp. 27–29), give lower density at least `0.5501 × 7/8 + 0.4499 × 19/24 > 0.8375` with 5-Selmer dimension at most one.
- **Derivation.**
  1. Let `t = dim Sel₅ − dim E(ℚ)[5]`. Then `s₅ ≤ t`, `t ≡ s₅ (mod 2)` by Cassels–Tate, and `(−1)^{s₅} = w(E)` by Dokchitser–Dokchitser.
  2. Three inputs:
     - the average of `#Sel₅` is 6 (Bhargava–Shankar Thm 1);
     - root numbers are equidistributed on a family of density > 55.01% (their Thm 6);
     - `5^t ≥ 1 + 24·[t ≥ 2] + 4·[t odd]`.
  3. Together these give `P(t ≤ 1) ≥ 0.83750`, the 83.75% figure.
  4. Where `t ≤ 1`, we have `s₅ ≤ 1`, and 002 at `q = 5` gives the full formula, with no extra local conditions.
- **Credit.** An external review proposed the 5-Selmer route; the referee checked 002's exact statement at `q = 5`. The full write-up, with research implications, is [RP-4 in the research priorities](RESEARCH_PRIORITIES.md#rp-4-full-bsd-in-analytic-low-rank-and-a-height-density-consequence).
- **Comparison.** Bhargava–Skinner–Zhang's 66.48% is for the BSD *rank* conjecture with finite Sha, not the leading-term formula.

### Already in the corpus or the literature (not counted as corollaries)
- The 11/12 paper already states:
  - the effective class-number bound `h(D) ≫ √|D| / log log |D|`;
  - completeness of Euler's 65 idoneal numbers;
  - an effective prime number theorem in progressions with error `x^{11/12} log x` for `q ≤ x`;
  - a deterministic Miller test.
- The 7/8 paper already states a polylog least quadratic nonresidue and deterministic square roots mod `p`.
- 029's Theorem 1.2, used in NT-3, is in the corpus.
- **Former NT-10 (congruent numbers):**
  - full BSD for a density-one set of twists is a corpus statement (002 with 006);
  - "100% of squarefree `n ≡ 5, 6, 7 (mod 8)` are congruent" is Kriz + Smith (arXiv:2002.04767);
  - "100% of `n ≡ 1, 2, 3 (mod 8)` are not" is Smith's theorem alone.

### What the 7/8 half-plane does and does not improve
- **No improvement:**
  - primes in short intervals (Guth–Maynard `x^{17/30}`; the bottleneck is zero density near `σ = 7/10`);
  - Bombieri–Vinogradov, twin primes, Chen (even GRH does not move these).
- **Incomparable.** The half-plane and the density hypothesis are logically incomparable.
- **Improves.** Average Goldbach: `Σ_{n≤N} R(n) = N²/2 + O(N^{15/8} log² N)` (cf. Bhowmik–Ruzsa, arXiv:1711.06442).
- **Lead.** Linnik's constant, plausibly to about `8/3 + ε` via Montgomery's density bound. Not verified.

**Effectivity audit.**
- Siegel-type ineffective inputs appear in:
  - 011 (three papers), 021 and 029: Siegel–Walfisz;
  - 012 and 013: Siegel's real-zero bound.
- 023 uses a prime-ideal Siegel–Walfisz whose cubic version is already effective; 026 uses Bombieri–Vinogradov.
- Under 003 these inputs become effective. The papers say only that their constants "need not be effective". We have not checked whether any headline constant becomes effective.

---

## Diophantine approximation

### DA-1 · Liouville exponents of `π` and its rational images · **L** · refereed
Assume OpenAI's `PiExponent.main`.
- **Upper bound.** For `r, s ∈ ℚ` with `r ≠ 0` and every `p > 2`: `¬ LiouvilleWith p (π·r + s)`. Also `¬ Liouville π`.
- **Möbius images.** The same holds for every `(aπ+b)/(cπ+d)` with `a, b, c, d ∈ ℚ` and `ad − bc ≠ 0`. This uses a new lemma, `LiouvilleWith p x⁻¹ ↔ LiouvilleWith p x`, which Mathlib lacked.
- **Exact value.** Dirichlet's theorem gives that every irrational is `LiouvilleWith 2`; Mathlib's file listed this as not yet formalized. So `{p | LiouvilleWith p (rπ+s)} = (−∞, 2]`, and its supremum, the irrationality exponent, is exactly 2. The same holds for every rational Möbius image of `π`.
- **Lean.**
  - `Pi.lean`: `pi_not_liouvilleWith`, `rat_affine_pi_not_liouvilleWith`, `pi_not_liouville`.
  - `PiMobius.lean`: `liouvilleWith_inv_iff`, `liouvilleWith_mobius_iff`, `mobius_pi_not_liouvilleWith`.
  - `PiDirichlet.lean`: `liouvilleWith_two_of_irrational`, `rat_affine_pi_liouvilleWith_eq_Iic`, `rat_affine_pi_irrationalityExponent`, `mobius_pi_liouvilleWith_eq_Iic`.
- "`π` is not Liouville" was already known (Mahler 1953).

### DA-2 · The Cookson Hills series converges · **D** · refereed
- **Premise.** 017, eq. (5.1): `Σ_q 1/(q³‖qπ‖²) < ∞`. Cor 5.2: `Σ n^{−a}|sin n|^{−b}` converges iff `a > max{1, b}`.
- **Statement.**
  - `Σ sec²(n)/n³ < ∞`.
  - More generally, `Σ n^{−a}|cos n|^{−b}` converges iff `a > max{1,b}`.
  - The same holds for `Σ n^{−a}|sin(rn)|^{−b}` with `r ∈ ℚ ∖ {0}`. The case `r = 1` is Cor 5.2; `r = π` fails.
- **Derivation.**
  1. Group the `n` by the nearest odd multiple `(2k+1)π/2`. For `k ≥ 1`, `|cos n| ≥ ‖(2k+1)π‖/π` and `n ≥ (π/3)(2k+1)`, with at most 4 terms per group.
  2. So `Σ sec²n/n³ ≤ C Σ_{q odd} q^{−3}‖qπ‖^{−2} < ∞` by (5.1).
  3. For general exponents, run Cor 5.2's dyadic spacing argument on the points `(2k+1)π`, or on `kvπ` for `r = u/v`.
  4. Divergence when `1 < a ≤ b`: Minkowski's inhomogeneous theorem for cos, and Dirichlet for `sin(rn)`.
- **Unstated.** `grep -i cookson` over the whole repo finds nothing.

### DA-3 · Discrepancy `O(N^{−1+ε})` for `n mod 2π` · **D** · refereed
- **Derivation.**
  1. Theorem 1.1 applied to the fraction `q/(2p)` shows `1/(2π)` has type 1.
  2. Kuipers–Niederreiter (Ch. 2, Thm 3.2) then gives `D_N = O(N^{−1+ε})`.
  3. Koksma's inequality (K–N Ch. 2, Thm 5.1) with total variation 4 gives
     - `Σ_{n≤N} sgn(sin n) = O(N^ε)`;
     - `Σ_{n≤N} |sin n| = (2/π)N + O(N^ε)`.
- **Before.** The previous bound `μ(π) ≤ 7.1032` gave only `N^{−0.1638}`.

---

## Group rings and operator algebras

### GR-1 · Kaplansky's counterexample survives every field map; stable finiteness fails in every characteristic-2 field · **L** · refereed
- **Field maps.** For every ring map `K →+* L` out of OpenAI's finite field, `L[G]` is not directly finite.
- **Stable finiteness.** For every field `L` of characteristic 2, `𝔽₂` included, `L[G]` is not stably finite. The proof embeds `K ↪ M_m(𝔽₂)` with `m = [K:𝔽₂]`, then builds an injective ring map `K[G] → M_m(L[G])`.
- **Contrast.** The same `G` is stably finite over every characteristic-0 field. This is classical, and stated in the Sept 23 paper.
- **Lean.** `Corollaries.directFiniteness_transfer`, `Fidelity.kaplansky_transfer`, `Fidelity.not_isStablyFiniteRing_of_kaplansky`, `Fidelity.not_isStablyFiniteRing_zmod_two_of_kaplansky`.

### GR-2 · The torsion-free counterexample also breaks the idempotent conjecture in characteristic 2 · **D** (ring step **L**) · refereed
- **Premise.** "A Torsion-Free Group Algebra That Is Not Directly Finite" (Oct 4), Thm 1.1: "There exist a finitely presented torsion-free group G and elements a, b, c ∈ F2[G] such that ab = 1, ac = 0, c ≠ 0 … The group G admits a finite two-dimensional classifying complex."
- **Statement.**
  - (i) `ba` is an idempotent other than 0 and 1. So Kaplansky's idempotent conjecture fails for torsion-free groups over `𝔽₂`, and over every field containing it.
  - (ii) `𝔽₂[G]` has zero divisors (`a ≠ 0`, `ac = 0`). This is family 196's headline.
  - (iii) 207 proves the idempotent conjecture "for every torsion-free group G and every commutative unital domain R of characteristic zero". So its characteristic-0 hypothesis cannot be dropped.
  - (iv) The cellular automaton `T_b` on `𝔽₂^G` is injective and not surjective. This gives a torsion-free, finitely presented counterexample to Gottschalk's surjunctivity conjecture, via Prop 7.2 of the Sept 23 characteristic-two paper, which holds for any finite field and group.
- **Lean.** `Corollaries.idempotent_of_directFiniteness_witness` checks the ring identities in any ring.
- **Note.** The Oct 4 paper adapts the 196 construction ("We adapt those arguments… and reproduce the estimates and topology needed here"). So "197 ⇒ 196" is a second written proof by the same method, not an independent route.

### GR-3 · Family 196's group is not left-orderable · **L**, consequences **D** · refereed
- **Lean.** `Fidelity.zeroDivisor_group_not_leftOrderable`, via Mathlib's `UniqueProds ⇒ NoZeroDivisors`.
- **Consequences.**
  - Not locally indicable (Burns–Hale, *Canad. Math. Bull.* 15 (1972)).
  - Not bi-orderable.
  - Not a subgroup of any right-angled Artin group, since RAAGs are bi-orderable (Duchamp–Krob; Duchamp–Thibon 1992).
- The same holds for the Oct 4 group, which also has zero divisors.

### GR-4 · No nontrivial idempotents in `ℓ¹(G)` for torsion-free `G`; consistency with 285 · **D** · refereed
- **Premises.**
  - ℓ¹-Bass Thm 1.1 (Oct 5): idempotent traces over `ℓ¹G` vanish outside finitely many finite-order classes.
  - 285 Thm 1.1: a torsion-free `G_proj` has a projection `e ∈ C*_r(G_proj)` with `0 < τ(e) < 1/2`.
- **Derivation.**
  1. For torsion-free `G`, `τ = tr ε(·)` with `ε` the augmentation, so the trace is integer-valued on `K₀(ℓ¹G)`.
  2. Hence `[e]` is not in the image of `K₀(ℓ¹G)`.
  3. A scalar idempotent is similar in `C*_r` to a projection (Blackadar, Prop 4.6.2). By faithfulness of the trace it is 0 or 1.
- **Consistency.** No tension: the failure sits in the comparison `ℓ¹ → C*_r`.

### GR-5 · Thompson's groups `F` and `T` are C*-simple · **D** · refereed
- **Derivation.**
  - 248: `F` is nonamenable.
  - Le Boudec–Matte Bon (*Ann. Sci. ÉNS* 51 (2018), Thm 1.6): `F` nonamenable ⇔ `F` C*-simple ⇔ `T` C*-simple.
  - Breuillard–Kalantar–Kennedy–Ozawa (*Publ. IHÉS* 126 (2017)): C*-simple ⇒ unique trace.
- **What is new.** `T` already had a unique trace. The new content is a unique trace for `F` and C*-simplicity for `T`.

### GR-6 · Every subfactor standard invariant is realized inside `L(F₂)` · **D** · refereed
- **Derivation.**
  - Popa–Shlyakhtenko (*Acta Math.* 191 (2003)) realize every λ-lattice with `N ≅ M ≅ L(F_∞)`.
  - 287 Cor 6.1 gives `L(F_∞) ≅ L(F₂)`.
  - Also `L(F₂) * L(F₂) = L(F₄) ≅ L(F₂)`.

### GR-7 · Connes–Shlyakhtenko `L²`-Betti numbers of `L(F_r)` are 0 or ∞ · **D** · refereed
- **Derivation.**
  - Connes–Shlyakhtenko (*J. reine angew. Math.* 586 (2005), Thm 2.4): `β_k(pMp) = τ(p)^{−2}β_k(M)` for factors.
  - 287 gives fundamental group `ℝ_{>0}`, so `β = 4β`.
- **Wording.** Refuting `β₁(L(F_n)) = n − 1` needs only `L(F₂) ≅ L(F₃)`. The `{0, ∞}` dichotomy is the extra content: if CS's lower bound `β₁ ≥ n − 1` holds, then `β₁ = ∞`.
- **Folklore.** The continuous analogue is Alekseev–Kyed (arXiv:1110.6155, Cor 4.13).

### GR-8 · Haagerup–Størmer for all separable type III₁ factors · **D** (already known without the corpus) · refereed
- **Derivation.** 290 (trivial bicentralizer) plus **Isono**, arXiv:2309.05279, Cor B: "Haagerup–Størmer's conjecture holds for any type III₁ factor with separable predual that has trivial bicentralizer."
- **Citation fix.** The first edition misattributed this to Marrakchi.
- **Already known.** Houdayer–Marrakchi (arXiv:2609.11462), cited by 290, already supply the bicentralizer input.

### GR-9 · Artin groups: Euler characteristic, cohomological dimension, `L²`-Betti numbers · **D** · refereed
- **Premise.** 254 Thm 1.1: the Salvetti complex is aspherical, with one cell of dimension `|T|` per spherical `T`.
- **Euler characteristic.** `χ(A) = Σ_{T spherical} (−1)^{|T|}`.
- **Cohomological dimension.** `cd A = max{|T| : W_T finite}`.
  - The upper bound comes from the dimension of the complex.
  - For the lower bound:
    - `A_T ↪ A` (van der Lek);
    - `cd PA_T = |T|` (Deligne; Orlik–Solomon);
    - Serre's finite-index theorem.
- **`L²`-Betti numbers.** These are given by **Davis–Leary** (*J. London Math. Soc.* 68 (2003), Cor 2), which was conditional on `K(π,1)`.
- **Citation fix.** The first edition attributed this to Davis–Okun.

### GR-10 · The nonsofic group and Aldous–Lyons · **Lead** · refereed
- **Claim.** The Sept 23 group is finitely presented and specified by a terminating prescription. It gives a group-theoretic counterexample to the network Aldous–Lyons conjecture.
- **Already refuted.** Aldous–Lyons was already refuted non-constructively by Bowen–Chapman–Lubotzky–Vidick (arXiv:2408.00110; 2501.00173).
- **Limits.** The Oct 4 group comes from a random construction, so it is not explicit. Hyperlinearity does not follow.
- **To reach D.** Cite the δ_N ⇔ soficity equivalence precisely.

### GR-11 · Gottschalk's surjunctivity fails for OpenAI's Kaplansky groups · **L** · consistent with refereed GR-2(iv)
- **Statement.** These are proved against OpenAI's own `cellular` map (`OddKaplansky.lean`):
  - the composition law `cellular a ∘ cellular b = cellular (ab)`;
  - faithfulness;
  - `cellular d` is a cellular automaton with memory set `supp d`;
  - `ab = 1 ≠ ba` makes `cellular b` injective and not surjective.
- **Consequences.**
  - The characteristic-2 comparator gives a finitely generated non-surjunctive group.
  - The finitely presented comparator gives a finitely presented one.
  - In the odd-characteristic `MainClaim`, the two cellular-automaton conjuncts are redundant (`oddKaplansky_mainClaim_iff`).
- **Lean.** `Fidelity/Surjunctivity.lean`.
- **Not new mathematics.** The Sept 23 paper proves the transfer in prose (§6). The new part is the check against OpenAI's definitions, and the redundancy of OpenAI's conjuncts.

---

## Algebraic geometry

### AG-1 · Tate and `num = hom` for products of curves over finite fields · **Lead** · refereed
- **Already in the corpus.** The CM-Hodge paper's Cor 8.4 states `num = hom` (standard conjecture D) and the Hodge standard conjecture (I) for abelian varieties in every characteristic. B and C are classical (Lieberman; Kleiman). So the first edition's "all four standard conjectures" adds nothing new.
- **New and sound.**
  - Tate and `num = hom` for products of curves: `h(∏ Cᵢ)` is a sum of Tate twists of summands of `h(∏ Jᵢ)`, and Cor 8.3 covers all abelian varieties over `𝔽_q`.
  - The zeta pole-order form follows via Tate 1994 (Milne, arXiv:0709.3040, Thm 1.5).
- **To reach D.** Write out the motive step.

### AG-2 · Rational Hodge conjecture for Hilbert schemes and moduli of sheaves on any K3 · **D** · refereed
- **Premise.** "Rational Hodge conjecture for products of K3 surfaces" (Oct 4): "rational Hodge conjecture for every finite product of projective complex K3 surfaces… factors may be distinct or repeated."
- **Derivation.** Repeat the proof of Cor 9.5 of the K3-quadratic-locus paper (Sept 30), which uses:
  - de Cataldo–Migliorini, Thm 6.2.1;
  - Bülles, Thm 0.1;
  - Arapura, Lemma 4.2.

  That corollary was stated only on the quadratic locus. Here it is fed the Oct 4 theorem for arbitrary products instead.
- **Scope.** All `S₁^{[n₁]} × … × S_k^{[n_k]}`, and all smooth projective moduli of (twisted) Gieseker- or Bridgeland-stable objects on K3s.

### AG-3 · Two projective MMP papers are special cases of "Log abundance in characteristic zero" · **D** · refereed
*(Formerly AG-4.)*
- **Fourfold nonvanishing.** Special case of the canonical nonvanishing "for smooth projective varieties in every dimension".
- **"Lifting sections from the reduced support of an adjoint", Thms 1.1–1.3 and Cor 1.4.**
  - Their hypotheses force `A` to be nef, so log abundance makes it semiample.
  - `κ = 0` would give `G ~_ℚ 0`, which is impossible.
- **Lead.** The characteristic-0 "numerical dimension one" paper (via log abundance Cor 11.2). The characteristic-p papers in 035 are not special cases.

### AG-4 · Effective log Iitaka fibrations in every dimension over ℂ · **D** · refereed
*(Formerly AG-5.)*
- **Derivation.** Combine three results:
  - the `d ≥ 5` paper (Thm 1.1, any algebraically closed field of characteristic 0);
  - the `d = 4` paper (over ℂ);
  - Chen–Han–Liu (arXiv:2301.04813, Cor 1.5, `d ≤ 3`, DCC coefficients).
- **Scope.** Other fields need the Lefschetz principle for `d ≤ 4`.

### Already in the corpus (moved here)
- **Former AG-3 (compact Kähler log abundance).** The 034 Kähler paper's Assumption 1.1 has the same content as 033's Cor 6.2 (`spec:logarithmic`); the wording is close but not identical.
  - The corpus already treats it as proved: the log abundance paper's Thm 1.2 cites it, and the 034 `CONTENTS.md` entry says "Using logarithmic Iitaka subadditivity, proves log abundance in every dimension".
  - The first edition said this was family 033's title. It is the 034 Kähler paper's title that still says "conditional".

---

## Analysis, geometry and physics

### GE-1 · Bourgain–Milman with the optimal base `2/π` · **L** (bound), **D** (optimality, general case) · refereed
- **Premise.** `MahlerConjecture.lean`: `vol(K)·vol(K°) ≥ 4ⁿ/n!` for compact convex symmetric `K ⊂ ℝⁿ` with nonempty interior.
- **Statement.** `vol(K)·vol(K°) ≥ 2ⁿ/Γ(n/2+1)² = (2/π)ⁿκₙ²`.
- **Lean.**
  - `Fidelity.factorial_le_two_pow_mul_Gamma_sq` proves `n! ≤ 2ⁿΓ(n/2+1)²` by two-step induction. The ratio gains a factor `(n+2)/(n+1) ≥ 1` at each step, and equals `1` at `n = 0` and `π/2` at `n = 1`.
  - `Fidelity.symmetric_mahler_gamma`, `Fidelity.symmetric_mahler_bourgainMilman`.
- **Optimality (D).** The cube gives `4ⁿ/n!`. The ratio `2ⁿΓ(n/2+1)²/n! ~ √(πn/2)` has `n`-th root tending to 1 (`1.571, 2.000, 4.063, 17.75` at `n = 1, 2, 10, 200`).
- **General bodies (D).**
  1. `general_mahler` takes an infimum over interior centers, so every interior `z` satisfies `|K||(K−z)°| ≥ (n+1)^{n+1}/(n!)²`.
  2. `(n+1)^{n+1}/(n!)² ≥ eⁿ/n! ≥ (e/2π)ⁿκₙ²`.
  3. The base `e/2π` is optimal, as simplices show.
- **Context.** Kuperberg (*GAFA* 18 (2008), Cor 1.6) gives about `(1/2)ⁿ√(πn)·κₙ²`, so Mahler improves the base from `1/2` to `2/π`. The corpus mentions Bourgain–Milman only as history.

### GE-2 · Lattice transference `λ₁(K, Λ)·λ₁(K°, Λ*) ≤ (n!)^{1/n}` · **D** · refereed
- **Statement.** This holds for symmetric `K`, any lattice `Λ` and its dual `Λ*`.
- **Derivation.** Minkowski gives `λ₁ⁿ vol K ≤ 2ⁿ det Λ`, and the same for `K°, Λ*`. Multiply the two and apply Mahler. Sharp at `n = 1`.
- **Comparison.** Kuperberg already gives `≤ (4/π)γₙ^{−1/n}(n!)^{1/n}`; Mahler removes the `4/π`.

### GE-3 · Symplectic ball rigidity · **D** · refereed
- **Statement.** If `int K × int K°` embeds symplectically in `B^{2n}(4)`, then `K` is a linear Hanner body.
- **Derivation.**
  1. `vol B^{2n}(c) = cⁿ/n!`.
  2. A symplectic embedding preserves volume, so `vol K · vol K° ≤ 4ⁿ/n!`.
  3. Mahler forces equality, and `symmetric_mahler_equality` then forces a Hanner body.
- **In the corpus.** The symplectic paper "make[s] no claim … about the classification of equality cases."

### GE-4 · Isotropic constant `L_K < 1/e` in every dimension, and `1/e` is sharp · **D** · refereed
- **Premise.** 101 Thm 1.1, with its normalization (1.1) `L_K = (det Σ_K/|K|²)^{1/(2n)}`: `L_K ≤ b(n) := (n!)^{1/n}/((n+1)^{(n+1)/(2n)}√(n+2))`, with equality iff `K` is a simplex.
- **Derivation.**
  1. `b(n)^{2n} = (n!)²/((n+1)^{n+1}(n+2)ⁿ)`.
  2. Three elementary bounds:
     - `n! ≤ e·n^{n+½}e^{−n}` (trapezoid rule for the concave `log`);
     - `(n+1)^{n+1} > e·n^{n+1}`;
     - `(n+2)ⁿ ≥ 3nⁿ`.
  3. Together: `b(n)^{2n} < (e/3)e^{−2n}`, so `b(n) < 1/e`.
  4. Stirling gives `n·log(e·b(n)) → (log 2π − 3)/2 = −0.58106`, so `b(n) → 1/e`.
- **Referee check.** The simplex formula was re-derived from `Σ = ((n+1)I − J)/((n+1)²(n+2))`.

### GE-5 · Sharp functional isotropic constant · **D** (known given the input) · refereed
- **Derivation.** Bobkov–Madiman (arXiv:1006.2883, Prop I.2) give `h ≤ n + log‖f‖∞^{−1}`. Combined with 101 Thm 1.2, this gives `‖f‖∞² det Cov f ≤ 1`, with equality exactly for affine images of products of one-sided exponentials.
- **Known given the input.** Fradelizi–Marín Sola (arXiv:2406.07406) note that their Conjecture 3(iii) implies 3(i).

### GE-6 · Sharp Euclidean Sobolev inequalities on Cartan–Hadamard manifolds · **D** (known given the input) · refereed
- **Derivation.**
  - For `1 < p < n`: the rearrangement in 337's §9 (Nobili–Violo, with Thm 1.1 at `κ = 0`), then Aubin–Talenti.
  - For `p = 1`: coarea plus isoperimetry.
- **Known given the input.** Aubin (*JDG* 1976) derived this from the isoperimetric conjecture.

### GE-7 · Falconer for analytic (in particular Borel) sets · **D** · refereed
- **Premise.** 073's Thm 1.1 and its comparator, which are for compact sets.
- **Derivation.**
  - Davies (*Indag. Math.* 14 (1952); Howroyd 1995) gives a compact `K ⊂ A` with `0 < H^s(K) < ∞` for `d/2 < s < dim A`.
  - `Δ(A) ⊇ Δ(K)`, and `Δ(A)` is analytic, hence measurable.

### GE-8 · Scalar Hénon–Lane–Emden Liouville theorem · **L** · refereed
- **Statement.** For `n ≥ 2`, `p > 0` and `n − 2 < 2(n+A)/(p+1)`, there is no positive `u` with `−Δu = |x|^A u^p` on `ℝⁿ ∖ {0}`.
- **Lean.** `Fidelity.scalar_henon_nonexistence`.

### GE-9 · Near-sharp Lieb–Thirring constants in every dimension for `γ ≠ 1` · **D** · refereed
- **Premise.** 262's matrix paper proves the constant `r_γ·L^cl`, `r_γ = 2((γ−½)/(γ+½))^{γ−½}`, "independently of the matrix size".
- **Derivation.**
  1. Pass to operator-valued potentials by compression `W_N = P_N W P_N`, using min-max, interlacing and dominated convergence.
  2. Lift with Hundertmark–Laptev–Weidl (*Invent. Math.* 140 (2000), proof of Thm 4.1), and use Laptev–Weidl for exponents `≥ 3/2`.
- **Result.**
  - `L_{γ,d}/L^cl ≤ r_γ` for `1 ≤ γ < 3/2`, in every dimension `d`.
  - `≤ r_γ r_{γ+½}` for `1/2 < γ < 1`, `d ≥ 2`.
- **Already known.** `γ = 1` (Read–Schulz, `2/√3`) is cited in the corpus.

### GE-10 · Pure-loss trade-off capacity regions become unconditional · **Lead** · refereed
- **Claim.** Wilde–Hayden–Guha (arXiv:1105.0119) condition their result on "Strong Conjecture 2". That conjecture is exactly 273's Cor 1.2 with `N_B = 0`, for finite-energy inputs.
- **To reach D.** Check that WHG use the conjecture only on codeword states.

### GE-11 · Nagata with equal multiplicities · **L** (a specialization)
- **Statement.** For `r ≥ 10` very general points:
  - `m√r < d`;
  - `r·m² < d²`;
  - `⌊√r⌋·m < d`;
  - `d ≥ 3m + 1` for `r = 10`.
- **Lean.** `Fidelity.nagata_equal_multiplicity`, `nagata_sqrt_floor`, `nagata_ten_points`. These use only the comparator's `FullNagata`, because its `nagata_conjecture` depends on a `sorry`d lemma.
- **Not new mathematics.** The paper reduces to equal multiplicities itself, and its lemma "Excluding degree at most 3m" gives `d > 3m`.

---

## Redundant comparator statements

### RD-1 · Two Elliott comparators are the same theorem · **L**
- **Equivalence.** `OrdinaryTwoPointCorrelations.binary_corrected_elliott` ⇔ `OrdinaryElliott.binary_corrected_elliott`. They differ in their `OneBounded` convention, their nonpretentiousness formulation and their averaging. OpenAI proves them in two separate developments.
- **Further implication.** The affine comparator implies both.
- **Lean.** `Fidelity.twoPoint_binary_iff_ordinaryElliott`, `Fidelity.binary_of_affine_corrected_elliott`, `Fidelity.ordinaryElliott_of_affine_corrected_elliott`.

### RD-2 · Ostmann comparators · **L**
- **Same proposition.** `OstmannPrimes.main` and `OstmannComplete.InverseGoldbach` are identical.
- **Implication.** `InverseGoldbach ⇒ TwoInfiniteSummandsImpossible`. The converse needs Dirichlet plus CRT and is not formalized here.
- **Lean.** `Fidelity.ostmann_main_iff_inverseGoldbach`, `Fidelity.twoInfiniteSummandsImpossible_of_inverseGoldbach`.

---

## Theoretical computer science · refereed

### TC-1 · Khot's 2-to-2 Games Conjecture with perfect completeness · **D** (implication already published)
- **Premise.** 105, "Perfect completeness for 2-to-1 games", Thm 1.1: "For every fixed rational δ∈(0,1) there are an integer q=q(δ)≥2 and a deterministic polynomial-time reduction from 3-SAT to 2-to-1 games with alphabets [2q] and [q] … Every table has exactly two preimages for each right answer."
- **Statement.** For every rational `δ′ ∈ (0,1)`, take `q = q(δ′/2)` from 105. Then there is a deterministic polynomial-time reduction from 3-SAT to unweighted bipartite 2-to-2 games with alphabet `[2q]` on both sides:
  - each constraint is `{(a,a′) : σ(a) = σ′(a′)}` for exactly-2-to-1 maps `σ, σ′ : [2q] → [q]`;
  - satisfiable formulas give value 1;
  - unsatisfiable formulas give value `≤ δ′`.
- **Derivation.**
  1. For each right vertex `v` and each ordered pair of its edges `e, e′`, put the constraint `π_e(a) = π_{e′}(a′)` between two **copies** of the left side, with weight `1/d_v`.
     - The two copies are needed: on a single copy the `e = e′` pairs would be trivially satisfied self-loops.
     - Each constraint matches the fibres of two exactly-2-to-1 maps, so it is 2-to-2 in Khot's sense.
  2. **Completeness** carries over.
  3. **Soundness.** The satisfied weight at `v` is `≤ max_b n′_v(b)`. Decoding `v` to that argmax gives `val(H) ≤ val(G)`.
  4. **Unweighting.** Use multiplicity `⌈D/d_v⌉` with `D = max d_v`. Since `D/d_v ≤ ⌈D/d_v⌉ ≤ 2D/d_v`, this at most doubles the value. Hence `δ = δ′/2`.
- **Already published as an implication.** This is the `d = 2` case of Dinur–Mossel–Regev (*SICOMP* 39 (2009); arXiv cs/0504062), Thm A.3, applied to 105. With completeness `1 − ε`, the 2-to-2 theorem is due to DKKMS, Barak–Kothari–Steurer (ECCC TR18-077) and Khot–Minzer–Safra (ECCC TR18-006; *Ann. Math.* 2023). The first edition cited TR18-077 as Khot–Minzer–Safra; it is Barak–Kothari–Steurer.
- **Unstated in the corpus.** "2-to-2" appears only in reference titles.

### TC-2 · 114's polymatroid FPRAS contains 115's contingency-table FPRAS · **D** (statement-level), sampling **Lead**
- **Derivation.**
  1. Set `r₁(A) = Σᵢ min(rᵢ, Σ_{j:(i,j)∈A} b_ij)`, and define `r₂` the same way over columns. Each is normalized, monotone, submodular and integer-valued.
  2. If some `rᵢ > Σ_j b_ij` or some `c_j > Σ_i b_ij`, then `Z = 0`. Otherwise `r₁(E) = r₂(E)`.
  3. `Ω(r₁, r₂)` is exactly the set of cell-bounded tables: singletons give the cell bounds, rows give the row bounds, and `x(E) = R` forces equality.
  4. So 114's Thm 1.1 contains 115's Thm 1.1.
- **Containment of statements only.** 114's proof imports the 115 companion's statements, and 114's introduction already presents itself as generalizing capacitated transportation.
- **Lead.** Almost-uniform sampling via Jerrum–Valiant–Vazirani.

### TC-3 · Deterministic construction of `𝔽_{p^n}`; deterministic factoring over `𝔽_{p^k}` · **D** (known given the input)
- **Premise.** 142, Thm 1.1: "O(((n+1)⌈log₂p⌉)^{10^{12}}) bit operations … uses no randomness, integer-factorization oracle, primitive-root oracle, or GRH assumption."
- **Statement.** Two consequences:
  - A degree-`n` irreducible polynomial over `𝔽_p` can be found deterministically in `poly(n log p)`.
  - Factoring over `𝔽_q = 𝔽_p[y]/(g)` is deterministic `poly(d, k, log p)`.
- **Derivation.**
  - **Construction.** Shoup, *Math. Comp.* 54 (1990) 435–447: finding irreducible polynomials of a given degree "is deterministic polynomial-time reducible to … factoring polynomials over the prime field". (This is not the Shoup 1990 *Inform. Process. Lett.* paper that 142 cites.)
  - **Factoring over `𝔽_q`.** Berlekamp, *Math. Comp.* 24 (1970):
    1. Take the squarefree part.
    2. Compute `B_p = ker(h ↦ h^p − h) ≅ 𝔽_p^r` by `𝔽_p`-linear algebra.
    3. Find the roots of the minimal polynomials of a basis with 142.
    4. Take gcds to split `f`. They separate every pair of factors.
- **Context.** Previous unconditional deterministic algorithms had `p^{1/2+o(1)}` dependence on the characteristic (Shoup). So both consequences are immediate from 142 by classical reductions.

### TC-4 · Directed APSP with small integer weights in `O(n^{2.5082})` · **D**
- **Premise.** 107, Thm 1.1 and Cors 14.1–14.2: over every characteristic-0 field, `α > 0.465` and `ω(1, 0.709, 1) < 2.092`.
- **Statement.** All-pairs shortest paths in **directed** graphs with integer weights in `{−M,…,M}`, `M = O(1)` and no negative cycles, can be solved in `Õ(n^{2+μ*}) ⊂ O(n^{2.5082})`, where `μ* = 10061/19800 = 0.508131…`.
- **Derivation.**
  1. `k ↦ ω(1,k,1)` is convex. 107 itself proves this in §2, and the fact is classical (Lotti–Romani).
  2. Interpolating between `(0.465, 2)` and `(0.709, 2.092)` with slope `23/61` gives `ω(1,μ,1) < 1 + 2μ` for `μ > μ*`.
  3. Zwick (*JACM* 49 (2002)) gives `Õ(n^{2+μ})` whenever `ω(1,μ,1) ≤ 1 + 2μ`.
- **Comparison.** The best previously published bound is `μ < 0.5275` (Alman–Duan–Vassilevska Williams–Xu–Xu–Zhou, arXiv:2404.16349). For undirected graphs, Shoshan–Zwick's `Õ(Mn^ω)` is already better.
- **Lead.** 107's full exponent curve (its eq. (12.12) at `t = 0.213`) would give `μ < 0.50346`, i.e. `O(n^{2.5035})`. That needs 107's characteristic-0 descent repeated for that scheme.

### TC-5 · 0/1 Knapsack in randomized `O(2^{0.49n})` · **D**
- **Statement.** For 0/1 Knapsack with `n` items and bit length `b ≤ n^c`, a randomized algorithm with error `≤ 1/3` runs in `O_c(2^{0.49n})` word-RAM time.
- **Derivation.**
  1. 138 Thm 1.1 gives Subset Sum for positive integers, success probability `≥ 2/3`, time `C_c 2^{0.49n}` for `b ≤ n^c`.
  2. Nederlof–van Leeuwen–van der Zwaan (arXiv:1208.4225, Thm 2) reduce Knapsack deterministically to Subset Sum with the same `n`, preserving `O*` time and space, using `O(n² lg²(nN))` queries.
  3. Query bit lengths are about `2b + log₂(n+1) + O(1)`, so still polynomial.
  4. Drop zero-weight items, since 138 needs positive integers.
  5. Amplify each query to error `1/(3K)`, where `K` is the number of queries, and take a union bound.
- **Space variant.** 138's low-space companion gives Knapsack in `O*(2^{n/2})` time and `O*(2^{n/5})` space.

### TC-6 · Tension sweep: none found
- **Families checked.** 102, 107, 109, 110, 117, 118, 124, 125, 129, 130, 132, 133, 138 and 141, against ETH, UGC, known lower bounds and barriers. All are consistent.
- **Shapes forced.** Some combinations force the shape of hard instances.
  - For 129's complementation bound, inductive counting means the hard inputs must be exponentially long.
  - For 129's 1NFA → 2DFA half, superpolynomially long inputs are needed unless NL ⊄ L/poly (Kapoutsis–Pighizzini).
- **Spot checks by the referee.**
  - 107 sits below the Christandl–Le Gall–Lysikov–Zuiddam cap on `α`.
  - 138 is consistent with ETH and with the Abboud–Bringmann–Hermelin–Shabtay bound.

### Lean confirmation (low novelty)
- Family 126's affine-lift comparator implies a superpolynomial lower bound on LP lifts of the perfect-matching polytope: an LP lift is a diagonal PSD lift. This is weaker than Rothvoss's exponential bound. Lean: `Fidelity.hasAffineLift_of_hasLPLift`, `Fidelity.lp_lift_lower_bound`.
- The nonnegative-rank analogue is drafted but not built: `MatchingPSD.lean` and `MatchingAffineLift.lean` declare the same names, so they cannot be vendored together.

---

## Combinatorics and logic · refereed

### CL-1 · Algebraic coordinates: Euclidean-Ramsey ⇔ spherical · **L** (new direction) · refereed
- **Premises.**
  - 172, `EuclideanRamsey.lean` `classification`: assume `2 ≤ s`, `1 ≤ d`, injective `a`, and `affineSpan ℝ (range a) = ⊤`. Then `a` is Ramsey iff some `P ∈ Mat_{Option (Fin d)}(F ⊗_ℚ F)` satisfies `Σ_{α,β} (p_iα ⊗ 1) P_αβ (1 ⊗ p_iβ) = 0` for all `i`, together with `m_F(P_αβ) = δ_αβ` for spatial `α, β`. Here `F` is the coordinate field.
  - The forward direction, Ramsey ⇒ spherical, is classical (Erdős–Graham–Montgomery–Rothschild–Spencer–Straus 1973, Thm 13); 172 also states it.
- **Statement.** A finite nonempty Euclidean set similar to a set with real-algebraic coordinates is Ramsey iff it is spherical. So Graham's spherical conjecture holds for all such sets, for example lattice points on a sphere, or any number of rational points on a circle.
- **Derivation.**
  1. **Reduction.** Ramsey and spherical are both similarity-invariant, and singletons are trivial. Otherwise, re-embed the set in its affine span by Gram–Schmidt over the real algebraic numbers, which form a real closed field. This gives full span, `d ≥ 1`, and `F` a number field.
  2. If the set is spherical, `‖a_i‖² + ℓ·a_i + c = 0`. Because the span is full, `(c, ℓ)` is the unique solution of an `F`-linear system, so `ℓ, c ∈ F` by Cramer's rule. That gives `H` with `p_iᵀ H p_i = 0` and spatial block `I`.
  3. **Separability idempotent.** Write `F = ℚ(θ)` and `f(X) = (X − θ)Σ b_k X^k`. Then `e = (f′(θ)^{−1} ⊗ 1)·Σ_k (b_k ⊗ θ^k)` satisfies `m(e) = 1` and `(1⊗x − x⊗1)e = 0`.
  4. `P = e·(H ⊗ 1)` satisfies both conditions. The referee checked this exactly in `ℚ(√2) ⊗ ℚ(√2)` for five points on a circle; without `e`, the first condition fails.
- **Consistency.** Every known spherical non-Ramsey set is transcendental:
  - 172's nine-point and twelve-point examples (algebraically independent parameters; Liouville's constant);
  - Pálvölgyi's heptagon (arXiv:2609.23327).

  This fits the mechanism: the obstructions come from derivations, and a number field has none.
- **Lean.**
  - `Fidelity.ramsey_of_cospherical_of_algebraic` proves spherical ⇒ Ramsey for algebraic coordinates, from OpenAI's `classification` alone (kernel-checked hypothesis). Helpers: `exists_sphere_coeffs`, `fieldCriterion_of_sphere`.
  - `ramsey_iff_cospherical_of_algebraic` is the ⇔ form. Its forward direction is taken as a hypothesis restated from `EuclideanRamseySpherical.lean`. That file cannot be vendored next to `EuclideanRamsey.lean` (both declare `OAI.EuclideanRamsey.Ramsey`), so this one hypothesis is not kernel-checked against OpenAI's file.
- **Unstated.** Neither the corpus nor the literature the referee could search states it.

### CL-2 · Consecutive off-diagonal Ramsey ratios: the sharp logarithmic exponent · **L** · refereed
- **Premise.** 170: `SharpLogRamsey.lean` `MainLimit s` for `s ≥ 6`, and `RamseyFive.lean` for `s = 5`. `MainLimit s` is `((s−1) log t − log r(s,t)) / log log t → s − 2`.
- **Statement.** For `s ≥ 5`, `r(s+1,t)/r(s,t) = t/(log t)^{1+o(1)}`. With `MainBounds`, for every `ε > 0` and all large `t`:

  `t/(C_s (log t)^{1+ε}) ≤ r(s+1,t)/r(s,t) ≤ C_{s+1}·t/(log t)^{1−ε}`.
- **Derivation.** Subtract `MainLimit s` from `MainLimit (s+1)`. The limits differ by `(s−1) − (s−2) = 1`.
- **Lean.**
  - `Fidelity.ramsey_log_ratio` (`s ≥ 6`) and `ramsey_log_ratio_five` (`s = 5`, after proving the two comparators' `ramsey` functions agree);
  - `ramsey_ratio_tendsto_atTop`, `ramsey_ratio_five_tendsto_atTop`.
- **Already known without the corpus.** The weaker facts that the ratio is `t^{1+o(1)}` and tends to infinity, for every `s ≥ 2`, follow from Bradač (arXiv:2605.28793) together with Ajtai–Komlós–Szemerédi. Only the `1 + o(1)` exponent on the logarithm, for `s ≥ 5`, needs 170.
- **Not the same as** Erdős problem #1014, which is about `R(k, l+1)/R(k, l) → 1`.

### CL-3 · The enumeration degrees are rigid · **D** (already known once 241 is granted)
- **Premise.** 241, `DegreeRigidity.lean`: every order automorphism of the Turing degrees is the identity.
- **Derivation.** This is exactly Cai–Ganchev–Lempp–Miller–Soskova (*JAMS* 29 (2016)), Corollary 3.8: "If the structure of the Turing degrees is rigid, then so is the structure of the enumeration degrees."
  1. The total degrees are definable (CGLMS 2016; Kalimullin 2003 supplied the K-pair tool).
  2. They form an order-isomorphic copy of `D_T`, via `deg_T(A) ↦ deg_e(A ⊕ Ā)`.
  3. Selman (1971): `A ≤_e B` iff every total degree above `B` is above `A`.
- **What is new.** Only that the corpus supplies the premise.

### CL-4 · Hilbert's tenth over ℤ under a finitely-many-zeros promise · **D**
- **Premise.** 242, Thm 1.1 and Cor 1.2: there are fixed `m, D` such that integer solvability is undecidable for polynomials promised to satisfy `#{w ∈ ℕ^m : F(w) = 0} ≤ 1`. Its §8 makes "no claim about analogous uniqueness promises for solutions over ℤ or ℚ."
- **Statement.** There are fixed `m′ = 4m` and `D′ = 2D` such that no algorithm decides integer solvability for `G ∈ ℤ[X₁…X_{m′}]` of degree `≤ D′` that is promised to have finitely many integer zeros.
- **Derivation.** Replace each `w_j` by a sum of four squares (Lagrange). The integer zeros then number `∏_j r₄(w_j)`, which is finite. The count is not uniformly bounded, so this says nothing about "at most one zero" over ℤ.

### CL-5 · Polyomino achievement games: exactly 12 winners · **Lead**
- **Claim.** Consider the weak (Maker–Breaker) achievement game on the infinite square board, with free polyominoes and no handicap. By 187 (Maker wins Snaky in 21 moves), exactly 12 polyominoes are winners:
  - the 11 classical winners: monomino; domino; I- and V-tromino; I-, L-, T- and Z-tetromino; L-, N- and Y-pentomino;
  - plus Snaky.
- **Scope.** Nothing is claimed for the strong game, which 187 explicitly excludes. The conditional "if Snaky wins, there are 12 winners" is classical.
- **To reach D.** Cite Harary (*Ann. Discrete Math.* 13 (1982)) and Gardner directly. The entry would then be "already known once 187 is granted".

### CL-6 · Logic and combinatorics tension checks: none found
- 004 vs Mazur's conjecture: 004 is a Turing reduction, not a Diophantine model. Its §1.3 yields degree `0′`, and it discusses the Mazur and Cornelissen–Zahidi obstructions explicitly.
- 240 vs the CH obstruction: compatible. This rests on 240's Thm 1.1(iii) (categoricity on the tail above `Λ`) and the text after Cor 6.1. The CH paper also notes it contradicts Espíndola's claimed transfer (arXiv:2301.13167v1) under CH. That is a tension with outside literature, not inside the corpus.
- 244: no family asserts PP ⇒ AC.
- 159/160 vs Behrend.
- 170 vs 184.
- Infinite vs finite matroids.
- 189, 165 vs known small values.
- **Dependency note.** 004 cites corpus papers by path. Fontaine–Mazur modularity at 2 (family 010) is an essential input ("The modularity input is [Thm 1.1]…"). The family-006 Goldfeld/2-converse paper appears only in a remark, as an optional replacement. So 004 depends on 010 but not on 006.

### Lean confirmations of content the corpus already states (not counted as corollaries)
- **Green–Tao.** The primes contain arbitrarily long arithmetic progressions, with first term above any bound. This follows from OpenAI's `ErdosReciprocal` comparator and Mathlib's `Σ 1/p = ∞`. Lean: `Fidelity.green_tao`, `green_tao_above`, `green_tao_infinite`. The paper says so in prose; the comparator does not state it.
- **The chromatic number of the plane is 6 or 7**, in both comparator formulations (ℂ and `EuclideanSpace ℝ (Fin 2)`). Lean: `Fidelity.planeChromaticNumber_eq_six_or_seven`, `complexChromaticNumber_eq_planeChromaticNumber`.

---

## Tensions checked (all areas)

**No internal contradictions were found.** Checks with real content:
- 196/197 (characteristic 2) vs 207 (characteristic 0) vs 285 (`C*_r`): consistent (GR-2, GR-4).
- 088's projection-body witnesses at `n = 20`: inside the Petty and Zhang–Santaló bounds (`R₂₀ = 9.19·10⁸ ∈ [3.54·10³, 5.07·10¹¹]`, recomputed by the referee).
- The TCS sweep (TC-6) and the logic sweep (CL-6).
- 195 vs 193/194.

**Removed as non-checks:**
- "7/8 ⊂ 11/12 ⊂ 1 − 10⁻⁶": zero-free claims cannot contradict each other.
- 046 vs 057 and Elek–Szabó: the corpus already handles these.
- "234 vs SK/Parisi": never computed.

## Summary

| Area | L | D | Lead |
|---|---|---|---|
| Number theory | NT-1, NT-2, NT-7 | NT-3, NT-5, NT-6, NT-8, NT-9 | NT-4 |
| Diophantine approximation | DA-1 | DA-2, DA-3 | — |
| Group rings, operator algebras | GR-1, GR-3, GR-11 | GR-2, GR-4, GR-5, GR-6, GR-7, GR-8, GR-9 | GR-10 |
| Algebraic geometry | — | AG-2, AG-3, AG-4 | AG-1 |
| Analysis, geometry, physics | GE-1, GE-8, GE-11 | GE-2, GE-3, GE-4, GE-5, GE-6, GE-7, GE-9 | GE-10 |
| Redundant comparators | RD-1, RD-2 | — | — |
| Theoretical CS | — | TC-1, TC-2, TC-3, TC-4, TC-5 | — |
| Combinatorics, logic | CL-1, CL-2 | CL-3, CL-4 | CL-5 |
| **Total (50)** | **14** | **31** | **5** |

Some entries are not new to the literature even though they are correct:
- **D, known once the corpus input is granted:** GR-8, GE-5, GE-6, TC-3, CL-3; TC-1's implication is already published (Dinur–Mossel–Regev).
- **L, not new mathematics:** GE-11, GR-11.

Each of these entries says so.

## Review history
- **External review of commit `77ab999`.** Four findings, all fixed:
  - the axiom checker matched counts, not names, and could miss Lean errors;
  - the old `W` tier overstated sketches;
  - the animation omitted conditionality;
  - the π statement claimed `μ = 2` but proved only the upper bound. The equality is now a Lean theorem (DA-1).

  The review also narrowed NT-9.
- **Independent referee pass (two agents) on every first-edition entry.**
  - Nothing was found wrong.
  - Two citations were corrected: GR-8 (Isono) and GR-9 (Davis–Leary).
  - Three items moved to "already in the corpus/literature": old NT-10, old AG-3 and most of AG-1.
  - About 25 entries were upgraded from Lead to D, with full derivations.
- **Second referee pass (two agents) on the final-pass entries (TC, CL).**
  - Nothing was found wrong.
  - Corrections:
    - TC-1's ECCC citation (TR18-077 is Barak–Kothari–Steurer; Khot–Minzer–Safra is TR18-006), and the note that DMR Thm A.3 already gives the implication;
    - TC-4 is for directed graphs, with exact `μ*` and a verified improvement over `μ < 0.5275`;
    - TC-5's bit-length accounting;
    - CL-3 is CGLMS 2016 Cor 3.8;
    - CL-2's weaker forms follow from Bradač + AKS;
    - 004 depends on family 010, not on 006.
