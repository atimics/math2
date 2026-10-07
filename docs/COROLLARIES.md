# Cross-family corollaries of openai/math

Source corpus: [`openai/math@adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a), 722 manuscripts in 372 families.
**Every corpus result is treated as a claim by OpenAI.** Every corollary below is conditional on the claims it cites.

"Unstated" means we grepped `CONTENTS.md`, `overview.tex`, the cited papers' text and `.tex` sources, and the Lean docs, and found nothing. It does **not** mean the result is new to the wider literature. Several items are already known once you grant the corpus input, and we say so where we know it.

## Evidence tiers

| Tier | Meaning |
|---|---|
| **L** | Proved in Lean in this repo (`Corollaries/`, `Fidelity/`). The hypotheses are OpenAI's comparator statements, checked equal to OpenAI's types in the kernel. The CI audit accepts only `propext`, `Classical.choice` and `Quot.sound`. |
| **W** | Written derivation. Every step is either a corpus claim, a cited classical theorem, or elementary. Not formalized. |
| **W?** | Written derivation in which at least one bridge step is plausible but not checked line by line. Treat as a lead, not a result. |

---

## Number theory

### NT-1 · The Landau–Siegel paper is a corollary of the 7/8 paper · **L**
- **Statement.** `DirichletSevenEighths` implies OpenAI's `SiegelZeros` comparator in both of its forms, with explicit `c = log 3 / 8`. It also gives the stronger uniform gap: every real zero of every nontrivial Dirichlet `L`-function, of any modulus, satisfies `β ≤ 7/8`. No primitivity or reality is assumed.
- **Lean.** `Corollaries.real_zero_le_seven_eighths`, `Corollaries.siegel_of_sevenEighths`, `Fidelity.siegel_comparator_of_sevenEighths` and `Fidelity.siegel_comparator'_of_sevenEighths`.
- **Why it matters.** "Uniform exclusion of Landau–Siegel zeros" (Oct 1) has its own interpolation-determinant proof, does not cite the Sept 30 7/8 paper, and its Lean doc says "no explicit value of c is given". Inside the corpus, the second paper adds nothing beyond a lemma the first already implies.

### NT-2 · The zeta comparator is the modulus-1 case · **L**
- **Statement.** `DirichletSevenEighths` implies `QuasiRiemannHypothesis.lean` (ζ(s) ≠ 0 for Re s > 7/8).
- **Lean.** `Corollaries.zeta_of_sevenEighths`, `Fidelity.zeta_comparator_of_sevenEighths`.

### NT-3 · A third, independent route to Siegel · **W**
- **Statement.** Theorem 1.2 of family 029 gives Hecke L-functions over cyclotomic `F ⊇ μ₁₂` no zeros in `Re s > 1 − 10⁻⁶`. Factoring over `Q(μ₁₂q)` (Artin formalism) makes every Dirichlet `L`-function zero-free there. So the Siegel comparator also holds with `c = 10⁻⁶·log 3`, independently of family 003.
- **Further consequence (W).** Via Kronecker–Weber and Aramata–Brauer, `ζ_K(s) ≠ 0` for `Re s > 1 − 10⁻⁶` uniformly, for every number field with metabelian Galois closure.
- **Unstated.** The Artin paper descends only to its Kummer fields (§9.1).

### NT-4 · Least primitive root `g(p) = p^{o(1)}`, effectively · **W**
- **Statement.** The 7/8 half-plane gives the following via character detection, the explicit formula (error `x^{7/8}`) and `2^{ω(p−1)} = p^{o(1)}`.
  - `g(p) ≤ exp(C log p / log log p)`.
  - The best unconditional bound in the literature is about `p^{1/4+ε}` (Burgess).
- **Unstated.** The 7/8 paper derives least quadratic nonresidues and deterministic square roots, but not primitive roots.

### NT-5 · 7/8 for Dedekind zeta of pure cubic fields · **W?**
- **Statement.** `ζ_{Q(∛m)} = ζ · L_F(s, χ)` with `F = Q(√−3)` and `χ` cubic. Combined with OpenAI's `HeckeSevenEighths`, this gives no zeros in `Re s > 7/8`. Consequences:
  - effective Brauer–Siegel for these fields;
  - Chebotarev in `Q(ζ₃, ∛m)` with error `x^{7/8+ε}`.
- **Unchecked.** That the comparator's `Character` structure covers all ray-class characters is OpenAI's claim, not checked here.

### NT-6 · Artin's conjecture for bases 10 and 2 · **W**
Family 029, Theorem 1.1, with `a = 10` and `a = 2` gives `≫ x/(log x)²` primes in `(x, 2x)` with each of the following:
- `1/p` has decimal period `p − 1` (full-reptend primes);
- `1 + X + … + X^{p−1}` is irreducible over `𝔽₂`, so `𝔽_{2^{p−1}}` has a type-I optimal normal basis (Lidl–Niederreiter, Thm 2.47).

Neither is stated.

### NT-7 · Liouville parity densities · **W** (Lean target)
- **Statement.** From family 007's two-point Chowla theorem, for any non-proportional affine forms there is a power-of-log rate in

  `#{n ≤ X : Ω(a₁n+b₁) ≡ Ω(a₂n+b₂) (mod 2)} = X/2 + O(X/(log X)^c)`.

  For example, `Ω(n)` and `Ω(n+1)` agree in parity for exactly half of all `n`.
- **Proof idea.** Pointwise `1[same parity] = (1 + λλ′)/2`.
- **Not yet in Lean.** It needs OpenAI's `affineSum` definitions vendored.

### NT-8 · Sums of two rational cubes: at least 47.92% of integers · **W?**
- **Statement.** Koymans–Smith (arXiv:2405.09311, Cor 1.8) assume "`r₃ = 1` ⇒ rank 1". Family 002's Selmer `p`-converse at `p = 3`, via Cassels–Tate parity, supplies that assumption.
- **Unchecked.** Their normalisations, and `dim E′(ℚ)[3] = 1` for every `n`.

### NT-9 · BSD for at least 83.75% of elliptic curves ordered by height · **W?**
- **Statement.** If Bhargava–Shankar's 83.75% is a proportion with `dim Sel₅ ≤ 1`, family 002's hypothesis-free corank-≤1 converse upgrades it to full BSD. The best previous proportion is 66% (Bhargava–Skinner–Zhang).
- **Hinges on.** The Bhargava–Shankar normalisation, which we could not open (the network proxy blocked it).

### NT-10 · Congruent numbers · **W** (known given the corpus input)
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

### DA-1 · `μ(rπ + s) = 2` and `π` is not Liouville · **L**
- **Statement.** For `r, s ∈ ℚ` with `r ≠ 0` and every `p > 2`, `¬ LiouvilleWith p (π·r + s)`, and `¬ Liouville π`.
- **Lean.** `Corollaries.pi_not_liouvilleWith`, `Corollaries.rat_affine_pi_not_liouvilleWith`, `Corollaries.pi_not_liouville`.
- "Not Liouville" was already known from Mahler (1953). The exponent-2 statements for `rπ + s` are new consequences of the corpus claim.

### DA-2 · The Cookson Hills series converges · **W**
- **Statement.** `Σ sec²(n)/n³ < ∞`. More generally, `Σ n^{-a}|cos n|^{-b}` and `Σ n^{-a}|sin(rn)|^{-b}` converge iff `a > max{1, b}`.
- **Bridge.** `|cos n| ≥ ‖(2k+1)π‖/π` for the nearest half-integer multiple, then the paper's own dyadic spacing lemma.
- **Divergence for cos.** Uses Minkowski's inhomogeneous theorem.
- **Unstated.** `grep -i cookson` over the whole repo returns nothing.

### DA-3 · Discrepancy `O(N^{−1+ε})` for `n mod 2π` · **W**
- **Statement.** Exponent 2 means type 1, so Kuipers–Niederreiter Thm 2.3.2 and Koksma's inequality give, for example:
  - `Σ_{n≤N} sgn(sin n) = O(N^ε)`;
  - `Σ_{n≤N} |sin n| = (2/π)N + O(N^ε)`.
- **Previous bound.** The exponent bound 7.11 gave only about `N^{−0.16}`.

---

## Group rings and operator algebras

### GR-1 · Kaplansky's counterexample survives every field extension · **L**
- **Statement.** For every ring map `K →+* L` out of OpenAI's finite field, `L[G]` is not directly finite. In particular this holds for `L = 𝔽̄₂`.
- **Lean.** `Corollaries.directFiniteness_transfer`, `Fidelity.kaplansky_transfer`.
- **Extension (W).** Stable finiteness fails over *every* characteristic-2 field, including `𝔽₂` and `𝔽₂(t)`, via `m × m` matrices with `m = [K:𝔽₂]`. The same group is stably finite over every characteristic-0 field.

### GR-2 · The torsion-free counterexample also breaks the idempotent conjecture in characteristic 2 · **L** (ring step) + **W**
- **Statement.** The torsion-free family-197 paper gives `ab = 1`, `ac = 0`, `c ≠ 0` in `𝔽₂[G]`. Then `ba` is an idempotent other than 0 and 1.
- **Consequences.**
  - That one theorem implies family 196's whole headline: zero divisors in `𝔽₂[G]` for a finitely presented torsion-free group.
  - It shows family 207's characteristic-0 hypothesis (idempotent conjecture for torsion-free groups) is sharp.
  - It gives an injective, non-surjective cellular automaton on a torsion-free finitely presented group, against Gottschalk.
- **Lean.** `Corollaries.idempotent_of_directFiniteness_witness` (the ring-theoretic step). The torsion-free paper has no comparator, so the input is not formalized.

### GR-3 · Family 196's group is not left-orderable · **L**
- **Statement.** It is not left-orderable.
- **Lean.** `Fidelity.zeroDivisor_group_not_leftOrderable`, via Mathlib's `UniqueProds ⇒ NoZeroDivisors`.
- **Classical consequences (W).** Not locally indicable (Burns–Hale), not bi-orderable, and not a subgroup of any right-angled Artin group.

### GR-4 · Kadison–Kaplansky counterexample vs ℓ¹: consistent · **W**
- **Statement.** Family 207's ℓ¹-Bass theorem gives integer traces on `K₀(ℓ¹(G))` for torsion-free `G`, so `ℓ¹(G)` has no idempotents other than 0 and 1. Family 285's projection, with trace in `(0, ½)`, therefore lies outside the image of `K₀(ℓ¹ G) → K₀(C*_r G)`.
- **Tension check.** We found no contradiction between 285 and 207. The failure sits in the ℓ¹ → C*_r comparison.

### GR-5 · Thompson's groups `F` and `T` are C*-simple · **W**
- **Statement.** Family 248 (F is nonamenable) plus Le Boudec–Matte Bon (2018) give that both are C*-simple with unique trace.

### GR-6 · `L(F₂)` realizes every subfactor standard invariant · **W**
- **Statement.** Family 287 (`L(F_∞) ≅ L(F₂)`) plus Popa–Shlyakhtenko (2003) give that every standard invariant is realized in `L(F₂)`. Also `L(F₂) ≅ L(F₂) * L(F₂)`.

### GR-7 · Connes–Shlyakhtenko L²-Betti numbers of `L(F_r)` are 0 or ∞ · **W?**
- **Statement.** Fundamental group `ℝ>0` (family 287), with the compression formula `β_k(pMp) = β_k(M)/τ(p)²`, forces `β_k ∈ {0, ∞}`. This refutes the heuristic `β₁(L(F_n)) = n − 1`.

### GR-8 · Haagerup–Størmer for all separable type III₁ factors · **W?**
- **Statement.** Family 290 (trivial bicentralizer) plus Marrakchi (arXiv:2309.05279, Cor B) give this.

### GR-9 · Artin groups: unconditional invariants · **W**
- **Statement.** Family 254 (`K(π,1)` for all finite-rank Artin groups) discharges the hypothesis of Davis–Okun and related results. This gives:
  - L²-Betti numbers;
  - `χ(A) = Σ_{T spherical} (−1)^{|T|}`;
  - `cd A = max{|T| : W_T finite}` (the last one W?).

### GR-10 · The nonsofic group and Aldous–Lyons · **W?**
- **Follows.** Family 197's group gives an explicit finitely presented counterexample to the marked-network Aldous–Lyons conjecture.
- **Does not follow.** Whether the group is hyperlinear. Its direct-finiteness failure in characteristic 2 says nothing over ℂ.

---

## Algebraic geometry

### AG-1 · Tate for products of curves over finite fields, and all four standard conjectures for abelian varieties · **W?**
- **Statement.**
  - Family 032's Tate result, through Künneth motives of curves, gives Tate and `num = hom` for products of curves.
  - Tate's 1994 Thm 2.9 then gives the zeta pole-order form.
  - With the classical B and C, all four standard conjectures hold for abelian varieties.

### AG-2 · Hodge for Hilbert schemes of points on any K3 · **W**
- **Statement.** Family 032 (products of K3s) plus de Cataldo–Migliorini's motivic decomposition of `S^{[n]}` give the Hodge conjecture for `S^{[n]}` and their products.

### AG-3 · Compact Kähler log abundance is unconditional inside the corpus · **W**
- **Statement.** Assumption 1.1 of family 034's Kähler paper is word for word Corollary `spec:logarithmic` of family 033. Family 033's title and abstract still call it conditional. Two Kähler-fourfold papers are subsumed as main theorems, though they remain lemma inputs.
- **Circularity.** None found.

### AG-4 · Three projective MMP papers are special cases · **W**
- **Statement.** The fourfold nonvanishing and "lifting sections" papers (and probably the numerical-dimension-one paper) are special cases of "Log abundance in characteristic zero".

### AG-5 · Effective log Iitaka in every dimension · **W?**
- **Statement.** It follows by combining the `d ≥ 5` paper, the `d = 4` paper and Chen–Han–Liu (`d ≤ 3`).

---

## Analysis, geometry and physics

### GE-1 · Bourgain–Milman with the optimal dimension-free constant · **W** (Lean target)
- **Statement.** Symmetric Mahler gives `|K||K°| ≥ (2/π)ⁿ κₙ²`, and general Mahler gives `(e/2π)ⁿ κₙ²`. Both constants are optimal as `n → ∞`.
- **Bridge.** Legendre duplication plus log-convexity of Γ.
- **In the corpus.** Bourgain–Milman appears only as history.

### GE-2 · Lattice transference `λ₁(K)λ₁(K°) ≤ (n!)^{1/n} ≈ n/e` · **W** (Lean target)
- **Statement.** Mahler plus Minkowski's first theorem (in Mathlib) give this. The trivial bound is `(n!)^{2/n}`.

### GE-3 · Symplectic ball rigidity · **W**
- **Statement.** If `int K × int K°` embeds symplectically in `B(4)`, then `K` is a linear Hanner body (Liouville volume plus Mahler's equality case).
- **In the corpus.** The symplectic paper explicitly makes no equality-case claim.

### GE-4 · Isotropic constant `L_K < 1/e` in every dimension, sharp · **W**
- **Statement.** Family 101's simplex bound `b(n)` satisfies `b(n) < 1/e`, with `b(n) → 1/e`.

### GE-5 · Sharp functional isotropic constant · **W**
- **Statement.** `‖f‖∞² det Cov f ≤ 1` for log-concave densities. It follows from family 101 and Bobkov–Madiman.

### GE-6 · Aubin's sharp Sobolev conjecture on Cartan–Hadamard manifolds · **W?**
- **Statement.** Family 337 (κ = 0) plus Pólya–Szegő and Aubin–Talenti give it.

### GE-7 · Falconer for analytic (Borel) sets · **W**
- **Statement.** Family 073 is stated for compact sets. Davies–Howroyd compact-subset approximation extends it to analytic sets.

### GE-8 · Scalar Hénon–Lane–Emden Liouville theorem · **W** (one line given OpenAI's system theorem)
- **Statement.** Set `u = v` in family 370's `HenonEmden` comparator.

### GE-9 · Lieb–Thirring near-sharp constants in all dimensions · **W?**
- **Statement.** Family 262's matrix constant plus Laptev–Weidl lifting give the near-sharp constants, assuming an operator-valued extension of 262 that we have not checked.

### GE-10 · Pure-loss trade-off regions become unconditional · **W?**
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

## Coverage

Fully mined: number theory, algebraic and complex geometry, algebra, analysis, PDE, mathematical physics, group theory, operator algebras, topology, dynamics, differential and convex geometry, probability. That is 289 of 372 families.

**Not yet mined:** theoretical computer science, combinatorics and logic (83 families). The mining pass for that shard was cut off by a session limit.
