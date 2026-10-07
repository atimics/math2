import Corollaries.Hypotheses

/-!
# Consequences of `μ(π) = 2` (family 017)

OpenAI's `PiExponent.main` says `π` has irrationality exponent `2`. Here we
connect it to Mathlib's `LiouvilleWith` API and carry it over to every
rational affine image `rπ + s`. None of these consequences is stated in the
corpus.
-/

namespace Corollaries

open OAIHyp Filter

/-- `π` is not Liouville with any exponent `p > 2`. -/
theorem pi_not_liouvilleWith (h : PiExponentMain) {p : ℝ} (hp : 2 < p) :
    ¬ LiouvilleWith p Real.pi := by
  intro hL
  obtain ⟨ν, h2ν, hνp⟩ := exists_between hp
  obtain ⟨Q, -, hQ⟩ := h.1 ν h2ν
  obtain ⟨n, ⟨m, -, hlt⟩, hn⟩ :=
    ((hL.frequently_lt_rpow_neg hνp).and_eventually
      (eventually_ge_atTop Q.toNat)).exists
  have hQn : Q ≤ (n : ℤ) := by omega
  have key := hQ m n hQn
  push_cast at key
  linarith

/-- Every `rπ + s` with `r, s ∈ ℚ`, `r ≠ 0`, has irrationality exponent `2` in
Mathlib's sense: it is not `LiouvilleWith p` for any `p > 2`. -/
theorem rat_affine_pi_not_liouvilleWith (h : PiExponentMain)
    (r s : ℚ) (hr : r ≠ 0) {p : ℝ} (hp : 2 < p) :
    ¬ LiouvilleWith p (Real.pi * r + s) := fun hL =>
  pi_not_liouvilleWith h hp
    ((LiouvilleWith.mul_rat_iff hr).1 (LiouvilleWith.add_rat_iff.1 hL))

/-- `π` is not a Liouville number. (Mahler already showed this in 1953; here it
is a two-line consequence of the corpus claim.) -/
theorem pi_not_liouville (h : PiExponentMain) : ¬ Liouville Real.pi :=
  fun hL => pi_not_liouvilleWith h (by norm_num : (2 : ℝ) < 3) (hL.liouvilleWith 3)

end Corollaries
