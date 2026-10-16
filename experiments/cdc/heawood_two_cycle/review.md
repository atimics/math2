# Independent review of the exact two-cycle question

Alexander Richard Towell, with substantial OpenAI Codex assistance.
Separately tasked AI review, 2026-10-16. This is not human peer review or
proof-assistant verification. No historical novelty claim is made.

## Finding

The specified original flow cannot reach a three-colorable affine palette
in zero, one, or two legal nonzero constant-XOR changes on simple cycles.
The independent check establishes this without recomputing the discovery
palette histogram or enumerating the 22,637 reported distinct final flows.
Its proof combines a graph property with 1,393 binary-projection checks.

The separate three-step witness subsequently found by the parent is outside
this review's lower-bound checker. The parent's witness verifier must check
it before combining the lower bound with an exact-distance conclusion.

## Why three colors force rank two on this graph

The graph has 24 perfect matchings, and the complement of every one is a
Hamiltonian cycle. The independent checker exhausts the matchings by choosing
an edge at the least unmatched vertex. Each perfect matching follows exactly
one recursion branch, so no symmetry or sampling assumption enters the count.
In a cubic graph the complements of perfect matchings are exactly the spanning
2-factors. Thus every spanning 2-factor of this graph is Hamiltonian.

At a cubic vertex, the incident nonzero flow values are three distinct
vectors whose XOR is zero. Their translates are three distinct palette
labels, and the three incident edge pairs form a triangle on these labels.
A proper palette coloring with at most three colors therefore uses all three
colors at every vertex. The edges carrying a given color form a spanning
2-factor: the unique local vector label of that color belongs to exactly two
incident pairs.

Compatibility of the endpoint pairs makes this same vector label continue
along each edge of the 2-factor. Since the 2-factor is Hamiltonian, the label
is constant globally. Consequently there are exactly three underlying vector
labels, say a, b, c. Every edge flow is one of a XOR b, a XOR c, b XOR c;
these are the three nonzero vectors of a two-dimensional subspace. Vector
label zero is allowed and causes no exception to this argument.

Conversely, a nowhere-zero cubic flow whose values lie in a two-dimensional
subspace uses all three nonzero vectors of that subspace at every vertex.
Translations identically zero then give compatible pairs, and the palette
is a triangle. Hence, on this graph, admitting a three-colorable affine
palette is equivalent to the edge values spanning dimension two.

This implication uses Hamiltonicity of **every** spanning 2-factor. Mere
connectedness, bipartiteness, or the existence of one Hamiltonian cycle would
not suffice. It does not assume that label classes are connected in the
general definition; their connectedness here follows from the checked graph
property.

## The smaller complete obstruction check

For a nonzero linear functional p on F2^3 and flow g, define

```
Q_p(g) = { e : p(g(e)) = 1 }.
```

There are seven functionals, represented by binary dot product with integers
1 through 7. A flow has rank at most two exactly when some Q_p is empty.
The checker verifies that all seven original projections are nonempty.

For one further cycle change with nonzero vector d on simple cycle C,

```
Q_p(g XOR d 1_C) = Q_p(g) symmetric_difference (p(d) C).
```

When Q_p(g) is nonempty, the new projection can be empty only if p(d)=1
and C=Q_p(g). If this support is disconnected, no such simple cycle exists.
If it is a simple cycle but contains every one of the four flow values d
with p(d)=1, every possible d creates a zero edge and is illegal.

The checker independently generates all graph cycles from the binary cycle
space. The graph is connected with 21 edges and 14 vertices, so a spanning
tree leaves eight free chord bits. Every assignment of these bits determines
the tree bits uniquely by vertex parity, from leaves to root. This gives all
256 even supports. Cubicity makes every active degree two, so exactly the
connected nonempty supports are simple cycles. There are 213.

For each cycle, the checker takes every nonzero vector absent from the flow
values on that cycle. Absence is exactly the nowhere-zero condition; XOR
conservation follows because two incident edges change at each cycle vertex
and is also checked directly. This produces all 199 legal first moves.
For every resulting flow and all seven functionals, it verifies:

| Projection type | Count | Obstruction to a rank-reducing second move |
|---|---:|---|
| Empty | 0 | No first move already has rank two |
| One simple cycle | 739 | All four eligible XOR vectors occur on the cycle |
| Two disjoint six-cycles | 654 | The support is not a simple cycle |
| Total | 1,393 | Every first flow and nonzero functional covered |

The 739 simple-projection barriers split by functional 1 through 7 as
`[92,95,95,178,95,92,92]`. Their cycle-length counts are
`{6:12,8:12,10:156,12:343,14:216}`.

An initially tempting simplification is false: the original p=4 projection
is a 12-cycle, while the other six projections are disconnected pairs of
six-cycles. The argument above covers that case, including first changes
whose XOR vector has p(d)=0. It does not assume both changes affect every
projection.

## Completeness and scope audit

The lower bound permits the same cycle twice, overlapping cycles, and equal
XOR vectors. It makes no disjointness or distinctness assumption. The final
projection identity handles all of these possibilities. Cycle orientation
and starting vertex do not matter for constant XOR changes; edge sets identify
the operation. Every intermediate and final flow in the allowed domain must
be nowhere zero. A route through zero edges is outside the claim.

The first-move enumeration is complete, and the projection criterion considers
every possible second move implicitly. It therefore does not require either
a final-flow deduplication argument or the predecessor's affine-lift solver.
Root-fixed translations are irrelevant to this lower-bound proof. No generic
cycle-double-cover theorem or unrestricted cover obstruction is invoked.

The obstruction concerns at most two legal cycle operations. It is not a
minimum-support result, a classification of all Heawood flows, or a universal
repair theorem. A general conservative difference may require several cycle
terms, so it is not excluded merely by this two-operation result.

## Implementation and trust boundary

`review_check.verify(source_path=DEFAULT_SOURCE)` reads only the pinned
original source certificate. It validates its exact SHA256 bytes, reconstructs
the specified ordered graph from Fano-plane incidence, validates the original
flow, and recomputes the structural receipt above. It imports no discovery or
predecessor-checker implementation. It does not validate the source's saved
affine lifts because none is needed for this argument.

The helper functions `cycle_space`, `perfect_matchings`, and
`projection_barriers` expose the finite checks for tests. `verify` itself
supplies the complete generated cycle domain; `projection_barriers` also
checks that a caller-supplied cycle domain is complete. All validation uses explicit exceptions and
survives Python `-O`.

The checker does **not** consume `search-result.json`. Thus its reported
296,709 visited ordered candidates, 46,837 legal sequences, 22,637 unique
final flows, timing, and exact chromatic histogram remain discovery output
unless separately replayed. The structural result independently establishes
the requested negative conclusion despite that narrower validation boundary.

Both commands below passed with identical structural counts:

```
python experiments/cdc/heawood_two_cycle/review_check.py
python -O experiments/cdc/heawood_two_cycle/review_check.py
```

Additional controls rejected a byte-modified source, a rank-two comparator,
a rank-three flow one legal move from that comparator, and an incomplete
cycle domain. The parent's 13 structural, witness, and search tests passed
under `python -m unittest`. An initial ordinary pytest collection attempt
exposed a missing package initializer; this was reported to the parent for
the final test packaging pass.

The parent's `PROOF.md` and `witness.py` were subsequently read for statement
fidelity. Their reduction and explicit three-step witness have no additional
disjointness, global-gauge, or nonzero-palette-label assumption. The direct
witness test passes. Together with the independently checked lower bound,
that verified witness supports the parent's exact-distance-three statement.

Remaining trust is ordinary Python execution plus the written implications
connecting these exact finite checks. The checker is not a proof-assistant
kernel certificate.
