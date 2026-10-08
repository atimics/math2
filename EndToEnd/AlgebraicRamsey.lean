import Mathlib
import OAI.Combinatorics.EuclideanRamsey.Main
import OAI.Combinatorics.EuclideanRamsey.Spherical

/-!
# CL-1 end to end: no hypotheses left

This file composes our CL-1 proof with **OpenAI's own Lean proof** of family 172.

* `OAI/Combinatorics/EuclideanRamsey/` holds byte-identical copies of the 31 upstream
  files (`openai/math` `lean/OAI/Combinatorics/EuclideanRamsey/`, Apache-2.0) that prove
  `OAI.EuclideanRamsey.classification` and `OAI.EuclideanRamsey.ramsey_cospherical`.
  They use Mathlib only and contain no `sorry`. CI diffs them against upstream and
  rebuilds them here.
* The block `namespace Fidelity … end Fidelity` below is copied verbatim from
  `Fidelity/AlgebraicRamsey.lean`, and CI checks the bytes. There it is elaborated
  against the vendored comparator. Here it is elaborated against OpenAI's proof files,
  whose definitions of `Space`, `Congruent`, `Ramsey`, `coordinateField`, `Coeff`,
  `TensorRing`, `coordinate`, `augmented`, `multiply` and `FieldCriterion` are
  byte-identical to the comparator's (also checked in CI).
* `EndToEnd.algebraic_ramsey_iff_cospherical` then discharges both hypotheses with
  OpenAI's proofs. Its axiom audit (`scripts/AxiomsEndToEnd.lean`) accepts only
  `propext`, `Classical.choice` and `Quot.sound`.

So, given Lean and Mathlib, CL-1 is a theorem rather than a conditional. For a
configuration with algebraic coordinates, at least two points and full affine span,
being Euclidean Ramsey is equivalent to being spherical. One step is still not
formalized: reducing an arbitrary algebraic configuration to a full-span algebraic
representative (catalogue entry CL-1, step 1).
-/

namespace EndToEnd

namespace Fidelity

open OAI.EuclideanRamsey (Space Ramsey Coeff coordinate augmented coordinateField
  FieldCriterion)
open scoped TensorProduct

/-! ## The sphere matrix -/

/-- The matrix of `x ↦ |x|² − 2⟨y, x⟩ + z` in augmented coordinates `(1, x)`: rows and
columns are indexed by `Option (Fin d)`, `none` being the constant coordinate. -/
def sphereMatrix {d : ℕ} {K : Type*} [Field K] (y : Fin d → K) (z : K) :
    Option (Fin d) → Option (Fin d) → K
  | none, none => z
  | none, some k => -2 * y k
  | some _, none => 0
  | some j, some k => if j = k then 1 else 0

theorem sphereMatrix_row_some {d : ℕ} {K : Type*} [Field K] (y : Fin d → K) (z : K)
    (x : Fin d → K) (j : Fin d) :
    ∑ k : Fin d, x j * sphereMatrix y z (some j) (some k) * x k = x j ^ 2 := by
  rw [Finset.sum_eq_single j]
  · show x j * (if j = j then (1 : K) else 0) * x j = x j ^ 2
    rw [if_pos (rfl : j = j)]
    ring
  · intro k _ hkj
    show x j * (if j = k then (1 : K) else 0) * x k = 0
    rw [if_neg (Ne.symm hkj)]
    ring
  · intro hj
    exact absurd (Finset.mem_univ j) hj

/-- `pᵀ H p = |x|² − 2⟨y, x⟩ + z` for `p = (1, x)`. -/
theorem sphereMatrix_quadForm {d : ℕ} {K : Type*} [Field K] (y : Fin d → K) (z : K)
    (x : Fin d → K) (aug : Option (Fin d) → K) (h0 : aug none = 1)
    (h1 : ∀ j, aug (some j) = x j) :
    ∑ α, ∑ β, aug α * sphereMatrix y z α β * aug β =
      ∑ j, x j ^ 2 + ∑ j, (-2 * x j) * y j + z := by
  have hnone : ∑ β, aug none * sphereMatrix y z none β * aug β =
      z + ∑ k, (-2 * y k) * x k := by
    rw [Fintype.sum_option, h0]
    simp only [h1]
    show 1 * z * 1 + ∑ k, 1 * (-2 * y k) * x k = z + ∑ k, (-2 * y k) * x k
    simp only [one_mul, mul_one]
  have hsome : ∀ j, ∑ β, aug (some j) * sphereMatrix y z (some j) β * aug β = x j ^ 2 := by
    intro j
    rw [Fintype.sum_option, h0, h1]
    simp only [h1]
    show x j * 0 * 1 + ∑ k, x j * sphereMatrix y z (some j) (some k) * x k = x j ^ 2
    rw [sphereMatrix_row_some y z x j, mul_zero, zero_mul, zero_add]
  rw [Fintype.sum_option, hnone]
  simp only [hsome]
  have hswap : ∑ k, (-2 * y k) * x k = ∑ j, (-2 * x j) * y j :=
    Finset.sum_congr rfl (fun k _ => by ring)
  rw [hswap]
  ring

/-! ## The coordinate field -/

/-- With algebraic coordinates, OpenAI's coordinate field is finite over `ℚ`. -/
theorem coordinateField_finiteDimensional {s d : ℕ} (a : Fin s → Space d)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j)) :
    FiniteDimensional ℚ (coordinateField a) := by
  unfold OAI.EuclideanRamsey.coordinateField
  refine IntermediateField.finiteDimensional_adjoin (fun x hx => ?_)
  obtain ⟨ij, rfl⟩ := hx
  exact isAlgebraic_iff_isIntegral.mp (halg ij.1 ij.2)

/-- **Step 1.** A sphere through all points has an equation with coefficients in the
coordinate field. -/
theorem exists_sphere_coeffs {s d : ℕ} (a : Fin s → Space d)
    (hcos : EuclideanGeometry.Cospherical (Set.range a)) :
    ∃ (y : Fin d → Coeff a) (z : Coeff a),
      ∀ i, ∑ j, coordinate a i j ^ 2 + ∑ j, (-2 * coordinate a i j) * y j + z = 0 := by
  obtain ⟨c, ρ, hc⟩ := hcos
  -- the real sphere equations
  have hreal : ∀ i, ∑ j, (a i j) ^ 2 + ∑ j, (-2 * a i j) * c j +
      (∑ j, (c j) ^ 2 - ρ ^ 2) = 0 := by
    intro i
    have h2 : ρ ^ 2 = ∑ j, dist (a i j) (c j) ^ 2 := by
      rw [← hc (a i) (Set.mem_range_self i)]
      exact EuclideanSpace.dist_sq_eq (a i) c
    have h3 : ∀ j, dist (a i j) (c j) ^ 2 = (a i j) ^ 2 + (-2 * a i j) * c j + (c j) ^ 2 := by
      intro j
      rw [Real.dist_eq, sq_abs]
      ring
    simp only [h3, Finset.sum_add_distrib] at h2
    linarith
  -- the same equations, with the `F`-coefficients written through `algebraMap`
  have hcoe : ∀ i j, algebraMap (Coeff a) ℝ (coordinate a i j) = a i j := fun _ _ => rfl
  have hK : ∀ i, ∑ j, algebraMap (Coeff a) ℝ (coordinate a i j ^ 2) +
      ∑ j, algebraMap (Coeff a) ℝ (-2 * coordinate a i j) * c j +
        (∑ j, (c j) ^ 2 - ρ ^ 2) = 0 := by
    intro i
    simp only [map_pow, map_mul, map_neg, map_ofNat, hcoe]
    exact hreal i
  -- an `F`-linear projection `φ : ℝ → F` with `φ|_F = id`
  obtain ⟨φ, hφ⟩ := LinearMap.exists_leftInverse_of_injective
    (Algebra.linearMap (Coeff a) ℝ)
    (LinearMap.ker_eq_bot.mpr (by
      rw [Algebra.coe_linearMap]
      exact (algebraMap (Coeff a) ℝ).injective))
  have hφ' : ∀ k : Coeff a, φ (algebraMap (Coeff a) ℝ k) = k := by
    intro k
    have hk := LinearMap.congr_fun hφ k
    rw [LinearMap.comp_apply, Algebra.linearMap_apply, LinearMap.id_apply] at hk
    exact hk
  have hφmul : ∀ (k : Coeff a) (x : ℝ), φ (algebraMap (Coeff a) ℝ k * x) = k * φ x := by
    intro k x
    rw [← Algebra.smul_def, map_smul, smul_eq_mul]
  refine ⟨fun j => φ (c j), φ (∑ j, (c j) ^ 2 - ρ ^ 2), fun i => ?_⟩
  have hi := congrArg φ (hK i)
  simp only [map_add, map_sum, hφmul, hφ', map_zero] at hi
  exact hi

/-- **Steps 2–4.** If the coordinate field is finite over `ℚ` and the points satisfy a
sphere equation with coefficients in it, OpenAI's `FieldCriterion` holds, with
`P = (H ⊗ 1)·e` for the separability idempotent `e`. -/
theorem fieldCriterion_of_sphere {s d : ℕ} (a : Fin s → Space d)
    [FiniteDimensional ℚ (Coeff a)] (y : Fin d → Coeff a) (z : Coeff a)
    (hsph : ∀ i, ∑ j, coordinate a i j ^ 2 + ∑ j, (-2 * coordinate a i j) * y j + z = 0) :
    FieldCriterion a := by
  haveI : Algebra.FormallyUnramified ℚ (Coeff a) :=
    Algebra.FormallyUnramified.of_isSeparable (K := ℚ) (L := Coeff a)
  obtain ⟨e, he1, he2⟩ :=
    (Algebra.FormallyUnramified.iff_exists_tensorProduct (R := ℚ) (S := Coeff a)).mp
      inferInstance
  have hswap : ∀ w : Coeff a,
      ((1 : Coeff a) ⊗ₜ[ℚ] w) * e = (w ⊗ₜ[ℚ] (1 : Coeff a)) * e := by
    intro w
    have h := he1 w
    rw [sub_mul, sub_eq_zero] at h
    exact h
  refine ⟨fun α β => (sphereMatrix y z α β ⊗ₜ[ℚ] (1 : Coeff a)) * e,
    fun i => ?_, fun α β => ?_⟩
  · have hterm : ∀ u m w : Coeff a,
        (u ⊗ₜ[ℚ] (1 : Coeff a)) * ((m ⊗ₜ[ℚ] (1 : Coeff a)) * e) *
            ((1 : Coeff a) ⊗ₜ[ℚ] w) =
          ((u * m * w) ⊗ₜ[ℚ] (1 : Coeff a)) * e := by
      intro u m w
      calc (u ⊗ₜ[ℚ] (1 : Coeff a)) * ((m ⊗ₜ[ℚ] (1 : Coeff a)) * e) *
            ((1 : Coeff a) ⊗ₜ[ℚ] w)
          = (u ⊗ₜ[ℚ] (1 : Coeff a)) * (m ⊗ₜ[ℚ] (1 : Coeff a)) *
              (((1 : Coeff a) ⊗ₜ[ℚ] w) * e) := by ring
        _ = (u ⊗ₜ[ℚ] (1 : Coeff a)) * (m ⊗ₜ[ℚ] (1 : Coeff a)) *
              ((w ⊗ₜ[ℚ] (1 : Coeff a)) * e) := by rw [hswap]
        _ = ((u ⊗ₜ[ℚ] (1 : Coeff a)) * (m ⊗ₜ[ℚ] (1 : Coeff a)) *
              (w ⊗ₜ[ℚ] (1 : Coeff a))) * e := by ring
        _ = ((u * m * w) ⊗ₜ[ℚ] (1 : Coeff a)) * e := by
          rw [Algebra.TensorProduct.tmul_mul_tmul, Algebra.TensorProduct.tmul_mul_tmul,
            mul_one, mul_one]
    show ∑ α, ∑ β, (augmented a i α ⊗ₜ[ℚ] (1 : Coeff a)) *
        ((sphereMatrix y z α β ⊗ₜ[ℚ] (1 : Coeff a)) * e) *
        ((1 : Coeff a) ⊗ₜ[ℚ] augmented a i β) = 0
    simp only [hterm]
    have hsum : ∑ α, ∑ β, ((augmented a i α * sphereMatrix y z α β * augmented a i β) ⊗ₜ[ℚ]
          (1 : Coeff a)) * e =
        ((∑ α, ∑ β, augmented a i α * sphereMatrix y z α β * augmented a i β) ⊗ₜ[ℚ]
          (1 : Coeff a)) * e := by
      rw [TensorProduct.sum_tmul, Finset.sum_mul]
      refine Finset.sum_congr rfl (fun α _ => ?_)
      rw [TensorProduct.sum_tmul, Finset.sum_mul]
    rw [hsum, sphereMatrix_quadForm y z (coordinate a i) (augmented a i) rfl (fun _ => rfl),
      hsph i, TensorProduct.zero_tmul, zero_mul]
  · show Algebra.TensorProduct.lmul' ℚ
        (((if α = β then (1 : Coeff a) else 0) ⊗ₜ[ℚ] (1 : Coeff a)) * e) =
      if α = β then 1 else 0
    rw [map_mul, Algebra.TensorProduct.lmul'_apply_tmul, he2, mul_one, mul_one]

/-! ## Consequences for OpenAI's statements -/

/-- **Graham's conjecture for algebraic configurations.** If OpenAI's classification
holds, every injective spherical configuration `a : Fin s → ℝ^d` (`s ≥ 2`, `d ≥ 1`,
affine span `ℝ^d`) whose coordinates are algebraic over `ℚ` is Ramsey. -/
theorem ramsey_of_cospherical_of_algebraic
    (hclass : type_of% @OAI.EuclideanRamsey.classification)
    {s d : ℕ} (a : Fin s → Space d) (hs : 2 ≤ s) (hd : 1 ≤ d)
    (ha : Function.Injective a) (hspan : affineSpan ℝ (Set.range a) = ⊤)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j))
    (hcos : EuclideanGeometry.Cospherical (Set.range a)) : Ramsey a := by
  haveI := coordinateField_finiteDimensional a halg
  obtain ⟨y, z, hyz⟩ := exists_sphere_coeffs a hcos
  exact (hclass a hs hd ha hspan).mpr (fieldCriterion_of_sphere a y z hyz)

/-- The statement of `OAI.EuclideanRamsey.ramsey_cospherical` (comparator
`EuclideanRamseySpherical.lean`: every injective Ramsey configuration is cospherical),
restated over the identical definitions of `EuclideanRamsey.lean` with `s d` explicit.
See the build note in the module docstring. -/
def RamseyCosphericalStatement : Prop :=
  ∀ (s d : ℕ) (a : Fin s → Space d), Function.Injective a → Ramsey a →
    EuclideanGeometry.Cospherical (Set.range a)

/-- **Algebraic configurations: Ramsey ⇔ spherical.** -/
theorem ramsey_iff_cospherical_of_algebraic
    (hclass : type_of% @OAI.EuclideanRamsey.classification)
    (hsph : RamseyCosphericalStatement)
    {s d : ℕ} (a : Fin s → Space d) (hs : 2 ≤ s) (hd : 1 ≤ d)
    (ha : Function.Injective a) (hspan : affineSpan ℝ (Set.range a) = ⊤)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j)) :
    Ramsey a ↔ EuclideanGeometry.Cospherical (Set.range a) :=
  ⟨hsph s d a ha, ramsey_of_cospherical_of_algebraic hclass a hs hd ha hspan halg⟩

end Fidelity

open OAI.EuclideanRamsey (Space Ramsey)

/-- **CL-1, unconditionally.** For an injective configuration `a : Fin s → ℝ^d` with
`s ≥ 2`, `d ≥ 1`, affine span `ℝ^d` and coordinates algebraic over `ℚ`, `a` is Euclidean
Ramsey iff it is spherical. Both directions use OpenAI's proofs of family 172, rebuilt here. -/
theorem algebraic_ramsey_iff_cospherical {s d : ℕ} (a : Fin s → Space d)
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (hspan : affineSpan ℝ (Set.range a) = ⊤)
    (halg : ∀ i j, IsAlgebraic ℚ (a i j)) :
    Ramsey a ↔ EuclideanGeometry.Cospherical (Set.range a) :=
  Fidelity.ramsey_iff_cospherical_of_algebraic OAI.EuclideanRamsey.classification
    (fun _ _ b hb hR => OAI.EuclideanRamsey.ramsey_cospherical b hb hR)
    a hs hd ha hspan halg

/-- **Rational points.** A finite configuration with rational coordinates that lies on a
sphere and spans its space is Euclidean Ramsey, whatever the number of points. (Family
172 itself covers at most five points on a circle, and configurations whose quadratic
evaluation rows are linearly independent.) -/
theorem ramsey_of_cospherical_of_rational {s d : ℕ} (a : Fin s → Space d)
    (hs : 2 ≤ s) (hd : 1 ≤ d) (ha : Function.Injective a)
    (hspan : affineSpan ℝ (Set.range a) = ⊤)
    (hrat : ∀ i j, ∃ q : ℚ, a i j = q)
    (hcos : EuclideanGeometry.Cospherical (Set.range a)) : Ramsey a := by
  refine (algebraic_ramsey_iff_cospherical a hs hd ha hspan fun i j => ?_).mpr hcos
  obtain ⟨q, hq⟩ := hrat i j
  rw [hq]
  exact ⟨Polynomial.X - Polynomial.C q, Polynomial.X_sub_C_ne_zero q, by simp⟩

end EndToEnd
