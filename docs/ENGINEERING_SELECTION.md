# Engineering selection after the first pilot

The goal is an observable benefit on a specified workload, taking the corpus
claims as premises. A theorem can improve runtime, representation size,
solution quality or an actionable guarantee. These are different outcomes;
a smaller intermediate graph is not automatically a faster solver.

## Admission rule

Before implementing a candidate, record the workload and exact assumptions,
the strongest relevant practical baseline, the operation or guarantee that
changes, a finite cost estimate, and a success criterion. Reject candidates
whose constants or prerequisite computations erase the proposed benefit.
Measurements then determine feasibility; passing correctness tests alone
does not establish the benefit.

## Decisions

| Candidate | Workload and baseline | Finite comparison | Decision |
|---|---|---|---|
| 120: quota gadgets | Prescribed-degree edge subsets; dense reduction with the same exact solver | PR #5's half-quota 256-edge star reduces `V+E` by 32.8% but increases vertices 12.3-fold. Every star is solved by leaf forcing before matching is needed. The near-linear matching engine was not implemented. | Keep as a component-overhead pilot. It does not test the full breakthrough or difficult application workloads. Defer further optimization until preprocessing and nontrivial instances are specified. |
| 325: complete Crouzeix bound | Certify generic polynomial functions of nonnormal matrices; compare specialized matrix bounds too | Universal multiplier falls from `1+sqrt(2)` to 2. If scalar error is `C q^j`, the continuous degree saving is `log((1+sqrt(2))/2)/abs(log(q))`: 1.79 at `q=.9`, 0.27 at `q=.5`. Integer savings may be zero, before paying for rigorous numerical-range enclosure. | No new implementation. An existing code path already using the universal bound can update its multiplier; no such workload has been identified here. |
| 128: shortest common superstring | Exact pooling of overlapping strings; maximum-overlap greedy plus exact OPT for tiny sets | The published construction enumerates `O(L^2)` substrings and periodic blocking placements before producing its small output graph. No usable finite exponent/crossover is supplied. Its lower-bound certificate has not been shown to beat standard overlap/assignment lower bounds on an actual workload. | Defer both full algorithm and certificate prototype. No evidence yet that either beats the relevant baseline. |
| 115: fixed-margin tables | Uniform contingency-table null models; compare exact small-table enumeration and practical MCMC | The specified approximate sampler uses `T=d^200(k+b)^2` transitions. Even `14^200 > 10^229` before other factors. Exact sampling additionally has rare exhaustive correction. | Reject this implementation as a practical next step. Polynomial asymptotics do not provide a usable runtime here. |
| 131: undirected graph null models | Approximate-uniform graphs preserving labeled degrees; existing Curveball with a fixed-step heuristic | The proof's pair-fiber Poincare inequality directly gives Curveball gap at least `1/binom(n,2)`. A conservative integer stopping rule needs about tens to hundreds of thousands of trades for the selected 20–50 vertex cases. | Admit a finite-time **bias guarantee**, not a faster kernel. Implement, independently check transitions and measure full-budget execution. |

These decisions are scoped to the inspected candidates, not an exhaustive
negative assessment of the corpus or a claim that the rejected theorems
have no application.

## Why the numerical comparison matters

For GMRES, the actual residual is directly measurable; a numerical-range
certificate adds work. Dissipative evolution has a classical contraction
bound of 1, and resolvents have the direct bound
`||(zI-A)^-1|| <= 1/dist(z,W(A))`. For Faber polynomials on convex enclosures,
[Beckermann–Crouzeix (2013)](https://arxiv.org/abs/1310.1356) already gives
the relevant factor-two basis estimate. The new generic theorem cannot be
credited with improving those existing specialized guarantees.

Even where the generic bound applies, a planning example of 32 support
directions with 50 Hermitian matvecs each costs 1,600 matvecs. Saving two
degrees per application needs about 800 applications merely to amortize
that work. This is an illustrative operation count, not a measured or
certified enclosure algorithm; obtaining rigorous upper eigenvalue bounds
and controlling floating-point error adds work.

## The admitted experiment and its result

The [Curveball experiment](../experiments/curveball/README.md) derives and
implements an integer trade budget for TV at most `2^-k`, valid from any
starting realization under family 131's premise. It uses the stronger
pair-resampling statement inside the proof, rather than transferring its
looser switch-chain bound unchanged.

At `k=7`, full-budget runs on three synthetic heterogeneous networks took
median 0.155 seconds (20 vertices), 1.55 seconds (30) and 8.21 seconds (50).
All 18 benchmark outputs preserve the labeled degrees; exact rational
kernel tests cover 125 small states. The implementation and documentation
distinguish those finite checks from the assumed general mixing theorem.

The fixed `10*m`-trade policy is faster but carries no TV guarantee from
this experiment. The demonstrated payoff is an affordable sufficient
stopping rule for **one small-network draw** when controlled bias matters.
No application-level anomaly-detection gain, kernel speedup, large-network
scalability, exact-uniform output or independent batch guarantee is claimed.
The next application evaluation should supply a real network, a statistic,
a required number of null draws, an allowed joint bias and a latency budget.

## Pinned corpus sources

All source references use `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

- [120 factor reduction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-September-24-2026/build/sections/10-f-factors.tex).
- [325 theorem and prior bound](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex).
- [128 algorithm and cost accounting](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Polynomial-Time-2-Approximation-for-Shortest-Common-Superstring-September-24-2026/build/sections/07-algorithm.tex).
- [115 explicit sampling schedule](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/algorithms.tex).
- [131 pair fibers](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/setup.tex) and [Poincare inequality](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/mixing.tex).
