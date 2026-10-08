import Lake
open Lake DSL

package «oai-math-corollaries» where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

/-- The corollaries. Mathlib only; OpenAI's results appear as explicit hypotheses. -/
@[default_target]
lean_lib Corollaries where

/-- Kernel checks against verbatim copies of OpenAI's comparator statements. -/
lean_lib Fidelity where

/-- Kernel checks against comparator files that clash with ones in `Fidelity`
(they redeclare the same OpenAI names), so they are built separately. -/
lean_lib FidelityAlt where
