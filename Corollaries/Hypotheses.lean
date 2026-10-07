import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.Harmonic.ZetaAsymp
import Mathlib.NumberTheory.DirichletCharacter.Basic
import Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith
import Mathlib.Algebra.MonoidAlgebra.MapDomain
import Mathlib.Algebra.MonoidAlgebra.NoZeroDivisors
import Mathlib.Algebra.Group.UniqueProds.Basic
import Mathlib.GroupTheory.Finiteness
import Mathlib.Algebra.CharP.Defs
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# OpenAI's comparator statements, used as hypotheses

Each `Prop` below is the statement of one theorem from
`openai/math`, `lean/ComparatorChallenges/*.lean`, copied verbatim. The only
change is that the theorem's binders are moved into a `∀`.

**Nothing here is an axiom.** Every corollary in this library takes the
relevant `Prop` as an explicit hypothesis, so each result reads as
"if OpenAI's theorem holds, then …". The `Fidelity` library checks in the
Lean kernel that OpenAI's own theorem has this exact type, by elaborating
`(@OAI.theoremName : OAIHyp.Statement)`.
-/

namespace OAIHyp

/-- `ComparatorChallenges/DirichletSevenEighths.lean`:
`OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re` (family 003).
Every Dirichlet `L`-function is zero-free in `Re s > 7/8`, except at the pole. -/
def DirichletSevenEighths : Prop :=
  ∀ {q : ℕ} [NeZero q] (χ : DirichletCharacter ℂ q) {s : ℂ},
    (7 / 8 : ℝ) < s.re → ¬ (χ = 1 ∧ s = 1) →
      _root_.DirichletCharacter.LFunction χ s ≠ 0

/-- `ComparatorChallenges/PiExponent.lean`: `OAI.PiExponent.main` (family 017).
The irrationality exponent of `π` is `2`. -/
def PiExponentMain : Prop :=
  (∀ ν : ℝ, 2 < ν → ∃ Q : ℤ, 2 ≤ Q ∧
    ∀ p q : ℤ, Q ≤ q →
      (q : ℝ) ^ (-ν) ≤ |Real.pi - (p : ℝ) / (q : ℝ)|) ∧
  sSup {ν : ℝ | 0 < ν ∧
    Set.Infinite {r : ℚ | 2 ≤ r.den ∧
      0 < |Real.pi - (r : ℝ)| ∧
      |Real.pi - (r : ℝ)| < (r.den : ℝ) ^ (-ν)}} = 2

/-- `ComparatorChallenges/KaplanskyDirectFiniteness.lean`:
`OAI.KaplanskyCounterexample.MainClaim` (family 197).
A finite field of characteristic 2 and a finitely generated group whose group
algebra is not directly finite. -/
def KaplanskyMainClaim : Prop :=
  ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K 2),
    ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
      ∃ a b : MonoidAlgebra K G, a * b = 1 ∧ b * a ≠ 1

end OAIHyp
