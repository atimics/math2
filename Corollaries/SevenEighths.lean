import Corollaries.Hypotheses

/-!
# Consequences of the 7/8 zero-free half-plane (family 003)

OpenAI's family 003 contains two separately formalized theorems:

* `DirichletSevenEighths`: every Dirichlet `L`-function has no zeros with
  `Re s > 7/8`, apart from the pole of the trivial character at `s = 1`;
* `SiegelZeros`: there is some unspecified `c > 0` such that every real zero
  `β` of a primitive real nonprincipal character of conductor `q ≥ 3`
  satisfies `(1 - β) log q ≥ c`. This one has its own paper, "Uniform
  exclusion of Landau–Siegel zeros", with a separate interpolation-determinant
  proof.

The second follows from the first in a few lines, with the explicit constant
`c = log 3 / 8`. The first actually gives the stronger fact that real zeros
stay at least `1/8` away from `1`, uniformly in the modulus
(`real_zero_le_seven_eighths`). The zeta statement, also proved separately
(`QuasiRiemannHypothesis.lean`), is the modulus-1 case.
-/

namespace Corollaries

open OAIHyp

/-- **Uniform real-zero gap.** Under `DirichletSevenEighths`, every real zero
`β ∈ (0,1)` of any nontrivial Dirichlet `L`-function, for any modulus,
satisfies `β ≤ 7/8`. No primitivity or reality assumption is needed. -/
theorem real_zero_le_seven_eighths (h : DirichletSevenEighths)
    {q : ℕ} [NeZero q] (χ : DirichletCharacter ℂ q) (hχ : χ ≠ 1)
    {β : ℝ} (hzero : χ.LFunction (β : ℂ) = 0) : β ≤ 7 / 8 := by
  by_contra hlt
  push_neg at hlt
  exact h χ (s := (β : ℂ)) (by simpa using hlt) (fun hc => hχ hc.1) hzero

/-- **The Landau–Siegel comparator statement, with an explicit constant.**
Under `DirichletSevenEighths`, the statement of OpenAI's
`OAI.SiegelZeros.WeightedTorusJets.exists_absolute_real_zero_gap` holds with
`c = log 3 / 8`. (`Fidelity` checks that this type matches OpenAI's exactly.) -/
theorem siegel_explicit (h : DirichletSevenEighths) :
    ∀ (q : ℕ) [NeZero q], 3 ≤ q →
      ∀ χ : DirichletCharacter ℂ q,
        χ.IsPrimitive → χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) →
        ∀ β : ℝ, 0 < β → β < 1 → χ.LFunction (β : ℂ) = 0 →
          Real.log 3 / 8 ≤ (1 - β) * Real.log (q : ℝ) := by
  intro q _ hq χ _ hχ _ β _ _ hzero
  have hβ := real_zero_le_seven_eighths h χ hχ hzero
  have hlog : Real.log 3 ≤ Real.log q :=
    Real.log_le_log (by norm_num) (by exact_mod_cast hq)
  have hlog3 : 0 ≤ Real.log 3 := Real.log_nonneg (by norm_num)
  have hprod : 0 ≤ (1 - β - 1 / 8) * Real.log q :=
    mul_nonneg (by linarith) (by linarith)
  nlinarith

/-- The exact shape of OpenAI's `SiegelZeros` comparator statement. -/
theorem siegel_of_sevenEighths (h : DirichletSevenEighths) :
    ∃ c : ℝ, 0 < c ∧
      ∀ (q : ℕ) [NeZero q], 3 ≤ q →
      ∀ χ : DirichletCharacter ℂ q,
        χ.IsPrimitive → χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) →
        ∀ β : ℝ, 0 < β → β < 1 → χ.LFunction (β : ℂ) = 0 →
          c ≤ (1 - β) * Real.log (q : ℝ) :=
  ⟨Real.log 3 / 8, div_pos (Real.log_pos (by norm_num)) (by norm_num),
    siegel_explicit h⟩

/-- **Zeta is the modulus-1 case.** Under `DirichletSevenEighths`, the statement
of OpenAI's separately formalized `OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re`
holds. -/
theorem zeta_of_sevenEighths (h : DirichletSevenEighths)
    {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0 := by
  by_cases h1 : s = 1
  · subst h1
    exact riemannZeta_one_ne_zero
  · have := h (q := 1) (1 : DirichletCharacter ℂ 1) hs (fun hc => h1 hc.2)
    rwa [DirichletCharacter.LFunction_modOne_eq] at this

end Corollaries
