import Fidelity.Vendor.HenonEmden

/-!
# Scalar Hénon–Lane–Emden Liouville theorem (family 370)

OpenAI's `OAI.HenonLaneEmden.main_nonexistence` concerns the *system*
`−Δu = |x|^A v^p`, `−Δv = |x|^B u^q` on `ℝⁿ ∖ {0}`. Setting `v = u`, `q = p`,
`B = A` gives the scalar Hardy–Hénon Liouville theorem below. The corpus states
the system, its unweighted case and Phan's Conjecture C, but not this scalar
specialization. For `A = 0` it is the classical Gidas–Spruck range
`p < (n+2)/(n−2)`.

Conditional on OpenAI's statement, which is taken as the hypothesis `h`.
-/

namespace Fidelity

open OAI.HenonLaneEmden

/-- **Scalar Hénon Liouville theorem.** If OpenAI's system theorem holds, then
for `n ≥ 2`, `p > 0` and `n − 2 < 2(n + A)/(p + 1)` there is no positive
continuous `u`, `C²` away from the origin, with `−Δu = |x|^A u^p` on `ℝⁿ ∖ {0}`. -/
theorem scalar_henon_nonexistence
    (h : type_of% @OAI.HenonLaneEmden.main_nonexistence)
    (n : ℕ) (hn : 2 ≤ n) (p A : ℝ) (hp : 0 < p)
    (hsub : (n : ℝ) - 2 < 2 * ((n : ℝ) + A) / (p + 1)) :
    ¬ ∃ u : Space n → ℝ, Continuous u ∧
        ContDiffOn ℝ 2 u ({0}ᶜ : Set (Space n)) ∧ (∀ x, 0 < u x) ∧
        ∀ x, x ≠ 0 → -(Laplacian.laplacian u) x = Real.rpow ‖x‖ A * Real.rpow (u x) p := by
  rintro ⟨u, hc, hr, hpos, heq⟩
  have hs : Subcritical n p p A A := by
    unfold Subcritical
    have e : ((n : ℝ) + A) / (p + 1) + ((n : ℝ) + A) / (p + 1)
        = 2 * ((n : ℝ) + A) / (p + 1) := by ring
    rw [e]
    linarith
  exact h n hn p p A A hp hp hs ⟨u, u, ⟨hc, hc, hr, hr, hpos, hpos, heq, heq⟩⟩

end Fidelity
