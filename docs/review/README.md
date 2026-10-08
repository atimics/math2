# Expert review packets

The catalogue in [`docs/COROLLARIES.md`](../COROLLARIES.md) has 50 entries. Three would
matter to working mathematicians if they hold:

| Packet | Claim | Rests on | What we need from you | Reviewer profile |
|---|---|---|---|---|
| [NT-9](NT-9.md) | The full BSD leading-term formula holds for at least **83.75%** of elliptic curves over ℚ ordered by height | OpenAI family 002 (not formalized) plus Bhargava–Shankar | Confirm the Selmer averages on Bhargava–Shankar's root-number family and on its complement | Arithmetic statistics or Iwasawa theory |
| [TC-4](TC-4.md) | Directed APSP with small integer weights runs in **`O(n^2.5082)`** (previously `n^2.5275`) | OpenAI family 107 (formalized by OpenAI over ℂ) plus Zwick 2002 | Check the convexity interpolation, the use of Zwick's theorem, and novelty | Fast matrix multiplication or fine-grained complexity |
| [CL-1](CL-1.md) | A finite point set with algebraic coordinates is Euclidean Ramsey **iff it is spherical** | OpenAI family 172, whose Lean proof we rebuild and compose with ours | Check that the Lean statement says what we claim, check the unformalized part of one reduction step, and tell us whether it is known | Euclidean Ramsey theory or commutative algebra |

Each packet is self-contained. Each one has:

1. **The claim**, with the exact conditions.
2. **Numbered questions.** Most can be answered yes or no.
3. **Premises, quoted verbatim** with file paths in [`openai/math@adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
4. **The bridge, step by step.** This is the only part that is ours.
5. **How it could fail**, ranked by our estimate of likelihood.
6. **A reproducer script** that recomputes every number in exact arithmetic. The one
   exception is TC-4's lead part, which uses 30-digit floating point.
7. **Formal and literature status.**

Every packet should take a specialist under an hour. CL-1's bridge is five lines, and
NT-9's is about a page.

## What "conditional" means here

The corpus results are claims by OpenAI. No journal has checked them, and we have not
checked their proofs, except where we rebuild OpenAI's own Lean proof (CL-1). Each packet separates three things: what OpenAI claims, what is classical, and
what we added. Our part is the bridge. If the bridge is right and the cited result is right,
the claim holds.

Formal verification varies by packet:

- **CL-1:** the two family-172 theorems that CL-1 uses are proved in OpenAI's Lean
  project. We rebuild that proof from byte-identical files and compose it with ours. The
  theorem `EndToEnd.algebraic_ramsey_iff_cospherical` therefore has **no unproved
  premise**, only its side conditions. Its axiom audit accepts only `propext`,
  `Classical.choice` and `Quot.sound`.
- **TC-4:** OpenAI's Lean project proves both rectangular premises over ℂ, which their
  `formalization.yaml` lists. Our bridge is not formalized.
- **NT-9:** family 002 has no formalization.

## Reproduce everything

```sh
pip install sympy            # CL-1 uses sympy; TC-4's lead part uses mpmath, which sympy installs
python3 scripts/review/nt9_density.py
python3 scripts/review/tc4_apsp.py
python3 scripts/review/cl1_idempotent.py
lake exe cache get && lake build EndToEnd && lake env lean scripts/AxiomsEndToEnd.lean   # CL-1, end to end
```

CI runs all of these on every push: the
[Lean workflow](https://github.com/atimics/math2/actions/workflows/lean.yml) has the
steps "Expert-review reproducers" and "Axiom audit, CL-1 end to end".

## How to respond

[Open an issue with the expert-review template](https://github.com/atimics/math2/issues/new?template=expert-review.md).
Give the packet name and answer the questions by number. "Unsure" is a useful answer.
You can stay anonymous. If you'd like credit, say how you want it to appear. We will
record the outcome in the packet and in the catalogue's review history, including
negative outcomes: a gap, an error, or "already known, see …".
