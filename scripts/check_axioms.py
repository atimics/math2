"""Fail unless every `#print axioms` line uses only the three standard axioms."""
import re, sys

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
text = open(sys.argv[1], encoding="utf-8").read()
expected = int(sys.argv[2])
found, bad = 0, []
for m in re.finditer(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])", text):
    found += 1
    axioms = {a.strip() for a in (m.group(3) or "").split(",") if a.strip()}
    if not axioms <= ALLOWED:
        bad.append((m.group(1), sorted(axioms - ALLOWED)))
    print(f"{m.group(1)}: {sorted(axioms) or 'none'}")
if found != expected:
    sys.exit(f"expected {expected} axiom reports, found {found}")
if bad:
    sys.exit(f"non-standard axioms: {bad}")
print(f"OK: {found} declarations, standard axioms only")
