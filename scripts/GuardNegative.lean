import Fidelity.AxiomGuard

/-! Negative test: CI requires this file to FAIL, proving the guard is not vacuous. -/

theorem guard_negative_sorry : (1 : Nat) = 2 := by sorry

#assert_standard_axioms guard_negative_sorry
