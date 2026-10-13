# NT-4: a conditional small-range explicit formula

**Status:** written conditional proof, with a separate AI mathematical review.
This supplies the `x < q` argument left open in math2 NT-4. It does not verify
OpenAI family 003, prove its proposed zero-free region, or claim a new
unconditional bound. This is a classical Ankeny-style deduction; novelty of the
kernel or the implication is not claimed.

Alexander Richard Towell. Substantial OpenAI Codex assistance was used in the
derivation, source checking, implementation of finite controls, and review.
A separate Codex agent reviewed the analytic argument; this is not independent
human peer review or proof-assistant formalization. Licensed under
[Apache-2.0](LICENSE).

Local base: `f91481da76d2333eda3c3cc0709910c0a07bd66c`.
Target: [math2 NT-4 at its inspected commit](https://github.com/atimics/math2/blob/2c0f00528a8bb375d02bd48a513062254a53c285/docs/COROLLARIES.md).
Source contracts and hashes are in [provenance.json](provenance.json); the
separate review is in [review.md](review.md). The OpenAI source is used only to identify the hypothesis.

## 1. Precise analytic statement

Let `q >= 3`, and let \(\chi\) be a **primitive nonprincipal** Dirichlet
character modulo \(q\). Put \(a=(1-\chi(-1))/2\in\{0,1\}\), and let
\(\Lambda(n)\) denote the von Mangoldt function. Define, for real \(x\ge2\),

\[
 S_\chi(x)=\sum_{n\le x}\Lambda(n)\chi(n)\frac n x\left(1-\frac n x\right).
\]

There is an effective absolute constant \(B\ge1\) such that, if every
nontrivial zero of \(L(s,\chi)\) has real part at most \(\theta\), with
\(1/2\le\theta<1\), then

\[
 |S_\chi(x)|\le Bx^\theta\log q \qquad (x\ge2). \tag{1}
\]

The constant is independent of \(q,\chi,\theta,x\), including the order of
\(\chi\). In particular, there is **no assumption \(x\ge q\)**. Effective
means computable from the displayed classical estimates; no numerical value
for \(B\) is supplied here. All logarithms are natural.

More precisely, without the zero-location hypothesis,

\[
 S_\chi(x)=-\sum_\rho\frac{x^\rho}{(\rho+1)(\rho+2)}
 -\frac{1-a}{2}+O(x^{-1/2}\log q), \tag{2}
\]

where the sum counts all nontrivial zeros with multiplicity and converges
absolutely. Its implied constant is effective and absolute.

### Classical inputs and their scope

We use analytic continuation, the primitive Dirichlet functional equation,
nonvanishing on \(\Re s=1\), the Euler product in \(\Re s>1\), the
Hadamard product for the completed function, and Stirling estimates for the
gamma logarithmic derivative. None requires a new zero-free region.
Write

\[
 \mathcal L(s,\chi)=(q/\pi)^{(s+a)/2}\Gamma((s+a)/2)L(s,\chi).
\]

It is entire of order at most one, with precisely the nontrivial zeros, and
satisfies \(\mathcal L(s,\chi)=\varepsilon_\chi
\mathcal L(1-s,\bar\chi)\), \(|\varepsilon_\chi|=1\).
The extra constant factor in this normalization, compared with some references,
does not affect logarithmic derivatives. These facts and the real-part
Hadamard identity used below are recorded in Ian Petrow's
[*Introduction to Analytic Number Theory* notes](https://www.homepages.ucl.ac.uk/~ucahpet/IANTnotes2018.pdf),
Theorem 6.14 (printed p.52), Proposition 8.2 (p.61), Proposition 8.6 (p.64),
and Corollary 8.7 (pp.64–65). We derive the estimates needed here explicitly.

### A conductor-uniform zero mass bound

For real \(t\), taking real parts of the completed logarithmic derivative at
\(2+it\) gives

\[
 \sum_\rho\Re\frac1{2+it-\rho}
 =\frac12\log(q/\pi)+\frac12\Re\psi_\Gamma((2+a+it)/2)
   +\Re\frac{L'}L(2+it,\chi)
 \ll\log(q(2+|t|)), \tag{3}
\]

where \(\psi_\Gamma=\Gamma'/\Gamma\). The last logarithmic derivative is
bounded by the absolutely convergent series
\(\sum_{n\ge2}\Lambda(n)n^{-2}\), independently of the character.
Every term on the left is nonnegative. If \(\rho=\beta+i\gamma\), then
\(0<\beta<1\) and

\[
 \Re\frac1{2+it-\rho}\ge\frac1{4+(t-\gamma)^2}.
\]

At \(t=0\), this and

\[
 \frac1{|(\rho+1)(\rho+2)|}\le\frac1{1+\gamma^2}
 \le\frac4{4+\gamma^2}
\]

give the effective uniform estimate

\[
 \sum_\rho\frac1{|(\rho+1)(\rho+2)|}\ll\log q. \tag{4}
\]

Equation (3) also gives the local count
\(\#\{\rho:|\gamma-t|\le1\}\ll\log(q(2+|t|))\).
No lower bound on \(L(1,\chi)\), or separation of an exceptional zero
from one, enters these estimates.

### Mellin inversion and the contour shift

For \(w(u)=u(1-u)\) on \(0<u\le1\), extended by zero on \(u>1\),

\[
 \int_0^1 w(u)u^{s-1}\,du=\frac1{(s+1)(s+2)}\quad(\Re s>-1).
\]

Mellin inversion, then absolute convergence of the Dirichlet series on
\(\Re s=2\), give

\[
 S_\chi(x)=\frac1{2\pi i}\int_{(2)}
 -\frac{L'}L(s,\chi)\frac{x^s}{(s+1)(s+2)}\,ds. \tag{5}
\]

The weight is continuous and zero at \(u=1\); integer values of \(x\)
require no endpoint correction.

Shift the line to \(\Re s=-1/2\). Here are details ensuring the horizontal
integrals vanish. Subtract the Hadamard logarithmic derivatives at
\(s=\sigma+it\) and \(2+it\). For \(-1/2\le\sigma\le2\), \(|t|\ge2\),
the terms with \(|\gamma-t|>1\) are bounded by constant multiples of
\((t-\gamma)^{-2}\). Summing in unit intervals using the local count from
(3) bounds their total by \(O(\log(q(2+|t|)))\); explicitly the comparison
series is \(\sum_{k\ge1}\log(q(2+|t|+k))/k^2\).
The removed terms at \(2+it\), the gamma derivatives, and the convergent
Dirichlet series have the same bound. Thus, away from zeros,

\[
 \frac{L'}L(\sigma+it,\chi)
 =\sum_{|\gamma-t|\le1}\frac1{\sigma+it-\rho}
   +O(\log(q(2+|t|))). \tag{6}
\]

For every sufficiently large integer \(j\), choose \(T_j\in[j,j+1]\)
at distance at least \(c/\log(q(j+2))\) from the zero ordinates at **both**
heights \(+T_j\) and \(-T_j\). The local count makes the total excluded
interval length less than one for a sufficiently small effective absolute
\(c>0\). This does not assume conjugate symmetry of the zeros of a complex
character. Equation (6) then bounds the logarithmic derivative on both
horizontal sides by \(O(\log^2(q(j+2)))\). Their integrals are
\(O(x^2T_j^{-2}\log^2(q(T_j+2)))\), which tend to zero for fixed \(x,q\).
The final limiting estimates (4) and (7) below are uniform; choosing the
contour sequence separately for each character loses no uniformity.

On the new vertical line, the functional equation gives

\[
 -\frac{L'}L(s,\chi)=\log(q/\pi)
 +\frac12\psi_\Gamma((s+a)/2)
 +\frac12\psi_\Gamma((1-s+a)/2)
 +\frac{L'}L(1-s,\bar\chi).
\]

The reflected Dirichlet series has real part \(3/2\), and both gamma
arguments stay away from poles. Therefore
\(|L'/L(-1/2+it,\chi)|\ll\log(q(2+|t|))\). Quadratic decay of the
kernel yields

\[
 \left|\frac1{2\pi i}\int_{(-1/2)}
 -\frac{L'}L(s,\chi)\frac{x^s}{(s+1)(s+2)}ds\right|
 \ll x^{-1/2}\log q. \tag{7}
\]

The crossed poles of \(-L'/L\) are the nontrivial zeros, with residues
equal to minus their multiplicities, and the simple trivial zero at zero
when \(a=0\). Its weighted residue is \(-1/2\). Simplicity follows from
the functional equation and \(L(1,\bar\chi)\ne0\). For odd characters
the first trivial zero is at \(-1\). The kernel poles \(-1,-2\) are also
outside the shifted strip. There is no principal-character pole at one.
This proves (2). Apply (4) and \(|x^\rho|\le x^\theta\), then absorb the
bounded parity term and (7), to prove (1).

## 2. An elementary positive lower bound

Let \(\Psi(y)=\sum_{n\le y}\Lambda(n)\), and let \(W(x)\) denote
\(S_\chi(x)\) with every character value replaced by one. We prove

\[
 W(x)\ge x/512\qquad(x\ge64). \tag{8}
\]

For integer \(m\ge1\), Legendre's formula expresses the valuation of
\(\binom{2m}{m}\) as a sum of terms each zero or one, indexed by powers
of the prime at most \(2m\). Hence this binomial coefficient divides
\(\operatorname{lcm}(1,\ldots,2m)\). For real \(y\ge32\), taking
\(m=\lfloor y/2\rfloor\) and using the largest term in the binomial sum gives

\[
 \Psi(y)\ge\log\binom{2m}{m}
 \ge2m\log2-\log(2m+1)
 \ge(y-2)\log2-\log(y+1)\ge y/2. \tag{9}
\]

For the last inequality, \(\log2\ge2/3\), and
\(\log(y+1)\le y/8\) for \(y\ge32\): it holds at 32 since
\(e^4>33\), and the derivative of \(y/8-\log(y+1)\) is positive there
and afterwards. Thus the preceding expression is at least
\(13y/24-4/3\ge y/2\).

Also every prime power in \((m,2m]\) contributes one to the corresponding
Legendre sum, so
\(\Psi(2m)-\Psi(m)\le\log\binom{2m}{m}\le2m\log2\).
Iterating over powers of two and rounding \(y\) up to the next power of two
gives \(\Psi(y)<4y\log2<3y\) for \(y\ge1\). The elementary inequalities
\(2/3\le\log2<3/4\) follow by the midpoint and trapezoid bounds for the
integral of the strictly convex function \(1/t\) on \([1,2]\).

For \(x\ge64\), equations (9) and the upper bound imply
\(\Psi(x/2)-\Psi(x/16)\ge x/16\). Every \(n\) in this interval has
\((n/x)(1-n/x)\ge1/32\). Keeping just these nonnegative terms proves (8).
The threshold matters: \(W(2)=0\), so a positive linear lower bound for all
\(x\ge2\) would be false.

## 3. Nonresidues, uniformly in character order

Let \(p\ge3\) be prime. For a particular nonprincipal character \(\chi\)
modulo \(p\), assume all its nontrivial zeros have real part at most \(7/8\).
It is primitive. Choose the effective absolute constant
\(C=(1024B)^8\) and put \(y=C(\log p)^8\); thus \(y\ge64\).

If \(y\ge p\), nonprincipality supplies a unit \(a<p\) outside its
kernel. If \(y<p\) and every positive integer \(n\le y\) were in the
kernel, then \(S_\chi(y)=W(y)\), whereas (1) and (8) would give

\[
 y/512\le W(y)=|S_\chi(y)|\le B y^{7/8}\log p=y/1024,
\]

a contradiction. Consequently a unit \(a\le C(\log p)^8\) with
\(\chi(a)\ne1\) exists, with one constant for every character order.
For each prime \(\ell\mid p-1\), take a character of order exactly
\(\ell\); its kernel is the subgroup of \(\ell\)-th powers. This is
the nonresidue claim in NT-4, conditional on the stated zero bounds for those
characters. The same argument at general \(\theta<1\) yields exponent
\(1/(1-\theta)\), with a constant depending on \(\theta\).

## 4. The separate least-primitive-root deduction

Now assume the zero-location hypothesis for **all** nonprincipal characters
modulo \(p\), and put \(N=p-1\), \(r=\omega(N)\). For a unit \(n\),
the classical character indicator is

\[
 \mathbf1_{\operatorname{ord}_p(n)=N}
 =\frac{\phi(N)}N\sum_{d\mid N}\frac{\mu(d)}{\phi(d)}
       \sum_{\operatorname{ord}\chi=d}\chi(n). \tag{10}
\]

For completeness write \(n=g^k\) using any generator. The inner sum is
the Ramanujan sum \(c_d(k)\). Only squarefree \(d\) contribute, and the
normalized sum factors as
\(\prod_{\ell\mid N}(1-c_\ell(k)/(\ell-1))\).
Here \(c_\ell(k)=\ell-1\) if \(\ell\mid k\), and \(-1\) otherwise.
The product is zero if \(\gcd(k,N)>1\) and \(N/\phi(N)\) otherwise,
proving (10). The total absolute coefficient mass in its normalized sum is
\(\sum_{d\mid N}|\mu(d)|=2^r\); the nonprincipal mass is \(2^r-1\).

Take \(y=C(2^r\log p)^8\) with the same \(C\) as above. If \(y\ge p\),
the elementary existence of a primitive root already gives \(g(p)<p\le y\).
Otherwise every weighted integer is a unit. Multiply (10) by
\(\Lambda(n)w(n/y)\), sum, and apply (1) to each nonprincipal term:

\[
 \sum_{n\le y}\Lambda(n)w(n/y)\mathbf1_{\operatorname{ord}_p(n)=N}
 \ge\frac{\phi(N)}N
 \left(\frac y{512}-(2^r-1)B y^{7/8}\log p\right)>0.
\]

Thus some integer at most \(y\) is primitive, proving

\[
 g(p)\le C\bigl(2^{\omega(p-1)}\log p\bigr)^8. \tag{11}
\]

If an integer has \(r\) distinct prime factors, it is at least
\((r+1)!\); the last half of those factors give
\(\log N\ge (r/2)\log(r/2)\) for \(r\ge2\).
Consequently \(r=O(\log N/\log\log N)\) and (11) gives
\(g(p)\le\exp(O(\log p/\log\log p))\) for sufficiently large \(p\),
with effective constants. Small primes are absorbed in the constant; \(p=2\)
has primitive root one. This is a bound for the least **integer** primitive
root. The easy \(y\ge p\) case does not establish a least-prime-root bound.

## 5. Scope, verification, and handoff

OpenAI's [September 30 source theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/build/paper.tex),
Theorem 1.1 (`thm:main`), asserts the Dirichlet zero-free half-plane needed at
\(\theta=7/8\). We inspected its statement, **not its proof**. The present
argument establishes an implication from that hypothesis and the classical
inputs above. It does not upgrade the source theorem's verification status.

Math2's authors identified these consequences and recorded the missing range
obligation. Classical precedent is Ankeny's conditional nonresidue method;
Lamzouri, Li, and Soundararajan's
[*Conditional bounds for the least quadratic non-residue and related problems*](https://arxiv.org/abs/1309.3595)
gives modern GRH bounds for integers outside subgroups. We do not claim that
this generalization or smoothing weight is new. The contribution is a complete,
reviewable argument for the specific unresolved dependency in NT-4.

The constructive primitive-root assembly and quantum factoring interfaces are
outside this note. In particular, family 279 remains unverified here.

Reproduce the exact **finite arithmetic controls** from the repository root:

```sh
python -m experiments.nt4_small_range.checks
```

The expected output is [checks.json](checks.json). It checks the cyclic-group
indicator against direct gcd for every residue in orders 1 through 256, checks
the central-binomial divisibility and interval inequalities for integers
1 through 256, and rejects explicit mutations of the indicator coefficients
and Chebyshev threshold. These checks do not establish the infinite analytic
statement, the zero-location hypothesis, or effective numerical constants.
The proof is Sections 1–4; see [verification.json](verification.json) for the
finite command results and reviewed-file hashes.

This is a proposed supplement to NT-4. The catalogue tier and source-family
verification status are unchanged. No Lean files or CI workflows are modified;
existing Lean CI does not execute these Python controls.
