import Corollaries.Hypotheses

/-!
# Consequences of OpenAI's `PiExponent.main` (family 017)

OpenAI's `PiExponent.main` claims `π` has irrationality exponent `2`. This file
proves, from that claim, the **upper-bound side** in Mathlib's `LiouvilleWith`
language: no `rπ + s` (`r, s ∈ ℚ`, `r ≠ 0`) is `LiouvilleWith p` for any
`p > 2`, i.e. its irrationality exponent is `≤ 2`.

The matching lower bound (exponent `≥ 2`) is Dirichlet's approximation theorem,
true for every irrational number; it is **not** formalized here, so this file
does not state the equality `μ(rπ + s) = 2` as a theorem.
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

/-- For `r, s ∈ ℚ` with `r ≠ 0`, `rπ + s` is not `LiouvilleWith p` for any `p > 2`
(its irrationality exponent is at most `2`). -/
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
