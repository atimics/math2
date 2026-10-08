import EndToEnd
import Fidelity.AxiomGuard

/-! Axiom audit for the `EndToEnd` library: CL-1 composed with OpenAI's own proof of
family 172 (rebuilt from byte-identical upstream files). Same two layers as
scripts/Axioms.lean. The first two names are OpenAI's theorems themselves. -/

#assert_standard_axioms OAI.EuclideanRamsey.classification
#assert_standard_axioms OAI.EuclideanRamsey.ramsey_cospherical
#assert_standard_axioms EndToEnd.Fidelity.ramsey_of_cospherical_of_algebraic
#assert_standard_axioms EndToEnd.Fidelity.ramsey_iff_cospherical_of_algebraic
#assert_standard_axioms EndToEnd.algebraic_ramsey_iff_cospherical
#assert_standard_axioms EndToEnd.ramsey_of_cospherical_of_rational

#print axioms OAI.EuclideanRamsey.classification
#print axioms OAI.EuclideanRamsey.ramsey_cospherical
#print axioms EndToEnd.Fidelity.ramsey_of_cospherical_of_algebraic
#print axioms EndToEnd.Fidelity.ramsey_iff_cospherical_of_algebraic
#print axioms EndToEnd.algebraic_ramsey_iff_cospherical
#print axioms EndToEnd.ramsey_of_cospherical_of_rational
