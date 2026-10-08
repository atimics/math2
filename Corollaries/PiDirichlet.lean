import Corollaries.PiMobius
import Mathlib.NumberTheory.DiophantineApproximation.Basic

/-!
# Dirichlet's lower bound, and `μ(rπ + s) = 2` (family 017)

`Corollaries/Pi.lean` and `Corollaries/PiMobius.lean` prove, from OpenAI's
`PiExponent.main`, that `rπ + s` (and every rational Möbius image of `π`) is
not `LiouvilleWith p` for `p > 2`. The matching lower bound is Dirichlet's
approximation theorem: **every irrational `x` is `LiouvilleWith 2`**
(`liouvilleWith_two_of_irrational`). Mathlib's `LiouvilleWith` file lists this
direction as not yet formalized; here it is derived from Mathlib's
`Real.exists_nat_abs_mul_sub_round_le`.

Together they give the exact set of Liouville exponents,
`{p | LiouvilleWith p (rπ + s)} = Set.Iic 2`, and its supremum (the
irrationality exponent) `= 2`, as Lean theorems conditional on
`OAIHyp.PiExponentMain`.
-/

namespace Corollaries

open OAIHyp Filter

/-- **Dirichlet: every irrational number is `LiouvilleWith 2`.** For a target
denominator bound `a`, pick `n` larger than `∑_{1 ≤ j < a} 1/‖jx‖`; Dirichlet's
theorem gives `0 < k ≤ n` with `‖kx‖ ≤ 1/(n+1)`, which forces `k ≥ a`, and then
`|x - round(kx)/k| ≤ 1/k² < 2/k²`. -/
theorem liouvilleWith_two_of_irrational {ξ : ℝ} (hξ : Irrational ξ) : LiouvilleWith 2 ξ := by
  have hδ : ∀ k : ℕ, 0 < k → 0 < |(k : ℝ) * ξ - round ((k : ℝ) * ξ)| := by
    intro k hk
    exact abs_pos.mpr (sub_ne_zero.mpr ((hξ.natCast_mul hk.ne').ne_int _))
  refine ⟨2, Filter.frequently_atTop.mpr (fun a => ?_)⟩
  have hnonneg : ∀ j ∈ Finset.Ico 1 a,
      (0 : ℝ) ≤ 1 / |(j : ℝ) * ξ - round ((j : ℝ) * ξ)| :=
    fun j _ => by positivity
  have hS0 : (0 : ℝ) ≤ ∑ j ∈ Finset.Ico 1 a, 1 / |(j : ℝ) * ξ - round ((j : ℝ) * ξ)| :=
    Finset.sum_nonneg hnonneg
  obtain ⟨n, hn⟩ :=
    exists_nat_gt (∑ j ∈ Finset.Ico 1 a, 1 / |(j : ℝ) * ξ - round ((j : ℝ) * ξ)|)
  have hn0 : 0 < n := Nat.cast_pos.mp (lt_of_le_of_lt hS0 hn)
  obtain ⟨k, hk0, hkn, hk⟩ := Real.exists_nat_abs_mul_sub_round_le ξ hn0
  have hK : (0 : ℝ) < k := Nat.cast_pos.mpr hk0
  refine ⟨k, ?_, round ((k : ℝ) * ξ), ?_, ?_⟩
  · -- `k ≥ a`: for `1 ≤ k < a`, `‖kx‖` is too large for Dirichlet's bound
    by_contra hka
    have hmem : k ∈ Finset.Ico 1 a := Finset.mem_Ico.mpr ⟨by omega, not_le.mp hka⟩
    have hle : 1 / |(k : ℝ) * ξ - round ((k : ℝ) * ξ)| ≤
        ∑ j ∈ Finset.Ico 1 a, 1 / |(j : ℝ) * ξ - round ((j : ℝ) * ξ)| :=
      Finset.single_le_sum hnonneg hmem
    have hpos := hδ k hk0
    have hn1 : (0 : ℝ) < n + 1 := by positivity
    have h1 : |(k : ℝ) * ξ - round ((k : ℝ) * ξ)| * (n + 1) ≤ 1 :=
      (le_div_iff₀ hn1).mp hk
    have h2 : (n : ℝ) + 1 ≤ 1 / |(k : ℝ) * ξ - round ((k : ℝ) * ξ)| := by
      rw [le_div_iff₀ hpos]
      linarith
    linarith
  · -- `x ≠ round(kx)/k`
    have h := hξ.ne_rational (round ((k : ℝ) * ξ)) (k : ℤ)
    rwa [Int.cast_natCast] at h
  · -- `|x - round(kx)/k| < 2/k²`
    have hid : ξ - (round ((k : ℝ) * ξ) : ℝ) / k =
        ((k : ℝ) * ξ - round ((k : ℝ) * ξ)) / k := by
      rw [sub_div, mul_div_cancel_left₀ ξ hK.ne']
    have h1 : |(k : ℝ) * ξ - round ((k : ℝ) * ξ)| * k ≤ 1 := by
      have hkn' : (k : ℝ) ≤ n + 1 := by
        have : (k : ℝ) ≤ n := Nat.cast_le.mpr hkn
        linarith
      have h2 : |(k : ℝ) * ξ - round ((k : ℝ) * ξ)| ≤ 1 / k :=
        le_trans hk (one_div_le_one_div_of_le hK hkn')
      exact (le_div_iff₀ hK).mp h2
    rw [hid, abs_div, abs_of_pos hK, Real.rpow_two, div_lt_div_iff₀ hK (pow_pos hK 2)]
    nlinarith [mul_le_mul_of_nonneg_right h1 hK.le]

/-- Every irrational `x` is `LiouvilleWith p` for all `p ≤ 2`. -/
theorem liouvilleWith_of_irrational_of_le_two {ξ : ℝ} (hξ : Irrational ξ) {p : ℝ}
    (hp : p ≤ 2) : LiouvilleWith p ξ :=
  (liouvilleWith_two_of_irrational hξ).mono hp

/-- **The Liouville exponents of `rπ + s` are exactly `(-∞, 2]`**, under OpenAI's
`PiExponent.main`. -/
theorem rat_affine_pi_liouvilleWith_eq_Iic (h : PiExponentMain) (r s : ℚ) (hr : r ≠ 0) :
    {p : ℝ | LiouvilleWith p (Real.pi * r + s)} = Set.Iic 2 := by
  ext p
  simp only [Set.mem_setOf_eq, Set.mem_Iic]
  constructor
  · intro hL
    by_contra hp
    exact rat_affine_pi_not_liouvilleWith h r s hr (not_le.mp hp) hL
  · intro hp
    exact (((liouvilleWith_two_of_irrational irrational_pi).mul_rat hr).add_rat s).mono hp

/-- **The irrationality exponent of `rπ + s` is exactly `2`** (as the supremum of
its Liouville exponents), under OpenAI's `PiExponent.main`. -/
theorem rat_affine_pi_irrationalityExponent (h : PiExponentMain) (r s : ℚ) (hr : r ≠ 0) :
    sSup {p : ℝ | LiouvilleWith p (Real.pi * r + s)} = 2 := by
  rw [rat_affine_pi_liouvilleWith_eq_Iic h r s hr, csSup_Iic]

/-- The same for every rational Möbius image `(aπ + b)/(cπ + d)`, `ad − bc ≠ 0`. -/
theorem mobius_pi_liouvilleWith_eq_Iic (h : PiExponentMain) {a b c d : ℚ}
    (hdet : a * d - b * c ≠ 0) :
    {p : ℝ | LiouvilleWith p (((a : ℝ) * Real.pi + b) / ((c : ℝ) * Real.pi + d))} =
      Set.Iic 2 := by
  ext p
  simp only [Set.mem_setOf_eq, Set.mem_Iic]
  constructor
  · intro hL
    by_contra hp
    exact mobius_pi_not_liouvilleWith h hdet (not_le.mp hp) hL
  · intro hp
    exact (liouvilleWith_mobius_iff irrational_pi hdet).mpr
      (liouvilleWith_of_irrational_of_le_two irrational_pi hp)

end Corollaries
