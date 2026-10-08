import Corollaries
import Fidelity.Vendor.DirichletSevenEighths
import Fidelity.Vendor.SiegelZeros
import Fidelity.Vendor.QuasiRiemannHypothesis
import Fidelity.Vendor.PiExponent
import Fidelity.Vendor.KaplanskyDirectFiniteness
import Fidelity.Vendor.TorsionFreeZeroDivisors

/-!
# Fidelity checks against OpenAI's own comparator statements

`Fidelity/Vendor/` holds unmodified copies of six files from
`openai/math@adc7f1241b42e322a6451854ab7e4b4c146bf78a`,
`lean/ComparatorChallenges/`. CI checks that they match upstream byte for byte.
Their proofs are `sorry`, as in the upstream comparator files; OpenAI's actual
proofs live in its `OAI` library.

This file checks two things in the Lean kernel:

1. **Hypotheses are faithful.** Each `OAIHyp` statement is definitionally
   equal to the type of OpenAI's theorem, so this library assumes nothing
   beyond what OpenAI claims to have proved.
2. **Comparators that are redundant.** The theorems in section 2 derive the
   *statements* of OpenAI's separately formalized Siegel-zero and zeta
   comparators from the Dirichlet 7/8 statement alone. They take that statement
   as a hypothesis and never use a `sorry`d proof, as `scripts/Axioms.lean`
   confirms.
-/

namespace Fidelity

/-! ## 1. Hypotheses are faithful -/

example : OAIHyp.DirichletSevenEighths ↔
    type_of% @OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re :=
  Iff.rfl

example : OAIHyp.PiExponentMain ↔ type_of% @OAI.PiExponent.main := Iff.rfl

example : OAIHyp.KaplanskyMainClaim ↔ OAI.KaplanskyCounterexample.MainClaim := Iff.rfl

/-! ## 2. Comparators that are redundant -/

/-- OpenAI's `SiegelZeros` comparator (first form) follows from its
`DirichletSevenEighths` comparator, with `c = log 3 / 8`. -/
theorem siegel_comparator_of_sevenEighths :
    type_of% @OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re →
    type_of% @OAI.SiegelZeros.WeightedTorusJets.exists_absolute_real_zero_gap :=
  fun h => Corollaries.siegel_of_sevenEighths h

/-- OpenAI's `SiegelZeros` comparator (second form) follows as well. -/
theorem siegel_comparator'_of_sevenEighths :
    type_of% @OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re →
    type_of% @OAI.SiegelZeros.WeightedTorusJets.dirichletRealZeroBound_proof := by
  intro h
  obtain ⟨c, hc, hbound⟩ := Corollaries.siegel_of_sevenEighths h
  exact ⟨c, hc, fun q _ hq χ hprim hχ hreal β hβ =>
    hbound q hq χ hprim hχ hreal β hβ.1 hβ.2.1 hβ.2.2⟩

/-- OpenAI's `QuasiRiemannHypothesis` comparator (for `ζ`) is the modulus-1 case of
`DirichletSevenEighths`. -/
theorem zeta_comparator_of_sevenEighths :
    type_of% @OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re →
    type_of% @OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re :=
  fun h => @Corollaries.zeta_of_sevenEighths h

/-! ## 3. Applications to OpenAI's statements -/

/-- Family 196: OpenAI's finitely presented torsion-free group with zero
divisors in `𝔽₂[G]` admits no left-invariant linear order. -/
theorem zeroDivisor_group_not_leftOrderable :
    OAI.TorsionFreeZeroDivisors.MainTheorem →
    ∃ (G : Type) (_ : Group G), Group.IsFinitelyPresented G ∧
      OAI.TorsionFreeZeroDivisors.TorsionFree G ∧
      ∀ [LinearOrder G], MulLeftStrictMono G → False := by
  rintro ⟨G, inst, hfp, htf, -, α, β, hα, hβ, h0⟩
  refine ⟨G, inst, hfp, htf, ?_⟩
  intro _ _
  exact Corollaries.false_of_leftOrder_of_zeroDivisor hα hβ h0

/-- Family 197: the direct-finiteness failure survives base change along any
ring map out of OpenAI's finite field. -/
theorem kaplansky_transfer :
    OAI.KaplanskyCounterexample.MainClaim →
    ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K 2),
      ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
        ∀ (L : Type) [Field L] (_ : K →+* L),
          ∃ a b : MonoidAlgebra L G, a * b = 1 ∧ b * a ≠ 1 :=
  Corollaries.directFiniteness_transfer

end Fidelity
