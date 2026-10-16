# A Heawood flow for which every affine lift needs seven labels

Alexander Richard Towell, with substantial OpenAI Codex assistance.
Exact finite computation and written completeness argument; not Lean
verification or human peer review. No historical novelty claim.

The specified nowhere-zero F2^3 flow on the Heawood graph has exactly two
root-fixed affine lifts. Both palette interaction graphs are K7. Thus every
affine lift of this flow, including all global translates, needs seven colors
under a global label map. Changing the lift alone cannot yield five or six.

This gives a fixed-flow obstruction for the direction in
[math2 issue #3](https://github.com/atimics/math2/issues/3). It complements the
[complete Petersen classification](../ALL_FLOWS.md): every Petersen flow has a five-label lift,
but that property does not extend to this fourteen-vertex graph.

The graph nevertheless has an explicitly checked **three-label Eulerian
double cover from a different flow**. The obstruction concerns the fixed-flow
representation, not unrestricted cover existence. Label subgraphs are allowed
to be disconnected. No general cycle-double-cover theorem is assumed.

## Exact object

Use the bipartite incidence graph of the Fano plane. The left vertex p-1
corresponds to p in {1,...,7}; the right vertex n+6 corresponds to a nonzero
normal n. Join them when the binary dot product p·n is zero. Order edges by
increasing p, then n. This gives the following 21 ordered edges:

```
(0,8),(0,10),(0,12),(1,7),(1,10),(1,11),(2,9),
(2,10),(2,13),(3,7),(3,8),(3,9),(4,8),(4,11),
(4,13),(5,7),(5,12),(5,13),(6,9),(6,11),(6,12).
```

The flow in that order is

```
[1,2,3,4,6,2,1,4,5,3,7,4,6,1,7,7,5,2,5,3,6].
```

Integers encode F2^3 vectors; addition is XOR. Every flow value is nonzero,
and the three incident values XOR to zero at each vertex. The graph checks
also verify simplicity, cubic degree, connectivity and absence of bridges.

For an edge e incident to v, the local pair consists of the other two incident
flow values. An affine lift translates both entries by t[v] and requires the
two endpoint pairs to agree. Normalize t[0]=0. The complete translation list is

```
[0,3,2,1,2,3,1,2,4,3,5,6,7,1]
[0,1,4,7,3,5,2,4,5,5,7,6,4,7].
```

The first palette is the complete graph on {1,2,3,4,5,6,7}; the second is the
complete graph on {0,1,2,3,4,5,7}. All 21 possible pairs occur in each case.
The saved clique and coloring therefore certify chromatic number seven
without interpreting a failed coloring search as an impossibility proof.

## Why every lift is covered

Fix a spanning tree and t[0]=0. Across each tree edge, a parent translation
admits exactly two child translations: the two matches between distinct
pair entries with the same nonzero XOR. Every compatible root-fixed lift
therefore determines exactly one of the 2^13=8192 choice sequences.
Enumerating all of them and checking every non-tree edge gives exactly the
two displayed lifts. The main verifier repeats this with two different trees.

Every unrestricted translation vector has a unique normalization obtained by
XORing all entries with t[0]. Conversely, every one of the eight global
translates of a root-fixed lift is compatible and has an isomorphic palette.
There are therefore exactly 16 unrestricted lifts, all requiring seven colors.

The discovery implementation separately reduces the 66 compatibility/gauge
equations in 63 binary variables, giving rank 62 and nullity one. Its saved
row-combination certificate checks both row-span inclusions. The public
all-lifts conclusion does not rely on that elimination: the tree enumeration
and a separately authored finite-domain propagation checker give independent
completeness routes. The latter enumerates all endpoint-translation relations,
removes only unsupported values, and branches over every remaining value.
It finds the two root-fixed solutions in three recursive states and independently
enumerates all 16 unrestricted solutions.

## A different flow succeeds on the same graph

The comparator edge flow is

```
[1,2,3,1,3,2,3,1,2,2,3,1,2,1,3,3,2,1,2,3,1].
```

Each vertex sees all three colors 1,2,3. On an edge of color a, use the other
two colors as its pair. Every label then has degree two at every vertex,
and every edge has two distinct labels. These pairs are an affine lift of
the comparator flow with all translations zero. This is an explicit
three-label Eulerian double cover, checked directly; no general bipartite
edge-coloring theorem or connected-cycle claim is needed.

## Search, reproduction and scope

The OS-generated seed is 5036646479930497797. The declared search allowed at
most 512 distinct GL(3,2)-normalized flows from 100000 draws of eight independent
cycle-coordinate values, with a first 32-flow benchmark. It stopped during
that benchmark at draw 12: the **first** distinct nonzero normalized flow had
the certified obstruction. The sixteen-million-assignment flow domain was
not exhausted. The theorem concerns the specified flow, for which all lifts
were exhausted. It is not a statistical estimate or a classification of
all Heawood flows.

From the repository root:

```
python -m experiments.cdc.heawood.checker
python experiments/cdc/heawood/review_check.py
python -m unittest discover -s experiments/cdc -p 'test_*.py' -v
```

Expected: two root-fixed lifts, palettes [7,7], sixteen unrestricted lifts,
and a different-flow three-label cover. The main verifier retains failure
detection under Python -O. The independent review script explicitly rejects
-O because it uses assertions. Tests mutate the graph, flow, omitted or
duplicated lift, translations, pairs, clique, coloring, comparator, and linear
nullspace certificate. Search stopping conditions are also checked locally;
the public suite exercises the tree certificate and comparator.

## Provenance and remaining questions

Base/source: atimics/math2@2c0f00528a8bb375d02bd48a513062254a53c285;
existing PR8 predecessor efeba2be255592d39f690e3358d85c81601e4b01.
Local research start b59e88401857680fdbe4af1a95322642bbde117b, with the earlier exact methods committed in
9af772c369755e773e2b15b897dad46a53b46213 and their original packets preserved. The root-gauge, palette and
cover-converse definitions follow the existing fixed-flow packet. Credit to
atimics and math2 contributors for the experiment and explicit research
question, and to the cited CDC exposition for the affine construction.
Apache-2.0; predecessor attribution retained.

The next mathematical question is which features of a fixed flow force
this obstruction, and whether a useful class of flow changes guarantees a
small palette. This packet provides a concrete test case, not such a theorem.
The smallest possible obstructing graph and the classification of all flows
on this graph are not determined. No Lean modules were changed or rebuilt.
