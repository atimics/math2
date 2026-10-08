import Mathlib
import Fidelity.Vendor.Nagata

/-!
# Nagata's inequality with equal multiplicities (family 039)

OpenAI's `OAI.Nagata.FullNagata` (comparator `Nagata.lean`) states Nagata's
conjecture in coordinates: for `r ≥ 10` there is a countable family of proper
Zariski-closed subsets of ordered distinct configurations of `r` points in `ℙ²(ℂ)`
such that, for every configuration outside all of them, every nonzero homogeneous
`F ∈ ℂ[x, y, z]` of degree `d ≥ 1` vanishing to order `≥ mᵢ` at the `i`-th point
satisfies `∑ mᵢ < d·√r`.

Taking all `mᵢ = m` gives, for very general points:

* `nagata_equal_multiplicity`: `m·√r < d`, equivalently `r·m² < d²`;
* `nagata_sqrt_floor`: `⌊√r⌋·m < d`, so `d ≥ k·m + 1` when `r = k²` (`k ≥ 4`);
* `nagata_ten_points`: for `r = 10`, `d ≥ 3m + 1`.

These are specializations, not new mathematics. The paper's proof itself reduces
to equal multiplicities, and its Lemma "Excluding degree at most 3m"
(`lem:cubic-low-degree`) gives `d > 3m` for `r ≥ 10`. The comparator states only
the unequal-multiplicity form. This file checks the specializations against the
comparator's exact definitions (point ideals, chart dehomogenization, Zariski-closed
exceptional sets).

Only the definition `FullNagata` is used. The comparator's `nagata_conjecture`
mentions `curveDegree`, which is built from a `sorry`d lemma, so it is avoided.
Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

open OAI.Nagata.ProjectiveGeometry
  (OrderedDistinctPoints IsConfigurationZariskiClosed multiplicityAtLeast)

/-- Arithmetic core: `r·m < d·√r` with `r > 0` gives `m·√r < d`. -/
theorem mul_sqrt_lt_of_mul_lt {r m d : ℕ} (hr : 0 < r)
    (h : (r : ℝ) * m < d * Real.sqrt r) : (m : ℝ) * Real.sqrt r < d := by
  have hs : 0 < Real.sqrt (r : ℝ) := Real.sqrt_pos.mpr (by exact_mod_cast hr)
  have hrr : Real.sqrt (r : ℝ) * Real.sqrt r = r := Real.mul_self_sqrt (Nat.cast_nonneg r)
  refine lt_of_mul_lt_mul_right ?_ hs.le
  calc (m : ℝ) * Real.sqrt r * Real.sqrt r = (r : ℝ) * m := by
        rw [mul_assoc, hrr]
        ring
    _ < d * Real.sqrt r := h

/-- **Equal multiplicities.** If OpenAI's `FullNagata` holds, then for `r ≥ 10` very
general points, a nonzero homogeneous plane curve of degree `d ≥ 1` with multiplicity
`≥ m` at every point satisfies `m·√r < d` and `r·m² < d²`. -/
theorem nagata_equal_multiplicity (h : OAI.Nagata.FullNagata) (r : ℕ) (hr : 10 ≤ r) :
    ∃ exceptional : ℕ → Set (OrderedDistinctPoints r),
      (∀ i, IsConfigurationZariskiClosed (exceptional i) ∧ exceptional i ≠ Set.univ) ∧
      (∃ points : OrderedDistinctPoints r, ∀ i, points ∉ exceptional i) ∧
      ∀ points : OrderedDistinctPoints r, (∀ i, points ∉ exceptional i) →
        ∀ d : ℕ, 1 ≤ d → ∀ F : MvPolynomial (Fin 3) ℂ, F ≠ 0 → F.IsHomogeneous d →
        ∀ m : ℕ, (∀ i, multiplicityAtLeast F (points.val i) m) →
          (m : ℝ) * Real.sqrt r < d ∧ r * m ^ 2 < d ^ 2 := by
  obtain ⟨E, hE, hgen, hmain⟩ := h r hr
  refine ⟨E, hE, hgen, fun points hp d hd F hF hhom m hm => ?_⟩
  have h0 := hmain points hp d hd F hF hhom (fun _ => m) hm
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at h0
  have h1 : (m : ℝ) * Real.sqrt r < d := mul_sqrt_lt_of_mul_lt (by omega) h0
  refine ⟨h1, ?_⟩
  have h2 : ((m : ℝ) * Real.sqrt r) ^ 2 < (d : ℝ) ^ 2 :=
    pow_lt_pow_left₀ h1 (by positivity) two_ne_zero
  rw [mul_pow, Real.sq_sqrt (Nat.cast_nonneg r)] at h2
  have h3 : ((r * m ^ 2 : ℕ) : ℝ) < ((d ^ 2 : ℕ) : ℝ) := by
    push_cast
    linarith
  exact_mod_cast h3

/-- `⌊√r⌋·m < d`. For `r = k²` this is `d ≥ k·m + 1`. -/
theorem nagata_sqrt_floor (h : OAI.Nagata.FullNagata) (r : ℕ) (hr : 10 ≤ r) :
    ∃ exceptional : ℕ → Set (OrderedDistinctPoints r),
      (∀ i, IsConfigurationZariskiClosed (exceptional i) ∧ exceptional i ≠ Set.univ) ∧
      (∃ points : OrderedDistinctPoints r, ∀ i, points ∉ exceptional i) ∧
      ∀ points : OrderedDistinctPoints r, (∀ i, points ∉ exceptional i) →
        ∀ d : ℕ, 1 ≤ d → ∀ F : MvPolynomial (Fin 3) ℂ, F ≠ 0 → F.IsHomogeneous d →
        ∀ m : ℕ, (∀ i, multiplicityAtLeast F (points.val i) m) → Nat.sqrt r * m < d := by
  obtain ⟨E, hE, hgen, hmain⟩ := nagata_equal_multiplicity h r hr
  refine ⟨E, hE, hgen, fun points hp d hd F hF hhom m hm => ?_⟩
  have hsq : r * m ^ 2 < d ^ 2 := (hmain points hp d hd F hF hhom m hm).2
  by_contra hc
  have hle : d ≤ Nat.sqrt r * m := by omega
  have h1 : d ^ 2 ≤ (Nat.sqrt r * m) ^ 2 := Nat.pow_le_pow_left hle 2
  have h2 : (Nat.sqrt r * m) ^ 2 = Nat.sqrt r ^ 2 * m ^ 2 := by ring
  have h3 : Nat.sqrt r ^ 2 * m ^ 2 ≤ r * m ^ 2 := Nat.mul_le_mul (Nat.sqrt_le' r) (le_refl _)
  omega

/-- **Ten very general points.** A nonzero plane curve of degree `d` with multiplicity
`≥ m` at ten very general points has `d ≥ 3m + 1` (indeed `10m² < d²`). -/
theorem nagata_ten_points (h : OAI.Nagata.FullNagata) :
    ∃ exceptional : ℕ → Set (OrderedDistinctPoints 10),
      (∀ i, IsConfigurationZariskiClosed (exceptional i) ∧ exceptional i ≠ Set.univ) ∧
      (∃ points : OrderedDistinctPoints 10, ∀ i, points ∉ exceptional i) ∧
      ∀ points : OrderedDistinctPoints 10, (∀ i, points ∉ exceptional i) →
        ∀ d : ℕ, 1 ≤ d → ∀ F : MvPolynomial (Fin 3) ℂ, F ≠ 0 → F.IsHomogeneous d →
        ∀ m : ℕ, (∀ i, multiplicityAtLeast F (points.val i) m) → 3 * m + 1 ≤ d := by
  obtain ⟨E, hE, hgen, hmain⟩ := nagata_equal_multiplicity h 10 le_rfl
  refine ⟨E, hE, hgen, fun points hp d hd F hF hhom m hm => ?_⟩
  have hsq : 10 * m ^ 2 < d ^ 2 := (hmain points hp d hd F hF hhom m hm).2
  by_contra hc
  have hle : d ≤ 3 * m := by omega
  have h1 : d ^ 2 ≤ (3 * m) ^ 2 := Nat.pow_le_pow_left hle 2
  have h2 : (3 * m) ^ 2 = 9 * m ^ 2 := by ring
  omega

end Fidelity
