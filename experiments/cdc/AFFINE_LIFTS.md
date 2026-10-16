# The specified Petersen flow has a five-cycle lift

For the exact alternative flow in `results.json`, choosing a different affine
lift gives a double cover by **five individual cycles without changing the
flow**. This answers the fixed-flow question for the recorded obstruction in
[issue 3](https://github.com/atimics/math2/issues/3).

The original witness still has a `K6` palette and cannot be globally merged
into five labels. That obstruction concerns one witness: it does not rule out
other compatible choices of vertex translations for the same flow. The existing
experiment already supplied an unrestricted five-cover; the additional result
here is a complete classification within its specified obstructing flow.

## Exact result

Integers `0,...,7` encode vectors in `F2^3`; addition is XOR. Use the ordered
edges of `petersen-k6-palette` in `results.json` and its unchanged flow
`[6,5,3,7,1,5,2,1,4,4,4,7,3,2,6]`.

At an incidence `(v,e)`, the local label pair consists of the flow values of
the other two edges at `v`. XOR-translate it by `t[v]`. A lift is compatible
when the two endpoint pairs agree on every edge. With `t[0]=0`, **all** lifts are:

| Lift | Translations at vertices 0 through 9 | Palette |
|---|---|---|
| Original | `[0,4,0,3,2,2,0,3,5,5]` | `K6` on `{1,2,3,5,6,7}` |
| Repair | `[0,2,1,7,7,1,7,0,1,0]` | `K5` on `{2,3,4,5,6}` |

Global XOR translation gives eight literal lifts from each row, hence sixteen
in total. The two explicit palette cliques certify chromatic numbers six and
five. No graph-automorphism or linear-coordinate quotient is used.

The repaired labels are the following cycles; each graph edge occurs twice:

| Label | Closed vertex sequence |
|---|---|
| 2 | `3,4,9,7,5,8,3` |
| 3 | `0,1,2,3,4,0` |
| 4 | `1,2,7,9,6,1` |
| 5 | `0,1,6,8,5,0` |
| 6 | `0,4,9,6,8,3,2,7,5,0` |

## Why the enumeration is complete

Root a spanning tree at vertex 0 and fix its translation. Along a tree edge,
the two local pairs have the same nonzero XOR difference, namely its flow.
There are exactly two child translations making the pairs equal, obtained by
matching one parent label to either child label. These choices determine all
vertex translations uniquely. Every compatible lift determines one sequence
of choices, and checking the remaining edges filters out exactly the
incompatible sequences.

The independent checker exhausts all `2^9 = 512` choices on each of two different
BFS trees; both give the same two lifts. It imports neither the affine solver
nor SciPy. It also checks pair distinctness, flow recovery, even degrees,
palette cliques/colorings, and the displayed cycles. Corrupted flow, translation,
pair, coloring, and cycle controls must fail. This is exact finite computation
with a written completeness argument, not Lean kernel verification.

## Reproduce

From the repository root, Python 3.10 or later, standard library only:

```sh
python -m experiments.cdc.affine_lifts
python -m unittest experiments.cdc.test_affine_lifts -v
```

Expected: `complete_tree_assignments: 512`, `compatible_translations: 2`,
`histogram: {"5": 1, "6": 1}`, `independent_second_tree_agrees: true`; 18 tests
pass. The complete emitted record is [affine_lifts.json](affine_lifts.json).
Run all CDC regressions with `python -m unittest discover -s experiments/cdc`;
the existing MILP integration test additionally requires SciPy.

## Scope and credit

This explains why an algorithm returning only one affine solution can miss a
five-label solution for its own chosen flow. It neither supplies a repair for
every flow nor settles a graph-class or general five-cover theorem. Petersen
five-cover existence is already known; no such novelty is claimed.

Contribution by Alexander Richard Towell (`queelius`, `lex@metafunctor.com`),
2026-10-13, with substantial OpenAI Codex assistance in research, implementation,
and separate AI review. AI review is not human peer review. Apache-2.0.
Credit to atimics and contributors for the graph, specified flow, original
obstruction and unrestricted witness, and to the construction exposition linked
in the [existing experiment](README.md).

Source: `atimics/math2@2c0f00528a8bb375d02bd48a513062254a53c285`,
`experiments/cdc/results.json`, SHA-256
`4b490dd0cebb45b1d0ea74dcc8ecff411636d2f429b639b0b11c78518aa569f8`.
The source file and constructor are unchanged. The enumerator and its original
16 tests derive from the independently reviewed local packet at
`math-research@5b0a483d670ad7a78f845d0661e46f98c31f816c`; the public adaptation
selects the existing named record and adds two source-selection regressions.
