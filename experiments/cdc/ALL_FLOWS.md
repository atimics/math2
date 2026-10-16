# Every nowhere-zero Petersen flow has a five-label affine lift

Alexander Richard Towell, with substantial OpenAI Codex assistance.
Status: exact finite classification and written coverage proof; not Lean
verification or human peer review. No general CDC theorem is assumed.

For the fixed labelled Petersen graph in math2's `petersen-k6-palette` record,
**every nowhere-zero F2^3 flow has an affine lift using exactly five labels**.
There are 28,560 such flows. Under invertible linear relabelling of F2^3 they
form 170 orbits of size 168. The saved certificate records every root-fixed
affine lift of a representative of each orbit, including explicit clique and
coloring witnesses for its palette.
The graph remains labelled; graph automorphisms are not quotiented out.

This gives a complete all-flow Petersen follow-up to
[math2 issue #3](https://github.com/atimics/math2/issues/3). The predecessor
[PR #8](https://github.com/atimics/math2/pull/8) treated only the specified
obstructing flow. Changing the flow is unnecessary on the Petersen graph:
one can always choose a suitable affine lift. The earlier `K6` obstruction
remains valid for its particular supplied lift.

## Complete finite result

Root-fix translations by `t[0] = 0`. A profile lists the chromatic numbers of
**all** compatible lifts for one normalized flow.

| Palette profile | Flow orbits | Labelled flows |
|---|---:|---:|
| `(5)` | 80 | 13,440 |
| `(5,5)` | 60 | 10,080 |
| `(5,6)` | 20 | 3,360 |
| `(5,5,5,6)` | 10 | 1,680 |

There are 280 representative lifts: 250 use five labels and have palette `K5`;
30 use six labels and have palette `K6`. Thus the successful lifts already
use five of the original F2^3 labels. No global palette coarsening or change
to the edge flow is needed. The complete labelled count is 47,040 root-fixed
lifts: 42,000 five-label lifts and 5,040 six-label lifts.

Labels support even subgraphs. No general claim that a label always supports
one connected cycle is needed or made here. The proposition concerns this
specific graph, all its nonzero F2^3 flows, and the stated affine mechanism.
It does not settle a five-cover conjecture for other graphs.

## Exact definitions and completeness argument

The graph has vertices `0,...,9` and the pinned ordered edges

```
(0,1),(0,4),(0,5),(1,2),(1,6),(2,3),(2,7),(3,4),
(3,8),(4,9),(5,7),(5,8),(6,8),(6,9),(7,9).
```

A flow assigns each edge a nonzero vector in F2^3, encoded by `1,...,7`,
with XOR zero at every vertex. For an edge at vertex `v`, its local pair is
the flow values on the other two edges. A translation `t[v]` XOR-translates
that pair. A compatible lift makes the endpoint pairs equal on every edge.
The palette graph has these label pairs as edges.

**All flows.** A spanning tree has nine edges and six complementary chords.
Choose the six chord values freely in F2^3, then determine each tree value
from the conservation equation at its child, processing leaves first. The
root equation follows by XOR of the other vertex equations: each edge occurs
twice in the sum of all equations. This is a bijection between the `8^6`
assignments and all flows, including zero edges. Retaining only nowhere-zero
assignments produces the discovery list.

**Independent coverage count.** The verifier does not use that generator.
For `A` a subset of the fifteen edges, let `c(A)` count all connected
components, including isolated vertices. The flows supported on `A` form a
binary cycle space of dimension `|A| - 10 + c(A)` in each of the three
coordinates, and hence number `8^(|A| - 10 + c(A))`. Inclusion-exclusion gives

```
number of nowhere-zero flows =
sum over A subset E: (-1)^(15-|A|) * 8^(|A|-10+c(A)) = 28560.
```

Every one of the `2^15 = 32768` subsets is counted, with exact integers.
The same calculation at group order four gives zero. In particular every
nowhere-zero F2^3 flow spans dimension three: otherwise its values could be
embedded in F2^2.

**Relabelling and explicit orbit verification.** A linear bijection `g` sends
`f` to `g o f`, `t` to `g o t`, and every pair to its image. It preserves
compatibility, the root gauge, used labels, and palette chromatic number.
There are `(8-1)(8-2)(8-4)=168` such maps. A map fixing a spanning flow is the
identity, so the action is free. The discovery code normalizes by sending the
first linearly independent values to `1,2,4`; this choice is invariant under
linear relabelling. The verifier instead explicitly expands all 168 images
of each saved flow, checks each orbit has size 168 and that all orbits are
disjoint, and compares their union size with the inclusion-exclusion count.
Since the representatives are valid flows, this certifies coverage without
trusting the discovery enumeration or an assumed flow polynomial.

**Every lift.** On a tree edge with nonzero flow, fixing the parent
translation leaves exactly two child translations, corresponding to the two
possible matches of its distinct pair labels. Every compatible root-fixed
lift determines exactly one sequence of these choices. Exhausting all
`2^9=512` choices and checking the remaining edges therefore gives all lifts.
Discovery and replay use different spanning trees. Replay compares complete
translation/pair sets, so an omitted or repeated lift fails.

**Palette certificates.** Each saved lift includes a proper coloring with
`k` colors and a clique of size `k`, certifying both bounds on its chromatic
number. The verifier checks every clique edge, every coloring inequality,
the original lift equations, and even degrees after coloring. It additionally
checks that every orbit has a lift already using at most five original labels.
No failed heuristic search is used as a lower-bound certificate.

## Reproduce

Only Python's standard library is needed for the public checker. From the
math2 repository root:

```sh
python -m experiments.cdc.all_flows
python -m unittest discover -s experiments/cdc -p 'test_*.py' -v
python experiments/cdc/all_flows_review.py
```

In the original research workspace:

```sh
python -m research.petersen_all_flows.flows
python research/petersen_all_flows/review_check.py
```

Expected: `status: verified`, 28,560 flows, 170 orbits, 280 representative
lifts, the table above, and `all_flows_have_five_label_lift: true`.
The certificate is finite exact evidence with a written completeness proof;
the Python implementation has not been formally verified.
The review replay independently enumerates flows by conservation propagation,
lifts by translation-domain constraints, and colorings by subset dynamic
programming. It imports no primary checker code and rejects optimized Python,
since it uses assertions. The primary replay is checked under both normal and
optimized Python.

The optional `--write` command deterministically regenerates the certificate
by completing all 262,144 chord assignments and all 170 lift classifications,
then verifies it before writing. There is no random seed, sampling, timeout
cutoff, or unexamined parameter tail in this finite domain. Initial discovery
and classification took approximately 2.13 seconds in the recorded environment.

## Sources, attribution, and limits

- math2 main: `2c0f00528a8bb375d02bd48a513062254a53c285`.
- Existing PR #8 head: `b729fce7015913751e8634b567b15ff5dc884cba`.
- The graph, specified obstructing flow, affine setup, and prior experiments
  are credited to `atimics` and math2 contributors. The lift checker and prior
  fixed-flow classification are Towell's earlier contribution, reused here.
- The source's mathematical setting follows Sang-il Oum's CDC exposition,
  version 3, and the classical cycle-double-cover literature. No general
  theorem from that exposition or OpenAI's CDC proof is assumed by this check.

The independent reviewer is an AI agent, and the result is exact finite
computation supported by a written argument. External acceptance is recorded
separately from local verification. Novelty beyond the previously submitted
fixed-flow scope has not been established by a historical-priority survey.
Apache-2.0; see the repository LICENSE. This contribution retains the
source and predecessor attribution above.
