import Corollaries.Pi
import Mathlib.Analysis.Real.Pi.Irrational
import Mathlib.Tactic.LinearCombination

/-!
# `LiouvilleWith` under `x ↦ 1/x` and rational Möbius maps (family 017)

Mathlib proves that `LiouvilleWith p` is invariant under `x ↦ x + r` and
`x ↦ r·x` (`r ∈ ℚ`, `r ≠ 0`), but has no lemma for `x ↦ x⁻¹`. This file adds
it (`liouvilleWith_inv_iff`, valid for every real `p`) and combines the three
into invariance under every rational Möbius map `x ↦ (ax + b)/(cx + d)`,
`ad − bc ≠ 0`, for irrational `x` (`liouvilleWith_mobius_iff`).

Applied to OpenAI's `PiExponent.main` (taken as the hypothesis
`OAIHyp.PiExponentMain`), this gives: `1/π`, and more generally every
`(aπ + b)/(cπ + d)` with rational `a, b, c, d` and `ad − bc ≠ 0`, is not
`LiouvilleWith p` for any `p > 2` (irrationality exponent `≤ 2`). The corpus
states the exponent of `π` only.
-/

namespace Corollaries

open OAIHyp Filter

/-- For `1 < p` and `y > 0`: if `y` is `LiouvilleWith p`, so is `y⁻¹`. If
`|y - m/n| < C/n^p` with `n` large, then `m > 0`, `m ≍ n`, and
`|y⁻¹ - n/m| = |y - m/n| · n/(m y)`, which is `≪ 1/m^p`. -/
theorem liouvilleWith_inv_of_pos {p y : ℝ} (hp : 1 < p) (hy : 0 < y)
    (h : LiouvilleWith p y) : LiouvilleWith p y⁻¹ := by
  obtain ⟨C, hC0, hC⟩ := h.exists_pos
  refine ⟨2 * C * (2 * y) ^ p * y⁻¹ * y⁻¹, Filter.frequently_atTop.mpr (fun a => ?_)⟩
  have hev : ∀ᶠ n : ℕ in atTop, max (2 * C / y) (2 * (a : ℝ) / y) < (n : ℝ) :=
    tendsto_natCast_atTop_atTop.eventually_gt_atTop _
  obtain ⟨n, ⟨hn1, m, hne, hlt⟩, hbig⟩ := (hC.and_eventually hev).exists
  obtain ⟨hbigC, hbiga⟩ := max_lt_iff.mp hbig
  -- basic facts about the denominator `n`
  have hN : (0 : ℝ) < n := Nat.cast_pos.mpr (by omega)
  have hN1 : (1 : ℝ) ≤ n := by exact_mod_cast hn1
  have hNp : (0 : ℝ) < (n : ℝ) ^ p := Real.rpow_pos_of_pos hN p
  have hn_le : (n : ℝ) ≤ (n : ℝ) ^ p := by
    have h1 := Real.rpow_le_rpow_of_exponent_le hN1 hp.le
    rwa [Real.rpow_one] at h1
  -- the approximation is within `y/2`
  have hA : |y - m / n| * (n : ℝ) ^ p < C := (lt_div_iff₀ hNp).mp hlt
  have hAn : |y - m / n| * (n : ℝ) < C :=
    lt_of_le_of_lt (mul_le_mul_of_nonneg_left hn_le (abs_nonneg _)) hA
  have hCy : 2 * C < (n : ℝ) * y := (div_lt_iff₀ hy).mp hbigC
  have hclose : |y - m / n| < y / 2 := by
    have h1 : |y - m / n| * (n : ℝ) < y / 2 * n := by linarith
    exact lt_of_mul_lt_mul_right h1 hN.le
  obtain ⟨hlo, hhi⟩ := abs_lt.mp hclose
  -- hence `y n / 2 < m < 2 y n`
  have hM_lo : y / 2 * n < (m : ℝ) := (lt_div_iff₀ hN).mp (by linarith)
  have hM_hi : (m : ℝ) < 3 * y / 2 * n := (div_lt_iff₀ hN).mp (by linarith)
  have hyN : 0 < y * n := mul_pos hy hN
  have hM : (0 : ℝ) < m := by linarith
  have hM2 : (m : ℝ) < 2 * y * n := by linarith
  -- `m` is a positive integer; use it as the new denominator
  have hm0 : (0 : ℤ) ≤ m := by exact_mod_cast hM.le
  obtain ⟨k, hk⟩ := Int.eq_ofNat_of_zero_le hm0
  have hkm : (k : ℝ) = (m : ℝ) := by
    subst hk
    exact (Int.cast_natCast k).symm
  refine ⟨k, ?_, (n : ℤ), ?_, ?_⟩
  · -- the new denominator is at least `a`
    have h1 : 2 * (a : ℝ) < n * y := (div_lt_iff₀ hy).mp hbiga
    have h2 : (a : ℝ) < k := by rw [hkm]; linarith
    exact (Nat.cast_lt.mp h2).le
  · -- `y⁻¹ ≠ n/m`, since `y ≠ m/n`
    rw [Int.cast_natCast, hkm]
    intro heq
    apply hne
    rw [← inv_inv y, heq, inv_div]
  · -- the approximation bound
    rw [Int.cast_natCast, hkm]
    have hid : y⁻¹ - (n : ℝ) / m = (m / n - y) * (n / m) * y⁻¹ := by
      have hmn : (m : ℝ) / n * (n / m) = 1 := by
        rw [div_mul_div_comm, mul_comm (m : ℝ) n, div_self (mul_ne_zero hN.ne' hM.ne')]
      linear_combination (-y⁻¹) * hmn + ((n : ℝ) / m) * (mul_inv_cancel₀ hy.ne')
    have hD : |y⁻¹ - (n : ℝ) / m| = |y - m / n| * (n / m) * y⁻¹ := by
      rw [hid, abs_mul, abs_mul, abs_sub_comm, abs_of_pos (div_pos hN hM),
        abs_of_pos (inv_pos.mpr hy)]
    have h2y : (0 : ℝ) ≤ 2 * y := by positivity
    have hpow : (m : ℝ) ^ p ≤ (2 * y) ^ p * (n : ℝ) ^ p := by
      rw [← Real.mul_rpow h2y hN.le]
      exact Real.rpow_le_rpow hM.le hM2.le (by linarith)
    have hNM : (n : ℝ) / m ≤ 2 / y := by
      rw [div_le_div_iff₀ hM hy]
      linarith
    rw [hD, lt_div_iff₀ (Real.rpow_pos_of_pos hM p)]
    calc |y - m / n| * (n / m) * y⁻¹ * (m : ℝ) ^ p
        ≤ |y - m / n| * (n / m) * y⁻¹ * ((2 * y) ^ p * (n : ℝ) ^ p) :=
          mul_le_mul_of_nonneg_left hpow (by positivity)
      _ = (|y - m / n| * (n : ℝ) ^ p) * ((2 * y) ^ p * (n / m) * y⁻¹) := by ring
      _ < C * ((2 * y) ^ p * (n / m) * y⁻¹) := mul_lt_mul_of_pos_right hA (by positivity)
      _ ≤ C * ((2 * y) ^ p * (2 / y) * y⁻¹) :=
          mul_le_mul_of_nonneg_left
            (mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hNM (by positivity))
              (by positivity)) hC0.le
      _ = 2 * C * (2 * y) ^ p * y⁻¹ * y⁻¹ := by ring

/-- `LiouvilleWith p x → LiouvilleWith p x⁻¹`, for every real `p`. -/
theorem liouvilleWith_inv {p x : ℝ} (h : LiouvilleWith p x) : LiouvilleWith p x⁻¹ := by
  rcases le_or_gt p 1 with hp | hp
  · exact (liouvilleWith_one x⁻¹).mono hp
  · rcases lt_trichotomy x 0 with hx | hx | hx
    · have h' := liouvilleWith_inv_of_pos hp (neg_pos.mpr hx) h.neg
      rw [inv_neg] at h'
      exact LiouvilleWith.neg_iff.mp h'
    · rw [hx] at h
      exact absurd (h.irrational hp) not_irrational_zero
    · exact liouvilleWith_inv_of_pos hp hx h

/-- **`LiouvilleWith p` is invariant under `x ↦ x⁻¹`.** -/
theorem liouvilleWith_inv_iff {p x : ℝ} : LiouvilleWith p x⁻¹ ↔ LiouvilleWith p x := by
  refine ⟨fun h => ?_, liouvilleWith_inv⟩
  have h' := liouvilleWith_inv h
  rwa [inv_inv] at h'

/-- **`LiouvilleWith p` is invariant under rational Möbius maps.** For irrational
`x` and `a, b, c, d ∈ ℚ` with `ad − bc ≠ 0`,
`(ax + b)/(cx + d)` is `LiouvilleWith p` iff `x` is. -/
theorem liouvilleWith_mobius_iff {p x : ℝ} (hx : Irrational x) {a b c d : ℚ}
    (hdet : a * d - b * c ≠ 0) :
    LiouvilleWith p (((a : ℝ) * x + b) / ((c : ℝ) * x + d)) ↔ LiouvilleWith p x := by
  rcases eq_or_ne c 0 with hc | hc
  · -- `c = 0`: an affine map
    subst hc
    have ha : a ≠ 0 := by
      rintro rfl
      apply hdet
      ring
    have hd : d ≠ 0 := by
      rintro rfl
      apply hdet
      ring
    have hd' : (d : ℝ) ≠ 0 := Rat.cast_ne_zero.mpr hd
    have e : ((a : ℝ) * x + b) / d = x * ((a / d : ℚ) : ℝ) + ((b / d : ℚ) : ℝ) := by
      rw [div_eq_iff hd']
      push_cast
      linear_combination (-(a : ℝ) * x - b) * (mul_inv_cancel₀ hd')
    have h0 : ((0 : ℚ) : ℝ) * x + d = d := by simp
    rw [h0, e, LiouvilleWith.add_rat_iff, LiouvilleWith.mul_rat_iff (div_ne_zero ha hd)]
  · -- `c ≠ 0`: `(ax + b)/(cx + d) = (cx + d)⁻¹ · (bc − ad)/c + a/c`
    have hc' : (c : ℝ) ≠ 0 := Rat.cast_ne_zero.mpr hc
    have hu : (c : ℝ) * x + d ≠ 0 := by
      intro h0
      have hx' : x = -(d : ℝ) / c := by
        rw [eq_div_iff hc']
        linarith
      exact hx.ne_rat (-d / c) (by exact_mod_cast hx')
    have e : ((a : ℝ) * x + b) / ((c : ℝ) * x + d) =
        ((c : ℝ) * x + d)⁻¹ * (((b * c - a * d) / c : ℚ) : ℝ) + ((a / c : ℚ) : ℝ) := by
      rw [div_eq_iff hu]
      push_cast
      linear_combination (-(a : ℝ) * x - b) * (mul_inv_cancel₀ hc') +
        ((a : ℝ) * d * (c : ℝ)⁻¹ - b * ((c : ℝ) * (c : ℝ)⁻¹)) * (mul_inv_cancel₀ hu)
    have hK : (b * c - a * d) / c ≠ 0 :=
      div_ne_zero (fun h0 => hdet (by linarith)) hc
    rw [e, LiouvilleWith.add_rat_iff, LiouvilleWith.mul_rat_iff hK, liouvilleWith_inv_iff,
      LiouvilleWith.add_rat_iff, LiouvilleWith.rat_mul_iff hc]

/-- Under OpenAI's `PiExponent.main`, `1/π` is not `LiouvilleWith p` for any `p > 2`. -/
theorem inv_pi_not_liouvilleWith (h : PiExponentMain) {p : ℝ} (hp : 2 < p) :
    ¬ LiouvilleWith p Real.pi⁻¹ := fun hL =>
  pi_not_liouvilleWith h hp (liouvilleWith_inv_iff.mp hL)

/-- Under OpenAI's `PiExponent.main`, no rational Möbius image `(aπ + b)/(cπ + d)`
(`ad − bc ≠ 0`) is `LiouvilleWith p` for any `p > 2`: its irrationality
exponent is at most `2`. -/
theorem mobius_pi_not_liouvilleWith (h : PiExponentMain) {a b c d : ℚ}
    (hdet : a * d - b * c ≠ 0) {p : ℝ} (hp : 2 < p) :
    ¬ LiouvilleWith p (((a : ℝ) * Real.pi + b) / ((c : ℝ) * Real.pi + d)) := fun hL =>
  pi_not_liouvilleWith h hp ((liouvilleWith_mobius_iff irrational_pi hdet).mp hL)

end Corollaries
