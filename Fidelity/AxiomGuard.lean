import Lean

/-!
# Axiom guard

`#assert_standard_axioms foo` fails elaboration unless `foo` depends only on
`propext`, `Classical.choice` and `Quot.sound`. It is the Lean-side layer of the
axiom audit in `scripts/Axioms.lean`; `scripts/check_axioms.py` is the other.
-/

namespace Fidelity.AxiomGuard
open Lean Elab Command

/-- The only axioms an audited declaration may use. -/
def standardAxioms : List Name := [``propext, ``Classical.choice, ``Quot.sound]

/-- `#assert_standard_axioms foo` fails elaboration unless `foo` depends only on
`propext`, `Classical.choice` and `Quot.sound` (so `sorryAx` is rejected). -/
elab "#assert_standard_axioms " id:ident : command => do
  let name ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo id
  let axioms ← liftCoreM <| collectAxioms name
  let bad := axioms.toList.filter (fun a => !standardAxioms.contains a)
  unless bad.isEmpty do
    throwError "{name} depends on non-standard axioms: {bad}"
  logInfo m!"{name}: standard axioms only {axioms.toList}"

end Fidelity.AxiomGuard
