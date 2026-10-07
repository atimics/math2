import Corollaries.Hypotheses

/-!
# Group-ring consequences (families 196, 197, 207)

* `directFiniteness_transfer`: OpenAI's Kaplansky counterexample over a finite
  field `K` survives every ring map `K →+* L`. So, for example, it holds over
  any field containing `K`, including the algebraic closure of `𝔽₂`. The
  corpus only states it over `K` itself.
* `idempotent_of_directFiniteness_witness`: in any ring, a triple `ab = 1`,
  `ac = 0`, `c ≠ 0` (the shape of the *torsion-free* family-197 theorem)
  produces an idempotent other than `0` and `1`, namely `ba`. So the torsion-free
  counterexample also disproves Kaplansky's **idempotent** conjecture in
  characteristic 2, and shows that family 207's characteristic-0 hypothesis is
  sharp. (That paper has no comparator, so this is the ring-theoretic step only.)
* `false_of_leftOrder_of_zeroDivisor`: a group whose group ring over a domain
  has zero divisors cannot be left-orderable. Applied to family 196's group,
  this gives a corollary the corpus doesn't state. The application to OpenAI's
  `MainTheorem` is in `Fidelity`.
-/

namespace Corollaries

open OAIHyp

/-- Base change along any ring hom preserves OpenAI's direct-finiteness
failure. -/
theorem directFiniteness_transfer (h : KaplanskyMainClaim) :
    ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K 2),
      ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
        ∀ (L : Type) [Field L] (φ : K →+* L),
          ∃ a b : MonoidAlgebra L G, a * b = 1 ∧ b * a ≠ 1 := by
  obtain ⟨K, iK, fK, cK, G, iG, gG, a, b, hab, hba⟩ := h
  refine ⟨K, iK, fK, cK, G, iG, gG, fun L _ φ => ?_⟩
  have hinj : Function.Injective (MonoidAlgebra.mapRingHom G φ) := by
    intro x y hxy
    apply MonoidAlgebra.ext
    ext m
    have hm := congrArg (fun z => z.coeff m) hxy
    simp only [MonoidAlgebra.coeff_mapRingHom] at hm
    exact φ.injective hm
  refine ⟨MonoidAlgebra.mapRingHom G φ a, MonoidAlgebra.mapRingHom G φ b, ?_, ?_⟩
  · rw [← map_mul, hab, map_one]
  · intro h1
    apply hba
    apply hinj
    rw [map_mul, h1, map_one]

/-- In any ring, `ab = 1`, `ac = 0`, `c ≠ 0` give a nontrivial idempotent
`ba`, plus the zero-divisor pair `(a, c)`. -/
theorem idempotent_of_directFiniteness_witness {R : Type*} [Ring R]
    {a b c : R} (hab : a * b = 1) (hac : a * c = 0) (hc : c ≠ 0) :
    IsIdempotentElem (b * a) ∧ b * a ≠ 0 ∧ b * a ≠ 1 ∧ a ≠ 0 := by
  have hnt : (1 : R) ≠ 0 := by
    intro h10
    exact hc (by rw [← one_mul c, h10, zero_mul])
  refine ⟨?_, ?_, ?_, ?_⟩
  · show b * a * (b * a) = b * a
    rw [mul_assoc, ← mul_assoc a b a, hab, one_mul]
  · intro h0
    apply hnt
    calc (1 : R) = a * b * (a * b) := by rw [hab, one_mul]
      _ = a * (b * a) * b := by simp only [mul_assoc]
      _ = 0 := by rw [h0, mul_zero, zero_mul]
  · intro h1
    apply hc
    calc c = b * a * c := by rw [h1, one_mul]
      _ = b * (a * c) := mul_assoc _ _ _
      _ = 0 := by rw [hac, mul_zero]
  · intro ha
    apply hnt
    rw [← hab, ha, zero_mul]

/-- If `R[G]` has zero divisors for a domain `R`, then `G` has no left-invariant
linear order. -/
theorem false_of_leftOrder_of_zeroDivisor {G : Type*} [Group G] [LinearOrder G]
    [MulLeftStrictMono G] {R : Type*} [Semiring R] [NoZeroDivisors R]
    {α β : MonoidAlgebra R G} (hα : α ≠ 0) (hβ : β ≠ 0) (h0 : α * β = 0) :
    False :=
  (mul_eq_zero.mp h0).elim hα hβ

end Corollaries
