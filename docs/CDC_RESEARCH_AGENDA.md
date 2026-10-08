# After Cycle Double Cover: which problems should move next?

Reviewed 2026-10-08 UTC. This dossier takes the July 2026 Cycle Double Cover
(CDC) breakthrough as its input and identifies the resulting research agenda.
It extends the repository's consequence-first approach to an earlier public AI
result outside the pinned October corpus. It is a separate dossier, not an
addition to the 38-entry cross-family catalogue.

## Input and evidence

The public artifact is [openai/cdc-lean at 577e9d9](https://github.com/openai/cdc-lean/tree/577e9d9ea326d520f80672ee69b830bf1d513df5).
Its endpoint, [CDCLean.cycleDoubleCover_of_bridgeless](https://github.com/openai/cdc-lean/blob/577e9d9ea326d520f80672ee69b830bf1d513df5/CDCLean/Main.lean),
states existence for finite loopless bridgeless multigraphs. Its
[verification record](https://github.com/openai/cdc-lean/blob/577e9d9ea326d520f80672ee69b830bf1d513df5/VERIFICATION.md)
reports a successful build and standard Lean axioms only.

Sang-il Oum's [expert exposition, arXiv:2607.16356v3](https://arxiv.org/html/2607.16356v3)
attributes the proof to GPT-5.6 and provides a human-readable argument and
successor conjectures. We inspected these sources; we did not rebuild the
upstream Lean development. No theorem in this dossier is Lean-checked in math2.

## Two different quantities to optimize

An ordinary CDC is a list of connected cycles using every edge exactly twice.
A **k-CDC** instead permits at most k Eulerian subgraphs, each potentially
containing many connected cycles. Decomposing these subgraphs proves ordinary
existence but can increase the number of connected cycles.

Accordingly, minimizing the number of Eulerian covering subgraphs and
minimizing the total number of connected cycles are different problems.
An 8-CDC does not mean eight connected cycles.

## What the breakthrough settles, and what remains

The following status statements are recorded in Oum's exposition (§§1, 9);
the proposed work in the last column is our research synthesis.

| Target | Status given CDC and the cited classical results | Next work |
|---|---|---|
| Ordinary CDC existence | Settled for bridgeless graphs | Reuse the construction; stop searching for counterexamples to this statement |
| At most eight Eulerian covering subgraphs | Obtained by the proof | Investigate compression to five |
| At most five Eulerian covering subgraphs | Remains a conjecture | Study the obstruction to reducing the label set |
| Orientable 5-CDC | Remains a conjecture; would imply a nowhere-zero mod-5 flow | Seek compatible orientations, not merely undirected coverage |
| At most n/2 connected cycles in simple 2-connected cubic graphs, excluding K4 | Follows using Lai–Yu–Zhang | Study equality and constructive optimization |
| At most n−1 connected cycles in all simple 2-edge-connected graphs | Remains a conjecture | Control cycle count through graph reductions |
| CDC existence for coloopless regular matroids | Follows using Jamshy–Tarsi | Investigate size bounds depending on matroid parameters |
| A uniform constant bound for all coloopless regular matroids | False: cographic examples require unbounded size | Restrict the class or allow parameter-dependent bounds |
| Berge–Fulkerson's six perfect matchings, twice per edge | Remains a conjecture | Enforce matching structure rather than infer it from CDC |

These are known implications and boundaries, with attribution. They are not
claimed as new corollaries discovered by math2.

## Written bridge: why five is the first possible universal target

**D — complete written derivation.** For a finite loopless cubic graph, existence
of a 4-CDC implies proper 3-edge-colorability.

Pad a 4-CDC with empty subgraphs if necessary and call its members A, B, C, D.
Every edge belongs to exactly two of them. Form

$$
X=A\triangle B,\qquad Y=A\triangle C,\qquad Z=A\triangle D.
$$

Symmetric differences of Eulerian edge sets are Eulerian. For an edge whose
pair contains A, exactly two of X,Y,Z contain it; for a pair not containing A,
the same is true. Thus X,Y,Z are a 3-CDC.

At a cubic vertex each of these three subgraphs has degree zero or two.
Their degrees sum to six because each of the three incident edges is covered
twice. Each therefore has degree two and omits precisely one incident edge.
Color an edge by the unique member of X,Y,Z that omits it. The three incident
edges receive different colors, proving proper 3-edge-colorability.

Conversely, given three edge-color classes M1,M2,M3, use their pairwise unions.
Every union has degree two at each vertex and every edge occurs twice.
This constructs a 3-CDC and hence a 4-CDC.

The Petersen graph is bridgeless and not 3-edge-colorable, so a universal
4-CDC statement is impossible. A universal 5-CDC is the sharp possible
constant target. This restates Jaeger's classical equivalence (§9.2); it does
not prove that five always suffices.

## Written bridge: orientations would unlock mod-5 flows

**D — complete written derivation.** An orientable k-CDC, for k ≥ 2, gives a
nowhere-zero flow with values in the cyclic group Z/kZ.

Fix a reference orientation for every edge. Pad the cover to k members.
Let chi_i be the signed incidence vector of its ith directed Eulerian
subgraph: +1 along the reference orientation, −1 against it, and zero
when absent. Each chi_i conserves flow at every vertex. Consequently,

$$
\phi=\sum_{i=1}^{k}i\,\chi_i\pmod{k}
$$

also conserves flow. Each edge occurs in two distinct members i and j in
opposite directions, so its value is ±(i−j) modulo k. Since
0 < |i−j| < k, that value is nonzero.

Taking k=5 gives the mod-5 flow statement. The missing research step is
constructing an orientable 5-CDC; the undirected CDC input does not supply
it. This classical bridge is included to explain the payoff of orientation
research, not as a new theorem (Oum §9.3).

## Three investigations to prepare first

1. **Five-cover compression.** Start from explicit eight-label covers of
   bridgeless cubic graphs. Measure when labels can be reassigned while
   preserving even degree and exact double coverage. Compare restricted
   relabeling with unrestricted searches for five-member covers: failure
   of a restricted transformation is not a counterexample to 5-CDC.

2. **Orientability as a separate constraint.** For small graph classes, jointly
   search cover membership and direction assignments. Report the number
   of covering subgraphs, exact coverage, and signed conservation separately.
   A checker should reject either missing orientation compatibility or
   incorrect edge multiplicity. This targets the extra structure needed
   by the flow bridge above.

3. **Connected-cycle economy.** Given an explicit CDC, optimize its decomposition
   and track how splitting, expansion, and projection change connected-cycle
   count. Compare cubic and noncubic cases. This investigates why an existence
   construction may fail to preserve the small-cover bounds.

Each campaign should retain its graph generator, exact problem statement,
witness, independent checker, and search limits. SAT failure without an
UNSAT certificate establishes only that the search found no witness.
Finite experiments can suggest a transformation or obstruction lemma; the
universal conjectures still require proofs.

## Matroid boundary and a useful negative research decision

Oum §9.5 records CDC existence for binary coloopless matroids without an
F7* minor, via Jamshy–Tarsi; regular matroids are included. It also records
the Linial–Meshulam–Tarsi obstruction: M*(K_n) requires n covering cycles
for n ≥ 5.

The useful next question therefore depends on class and parameters:
which decomposition restrictions permit a constant bound, and which rank
or size parameters control the minimum cover? A project claiming a
universal regular-matroid 5-CDC would start from a false target.

## Sources and verification scope

- OpenAI, [pinned source and verification record](https://github.com/openai/cdc-lean/tree/577e9d9ea326d520f80672ee69b830bf1d513df5).
- Sang-il Oum, [A proof of the cycle double cover conjecture by OpenAI:
  An exposition, v3](https://arxiv.org/html/2607.16356v3).
  §9 gives precise successor statements and classical attributions.
- Classical bridges are credited there to Jaeger; the cubic small-cover
  result to Lai, Yu and Zhang (1994); matroid existence to Jamshy and
  Tarsi (1989); the cographic obstruction to Linial, Meshulam and Tarsi (1988).

The two D sections are written derivations, reviewed against the cited
exposition. The three investigations are research leads. Upstream verification
is reported evidence, not a fresh math2 build. No source, axiom audit, or
catalogue tier count is changed by this dossier.
