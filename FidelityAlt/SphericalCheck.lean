import FidelityAlt.Vendor.EuclideanRamseySpherical

/-!
# Kernel check for CL-1's restated hypothesis (family 172)

`Fidelity/AlgebraicRamsey.lean` proves *Ramsey ⇔ spherical* for algebraic
configurations. Its reverse direction uses OpenAI's `classification` comparator
(`EuclideanRamsey.lean`). Its forward direction is the hypothesis
`Fidelity.RamseyCosphericalStatement`, which restates OpenAI's
`ramsey_cospherical` comparator (`EuclideanRamseySpherical.lean`).

The two comparator files cannot be imported together: both declare
`OAI.EuclideanRamsey.Space`, `Congruent` and `Ramsey`. This separate library
imports only the spherical comparator, states the same `Prop` with the same
source text, and proves in the kernel that it is equivalent to OpenAI's
statement.

CI (`scripts/check_same_text.py`) then checks two things byte for byte:
* the shared definitions `Space`, `Congruent` and `Ramsey`, and their
  surrounding namespace and `open` context, in the two vendored files;
* the text of `RamseyCosphericalStatement` here and in
  `Fidelity/AlgebraicRamsey.lean`.

Together these close the gap noted in the catalogue entry CL-1.
-/

namespace FidelityAlt

open OAI.EuclideanRamsey (Space Ramsey)

def RamseyCosphericalStatement : Prop :=
  ∀ (s d : ℕ) (a : Fin s → Space d), Function.Injective a → Ramsey a →
    EuclideanGeometry.Cospherical (Set.range a)

/-- The restated hypothesis is exactly OpenAI's `ramsey_cospherical` statement. -/
theorem ramseyCosphericalStatement_iff_comparator :
    RamseyCosphericalStatement ↔ type_of% @OAI.EuclideanRamsey.ramsey_cospherical := by
  unfold RamseyCosphericalStatement
  constructor
  · intro h s d a ha hR
    exact h s d a ha hR
  · intro h s d a ha hR
    exact h a ha hR

end FidelityAlt
