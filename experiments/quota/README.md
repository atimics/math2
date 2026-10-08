# Degree-quota gadget engineering experiment

The network reduction makes some matching instances smaller by `V+E`, but
does **not** improve runtime with the exact NetworkX backend in this pilot.
Keep the default `dense`; treat `network` and `hybrid` as experimental.

This extracts an implementable component from family 120 of `openai/math`:
replace a dense local degree-quota gadget with a routing network. It does
not implement the manuscript's almost-linear matching algorithm. The input
is a simple undirected graph and integer quotas `f(v)`. The output is an
edge subset having exactly those degrees (an f-factor), or an infeasibility
decision from exact maximum-cardinality matching. Weights, parallel edges,
capacities and directed graphs are outside this experiment.

## Constructions

All three modes use the same ports and host-edge cross connections.
For host degree `d` and `b=d-f(v)`:

- `dense`: connect all `d` ports to `b` local sinks.
- `network`: pad to the next power of two `s`; use a recursive Beneš network
  with split positions, idle edges, input ports and `b` output sinks.
- `hybrid`: choose the smaller exact local `V+E` count at each vertex;
  ties choose dense. This minimizes representation count among these two
  gadgets, not solver time or bytes of memory.

The network has `Q=s(1+2 log2(s))` positions and `A=4s log2(s)` arcs.
Dense local counts are `V=d+b, E=db`; network counts are
`V=d+2Q+b, E=Q+A+d+b`. Cross edges are common to both choices. Neither
mode uses special zero/full-quota simplifications; isolated vertices need
no gadget. Consequently, this is a controlled gadget comparison, not a
competitive production f-factor solver.

The network is a DAG. In a perfect matching its non-idle position edges
form disjoint paths from unused host ports to the `b` sinks; other positions
use idle edges. Conversely, rearrangeability routes any chosen `b` ports
to those sinks, including with padded inputs unused. Thus exactly `f(v)`
ports must match across host edges, as in the dense construction. This is
a written explanation and tested implementation, not a Lean proof.

## Measured pilot

Checked-in [results.json](results.json) contains all 54 worker records,
inputs, decoded witnesses, build and solve times, local choices and memory
measurements. Python 3.12.14, NetworkX 3.7, Linux x86_64; three fresh worker
processes per input/mode, 10-second wall-clock timeout per worker. Every
completed feasible result passed an independent host-edge and degree check.
Every mode correctly reported the triangle infeasible.

Times below are medians of **build + solve**, in seconds, only when all three
runs completed. `V/E` counts refer to the constructed matching graph.

| Input | Dense V/E; seconds | Network V/E; seconds | Hybrid V/E; seconds |
|---|---|---|---|
| Star, 32 edges | 96/560; 0.00376 | 864/1152; 0.0854 | 96/560; 0.00342 |
| Star, 128 edges | 384/8384; 0.0453 | 4480/6144; 2.23 | 384/8384; 0.0439 |
| Star, 256 edges | 768/33152; 0.182 | 9984/13824; 3/3 timeouts | 9472/13312; 1/3 timeout |
| Clique, 8 vertices | 88/252; 0.00396 | 984/1332; 0.112 | 88/252; 0.00444 |
| Clique, 12 vertices | 204/858; 0.0178 | 3660/5070; 1.43 | 204/858; 0.0167 |
| Infeasible triangle | 9/9; 0.000727 | 45/54; 0.00154 | 9/9; 0.000804 |

On the 256-edge star, hybrid reduces `V+E` from 33,920 to 22,784 (32.8%)
while increasing vertices from 768 to 9,472. Dense finished every run;
hybrid did not. This directly rejects using `V+E` alone as a runtime policy
for this backend. NetworkX documents `O(V^3)` worst-case time for its
matching implementation; edge savings need not offset extra vertices.

Peak RSS is Linux `ru_maxrss` for each completed worker, including the
interpreter, graph and backend. It is not isolated gadget memory. For the
128-edge star, median peak RSS was 29,532 KiB dense versus 32,668 KiB
network, despite the latter having fewer edges. Timed sections exclude
imports, witness validation and process startup; the timeout includes all
of them. Timeout records have no feasibility decision, witness, completed
solve time or RSS measurement.

These are small synthetic cases, fixed method order, three repetitions and
one machine. The star quotas force a unique, easy answer: half its leaves
require their edge and half forbid it. Real preprocessing would resolve
such stars immediately. The cases expose gadget overhead; they do not
establish performance on application workloads or near-linear asymptotics.
Small dense/hybrid timing differences are noise, not claimed speedups.

## Reproduce and verify

From the repository root, on Linux:

```sh
python -m pip install -r experiments/quota/requirements.txt
python -m unittest discover -s experiments/quota -p 'test_*.py' -v
python -m experiments.quota.benchmark --timeout 10 --repetitions 3 --output /tmp/quota-results.json
```

Tests compare every simple graph and valid quota vector through three
vertices, plus seeded graphs through seven vertices, against brute-force
host-edge enumeration. They check padding, infeasibility, gadget validity,
decoding and malformed inputs. The benchmark separately validates actual
host edges and exact degrees without consulting gadget internals. Backend
infeasibility decisions are not independently certified on large inputs.

The next practical work is forced-edge preprocessing, less degenerate
high-degree workloads and a faster compiled exact matching backend. Compare
each change against dense with the same backend and independently checked
witnesses; select gadgets using measured cost rather than `V+E` alone.

## Sources

- [Pinned f-factor section](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-September-24-2026/build/sections/10-f-factors.tex).
- [Pinned routing-network section](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Almost-Linear-Time-Maximum-Cardinality-Matching-in-Sparse-General-Graphs-September-24-2026/build/sections/09-uniformization.tex).
- [NetworkX exact matching documentation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html).

The repository's source-claim assumptions remain unchanged. Empirical checks
here establish finite implementation behavior, not the upstream theorem.
