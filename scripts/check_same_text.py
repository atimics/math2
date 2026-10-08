"""Byte-level checks that let two separately built Lean libraries talk about the same objects.

`Fidelity` vendors EuclideanRamsey.lean; `FidelityAlt` vendors EuclideanRamseySpherical.lean.
Both declare OAI.EuclideanRamsey.{Space, Congruent, Ramsey}, so they cannot share a build.
This script checks that (1) those definitions and their enclosing context are identical in
the two vendored files, and (2) `RamseyCosphericalStatement` has identical source text in
Fidelity/AlgebraicRamsey.lean and FidelityAlt/SphericalCheck.lean. With the kernel check in
FidelityAlt/SphericalCheck.lean, CL-1's forward hypothesis is then tied to OpenAI's statement.
"""
import re
import sys

A = "Fidelity/Vendor/EuclideanRamsey.lean"
B = "FidelityAlt/Vendor/EuclideanRamseySpherical.lean"
STMT_FILES = ["Fidelity/AlgebraicRamsey.lean", "FidelityAlt/SphericalCheck.lean"]


def block(src: str, header: str) -> str:
    m = re.search(r"^" + header + r"\b.*?(?=^\S|\Z)", src, re.M | re.S)
    if not m:
        sys.exit(f"missing `{header}`")
    return m.group(0).rstrip()


def preamble(src: str) -> str:
    """Everything before the first declaration: imports, namespaces, opens, sections."""
    m = re.search(r"^(abbrev|def|theorem|structure|inductive)\b", src, re.M)
    return src[: m.start()].strip()


a, b = open(A).read(), open(B).read()
problems = []
if preamble(a) != preamble(b):
    problems.append("preamble (imports/namespaces/opens) differs")
for name in ["abbrev Space", "def Congruent", "def Ramsey"]:
    if block(a, name) != block(b, name):
        problems.append(f"`{name}` differs between the two vendored files")
stmts = [block(open(f).read(), "def RamseyCosphericalStatement") for f in STMT_FILES]
if stmts[0] != stmts[1]:
    problems.append("`RamseyCosphericalStatement` text differs between the two libraries")
if problems:
    sys.exit("TEXT CHECK FAILED:\n- " + "\n- ".join(problems))
print("OK: shared definitions, their context, and RamseyCosphericalStatement are byte-identical")
