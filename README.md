# math2 — cross-family corollaries of openai/math

What follows from combining the 722 AI-generated manuscripts in
[openai/math](https://github.com/openai/math) (snapshot
[`adc7f12`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a)),
that the corpus itself does not say.

OpenAI's pipeline posed about 4,000 problems one at a time and checked
results one statement at a time. Nothing in it looks at how the 372 result
families relate. This repo does that: it finds redundant results, chains, and
consequences that combine families, then proves the strongest ones in Lean.

> **Everything here is conditional.** OpenAI's results are claims; several
> have no formalization, and OpenAI warns that some unformalized ones may have
> issues. Every Lean theorem in this repo takes OpenAI's statement as an
> explicit hypothesis, so it is never assumed as an axiom. If an OpenAI claim
> is wrong, only the corollaries that cite it fall.

## Headline

**The Landau–Siegel paper is a corollary of the 7/8 paper.** Family 003
formalizes two theorems separately:

| OpenAI comparator | Claim | Proof in corpus |
|---|---|---|
| `DirichletSevenEighths.lean` | every Dirichlet `L(s,χ) ≠ 0` for `Re s > 7/8` (except the pole) | paper of Sept 30 |
| `SiegelZeros.lean` | real zeros satisfy `(1−β) log q ≥ c` for some unspecified `c > 0` | a *separate* paper of Oct 1, which does not cite the first |
| `QuasiRiemannHypothesis.lean` | `ζ(s) ≠ 0` for `Re s > 7/8` | separate comparator |

`Corollaries/SevenEighths.lean` derives the second and third from the first
alone, with explicit `c = log 3 / 8`. It also proves the stronger uniform
statement that no nontrivial Dirichlet `L`-function, of any modulus, has a
real zero in `(7/8, 1)`. `Fidelity/Checks.lean` re-proves both against
OpenAI's *verbatim* comparator types in the kernel. A third independent route,
through family 029's Hecke theorem, is in the docs (NT-3).

## What's here

| Path | Contents |
|---|---|
| [`docs/COROLLARIES.md`](docs/COROLLARIES.md) | 38 corollaries and redundancies, plus tension checks, across 289 families, each tagged by evidence tier (Lean / written / written-with-unchecked-bridge) |
| `Corollaries/` | Lean library. Mathlib only, with OpenAI statements as hypotheses (`Hypotheses.lean`) |
| `Fidelity/` | Kernel checks that those hypotheses equal OpenAI's own comparator types, plus applications to OpenAI's exact statements |
| `Fidelity/Vendor/` | Byte-identical copies of six `openai/math` comparator files (Apache-2.0); CI diffs them against upstream |
| `scripts/` | Axiom audit: every listed declaration may depend only on `propext`, `Classical.choice` and `Quot.sound` |

### Lean-checked corollaries

| Declaration | Statement | Families |
|---|---|---|
| `real_zero_le_seven_eighths` | real zeros of nontrivial Dirichlet `L`-functions are `≤ 7/8`, for every modulus | 003 |
| `siegel_of_sevenEighths` | OpenAI's Siegel-zero comparator, with `c = log 3 / 8` | 003 ⇒ 003′ |
| `zeta_of_sevenEighths` | OpenAI's zeta comparator | 003 ⇒ 003″ |
| `pi_not_liouvilleWith`, `rat_affine_pi_not_liouvilleWith`, `pi_not_liouville` | `rπ + s` is not `LiouvilleWith p` for any `p > 2` (in Mathlib's API) | 017 |
| `directFiniteness_transfer` | Kaplansky's direct-finiteness counterexample survives every ring map out of OpenAI's finite field | 197 |
| `idempotent_of_directFiniteness_witness` | `ab = 1`, `ac = 0`, `c ≠ 0` ⇒ `ba` is an idempotent other than 0 and 1, so the torsion-free counterexample also breaks the idempotent conjecture in characteristic 2 | 197 ⇒ 196, 207 |
| `zeroDivisor_group_not_leftOrderable` | OpenAI's torsion-free zero-divisor group is not left-orderable | 196 |

## Corrections to earlier claims

Our first pass suggested that "effective class numbers" was a consequence
missing from the corpus. **That was wrong.** The 11/12 paper in family 003
already states `h(D) ≫ √|D| / log log |D|` and the completeness of Euler's
idoneal numbers. The genuinely unstated items are the ones listed above and
in the docs.

## Coverage and limits

- Mined: 289 of 372 families. **Not yet mined:** theoretical computer science,
  combinatorics and logic (83 families).
- Lean status is whatever CI says. A corollary counts as checked only when the
  workflow is green on the commit you're reading.
- "Unstated in the corpus" was established by grep over the corpus text. It is
  not a literature search, and several items are already known once you grant
  the corpus input (marked in the docs).

## Building

```sh
lake exe cache get
lake build Corollaries Fidelity
lake env lean scripts/Axioms.lean
```

## License

Apache-2.0. Files under `Fidelity/Vendor/` are © OpenAI, from
`openai/math`, and unmodified under Apache-2.0.
