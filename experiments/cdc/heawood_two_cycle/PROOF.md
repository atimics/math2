# Exactly three legal cycle changes are needed

Alexander Richard Towell, with substantial OpenAI Codex assistance.
This is a written proof with exact finite checks, not a Lean proof or human
peer review. The graph and starting flow are the predecessor's fixed objects;
no universal cycle-double-cover or flow-repair theorem is claimed.

## Statement and definitions

Use the ordered 21 edges of the Heawood graph and the nowhere-zero flow

```
[1,2,3,4,6,2,1,4,5,3,7,4,6,1,7,7,5,2,5,3,6]
```

from `../heawood/certificate.json`, SHA256
`fb8503f1cc92725d9981dd3320e2556fa1dcf74a0ade94f77cca04c88cf5b98f`.
Values are vectors in F2^3 encoded as integers 0 through 7; addition is XOR.
At each vertex the three incident flow values sum to zero.

A legal operation chooses a simple cycle C and a nonzero vector d, and adds
d to every flow value on C, leaving all other values unchanged. It is legal
exactly when no edge of C currently has value d. Conservation is preserved
because each vertex on C has exactly two changed incident edges. Every
intermediate flow must remain nowhere zero.

For each vertex v choose a translation t(v) in F2^3. On an incident edge e,
the local pair is the other two incident flow values, translated by t(v).
An affine lift requires that the pairs at the two ends of every edge agree.
Its palette graph has vector labels as vertices and these unordered pairs
as edges. A proper palette coloring globally merges labels into Eulerian
double-cover classes without collapsing an edge's two memberships.

**Claim.** The minimum number of legal cycle operations needed to reach a
flow with an affine lift whose palette is at most three-colorable is exactly
three. The count is operations, not changed-edge support. Cycles may overlap
or repeat, and the XOR vector may change between operations.

## A structural reduction

**Lemma.** Let G be a finite simple cubic graph in which every spanning
2-factor is a single Hamiltonian cycle. For a nowhere-zero F2^3 flow f on G,
an affine lift has a three-colorable palette for some translations if and
only if the vector span of the edge values of f has dimension two.

*Proof.* At a vertex, the three flow values a,b,c are nonzero, distinct,
and satisfy a+b+c=0. Its three translated labels a+t,b+t,c+t form a triangle
in the palette: the three incident edge pairs are the three pairs of this
triple. A proper coloring with at most three colors therefore uses exactly
three colors at every vertex.

Fix one color. Exactly one underlying vector label of that color appears
at each vertex, and appears on exactly two incident edges. Thus the union
of all labels of this color is a spanning 2-factor. The supports of distinct
underlying labels of the same color are vertex-disjoint: otherwise the local
triangle would contain two labels of the same color. By hypothesis their
union is one Hamiltonian cycle, so there is only one nonempty underlying
label support of this color. There are consequently exactly three used
vector labels A,B,C in the entire affine lift.

On any edge the XOR of its pair is its flow value; translation cancels.
All edge values therefore lie among A+B,A+C,B+C. These are the three
nonzero vectors of one two-dimensional subspace. All three occur at each
vertex, so the span has dimension exactly two.

Conversely, a rank-two nowhere-zero flow uses the three nonzero vectors
of its plane. Conservation and cubic degree force all three at every
vertex. Set every translation to zero. The pair on an edge consists of
the other two plane vectors, independent of its endpoint. This is a
compatible affine lift with a three-label triangular palette. ∎

The exact checker enumerates all 24 perfect matchings of the pinned Heawood
graph and verifies that every complement is one cycle on all 14 vertices.
Every spanning 2-factor of a cubic graph is such a complement. This proves
the hypothesis of the lemma for this particular graph without importing an
unverified statement about Heawood graphs in general.

## A projection certificate excludes two operations

For each nonzero p in F2^3 write p(x) for the binary dot product with x.
A set of edge values has span of dimension at most two precisely when one
of these seven nonzero functionals vanishes on every value.

The checker constructs all 256 binary even edge sets from the eight chord
bits of a spanning tree. Leaf elimination uniquely reconstructs the tree
edge bits; parity is checked at every vertex. Thus every even edge set is
included exactly once. Keeping the nonempty connected 2-regular supports
gives exactly all 213 simple cycles. Filtering the seven nonzero XOR vectors
by the nowhere-zero condition gives all 199 legal first operations.

The checker establishes the following exact finite facts:

1. The original flow has rank three.
2. For each legal first result g and each of the seven p, the support
   Q(g,p) = {e : p(g(e)) = 1} is nonempty. Hence every first result has rank
   three. This checks 199 times 7 = 1,393 projections.
3. Exactly 739 of these supports are simple cycles. For every such support,
   the values g(e), e in Q(g,p), contain **all four** vectors d with p(d)=1.
   The counts by p=1,...,7 are 92,95,95,178,95,92,92.

Suppose a second legal operation (C,d) produced rank at most two. Choose
nonzero p annihilating the final values. If p(d)=0, then p already annihilates
g, contradicting fact 2. If p(d)=1, vanishing of the final projection forces
C=Q(g,p). This must be one of the simple supports in fact 3, so some edge
of C has value g(e)=d. Adding d there makes a zero edge, contradicting
legality. All cases are covered, including repeated/overlapping cycles and
a second operation undoing the first.

Together with the structural lemma, facts 1 and 2 exclude zero or one
operation, and fact 3 excludes two. No enumeration of affine lifts is
needed for this lower bound. In particular, it would be incorrect to claim
that every nonzero projection of the *original* flow is disconnected:
its p=4 projection is a simple 12-cycle. The stronger checked condition
above is what the argument uses.

## Three operations attain the target

The following edge-index sets, in order, form simple cycles:

| Operation | Cycle edge indices | Added vector |
|---|---|---|
| 1 | 6, 8, 16, 17, 18, 20 | 3 |
| 2 | 6, 8, 9, 10, 12, 14, 15, 16, 18, 20 | 4 |
| 3 | 3, 4, 6, 7, 9, 11 | 5 |

Every intermediate flow is listed in `three-step-experiment.json` and
checked for the specified XOR update, conservation, and absence of zero.
The final flow is

```
[1,2,3,1,3,2,3,1,2,2,3,1,2,1,3,3,2,1,2,3,1].
```

This is the predecessor's known three-label comparator. Zero translations
give the three labels 1,2,3. The direct witness checker reconstructs each
edge pair at both endpoints and checks that each label support is a
Hamiltonian 14-cycle. These three cycles cover each edge exactly twice.
Together with the lower bound, this establishes the claimed exact distance.

## Independent evidence and scope

The discovery implementation used exact binary elimination and palette
coloring, independently of the structural verification. It exhausted
296,709 ordered two-step candidates, of which 46,837 were legal. The 22,637
distinct final flows had minimum palette chromatic numbers 4 (6,550 flows),
5 (15,118), 6 (352), and 7 (617). Those detailed chromatic counts are
discovery output, not an additional claim established by the shorter
projection checker. The independently checked conclusion is that none
has a three-colorable affine palette.

The three-step witness search intersected the complete two-step final set
with legal one-step predecessors of 42 linear relabelings of the known
comparator. It stopped at the first witness, after 89 backward candidates
(50 legal). It does not enumerate all three-step routes or minimize total
changed edges. Both searches are deterministic; no random seed is used.

This result resolves the queued two-cycle question and supplies an explicit
next step. It does not characterize arbitrary Heawood flows, other graphs,
minimum support, or complexity of a general repair algorithm. The reduction
lemma has its stated Hamiltonian-2-factor hypothesis; omitting it would
invalidate the proof given here.

Credit to atimics and math2 contributors for the CDC experiment and issue3;
to Sang-il Oum's cited exposition for the affine construction; and to the
earlier Petersen, fixed-flow Heawood and one-cycle packets for definitions,
the obstructing flow, and the comparator. No historical novelty is claimed.
Code and text: Apache-2.0, predecessor attribution retained.
