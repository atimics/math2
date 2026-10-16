# The Heawood obstruction needs exactly three cycle changes

Alexander Richard Towell, with substantial OpenAI Codex assistance.

The specified Heawood F2^3 flow from [the fixed-flow packet](../heawood/README.md)
needs **exactly three** legal simple-cycle XOR changes before an affine lift
can have a three-colorable palette. The explicit successful cycle lengths are
6, 10, 6, with XOR vectors 3, 4, 5. Every intermediate flow remains nowhere zero.
This resolves the two-cycle question left after the
[complete one-cycle classification](../heawood_cycle_repair/README.md).

The [written proof](PROOF.md) gives a structural reduction: when every spanning
2-factor of a cubic graph is Hamiltonian, three-colorable affine palettes are
equivalent to rank-two flows. All 24 perfect-matching complements of this
Heawood graph are Hamiltonian. All 199 legal first moves retain rank three;
their 1,393 binary projections exclude every second rank-reducing move.
The three-step witness reaches the previously known rank-two comparator.

Reproduce from the repository root with Python 3.11 or later; the checkers
use only the standard library:

```sh
python -m experiments.cdc.heawood_two_cycle.review_check
python -m experiments.cdc.heawood_two_cycle.witness
python -m unittest experiments.cdc.heawood_two_cycle.test_structural experiments.cdc.heawood_two_cycle.test_witness -v
```

Expected: both checkers report `status: verified`. The structural checker
reports 213 cycles, 24 Hamiltonian complements, 199 first moves, 1,393
projections and 739 blocked simple projections. The witness checker reports
three operations with deltas `[3,4,5]`, final labels `[1,2,3]`, and three
Hamiltonian 14-cycles. Failure controls include genuinely repairable flows,
incomplete cycle domains, a non-Hamiltonian 2-factor, illegal intermediate
flows, and changed source bytes. Checks remain active under `python -O`.

The theorem checkers need only the pinned predecessor certificate and the
explicit witness, and import no discovery solver. The discovery histogram
mentioned in the proof is secondary exploration, outside the independent
checker’s claims. The three-step search stopped at its first witness; it did
not classify all three-step paths. Reproduction of the theorem does not need
either discovery search.

This is a written proof and exact finite verification, not Lean verification
or human peer review. A [separately tasked AI review](review.md) checked the
mathematical implication and witness implementation. The result is about
operation count for this starting flow: it is not a minimum-support theorem,
a classification of arbitrary Heawood flows, or a universal repair algorithm.

Base: `atimics/math2@2c0f00528a8bb375d02bd48a513062254a53c285`.
Predecessor contribution: `9ccdc1ab6bb02145fcef05d5cfbed13fd8cb5dfc`.
Source certificate SHA256:
`fb8503f1cc92725d9981dd3320e2556fa1dcf74a0ade94f77cca04c88cf5b98f`.
See `verification.json` for test receipts and source pins. The existing PR8
is the canonical destination; no duplicate submission is made.

Credit to atimics and math2 contributors, Sang-il Oum's cited CDC exposition,
and the preceding Petersen/Heawood packets for the construction, obstruction
and comparator. Apache-2.0; predecessor attribution retained. No historical
novelty is claimed. Codex substantially assisted derivation, search, checking,
tests and exposition; AI review is not human peer review.
