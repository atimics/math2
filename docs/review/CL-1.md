# CL-1 · Algebraic coordinates: Euclidean Ramsey ⇔ spherical — review packet

**Reviewer profile:** Euclidean Ramsey theory, or commutative algebra for the tensor step.
**Time:** 20–40 minutes. The algebraic bridge is five lines.
**Catalogue entry:** [CL-1](../COROLLARIES.md#cl-1).
**Tier:** L. For full-span configurations it is now **proved in Lean end to end**. Our
proof is composed with OpenAI's own Lean proof of family 172, so no unproved premise
remains, only the theorem's side conditions. The axiom audit accepts only standard axioms.

## The claim

Let `A ⊂ ℝ^n` be a finite nonempty set that is similar to a set with real-algebraic
coordinates. Then **`A` is Euclidean Ramsey if and only if `A` lies on a sphere.**

In particular, every finite set of rational points on a circle is Ramsey, however many
points it has. Examples include any subset of
`{(±1,0), (0,±1), (±3/5,±4/5), (±4/5,±3/5)}` and of the rational points of `x² + y² = 1`.

Graham conjectured that every spherical set is Ramsey. Pálvölgyi's heptagon and family
172's examples show this fails in general. CL-1 says it holds whenever the coordinates are
algebraic. Every known spherical non-Ramsey set uses transcendental coordinates.

What family 172 states without us:

- every subtransitive set is Ramsey;
- every set of at most five points on a circle is Ramsey (Cor 7.4);
- a spherical set whose quadratic evaluation rows are `F`-linearly independent is Ramsey
  (Prop 7.3).

Six or more points on a circle never satisfy Prop 7.3's hypothesis. The rows lie in the
6-dimensional space spanned by `1, x, y, x², xy, y²`, and the circle's equation is a
nonzero linear functional vanishing on all of them, so their rank is at most 5. The
reproducer shows one instance.

## Questions for you

1. **Fidelity.** Is `OAI.EuclideanRamsey.Ramsey` (quoted below) the standard notion? We
   read it as: for every `r ≥ 2` there is `D ≥ 1` such that every `r`-coloring of `ℝ^D`
   has a monochromatic congruent copy. The colorings are arbitrary. `D ≥ 1` and `r ≥ 2`
   are harmless normalizations.
2. **The unformalized part of step 1.** Lean covers configurations with full affine
   span. OpenAI's Lean already handles singletons, congruence invariance
   (`ramsey_congruent_iff`) and the full-span re-embedding (`full_affine_representative`).
   Three pieces remain written, not formalized: invariance under scaling, sphericity of
   the re-embedded copy, and the choice of a re-embedding with *algebraic* coordinates.
   Upstream re-embeds with `stdOrthonormalBasis`, which need not be algebraic. Are these
   three pieces right?
3. **Novelty.** Is "algebraic and spherical ⇒ Ramsey, given 172's criterion" known, or
   does it appear in Pálvölgyi's paper or Leader–Russell–Walters? Are finite sets of
   rational points on a circle known to be subtransitive? If they were, the
   rational-points corollary would already follow from classical results.
4. **Consistency.** Do you know of any spherical non-Ramsey set with algebraic
   coordinates? Given the end-to-end Lean proof, such a set would mean either a definition
   mismatch (Q1) or a Lean or Mathlib soundness bug.
5. **Optional.** In this picture the obstructions come from derivations of the coordinate
   field, and a number field has none. Is this the right lens for a full characterization
   (as in 172's §7 examples)?

## Premises, verbatim

**P1. OpenAI family 172**, *A classification of finite Euclidean Ramsey configurations*.
Source:
`preprints/A-classification-of-finite-Euclidean-Ramsey-configurations-September-23-2026/paper.pdf`,
§1.1 (definitions and Thm 1.1) and §7 (Prop 7.3, Cor 7.4).

> Define p_i = (1, a_i), F = Q((a_i)_α : 1 ≤ i ≤ s, 1 ≤ α ≤ d), B = F ⊗_Q F. The
> commutative ring B has a multiplication homomorphism m_F : B → F, m_F(x ⊗ y) = xy.
>
> **Theorem 1.1** (Classification). Let A = {a_1, …, a_s} ⊂ R^d be a finite set of at least
> two points with affine span R^d, and define p_i, F, B, m_F as above. Then A is Ramsey if
> and only if there is a matrix P ∈ Mat_{d+1}(B) such that
> (p_i ⊗ 1)^T P (1 ⊗ p_i) = 0 (1 ≤ i ≤ s), (1)
> m_F(P_αβ) = δ_αβ (1 ≤ α, β ≤ d). (2)
>
> **Proposition 7.3.** Let A = {a_1, …, a_s} ⊂ R^d be spherical and affinely span R^d. …
> If the s row vectors (p_iα p_iβ)_{0≤α,β≤d} (1 ≤ i ≤ s) are linearly independent over F,
> then A is Ramsey.
>
> **Corollary 7.4.** Every nonempty set of at most five distinct points on a circle is
> Ramsey.

On Pálvölgyi's heptagon: 172 says its own twelve-point example's "weighted cancellation
is related to the derivation obstruction in Pálvölgyi's smaller circular example
[20, Theorem 1]". A nonzero derivation of `F` exists only when `F` is transcendental
over ℚ.

**P2. OpenAI's Lean statements** (`lean/ComparatorChallenges/EuclideanRamsey.lean` and
`EuclideanRamseySpherical.lean`):

```lean
def Ramsey {s d : ℕ} (a : Fin s → Space d) : Prop :=
  ∀ r : ℕ, 2 ≤ r → ∃ D : ℕ, 1 ≤ D ∧
    ∀ c : Space D → Fin r, ∃ b : Fin s → Space D,
      Congruent a b ∧ ∃ k : Fin r, ∀ i, c (b i) = k

theorem classification {s d : ℕ} (a : Fin s → Space d)
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (hspan : affineSpan ℝ (Set.range a) = ⊤) :
    Ramsey a ↔ FieldCriterion a

theorem ramsey_cospherical {s d : ℕ} (a : Fin s → Space d)
    (ha : Function.Injective a) (hR : Ramsey a) :
    EuclideanGeometry.Cospherical (Set.range a)
```

Here `Space d = EuclideanSpace ℝ (Fin d)`, and `Congruent a b` means
`∀ i j, dist (b i) (b j) = dist (a i) (a j)`.

**P3. OpenAI's proofs.** Both theorems are proved in OpenAI's Lean project, in
`lean/OAI/Combinatorics/EuclideanRamsey/Main.lean` and `Spherical.lean`.
`formalization.yaml` lists `classification`. `ramsey_cospherical` is linked from
`ComparatorChallenges/EuclideanRamseySpherical.json` and `lean/docs/172.md`. The two
theorems' import closure is 31 files and about 6,700 lines. It imports only Mathlib and
contains no `sorry`, `axiom`, `admit` or `native_decide`.

## The bridge, step by step

1. **Reduction** (partly in OpenAI's Lean; see Q2). Ramsey and spherical are both invariant under
   similarity: rescale the coloring. Singletons are trivial. Otherwise translate `a₁` to
   0 and run Gram–Schmidt on a basis chosen from the `aᵢ − a₁`. The real algebraic numbers
   form a real closed field, so the square roots stay inside it. This gives a congruent
   copy in `ℝ^d` with full affine span, `d ≥ 1`, and algebraic coordinates, so `F` is a
   number field.
2. **The sphere is defined over `F`.** If `‖aᵢ‖² + ℓ·aᵢ + c = 0` for all `i` with real
   `ℓ, c`, then `(ℓ, c)` solves an `F`-linear system with a unique solution, because the
   span is full. So `ℓ, c ∈ F`. (The Lean proof uses an `F`-linear projection `ℝ → F`
   instead.) This gives `H ∈ Mat_{d+1}(F)` with `pᵢᵀ H pᵢ = 0` for all `i` and spatial
   block `I`.
3. **The separability idempotent.** `F/ℚ` is finite and separable, so there is
   `e ∈ F ⊗_ℚ F` with `m(e) = 1` and `(x ⊗ 1)e = (1 ⊗ x)e` for all `x ∈ F`. For
   `F = ℚ(θ)` with minimal polynomial `f = (X − θ)Σ b_k X^k`, take
   `e = (f′(θ)^{−1} ⊗ 1) Σ_k b_k ⊗ θ^k`. In Lean this is Mathlib's
   `Algebra.FormallyUnramified.iff_exists_tensorProduct`.
4. **`P = e·(H ⊗ 1)` satisfies (1).** For `x, y ∈ F`,
   `e·(x ⊗ y) = e(x ⊗ 1)(1 ⊗ y) = e(y ⊗ 1)(x ⊗ 1) = e·(xy ⊗ 1)`. Hence
   `Σ (p_iα ⊗ 1) e (H_αβ ⊗ 1)(1 ⊗ p_iβ) = e·(Σ p_iα H_αβ p_iβ ⊗ 1) = e·(pᵢᵀ H pᵢ ⊗ 1) = 0`.
5. **`P` satisfies (2).** `m(e·(H_αβ ⊗ 1)) = m(e)·H_αβ = H_αβ = δ_αβ` on the spatial block.

By 172's Theorem 1.1, `A` is Ramsey. The converse, Ramsey ⇒ spherical, is classical
(Erdős–Graham–Montgomery–Rothschild–Spencer–Straus 1973, Thm 13) and is OpenAI's
`ramsey_cospherical`.

## Lean, layer by layer

| Declaration | What it proves | Hypotheses |
|---|---|---|
| `Fidelity.ramsey_of_cospherical_of_algebraic` | spherical ⇒ Ramsey, for algebraic coordinates with full span | OpenAI's `classification`, with its type checked by the kernel against the vendored comparator |
| `FidelityAlt.ramseyCosphericalStatement_iff_comparator` | our restated forward hypothesis is equivalent to OpenAI's `ramsey_cospherical` | none; built separately because the two comparator files clash |
| **`EndToEnd.algebraic_ramsey_iff_cospherical`** | **Ramsey ⇔ spherical**, for algebraic coordinates with full span | **no unproved premise**: both directions use OpenAI's proofs, rebuilt here. The side conditions `s ≥ 2`, `d ≥ 1`, injectivity, full span and algebraicity remain |
| **`EndToEnd.ramsey_of_cospherical_of_rational`** | rational coordinates, spherical, full span ⇒ Ramsey | **no unproved premise** |

CI checks the following on every push (see the
[Lean workflow](https://github.com/atimics/math2/actions/workflows/lean.yml)):

- the 31 upstream proof files are byte-identical to `openai/math@adc7f12` and free of `sorry`;
- their definitions of `Space`, `Congruent`, `Ramsey`, `coordinateField`, `Coeff`,
  `TensorRing`, `coordinate`, `augmented`, `multiply` and `FieldCriterion` are
  byte-identical to the comparator's, and they state `classification` and
  `ramsey_cospherical` as the comparators do (identical up to whitespace);
- the proof block in `EndToEnd/AlgebraicRamsey.lean` is a verbatim copy of the one in
  `Fidelity/AlgebraicRamsey.lean`;
- `scripts/AxiomsEndToEnd.lean` accepts only `propext`, `Classical.choice` and `Quot.sound`,
  through both `#assert_standard_axioms` and `check_axioms.py`. This also covers OpenAI's
  `classification` and `ramsey_cospherical` themselves.

## How it could fail, most likely first

1. **The unformalized part of step 1 is wrong (Q2).** This would affect only
   configurations whose algebraic coordinates do not already span. It is the only
   mathematical content outside Lean.
2. **Lean's `Ramsey` is not the intended notion (Q1).** The Lean theorem would then be
   true but about something else. We read the definition as the standard one.
3. **Novelty (Q3).** The result may be known or folklore once 172's criterion is
   available. That would affect credit, not truth.
4. **A soundness bug in Lean, Mathlib or our build.** We consider this negligible. Note
   that the end-to-end theorem does *not* depend on 172's paper being right, only on its
   Lean proof.

## Reproduce

```sh
pip install sympy
python3 scripts/review/cl1_idempotent.py
```

The script uses `F = ℚ(√2)` and six points on the circle `(x − √2)² + y² = 1`. It works in
`F ⊗ F = ℚ[X,Y]/(X² − 2, Y² − 2)`. Expected output:

```
Prop 7.3 row rank = 5 < 6 points: neither 172's Prop 7.3 nor its Cor 7.4 (<= 5 points) applies
e = X*Y/4 + 1/2:  m_F(e) = 1 and (X - Y) e = 0
P = e*(H(x)1): condition (1) values = [0, 0, 0, 0, 0, 0]; condition (2) holds = True
naive P = H(x)1 (no idempotent): condition (1) values = [-X*Y - X + Y + 2, -X*Y + 2, -X*Y + 3*X/5 - 3*Y/5 + 2, -X*Y - 3*X/5 + 3*Y/5 + 2, -X*Y + 2, -X*Y + 4*X/5 - 4*Y/5 + 2]
OK: the criterion holds with the idempotent, and the naive choice fails;
so this 6-point algebraic circle set is Ramsey by 172's Theorem 1.1 itself.
```

The set may or may not be subtransitive (172's Cor 7.2). The script does not decide that.

To rebuild the Lean proof end to end (needs the Mathlib cache):

```sh
lake exe cache get
lake build UpstreamEuclideanRamsey EndToEnd
lake env lean scripts/AxiomsEndToEnd.lean
python3 scripts/check_same_text.py
```

## Status

- **Literature.** 172 covers subtransitive sets, at most five cocircular points, and
  independent quadratic rows. Kříž, Cantwell, and Frankl–Rödl cover soluble transitive
  sets, regular polytopes and simplices. We found no statement covering arbitrary
  algebraic spherical sets, or arbitrary finite sets of rational points on a circle.
- **Negative examples, all transcendental:**
  - 172's nine-point set (algebraically independent parameters);
  - its twelve-point set (the Liouville constant `Σ 10^{−m!}`; OpenAI's `GrahamSpherical`
    comparator);
  - Pálvölgyi's heptagon, arXiv:2609.23327, which 172 describes as a derivation obstruction.
