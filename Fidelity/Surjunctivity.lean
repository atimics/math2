import Fidelity.Vendor.OddKaplansky
import Fidelity.Vendor.KaplanskyDirectFiniteness
import Fidelity.Vendor.KaplanskyFinitelyPresented

/-!
# Kaplansky counterexamples break Gottschalk's surjunctivity (family 197)

OpenAI's odd-characteristic comparator `OAI.OddKaplansky` defines, for `d ∈ K[G]`,
the map `cellular d : K^G → K^G`, `(cellular d x)(g) = ∑ᵤ d(u)·x(g·u)`. With `K`
finite this is a cellular automaton with memory set `supp d`.

This file proves, against that exact definition:

* `cellular_mul`: `cellular a (cellular b x) = cellular (a * b) x` (so `a ↦ cellular a`
  is covariant: the product is `ab`, not `ba`), `cellular_one`, and faithfulness
  (`eq_of_cellular_eq`);
* `ab = 1` makes `cellular b` injective with left inverse `cellular a`
  (`cellular_leftInverse`), and surjectivity of `cellular b` would force `ba = 1`
  (`mul_eq_one_of_surjective`);
* every `cellular d` is a cellular automaton in the Curtis–Hedlund sense
  (`cellular_isCellularAutomaton`).

Consequences for OpenAI's statements:

* `oddKaplansky_mainClaim_iff`: in `OAI.OddKaplansky.MainClaim`, the conjuncts
  "`cellular b` is injective and not surjective" are implied by `ab = 1`, `ba ≠ 1`;
* `not_surjunctive_of_kaplansky`, `not_surjunctive_of_finitelyPresented`,
  `not_surjunctive_of_oddKaplansky`: each Kaplansky comparator gives a finite
  alphabet `K` and a finitely generated (resp. finitely presented) group `G` with an
  injective, non-surjective cellular automaton on `K^G`, i.e. a group that is not
  surjunctive, so Gottschalk's conjecture fails.

What is new, and what is not: the characteristic-two paper proves this transfer in
prose (its §6, following Elek–Szabó), and the odd-characteristic comparator asserts
the cellular conclusion as two extra conjuncts. Neither characteristic-two comparator
states it. Here the transfer is checked in Lean against OpenAI's own `cellular`, it
is applied to all three comparators, and the two extra conjuncts are shown to be
redundant. Every theorem that uses an OpenAI claim takes it as an explicit
hypothesis.
-/

namespace Fidelity

open OAI.OddKaplansky (cellular)

/-- `τ : K^G → K^G` is a cellular automaton over `G` with alphabet `K` (Curtis–Hedlund
form): there are a finite memory set `S ⊆ G` and a local rule `μ : K^S → K` with
`τ x g = μ (s ↦ x (g * s))` for every configuration `x` and cell `g`. -/
def IsCellularAutomaton {K G : Type} [Group G] (τ : (G → K) → G → K) : Prop :=
  ∃ (S : Finset G) (μ : (S → K) → K),
    ∀ (x : G → K) (g : G), τ x g = μ (fun s => x (g * s.1))

section Cellular

variable {K G : Type} [Field K] [Group G]

theorem cellular_zero (x : G → K) (g : G) : cellular (0 : MonoidAlgebra K G) x g = 0 := by
  simp only [cellular, MonoidAlgebra.coeff_zero, Finsupp.sum_zero_index]

theorem cellular_add (d₁ d₂ : MonoidAlgebra K G) (x : G → K) (g : G) :
    cellular (d₁ + d₂) x g = cellular d₁ x g + cellular d₂ x g := by
  simp only [cellular, MonoidAlgebra.coeff_add]
  exact Finsupp.sum_add_index' (fun _ => zero_mul _) (fun _ _ _ => add_mul _ _ _)

theorem cellular_single (u : G) (c : K) (x : G → K) (g : G) :
    cellular (MonoidAlgebra.single u c) x g = c * x (g * u) := by
  simp only [cellular, MonoidAlgebra.coeff_single]
  exact Finsupp.sum_single_index (zero_mul _)

theorem cellular_one (x : G → K) : cellular (1 : MonoidAlgebra K G) x = x := by
  funext g
  rw [MonoidAlgebra.one_def, cellular_single, one_mul, mul_one]

/-- `cellular d` commutes with the left shift `x ↦ x (h * ·)`. -/
theorem cellular_shift (d : MonoidAlgebra K G) (h : G) (x : G → K) (g : G) :
    cellular d (fun k => x (h * k)) g = cellular d x (h * g) := by
  simp only [cellular, mul_assoc]

theorem cellular_single_mul (u : G) (c : K) (b : MonoidAlgebra K G) (x : G → K) (g : G) :
    cellular (MonoidAlgebra.single u c * b) x g = c * cellular b x (g * u) := by
  induction b using MonoidAlgebra.induction_linear with
  | zero => rw [mul_zero, cellular_zero, cellular_zero, mul_zero]
  | add b₁ b₂ h₁ h₂ => rw [mul_add, cellular_add, cellular_add, h₁, h₂, mul_add]
  | single v e =>
    rw [MonoidAlgebra.single_mul_single, cellular_single, cellular_single]
    simp only [mul_assoc]

/-- **Composition law.** `cellular a ∘ cellular b = cellular (a * b)`. -/
theorem cellular_mul (a b : MonoidAlgebra K G) (x : G → K) :
    cellular a (cellular b x) = cellular (a * b) x := by
  funext g
  induction a using MonoidAlgebra.induction_linear with
  | zero => rw [zero_mul, cellular_zero, cellular_zero]
  | add a₁ a₂ h₁ h₂ => rw [add_mul, cellular_add, cellular_add, h₁, h₂]
  | single u c => rw [cellular_single, cellular_single_mul]

/-- Testing against the point mass at `1` reads off the coefficient at `g⁻¹`. -/
theorem cellular_delta (d : MonoidAlgebra K G) (g : G) :
    cellular d ⇑(Finsupp.single (1 : G) (1 : K)) g = d.coeff g⁻¹ := by
  induction d using MonoidAlgebra.induction_linear with
  | zero => rw [cellular_zero, MonoidAlgebra.coeff_zero, Finsupp.zero_apply]
  | add d₁ d₂ h₁ h₂ =>
    rw [cellular_add, h₁, h₂, MonoidAlgebra.coeff_add, Finsupp.add_apply]
  | single u c =>
    rw [cellular_single, MonoidAlgebra.coeff_single]
    by_cases hgu : g * u = 1
    · have hu : u = g⁻¹ := mul_eq_one_iff_eq_inv'.mp hgu
      rw [hgu, Finsupp.single_eq_same, mul_one, hu, Finsupp.single_eq_same]
    · have hu : u ≠ g⁻¹ := fun hu => hgu (mul_eq_one_iff_eq_inv'.mpr hu)
      rw [Finsupp.single_eq_of_ne' (Ne.symm hgu), mul_zero, Finsupp.single_eq_of_ne' hu]

/-- **Faithfulness.** `d ↦ cellular d` is injective. -/
theorem eq_of_cellular_eq {d d' : MonoidAlgebra K G} (h : cellular d = cellular d') :
    d = d' := by
  apply MonoidAlgebra.ext
  apply Finsupp.ext
  intro u
  have hu := congrFun (congrFun h ⇑(Finsupp.single (1 : G) (1 : K))) u⁻¹
  rw [cellular_delta, cellular_delta, inv_inv] at hu
  exact hu

/-- If `ab = 1`, then `cellular a` is a left inverse of `cellular b`. -/
theorem cellular_leftInverse {a b : MonoidAlgebra K G} (hab : a * b = 1) :
    Function.LeftInverse (cellular a) (cellular b) := fun x => by
  rw [cellular_mul, hab, cellular_one]

/-- If `ab = 1`, then `cellular b` is injective. -/
theorem cellular_injective_of_mul_eq_one {a b : MonoidAlgebra K G} (hab : a * b = 1) :
    Function.Injective (cellular b) :=
  (cellular_leftInverse hab).injective

/-- If `ab = 1` and `cellular b` is surjective, then `ba = 1`. -/
theorem mul_eq_one_of_surjective {a b : MonoidAlgebra K G} (hab : a * b = 1)
    (hs : Function.Surjective (cellular b)) : b * a = 1 := by
  apply eq_of_cellular_eq
  funext y
  obtain ⟨x, rfl⟩ := hs y
  have hx : cellular a (cellular b x) = x := cellular_leftInverse hab x
  rw [← cellular_mul, hx, cellular_one]

/-- `ab = 1 ≠ ba` gives an injective, non-surjective `cellular b`. -/
theorem cellular_injective_not_surjective {a b : MonoidAlgebra K G} (hab : a * b = 1)
    (hba : b * a ≠ 1) :
    Function.Injective (cellular b) ∧ ¬ Function.Surjective (cellular b) :=
  ⟨cellular_injective_of_mul_eq_one hab, fun hs => hba (mul_eq_one_of_surjective hab hs)⟩

/-- `cellular d` is a cellular automaton with memory set `supp d` and linear local
rule `p ↦ ∑_{s ∈ supp d} d(s) p(s)`. -/
theorem cellular_isCellularAutomaton (d : MonoidAlgebra K G) :
    IsCellularAutomaton (cellular d) := by
  refine ⟨d.coeff.support, fun p => ∑ s : d.coeff.support, d.coeff s.1 * p s, fun x g => ?_⟩
  exact (Finset.sum_coe_sort d.coeff.support (fun u => d.coeff u * x (g * u))).symm

end Cellular

/-! ## Applications to OpenAI's comparator statements -/

/-- In OpenAI's odd-characteristic `MainClaim`, the cellular-automaton conjuncts are
redundant: they follow from `ab = 1` and `ba ≠ 1`. -/
theorem oddKaplansky_mainClaim_iff :
    OAI.OddKaplansky.MainClaim ↔
      (OAI.OddKaplansky.sourcePrime.Prime ∧ Odd OAI.OddKaplansky.sourcePrime ∧
        ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K OAI.OddKaplansky.sourcePrime),
          Fintype.card K = OAI.OddKaplansky.sourcePrime ^ 4 ∧
          ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
            (∃ g : G, g ≠ 1 ∧ IsOfFinOrder g) ∧
            ∃ a b : MonoidAlgebra K G, a * b = 1 ∧ b * a ≠ 1) := by
  constructor
  · rintro ⟨hp, ho, K, iK, fK, cK, hc, G, iG, gG, ht, a, b, hab, hba, -, -⟩
    exact ⟨hp, ho, K, iK, fK, cK, hc, G, iG, gG, ht, a, b, hab, hba⟩
  · rintro ⟨hp, ho, K, iK, fK, cK, hc, G, iG, gG, ht, a, b, hab, hba⟩
    unfold OAI.OddKaplansky.MainClaim
    exact ⟨hp, ho, K, iK, fK, cK, hc, G, iG, gG, ht, a, b, hab, hba,
      cellular_injective_not_surjective hab hba⟩

/-- Family 197, characteristic two: OpenAI's direct-finiteness counterexample gives a
finitely generated group that is not surjunctive. -/
theorem not_surjunctive_of_kaplansky (h : OAI.KaplanskyCounterexample.MainClaim) :
    ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K 2),
      ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
        ∃ τ : (G → K) → G → K, IsCellularAutomaton τ ∧
          Function.Injective τ ∧ ¬ Function.Surjective τ := by
  obtain ⟨K, iK, fK, cK, G, iG, gG, a, b, hab, hba⟩ := h
  exact ⟨K, iK, fK, cK, G, iG, gG, cellular b, cellular_isCellularAutomaton b,
    cellular_injective_not_surjective hab hba⟩

/-- Family 197, characteristic two, finitely presented: OpenAI's Theorem 1.1
comparator gives a finitely presented group that is not surjunctive. -/
theorem not_surjunctive_of_finitelyPresented
    (h : type_of% @OAI.KaplanskyCounterexample.finitelyPresented_counterexample) :
    ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K 2),
      ∃ (G : Type) (_ : Group G) (_ : Group.IsFinitelyPresented G),
        ∃ τ : (G → K) → G → K, IsCellularAutomaton τ ∧
          Function.Injective τ ∧ ¬ Function.Surjective τ := by
  obtain ⟨K, iK, fK, cK, G, iG, hG, -, a, b, hab, hba⟩ := h
  exact ⟨K, iK, fK, cK, G, iG, hG, cellular b, cellular_isCellularAutomaton b,
    cellular_injective_not_surjective hab hba⟩

/-- Family 197, odd characteristic: the same conclusion from OpenAI's `OddKaplansky`
statement, with the cellular-automaton property made explicit. -/
theorem not_surjunctive_of_oddKaplansky (h : OAI.OddKaplansky.MainClaim) :
    ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K OAI.OddKaplansky.sourcePrime),
      ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
        ∃ τ : (G → K) → G → K, IsCellularAutomaton τ ∧
          Function.Injective τ ∧ ¬ Function.Surjective τ := by
  obtain ⟨-, -, K, iK, fK, cK, -, G, iG, gG, -, a, b, -, -, hinj, hsurj⟩ := h
  exact ⟨K, iK, fK, cK, G, iG, gG, cellular b, cellular_isCellularAutomaton b, hinj, hsurj⟩

end Fidelity
