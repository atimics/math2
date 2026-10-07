import Corollaries
import Fidelity.Checks

-- Every declaration below must depend only on propext, Classical.choice, Quot.sound.
-- scripts/check_axioms.py fails CI on anything else (in particular sorryAx).
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
