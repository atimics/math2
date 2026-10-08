import Corollaries
import Fidelity.Checks
import Fidelity.Henon
import Fidelity.Parity
import Fidelity.AxiomGuard

/-! Axiom audit, two independent layers:
* `#assert_standard_axioms` (Fidelity/AxiomGuard.lean) makes Lean itself fail on any
  axiom other than propext, Classical.choice, Quot.sound (in particular sorryAx);
* `#print axioms` output is checked by scripts/check_axioms.py against exactly
  the names below (no duplicates, none missing, no Lean errors). -/

#assert_standard_axioms Corollaries.real_zero_le_seven_eighths
#assert_standard_axioms Corollaries.siegel_explicit
#assert_standard_axioms Corollaries.siegel_of_sevenEighths
#assert_standard_axioms Corollaries.zeta_of_sevenEighths
#assert_standard_axioms Corollaries.pi_not_liouvilleWith
#assert_standard_axioms Corollaries.rat_affine_pi_not_liouvilleWith
#assert_standard_axioms Corollaries.pi_not_liouville
#assert_standard_axioms Corollaries.directFiniteness_transfer
#assert_standard_axioms Corollaries.idempotent_of_directFiniteness_witness
#assert_standard_axioms Corollaries.false_of_leftOrder_of_zeroDivisor
#assert_standard_axioms Fidelity.siegel_comparator_of_sevenEighths
#assert_standard_axioms Fidelity.siegel_comparator'_of_sevenEighths
#assert_standard_axioms Fidelity.zeta_comparator_of_sevenEighths
#assert_standard_axioms Fidelity.zeroDivisor_group_not_leftOrderable
#assert_standard_axioms Fidelity.kaplansky_transfer
#assert_standard_axioms Fidelity.scalar_henon_nonexistence
#assert_standard_axioms Fidelity.liouville_eq_one_or_neg_one
#assert_standard_axioms Fidelity.liouville_eq_iff_parity
#assert_standard_axioms Fidelity.liouville_agreement_density

#print axioms Corollaries.real_zero_le_seven_eighths
#print axioms Corollaries.siegel_explicit
#print axioms Corollaries.siegel_of_sevenEighths
#print axioms Corollaries.zeta_of_sevenEighths
#print axioms Corollaries.pi_not_liouvilleWith
#print axioms Corollaries.rat_affine_pi_not_liouvilleWith
#print axioms Corollaries.pi_not_liouville
#print axioms Corollaries.directFiniteness_transfer
#print axioms Corollaries.idempotent_of_directFiniteness_witness
#print axioms Corollaries.false_of_leftOrder_of_zeroDivisor
#print axioms Fidelity.siegel_comparator_of_sevenEighths
#print axioms Fidelity.siegel_comparator'_of_sevenEighths
#print axioms Fidelity.zeta_comparator_of_sevenEighths
#print axioms Fidelity.zeroDivisor_group_not_leftOrderable
#print axioms Fidelity.kaplansky_transfer
#print axioms Fidelity.scalar_henon_nonexistence
#print axioms Fidelity.liouville_eq_one_or_neg_one
#print axioms Fidelity.liouville_eq_iff_parity
#print axioms Fidelity.liouville_agreement_density
