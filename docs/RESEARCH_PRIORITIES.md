# Research priorities after the corpus breakthroughs

This note takes the statements in [openai/math at adc7f12][corpus] as premises.
It asks which consequences change the problems researchers should pursue.
Each derivation below is **D** in the [catalogue's evidence tiers](COROLLARIES.md#evidence-tiers):
a written implication using a corpus premise and cited classical results.
None is newly Lean-checked here. The proposed research questions are separate
from the deductions; they are not assertions that those questions remain open
in the entire literature.

This is a targeted follow-up, not a completed mining pass over the previously
unmined theoretical-computer-science shard. It makes no claim that these
implications are new to the literature or absent from every corpus manuscript.

| Entry | Premise | Deduced consequence | Research direction |
|---|---|---|---|
| RP-1 | 287: free group factors are isomorphic | Free entropy dimension varies with generators; a particular C*-generator supremum is infinite | Construct the varying generators and classify restrictions restoring invariance |
| RP-2 | 102: Unique Games hardness | The standard SDP framework has optimal general CSP approximation guarantees | Explicit thresholds, efficient rounding and structured instances |
| RP-3 | 087: symmetric Mahler and equality cases | Global linear stability in every fixed dimension | Explicit constants and dimension dependence |
| RP-4 | 002: full BSD from low Selmer corank | Full BSD in analytic ranks zero and one, and for at least 83.75% by height | Higher analytic rank and effective arithmetic |
| RP-5 | 374: sharp one-third transport-map stability | Cubic distribution-error tolerance suffices for a uniform map-error guarantee | Better stability under additional assumptions |
| RP-6 | 376: effective machine-to-fluid compilation | All-time particle reachability is undecidable on the constructed class | Finite horizons, restricted forcing and robustness |

## RP-1: Generator dependence and an infinite free-entropy supremum

**Premise.** [Family 287][f287] identifies all interpolated free group factors
with parameters greater than one, including infinity, by normal
trace-preserving isomorphisms.

**Derivation.** For every integer \(n\ge2\), \(L(\mathbb F_n)\) has a finite
selfadjoint semicircular generating tuple \(S_n\) with
\(\delta_0(S_n)=n\), where \(\delta_0\) is modified microstates free entropy
dimension. See [Jung, *The free entropy dimension of hyperfinite von Neumann
algebras*, Section 1.1, printed p. 3][jung-hyperfinite]. A trace-preserving
isomorphism preserves the joint moments of a tuple, and hence its
\(\delta_0\). Transport \(S_2\) and \(S_3\) to a common factor \(M\):
\[
W^*(X)=W^*(Y)=M,\qquad \delta_0(X)=2,\quad\delta_0(Y)=3.
\]
Thus \(\delta_0\) is not invariant under arbitrary changes of finite
selfadjoint W*-generators. Transporting every \(S_n\) shows that its values
over such generators of \(M\) are unbounded.

There is a second consequence for \(A=C_r^*(\mathbb F_2)\), with its canonical
trace and weak closure \(M=L(\mathbb F_2)\). [Jung, *A propagation property of
free entropy dimension*, Theorem 1.2][jung-propagation] gives
\[
\delta_0(X)\le
\sup\{\delta_0(Y):Y\text{ is a finite C*-generating set for }A\}
\]
for every finite W*-generating set \(X\) of \(M\). Apply this to the transported
tuples of dimension \(n\), for every \(n\). The supremum on the right is
infinite. Jung also states the relevant contrapositive in Corollary 1.6.

**Change of target.** General W*-generator invariance and a finite bound for
this C*-generator supremum cannot hold under the premise. A concrete task is
to turn the existence argument into explicit generating sets with arbitrarily
large \(\delta_0\), and quantify the cost of describing or approximating them.
Another is to specify restricted classes of generator changes on which
invariance does hold. This conclusion concerns \(\delta_0\); it does not
invalidate every entropy-based invariant or the known hyperfinite invariance
theorem.

## RP-2: A general CSP approximation boundary

**Premise.** [Family 102][f102] supplies deterministic polynomial-time
reductions establishing the Unique Games Conjecture's nearly-satisfiable
versus small-value gap, for every fixed choice of errors.

**Derivation.** [Raghavendra, *Optimal algorithms and inapproximability results
for every CSP?*, Theorems 1.1–1.2 and Corollary 1.3][raghavendra] converts the
integrality-gap curve of the standard SDP into Unique Games hardness, and
provides a matching generic rounding algorithm up to arbitrary fixed
accuracy. Composing its hardness reduction with family 102 removes the
Unique Games conjecture as an additional hypothesis.

For each fixed finite-domain, bounded-arity CSP in the theorem's framework,
the resulting approximation boundary is NP-hard to beat. Interpreting that
as an impossibility for polynomial-time algorithms retains the usual
complexity assumption \(P\ne NP\); randomized algorithms require the
corresponding assumption excluding randomized polynomial-time solutions
of NP-hard problems. This is a worst-case statement and does not cover
arbitrary optimization problems, growing domains or arities, or every
restricted instance class.

**Change of target.** Pursue explicit optimal ratios for individual predicates,
practical rounding schemes, running-time improvements at the established
ratio, parameterized algorithms and tractable structural subclasses.
A general improvement beyond a certified worst-case threshold would have
to overcome the associated NP-hardness reduction. The theorem does not make
its generic rounding procedure practical, nor preclude better results on
application-specific instances.

## RP-3: Global linear stability for symmetric Mahler

**Premise.** [Family 087][f087] proves \(P(K)=|K||K^\circ|\ge m_n=4^n/n!\)
for origin-symmetric convex bodies, with equality exactly for linear
images of Hanner polytopes.

**Classical input.** [Kim, *Minimal volume product near Hanner polytopes*,
Main theorem, printed p. 2][kim] gives constants \(a_n,\eta_n>0\) such that
\[
P(K)-m_n\ge a_n D(K)\quad\text{if }D(K)<\eta_n,\qquad
D(K)=\inf_{H\text{ Hanner}}\bigl(d_{\rm BM}(K,H)-1\bigr).
\]
Here \(d_{\rm BM}\) is Banach–Mazur distance. The constants depend on the
fixed dimension. Kim's introduction also records compactness and
continuity of the volume product on the Banach–Mazur compactum.

**Derivation.** In fixed dimension, there are finitely many Hanner types up
to linear equivalence, so \(D\) is continuous on that compactum and is
bounded by some \(B_n<\infty\). On the compact set \(D(K)\ge\eta_n\), the
premise's equality classification implies a positive minimum
\(b_n=\min(P(K)-m_n)>0\), if that set is nonempty. On this set,
\[
D(K)\le B_n\le (B_n/b_n)(P(K)-m_n).
\]
On its complement Kim gives \(D(K)\le (P(K)-m_n)/a_n\). Combining them
(and omitting the second constant if the compact set is empty) proves
that some \(C_n>0\) satisfies, for every symmetric convex body,
\[
D(K)\le C_n\left(\frac{P(K)}{m_n}-1\right).
\]
Dimension one is immediate since all such bodies are linearly equivalent
intervals.

**Change of target.** Qualitative stability and existence of a global
linear constant now follow from the premise and the classical local
estimate. The compactness proof does not compute \(b_n\). Useful targets
are explicit global constants, their optimal dependence on dimension,
and constructive recovery of a nearby Hanner type from an approximately
minimal body. No dimension-independent estimate is asserted here.

## RP-4: Full BSD in analytic low rank and a height-density consequence

**Premise.** [Family 002's full-formula theorem][bsd-introduction] says that
for \(E/\mathbb Q\), full \(q\)-power Selmer corank zero or one at any prime
\(q\) implies rank equality, finite \(\Sha\), and the full BSD leading-term
formula, in that manuscript's stated normalizations.

**Analytic-low-rank derivation.** The classical modularity,
Gross–Zagier–Kolyvagin analytic-low-rank theorem gives
\(\operatorname{rank}E(\mathbb Q)=r_{\rm an}(E)\) and finite \(\Sha\) when
\(r_{\rm an}(E)\in\{0,1\}\). These inputs are stated and referenced in the
family-002 introduction linked above. The full Kummer sequence is
\[
0\longrightarrow E(\mathbb Q)\otimes\mathbb Q_q/\mathbb Z_q
\longrightarrow \operatorname{Sel}_{q^\infty}(E/\mathbb Q)
\longrightarrow \Sha(E/\mathbb Q)[q^\infty]\longrightarrow0.
\]
Since the last group is finite, the Selmer corank equals \(r_{\rm an}(E)\).
Apply family 002. Full BSD therefore holds for every elliptic curve over
\(\mathbb Q\) of analytic rank zero or one under the premise. Algebraic
rank zero or one alone is not substituted for this hypothesis.

**Density derivation, resolving the bridge in [NT-9](COROLLARIES.md#nt-9).**
[Bhargava–Shankar, *The average size of the 5-Selmer group of elliptic curves
is 6, and the average rank is less than 1*, Propositions 38(b), 40(b), and
the concluding proof of Theorems 3–5, printed pp. 27–29][bhargava-shankar]
bound the lower density of curves with 5-Selmer dimension at most one by
\[
0.5501\cdot\frac78+0.4499\cdot\frac{19}{24}
=0.83750833\ldots>0.8375.
\]
The first bound is on a positive-density family with equidistributed root
numbers; the second is on its complement. Their global root-number
equidistribution conjecture is not assumed in this calculation.

Finite-level Kummer theory gives
\(\operatorname{corank}_{\mathbb Z_5}\operatorname{Sel}_{5^\infty}
\le\dim_{\mathbb F_5}\operatorname{Sel}_5\).
For example, the finite-level sequence expresses the latter dimension as
the Mordell–Weil rank plus the rational 5-torsion dimension plus
\(\dim_{\mathbb F_5}\Sha[5]\); the last term bounds the corank of the
5-primary part of \(\Sha\). Apply family 002 on this subfamily. Full BSD
holds on a set of lower density at least 83.75%, ordered by the height
used in Bhargava–Shankar. This does not give BSD for every curve of
algebraic rank at most one.

**Change of target.** Prioritize analytic rank two and higher, effective
computation of the formula's arithmetic terms, and quantitative control
of exceptional subfamilies. A density result leaves individual exceptional
curves as legitimate research targets.

## RP-5: Error tolerances for transport-map estimation

**Premise.** [Family 374][f374] fixes a uniform source on a compact convex
body with interior in dimension at least two, and bounds the quadratic
Brenier maps to targets supported in a fixed compact set by
\[
\|T_\mu-T_\nu\|_{L^2(\rho)}\le C W_2(\mu,\nu)^{1/3}.
\]
It supplies sharp examples even with three-atom targets.

**Derivation.** To obtain a uniform map-error guarantee \(\varepsilon>0\)
from this bound, it suffices to enforce
\(W_2(\mu,\nu)\le(\varepsilon/C)^3\).
The sharp examples exclude replacement of the exponent by a larger one
uniformly over this class with a fixed constant. This is a sufficient
worst-case error budget, not a necessary tolerance for every pair of
targets and not a sampling-complexity theorem.

**Change of target.** Determine which additional density, regularity or
geometric assumptions permit a better modulus, and separate regularization
bias from distribution-estimation error. Numerical guarantees should state
their source and target classes before borrowing a stability exponent.

## RP-6: Undecidable reachability in smooth forced viscous flows

**Premise.** [Family 376][f376] supplies a terminating compiler from a
Turing machine and input to a finite description of smooth forcing,
at fixed positive computable viscosity, with fluid initially at rest.
A designated particle enters a fixed open region if and only if that
machine halts.

**Derivation.** If a total algorithm decided all-time particle reachability
for every force in that compiled class, composing it with the compiler
would decide the halting problem. Therefore such an algorithm cannot exist.
This is a reduction about the stated effective input representation and
all-time observation, not a claim about every fluid model or finite-time
simulation.

**Change of target.** Study restricted forcing classes, bounded-time
questions with explicit observation margins, and whether the construction
can tolerate fixed perturbation and detector-error bounds. The premise
alone does not establish undecidability with a fixed noise margin;
that robustness question is a separate proposed target. Bounded horizon
alone does not automatically make exact boundary-crossing decisions
decidable.

## Priorities for follow-up

1. RP-1: document the two distinct entropy consequences and work toward
   explicit witnesses.
2. RP-3: extract an effective stability estimate beyond the compactness
   existence argument.
3. RP-2: map concrete predicate families to their certified approximation
   boundaries; this is an entry point into the unmined TCS shard.

The first formalization targets can be abstract bridge lemmas: transport
of a tuple invariant through an isomorphism, unboundedness from witnesses
at every integer, and globalization of a local error bound on a compact
space. They do not require pretending that the analytic theories of free
entropy or convex geometry are already formalized in this repository.

[corpus]: https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a
[f287]: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/287.md
[f102]: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/102.md
[f087]: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/087.md
[f374]: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/374.md
[f376]: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/376.md
[bsd-introduction]: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Exact-Birch-Swinnerton-Dyer-Formula-from-Low-Selmer-Corank-October-3-2026/build/sections/01-introduction.tex
[jung-hyperfinite]: https://arxiv.org/pdf/math/0112039
[jung-propagation]: https://arxiv.org/pdf/math/0611536
[raghavendra]: https://www.cs.cornell.edu/~abrahao/tdg/papers/p245.pdf
[kim]: https://arxiv.org/pdf/1212.2544
[bhargava-shankar]: https://arxiv.org/pdf/1312.7859
