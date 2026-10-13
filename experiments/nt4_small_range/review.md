# Independent analytic review of the NT-4 small-range step

Reviewer scope: the conditional implication only. This review does not certify OpenAI family003, its Theorem 1.1, or the provenance of its asserted zero bound. Target record: [math2 COROLLARIES.md, NT-4, commit 2c0f00528a8bb375d02bd48a513062254a53c285](https://github.com/atimics/math2/blob/2c0f00528a8bb375d02bd48a513062254a53c285/docs/COROLLARIES.md).

## Verdict

The proposed contour proof is correct for **primitive nonprincipal** Dirichlet characters. It yields, with an effective absolute implied constant,

\[
S_\chi(x)=-\sum_\rho\frac{x^\rho}{(\rho+1)(\rho+2)}
-\frac{\mathbf 1_{\chi(-1)=1}}2
+O(x^{-1/2}\log q),\qquad x\ge2.
\]

The sum counts nontrivial zeros with multiplicity and converges absolutely. Consequently, if every such zero has real part at most \(\theta\), where \(1/2\le\theta<1\), then

\[
|S_\chi(x)|\ll x^\theta\log q\qquad(x\ge2),
\]

uniformly in the conductor, the character, its order, and \(\theta\) in that interval. There is no \(x\ge q\) assumption. This closes the stated analytic gap, conditional on the zero-location hypothesis.

The nonprincipal qualification is necessary: the primitive principal character has conductor one, a pole at one, and a main term \(x/6\); the displayed claimed bound would even have \(\log q=0\).

## Contour and uniformity details

Put \(a=(1-\chi(-1))/2\), and distinguish the completed function \(\mathcal L(s,\chi)=(q/\pi)^{(s+a)/2}\Gamma((s+a)/2)L(s,\chi)\) from the von Mangoldt function. The usual Mellin inversion gives

\[
S_\chi(x)=\frac1{2\pi i}\int_{(2)}
-\frac{L'}L(s,\chi)\frac{x^s}{(s+1)(s+2)}\,ds.
\]

Indeed the inverse transform is \(u(1-u)\) for \(0<u<1\) and zero for \(u>1\). At \(u=1\), both one-sided limits equal zero. Thus integers \(x\), including \(x=2\), cause no half-weight correction. Absolute convergence on the initial line justifies interchange with the Dirichlet series.

On \(\Re s=-1/2\), logarithmically differentiating the functional equation gives

\[
-\frac{L'}L(s,\chi)=\log(q/\pi)
+\frac12\psi_\Gamma((s+a)/2)
+\frac12\psi_\Gamma((1-s+a)/2)
+\frac{L'}L(1-s,\overline\chi),
\]

where \(\psi_\Gamma=\Gamma'/\Gamma\). The reflected Dirichlet series is absolutely convergent on \(\Re(1-s)=3/2\). The gamma arguments stay away from poles, including at height zero, and their logarithmic derivatives are \(O(\log(2+|t|))\). Hence the new vertical integral is \(O(x^{-1/2}\log q)\), because the kernel has integrable quadratic decay. These estimates have effective absolute constants; there is no use of an ineffective lower bound for \(L(1,\chi)\).

The crossed singularities are precisely the nontrivial zeros and, when \(a=0\), the simple trivial zero at zero. Nonvanishing of \(L(1,\overline\chi)\) and the functional equation show that this latter zero is simple. Its residue is \(-1/2\). When \(a=1\), the first trivial zero is at \(-1\), outside the shifted strip. The kernel poles \(-1,-2\) are also outside it. No \(L'/L(0,\chi)\) constant is needed.

For completeness, horizontal sides must be sent to infinity through suitable heights, rather than through arbitrary integers. The effective local zero count is

\[
\#\{\rho:|\Im\rho-t|\le1\}\ll\log(q(2+|t|)).
\]

Hadamard logarithmic derivatives, subtracted at \(s\) and \(2+it\), imply for \(-1/2\le\Re s\le2\), \(|t|\ge2\),

\[
\frac{L'}L(s,\chi)=\sum_{|\Im\rho-t|\le1}\frac1{s-\rho}
+O(\log(q(2+|t|))).
\]

The far-zero differences are bounded by a constant times \((t-\Im\rho)^{-2}\), and summing the local counts gives the stated error. One can choose \(T_j\in[j,j+1]\) separated from **both** positive and negative zero ordinates at heights \(\pm T_j\) by at least \(c/\log(q(j+2))\). The union of forbidden intervals has length below one when \(c\) is sufficiently small. Thus the horizontal logarithmic derivatives are \(O(\log^2(q(j+2)))\); each horizontal integral is

\[
O\bigl(x^2 T_j^{-2}\log^2(q(T_j+2))\bigr)\longrightarrow0
\]

for fixed \(x,q\). Choosing the sequence for fixed parameters does not weaken final uniformity: the bounds on the limiting zero sum and vertical integral are themselves uniform. For complex characters, zeros need not be symmetric under \(\gamma\mapsto-\gamma\), so avoiding both sides is a genuine detail.

The zero contribution can be bounded directly without a full zero-count asymptotic. The real-part Hadamard identity at \(s=2\) gives

\[
\sum_\rho \Re\frac1{2-\rho}
=\frac12\log(q/\pi)+\frac12\psi_\Gamma((2+a)/2)
+\Re\frac{L'}L(2,\chi)\ll\log q.
\]

All summands are nonnegative, and, writing \(\rho=\beta+i\gamma\),

\[
\Re\frac1{2-\rho}\ge\frac1{4+\gamma^2},\qquad
\frac1{|(\rho+1)(\rho+2)|}\le\frac1{1+\gamma^2}.
\]

It follows that the total reciprocal-kernel mass is \(O(\log q)\), with an effective constant independent of zero proximity to zero or one. Finally \(|x^\rho|\le x^\theta\), and the bounded parity residue is absorbed since \(q\ge3\) and \(x\ge2\).

## Non-kernel consequence and its quantifiers

Suppose the elementary untwisted estimate \(W(x)=\sum_{n\le x}\Lambda(n)(n/x)(1-n/x)\ge c x\) has been proved for \(x\ge x_0\), with effective absolute \(c>0,x_0\). It cannot hold for every \(x\ge2\), since \(W(2)=0\).

Let \(p\) be odd and \(\chi\) any nonprincipal character modulo \(p\). It is primitive. Let \(B\) be the constant in the analytic estimate and set \(y=C(\log p)^8\), choosing one effective absolute \(C\) so that \(y\ge x_0\) for all \(p\ge3\) and \(cC^{1/8}>B\).

If \(y\ge p\), nonprincipality supplies a unit outside the kernel among \(1,\ldots,p-1\). If \(y<p\) and all positive integers \(n\le y\) lay in the kernel, then \(S_\chi(y)=W(y)\), contradicting

\[
cy\le |S_\chi(y)|\le B y^{7/8}\log p.
\]

Therefore a unit \(a\le C(\log p)^8\) with \(\chi(a)\ne1\) exists, uniformly in the character order. For a character of exact prime order \(\ell\mid p-1\), its kernel is exactly the subgroup of \(\ell\)-th powers. The case \(p=2\) has no nonprincipal characters.

The primitive-root corollary requires another argument; separate nonresidue witnesses do not by themselves supply a small single primitive root. The standard character indicator gives total normalized coefficient mass \(2^{\omega(p-1)}\). Applying the analytic estimate to every nonprincipal character and the lower bound to the principal term yields

\[
g(p)\ll\bigl(2^{\omega(p-1)}\log p\bigr)^8
\]

under the corresponding hypothesis for all those characters. Split off a trial bound \(y\ge p\) using \(g(p)<p\); otherwise all weighted integers are units. The usual elementary estimate \(\omega(n)=O(\log n/\log\log n)\) gives the recorded exponential bound. In the weighted argument a contributing primitive prime power also has a primitive prime base, but the trivial \(y\ge p\) case only establishes the bound for the least integer primitive root.

## Source contracts and remaining issues

The proof's classical analytic inputs are explicitly available in Ian Petrow's [*Introduction to Analytic Number Theory* notes](https://www.homepages.ucl.ac.uk/~ucahpet/IANTnotes2018.pdf): Theorem 6.14, printed p.52, gives completed continuation and functional equation; Proposition 8.2, p.61, gives order at most one; Proposition 8.6, p.64, gives the real-part logarithmic derivative identity; Corollary 8.7, pp.64–65, gives conductor-uniform local and cumulative zero counts. The horizontal estimate above is derived from these inputs rather than attributed to an unlocated exact proposition. PDF page indices are one less than printed page numbers. The local proof via the completed function at \(2+it\) also shows directly that the counting constants are effective.

This is an Ankeny-style classical consequence of a fixed zero-free half-plane, not evidence for a new zero-free region. A directly inspected research-paper comparison is Lau and Wu, [*On the least quadratic non-residue*](https://hkumath.hku.hk/~yklau/p/34.pdf), introduction p.1, equation (1.3), which records Ankeny's conditional \((\log q)^2\) bound and cites the 1952 original. The original is N. C. Ankeny, *Annals of Mathematics* 55 (1952), pp.65–72, [DOI 10.2307/1969420](https://doi.org/10.2307/1969420). The original was bibliographically located, not independently checked here. No novelty claim for this kernel or exact formulation has been established.

No mathematical gap remains in the analytic lemma after the stated nonprincipal qualification and contour-height detail. The parent's elementary lower bound is independently checked in the supplement below. Numerical constant optimization, formal proof-assistant verification, and an exhaustive prior-art search have not been performed. The zero-location premise remains an assumption throughout.

## Supplement: checked explicit elementary lower bound

**Verdict:** the proposed bound \(W(x)\ge x/512\) is valid for every real \(x\ge64\). Both the central-binomial divisibility and the real-endpoint dyadic upper bound are correct.

For every prime \(r\), Legendre's formula gives

\[
v_r\binom{2m}{m}=\sum_{j\ge1}
\left(\left\lfloor\frac{2m}{r^j}\right\rfloor
-2\left\lfloor\frac m{r^j}\right\rfloor\right).
\]

Each summand is zero or one, and is zero for \(r^j>2m\). This valuation is therefore at most \(\lfloor\log_r(2m)\rfloor\), the valuation in \(\operatorname{lcm}(1,\ldots,2m)\). Thus the binomial coefficient divides that least common multiple. Since the central coefficient is the largest of the \(2m+1\) coefficients whose sum is \(4^m\), for \(y\ge32\) and \(m=\lfloor y/2\rfloor\),

\[
\psi(y)\ge\log\binom{2m}{m}
\ge2m\log2-\log(2m+1)
\ge(y-2)\log2-\log(y+1)\ge y/2.
\]

The last step follows from \(\log2\ge2/3\), \(\log(y+1)\le y/8\) for \(y\ge32\), and \((13/24)y-4/3\ge y/2\). The logarithm estimates admit elementary checks: integrate \(1/t\) with its midpoint lower bound to obtain \(\log2\ge2/3\); \(\log33<4\) follows from \(e^4>1+4+4^2/2!+4^3/3!+4^4/4!=103/3>33\); and the derivative of \(y/8-\log(y+1)\) is positive for \(y\ge32\).

For the upper bound, every prime power \(r^j\in(m,2m]\) contributes one to the corresponding Legendre summand, so

\[
\psi(2m)-\psi(m)\le\log\binom{2m}{m}\le2m\log2.
\]

For real \(y>1\), choose an integer \(k\ge1\) with \(y\le2^k<2y\). Telescoping at the integer powers of two gives

\[
\psi(y)\le\psi(2^k)
\le(2^{k+1}-2)\log2<4y\log2<3y.
\]

At \(y=1\), the bound holds because \(\psi(1)=0\). The strict inequality \(\log2<3/4\) follows from the trapezoidal upper bound for the integral of the strictly convex function \(1/t\) on \([1,2]\). No dyadic recurrence at noninteger arguments is being assumed.

Finally, if \(x\ge64\), then

\[
\psi(x/2)-\psi(x/16)\ge x/4-3x/16=x/16.
\]

For each integer \(n\in(x/16,x/2]\), its weight is \((n/x)(1-n/x)\ge1/32\). Nonnegativity of all other terms now gives \(W(x)\ge x/512\), exactly as proposed. Thus the non-kernel deduction above may take \(c=1/512\) and \(x_0=64\).

## Final consistency read of the assembled proof

On 2026-10-13, the reviewer read Sections 1–4 of `research/nt4_small_range/README.md` against this review. **Verdict: pass; no corrections required.** This is an AI mathematical review of a conditional argument, not independent human refereeing or formal verification.

The checked whole-file SHA256 was:

```text
5af6338cebae8668391467ac91fccb23e68402005930dd29c60a02897188445d
```

In particular, \(B\ge1\), \(p\ge3\), and \(C=(1024B)^8\) ensure the chosen \(y\) exceeds 64. In Section 3, \(B y^{7/8}\log p=y/1024\), which strictly contradicts the lower bound \(y/512\). In Section 4, the indicator has the correct prefactor \(\phi(N)/N\), the inner sum has total absolute coefficient mass \(2^r\), and its nonprincipal part has mass \(2^r-1\). At the larger \(y\) chosen there, the error is at most \((1-2^{-r})y/1024\), so the displayed weighted count is positive. The Ramanujan-product verification of the indicator is consistent for every character order.

The elementary inequality \(N\ge(r+1)!\) and its weaker consequence \(\log N\ge(r/2)\log(r/2)\) for \(r\ge2\) are valid. They imply the effective asymptotic bound for \(r\), and thus the stated least integer primitive-root estimate. The \(y\ge p\) case and \(p=2\) handling preserve that exact scope. This consistency read did not review Section 5, finite-control scripts, output files, or provenance metadata.

## Upstream packaging

The hash above identifies the original workspace note. The submitted note has
the same Sections 1–4 byte for byte. Packaging changes relocate the finite
commands, remove workspace-only links, and describe submission scope. The
submitted files and unchanged proof-section hash are recorded in verification.json.
