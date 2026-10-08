# Reproducible CDC construction and compression experiment

This finite experiment implements the cubic affine construction from
[Sang-il Oum's CDC exposition, §§5–7](https://arxiv.org/html/2607.16356v3),
compares global palette merging with unrestricted cover search, and checks
every positive witness with a separate standard-library verifier.

The useful observation is a **failure of a restricted method**: a Petersen
cover with a K6 label interaction graph cannot be merged into five labels,
although an independently checked five-cover exists for the same graph.
This is a classical six-pentagon configuration used as an experiment fixture,
not a new theorem or a counterexample to the 5-CDC conjecture.

## Reproduce

From the repository root, using Python 3.11 or later:

```sh
python -m pip install -r experiments/cdc/requirements.txt
python -m experiments.cdc.run --time-limit 5 --output experiments/cdc/results.json
python -m unittest discover -s experiments/cdc -p 'test_*.py' -v
```

SciPy 1.17.0 is the version used for the committed run. The constructor,
palette search and checker use only the standard library. MILP replay needs
SciPy; stored positive witnesses can be checked without it:

```sh
python -m unittest discover -s experiments/cdc -p 'test_*.py' -k CheckerTests -v
```

The campaign includes five named fixtures, three generalized Petersen
graphs, and one alternative-flow Petersen record. It is not an exhaustive
enumeration of cubic graphs. The optional seeded generator is bounded
rejection sampling, not a uniform sampling claim.

## Encodings and independent checks

- `graphs.py` validates simple, connected, bridgeless cubic inputs. Multigraphs,
  noncubic graphs and a reduction from arbitrary graphs are outside this experiment.
- `construction.py` deterministically searches nonzero F2^3 edge flows.
  Vertex conservation is XOR-zero. Exact binary elimination then solves
  the vertex-translation/edge-flip compatibility equations and produces
  two distinct labels per edge, drawn from eight possible labels.
- `search.py` first tries a global label map. Its unrestricted MILP instead
  selects one unordered label pair per edge and requires each vertex-label
  degree to equal twice an integer. Thus every selected label supports an
  Eulerian subgraph. Labels may be unused; a five-label witness means at most five.
- `verify.py` independently checks the graph, graph identity, exactly two
  distinct in-range memberships per edge and even degrees. It does not
  import the constructor, the search module or SciPy. It also checks a
  palette-clique obstruction directly from the saved edge pairs.
- `run.py` sends every produced positive witness through this checker before
  writing the record. `results.json` retains graphs, flows, witnesses,
  bounds, solver statuses, environment versions and verification summaries.

An Eulerian covering subgraph can contain several connected cycles. This
experiment does not optimize the total number of connected cycles.

## Exact palette criterion

For a fixed witness, make an interaction graph J whose vertices are its
labels, with edge {a,b} whenever an original graph edge carries that pair.
A global map of labels into k colors preserves double coverage precisely
when it is a proper coloring of J.

To prove sufficiency, labels of the same color never share an original edge.
Their supports therefore combine as disjoint unions, preserving even degrees,
while the two memberships of each edge map to distinct colors. Necessity
follows because merging adjacent labels collapses that edge's two memberships.
Consequently global coarsening to k labels is equivalent to k-colorability of J.

This elementary criterion explains the restriction of the method. It makes
no claim about another flow, another affine solution, or reassignment of
individual edge pairs.

## Committed results

| Record | Global merging to five | Unrestricted four | Unrestricted five |
|---|---|---|---|
| K4, K3,3, cube, triangular prism | Checked witnesses | Checked witnesses | Checked witnesses |
| Generalized Petersen G(7,2), G(8,3), G(9,2) | Checked witnesses | Checked witnesses | Checked witnesses |
| Petersen, default flow | Checked witness | Solver reports infeasible | Checked witness |
| Petersen, specified alternative flow | K6 obstruction, checked directly | Solver reports infeasible | Checked witness |

For the alternative-flow record the ordered nonzero edge values are
`[6,5,3,7,1,5,2,1,4,4,4,7,3,2,6]`, on the exact ordered edges saved in JSON.
The interaction graph contains all fifteen pairs on labels `{1,2,3,5,6,7}`.
Any proper coloring of this clique needs six colors. This finite certificate
proves that the particular witness cannot be globally merged into five.

All nine records have positive eight-label construction witnesses and
positive unrestricted five-cover witnesses. A fresh bounded run may differ
in solver-selected witnesses or termination status; compare checked properties
and recorded limits rather than expecting byte-identical solver output.

## What the statuses establish

- `found` or `compressed`: an explicit witness, independently checked by the runner.
- Construction `limit` or palette `node_limit`: the bounded search did not settle its task.
- Palette `impossible`: exhaustive failure of global coarsening for that witness;
  the specified Petersen example additionally has a separate clique certificate.
- MILP `infeasible`: the solver reports infeasibility. No proof-certified UNSAT
  certificate is exported, so this result is not a formal nonexistence proof.
- MILP `timeout` or `error`: no conclusion about existence.

Petersen's four-cover infeasibility is a regression against the classical
equivalence between cubic 4-CDCs and 3-edge-colorability (§9.2 of the exposition).
The JSON explicitly distinguishes it from a proof-certified solver result.
The Python verifier is an executable check, not Lean kernel verification.

## Next lemma to pursue

The K6 witness rules out an algorithm that only merges one supplied palette.
A useful next investigation is whether changing the flow or affine lift can
always find a five-colorable palette in a specified graph class, or whether
local changes to edge memberships are required. Retain both the obstruction
and a successful five-cover when testing a proposed transformation.

No universal five-cover statement, new complexity bound, or change to math2's
cross-family Lean catalogue follows from these finite experiments.
