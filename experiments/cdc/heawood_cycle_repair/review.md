# Independent mathematical and implementation review

2026-10-15. A separately tasked read-only OpenAI Codex reviewer checked the
claim and supplied the standalone checker source. The primary agent saved
that source with condensed formatting and added mutation tests. The reviewer
then checked its AST and observed that the algorithm was preserved. This is
AI review and exact finite computation, not human peer review or Lean proof.

No blocking finding was reported. Independent cycle-space reconstruction,
translation-domain propagation and independent-set coloring DP reproduce:
213 simple cycles, 199 admissible changes, minima `{4:72,5:96,7:31}`,
168 successful repairs, and shortest successful support six. There are
96 flows with one root-fixed lift, 67 with two and 36 with four: 374 in total.

Completeness arguments checked by the reviewer:

* Chord bits uniquely extend to even edge sets by solving tree parity from
  leaves to root. Connected nonempty degree-two supports are exactly simple
  cycles. All 256 binary cycle-space assignments are exhausted.
* Arc consistency removes no compatible translation. Exhaustive branching
  over every remaining domain value finds all root-fixed lifts.
* Coloring DP considers every partition of the palette vertex set into
  independent sets, fixing the class of the least remaining vertex to avoid
  redundant ordering. It is not a clique-number approximation.

The reviewer independently ran 17 corrupt-input controls under optimized
Python, including duplicate JSON keys. The saved packet adds 20 subtest
mutations and a negative optimized CLI control. Exact final counts are in
verification.json; the earlier review observed eight tests plus 20 subtests.
The explicit repair, its clique, coloring and the table match the certificate.

The support corollaries are valid. A nonzero conservative difference has no
degree-one support vertex, so contains a cycle. Girth six forces at least six
changed edges. A six-edge support must itself be one six-cycle; its difference
values are equal around that cycle by conservation. For a nowhere-zero target
flow, this is an admissible cycle/vector pair in the checked domain. Therefore
no six-edge change of the specified starting flow admits a three-colorable
affine palette, although a six-edge change admits four colors. No claim for
larger arbitrary supports follows.

The public adaptation changes only the relative predecessor path from the
local packet name to `heawood`; the mathematical checker is otherwise the same.
Both the source and result certificates are pinned. Alexander Richard Towell
is the contributor, with substantial OpenAI Codex assistance.
