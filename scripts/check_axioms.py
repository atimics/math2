"""Check `#print axioms` output against the exact declarations requested.

Usage:
    python3 scripts/check_axioms.py LOG scripts/Axioms.lean
    python3 scripts/check_axioms.py --self-test

Fails (non-zero exit) unless:
  * the log contains no Lean error;
  * every `#print axioms NAME` in the Lean file has exactly one report in the
    log, under exactly that NAME (names may contain `'`; reports may wrap);
  * no report is duplicated, missing, or for an unrequested name;
  * every report uses only propext, Classical.choice and Quot.sound.

This is one of two independent layers: `scripts/Axioms.lean` also runs
`#assert_standard_axioms` (Fidelity/AxiomGuard.lean), which makes Lean itself
fail on any non-standard axiom.
"""
import re
import sys
from collections import Counter

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}

# A report is: 'NAME' depends on axioms: [A, B,\n C]   or   'NAME' does not depend on any axioms
# NAME may contain `'` (e.g. siegel_comparator'_of_sevenEighths), so a quote only
# ends the name when followed by " depends" / " does".
REPORT = re.compile(
    r"^'(?P<name>(?:[^'\n]|'(?! (?:depends on axioms|does not depend)))+)' "
    r"(?:depends on axioms: \[(?P<axioms>[^\]]*)\]|does not depend on any axioms)",
    re.MULTILINE,
)
ERROR = re.compile(r"(^|\s)error:|:\d+:\d+: error", re.MULTILINE)
REQUEST = re.compile(r"^#print axioms\s+(\S+)\s*$", re.MULTILINE)


def expected_names(lean_src: str) -> list[str]:
    return REQUEST.findall(lean_src)


def check(log: str, expected: list[str]) -> list[str]:
    """Return a list of problems (empty means OK)."""
    problems = []
    dup_expected = [n for n, c in Counter(expected).items() if c > 1]
    if dup_expected:
        problems.append(f"duplicate requests in Axioms.lean: {dup_expected}")
    if not expected:
        problems.append("no `#print axioms` requests found")
    if ERROR.search(log):
        problems.append("Lean reported an error:\n" +
                        "\n".join(l for l in log.splitlines() if "error" in l)[:2000])
    reports = [(m.group("name"),
                {a.strip() for a in (m.group("axioms") or "").split(",") if a.strip()})
               for m in REPORT.finditer(log)]
    counts = Counter(n for n, _ in reports)
    for n, c in counts.items():
        if c > 1:
            problems.append(f"duplicate report for {n} ({c}x)")
    exp = set(expected)
    for n in sorted(exp - counts.keys()):
        problems.append(f"missing report for {n}")
    for n in sorted(counts.keys() - exp):
        problems.append(f"unrequested report for {n}")
    for n, axioms in reports:
        extra = axioms - ALLOWED
        if extra:
            problems.append(f"{n} uses non-standard axioms {sorted(extra)}")
    return problems


def self_test() -> None:
    std = "[propext, Classical.choice, Quot.sound]"
    req = ["A.x", "A.y'_z", "B.t"]
    good = (f"'A.x' depends on axioms: {std}\n"
            "'A.y'_z' depends on axioms: [propext,\n Classical.choice,\n Quot.sound]\n"
            "'B.t' does not depend on any axioms\n")
    cases = {
        "good log passes": (good, req, True),
        "duplicate report fails": (good + f"'A.x' depends on axioms: {std}\n", req, False),
        "fifteen copies of one report fail": ((f"'A.x' depends on axioms: {std}\n") * 15, req, False),
        "trailing Lean error fails": (good + "scripts/Axioms.lean:9:0: error: unknown constant\n", req, False),
        "missing report fails": (good.replace("'B.t' does not depend on any axioms\n", ""), req, False),
        "unrequested report fails": (good + "'C.q' does not depend on any axioms\n", req, False),
        "sorryAx fails": (good.replace("Quot.sound]\n'B.t'", "sorryAx]\n'B.t'"), req, False),
        "primed name is not truncated": (good, ["A.x", "A.y'_z", "B.t"], True),
        "truncated-name request fails": (good, ["A.x", "_z", "B.t"], False),
        "duplicate request fails": (good, req + ["A.x"], False),
    }
    failed = 0
    for label, (log, exp, should_pass) in cases.items():
        ok = not check(log, exp)
        status = "ok" if ok == should_pass else "FAIL"
        failed += status == "FAIL"
        print(f"[{status}] {label}")
    if failed:
        sys.exit(f"{failed} self-test case(s) failed")
    print("self-test OK")


def main() -> None:
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    log = open(sys.argv[1], encoding="utf-8").read()
    expected = expected_names(open(sys.argv[2], encoding="utf-8").read())
    problems = check(log, expected)
    for n, axioms in ((m.group("name"), m.group("axioms")) for m in REPORT.finditer(log)):
        print(f"{n}: {' '.join((axioms or 'none').split())}")
    if problems:
        sys.exit("AXIOM AUDIT FAILED:\n- " + "\n- ".join(problems))
    print(f"OK: exactly {len(expected)} requested declarations, standard axioms only")


if __name__ == "__main__":
    main()
