# Repairing the specified Heawood flow by one cycle change

**Exact finite classification.** For the previously certified Heawood flow
whose every affine lift has a `K7` palette, XOR one nonzero vector `d` onto
the flow values along one simple cycle. Retain only changes that leave every
edge nonzero. Among all **199 admissible changes**, 168 admit a five-colorable
affine palette, while 31 still require seven colors. None admits three colors.

A six-edge change already admits four colors. Six is also the minimum number
of changed edges among **all distinct conservative flows** on this graph,
not merely among the tested one-cycle changes; the short support argument is
given below. This is not a universal repair theorem or a minimum-distance
claim for producing three colors.

Alexander Richard Towell, with substantial OpenAI Codex assistance. Exact
finite computation, written arguments and separate AI review; no proof-assistant
kernel verification, human peer review or historical novelty claim.

## Complete finite domain

Use the exact ordered graph and original flow in the preceding
[Heawood packet](../heawood/README.md). A change `(C,d)` sends
`f(e)` to `f(e) XOR d` on cycle `C`, leaving other edges unchanged. At each
cycle vertex, two incident values change by `d`, so their changes cancel in
the conservation equation. The changed flow is nowhere zero exactly when
`d` is absent from the original values on `C`.

The graph has 213 simple cycles. The table classifies **every** admissible
cycle/vector pair by the smallest palette chromatic number over **all** its
affine lifts:

| Cycle length | Simple cycles | Minimum 4 | Minimum 5 | Minimum 7 | Admissible changes |
|---|---:|---:|---:|---:|---:|
| 6 | 28 | 21 | 30 | 7 | 58 |
| 8 | 21 | 15 | 12 | 0 | 27 |
| 10 | 84 | 21 | 36 | 21 | 78 |
| 12 | 56 | 9 | 12 | 3 | 24 |
| 14 | 24 | 6 | 6 | 0 | 12 |
| Total | 213 | 72 | 96 | 31 | 199 |

There are 374 root-fixed lifts across these 199 flows, at most four for any
one flow. Root fixation loses no chromatic possibilities: XORing all vertex
translations by one common vector relabels every palette isomorphically.
Different `(C,d)` pairs yield different flows because their nonzero difference
supports recover `C`, and any changed edge recovers `d`.

This exhaustive neighborhood is a new search class relative to the earlier
fixed-flow audit. It does not enumerate all Heawood flows or claim that every
failed change can subsequently be repaired by another cycle.

## Explicit minimum-support repair

The six-cycle is the closed vertex sequence

```
0, 8, 4, 11, 1, 10, 0.
```

Its zero-based edge set is `[0,1,4,5,12,13]`. XOR `d=4` on those edges to get

```
[5,6,3,4,2,6,1,4,5,3,7,4,2,5,7,7,5,2,5,3,6].
```

A compatible root-fixed translation vector is

```
[0,1,2,0,1,1,0,0,1,2,1,0,0,1].
```

Its palette uses labels `{3,4,5,6,7}`. The color map
`3->0, 4->1, 5->1, 6->2, 7->3` is proper, and `{3,4,6,7}` is a clique.
Thus this palette has chromatic number exactly four. The certificate retains
all edge pairs and checks the resulting four-label Eulerian double cover.
The label subgraphs may be disconnected; no individual-cycle count is claimed.

For the support lower bound, let `g` be any conservative flow distinct from
`f`, and set `h=f XOR g`. This is a nonzero conservative flow, possibly with
zero edges. In its nonzero support, a vertex cannot have degree one: its sole
nonzero incident value would violate conservation. Every nonempty finite
graph of minimum degree at least two contains a simple cycle. The Heawood
graph has girth six, independently checked by complete cycle enumeration.
Therefore `h` has at least six supported edges. The displayed repair attains
six, proving minimum changed-edge support for a repair to at most five
colors, and indeed to at most four, from this particular starting flow.

The complete one-cycle classification proves that this entire mechanism
cannot reach a three-colorable affine palette in one step. It also rules out
**every six-edge repair to three colors**: a conservative difference supported
on exactly six edges must consist of one six-cycle, since any contained cycle
already uses all its edges. Conservation forces its two nonzero incident
values to agree at each vertex, so the difference is constant around that
cycle. If the target flow is nowhere zero, this is one of the 199 admissible
changes already checked. Nothing here rules out larger general difference
supports or contradicts the earlier explicit three-label cover from another
flow.

## Reproduce and trust boundary

This public packet includes the complete finite certificate and an independent
replay that does not need the discovery generator or an optimizer. The discovery
run took about 0.58 seconds; this timing is not a complexity bound.

The separately authored standalone checker recomputes the domain and the
mathematical conclusion by independent mechanisms:

```sh
python -m experiments.cdc.heawood_cycle_repair.checker
```

It uses all 256 binary cycle-space assignments instead of cycle DFS,
finite-domain translation propagation instead of Gaussian elimination, and
independent-set coloring dynamic programming instead of the primary coloring
search. It checks every stored lift, minimum and explicit best witness.
The [verification receipt](verification.json) records final tests and controls.

No claim depends on the absence of a candidate in an incomplete sample. The
initial 16-change benchmark is explicitly marked incomplete. The final domain
and every modified flow's affine solution space are completely covered.
The independent implementations remain ordinary Python, not formally verified
software. Every input is an exact finite graph, binary vector or integer.

## Pins and attribution

The local discovery packet was based on research commit
`816134e957b57d7d5dafc67471b076dc7b0f8626`; public replay is self-contained
with the pinned predecessor certificate below.
The destination base is `atimics/math2@2c0f00528a8bb375d02bd48a513062254a53c285`,
and the predecessor PR8 head is `8de7295f1eba30a82ec7c6e05585f1e71df88c4d`.
The exact preceding certificate bytes have SHA256
`fb8503f1cc92725d9981dd3320e2556fa1dcf74a0ade94f77cca04c88cf5b98f`.
Historical packets are unchanged.

The question comes from [math2 issue3](https://github.com/atimics/math2/issues/3).
Credit to atimics and math2 contributors, Sang-il Oum's cited CDC exposition
for the affine construction, and the preceding Petersen/Heawood certificates
for the exact methods and starting obstruction. License: [Apache-2.0](LICENSE);
see [NOTICE](NOTICE). This is finite evidence about a local repair mechanism,
not a solution of the unrestricted five-cycle-double-cover conjecture.

A distinct continuation would test whether two admissible cycle changes can
reach a three-colorable affine palette from this starting flow, with a new
finite domain and stopping rule. That experiment was not run here.
