# A finite stopping rule for degree-preserving graph sampling

**Result:** accepting corpus family 131, the established undirected Curveball
sampler can produce one approximate-uniform graph with an explicit bound on
distributional bias. The measured 20-, 30- and 50-vertex synthetic examples
complete the sufficient budget in median 0.155, 1.55 and 8.21 seconds.
The kernel itself is classical. The contribution is an explicit integer
stopping rule derived from the corpus proof and exercised in runnable code.

## Workload and baseline

A degree-preserving null model asks whether network structure is unusual
after controlling for every labeled vertex's degree. For example, a small
undirected relationship graph can be compared with random graphs having
exactly the same degrees. The target here is uniform over **all simple
undirected labeled realizations**, including disconnected ones. Directed,
weighted, bipartite and connected-only models need different guarantees.

The competitive practical baseline is the same existing Curveball kernel
with a heuristic number of trades. We compare with `10*m` trades as an
explicit illustrative policy, not an endorsed mixing rule. It is faster;
this experiment supplies no TV bound for that shorter run. We do not claim
the baseline is actually biased or that our sufficient budget is necessary.
Exact enumeration remains preferable on sufficiently tiny state spaces.

The go/no-go decision was based on finite counts before implementation:
the proof's pair-resampling operator yields a much smaller sufficient budget
than its switch-chain comparison. This makes a small-network certification
experiment feasible without implementing its expensive exact-sampling
correction. See [candidate screening](../../docs/ENGINEERING_SELECTION.md).

## Derivation

Let `n` be the number of vertices, `m` the number of edges and
`M = binom(n,2)`. Let `Omega` be the nonempty realization space of the
validated starting graph. The [source's pair fibers][setup] preserve:

- all edges outside the selected pair;
- the edge between the pair;
- common neighbors and the count of singleton neighbors assigned to each endpoint.

Uniformly redistribute singleton neighbors, then average over uniformly
chosen vertex pairs. If `E_a` is conditional expectation on a pair fiber,
the transition operator is `K = (1/M) sum E_a = I-H/M`.

The accepted [Poincare inequality][mixing], Corollary `mix:poincare`, is
`Var(f) <= <f,Hf>`. It gives a centered spectral gap of at least `1/M` for
`K`. Each `E_a` is an orthogonal projection, so their average is positive
semidefinite and no additional lazy step is needed. The standard L2-to-TV
argument, also written out in that source for the switch chain, gives

```text
TV(K^t(G, .), Uniform(Omega)) <= (1/2) sqrt(|Omega|-1) exp(-t/M).
```

Every realization has `m` edges, hence `|Omega| <= U = binom(M,m)`.
Compute `B = ceil(log2(U))` exactly as `(U-1).bit_length()`. For integer
`k >= 1`, choose

```text
t = ceil(7 M (B + 2k - 2) / 20).
```

Indeed `ln(2) < 7/10`, so `t/M >= (B/2+k-1) ln(2)` and the displayed TV
bound is at most `2^-k`. Integer arithmetic avoids downward floating-point
rounding. Empty and complete graph universes are singletons and use zero
steps. Some other degree sequences also have unique realizations; our
budget remains conservative for them.

This is a conditional written derivation, reviewed separately from the
implementation; it is not a new Lean theorem or a claim of literature
novelty. The source itself attributes the trade to Carstens et al. (2018).

## What the guarantee buys

The default `k=7` gives TV at most `1/128 = 0.0078125`. Under the stated
premise and random-choice model, the probability of **any event** differs
from the ideal uniform-null probability by at most 0.78125 percentage points.
The same bound applies to the bias of any statistic in `[0,1]`.
This controls sampler bias; Monte Carlo uncertainty remains separate.

It is a one-output marginal guarantee. Consecutive chain outputs are
correlated. Running the full worst-start budget between each of `q` outputs
gives a joint TV bound of at most `q*2^-k` from product-uniform sampling by
successive conditional coupling; choose `k` for the desired joint budget.
This can make a large null ensemble expensive. A 50-node single draw taking
seconds does not establish a fast service for thousands of draws.

## Measured feasibility

[results.json](results.json) retains exact input graphs, all 18 outputs,
trade counts and individual timings. Three runs per policy use Python
3.12.14, Linux x86_64 and `SystemRandom`. All outputs passed a separate
labeled-degree and simple-edge check.

| Vertices / edges | Heuristic trades | Heuristic median seconds | Sufficient trades for TV <= 1/128 | Certified-budget median seconds |
|---|---:|---:|---:|---:|
| 20 / 36 | 360 | 0.00412 | 9,443 | 0.155 |
| 30 / 82 | 820 | 0.0227 | 47,502 | 1.55 |
| 50 / 207 | 2,070 | 0.0405 | 347,288 | 8.21 |

These are synthetic heterogeneous graphs. They establish finite execution
cost, not accuracy on a real risk dataset. Timings include adjacency
construction, trades and output edge-list construction; they exclude the
independent check. Method order alternates between repetitions. The largest
case ranged from 7.74 to 12.63 seconds, so these are feasibility measurements,
not precise throughput claims. JSON serialization and imports are outside
the timed region.

For comparison of **sufficient theorem budgets only**, the source's lazy
switch gap bound is `1/(24 n^2 binom(n,4))`. Substituting that into the same
TV argument gives 2,311,646,400; 64,640,721,600; and 3,917,403,000,000 switch
proposals on these inputs. These counts were not executed and are not a
claim about actual switch mixing time or a measured speedup over switches.

The favorable scope is small graphs when an explicit bias guarantee matters.
At about one-sixth edge density, the same budget is 5,585,580 trades for
100 vertices and 56,763,754,425 for 1,000 vertices. Those are computed counts,
not runtime forecasts. For fixed density the worst-case trade count grows
as `O(n^4 + n^2 k)`, and individual trades can cost `O(n)` plus subset ordering.
We do not recommend this worst-case policy for large networks.

## Use and reproduce

No third-party packages are required. From the repository root:

```python
from experiments.curveball.sampler import budget, sample_graph

edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
steps = budget(5, len(edges), k=7)  # Inspect cost before scheduling a run.
result = sample_graph(5, edges, k=7)
print(result["edges"], result["certificate"])
```

```sh
python -m unittest discover -s experiments/curveball -p 'test_*.py' -v
python -m experiments.curveball.benchmark --output /tmp/curveball-results.json
```

`sample_graph` uses operating-system randomness through `SystemRandom` by
default. The mathematical statement assumes independent uniform random
choices; this code does not certify the entropy source. Supplying `seed=`
uses deterministic `Random` for diagnostic replay and marks the output
accordingly; a fixed-seed output is not a certified random draw.

Tests enumerate the exact rational transition laws on 125 states across
four regular and irregular degree sequences, comparing the implementation
with an independent full-fiber oracle. They check stochasticity, reversibility,
connectivity, pair orientation, preserved degrees, malformed inputs, corrupt
witness rejection and the integer budget inequality. These finite tests do
not prove the general gap premise, nor does degree preservation prove mixing.

[setup]: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/setup.tex
[mixing]: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/mixing.tex
