"""Byte-level checks that let two separately built Lean libraries talk about the same objects.

`Fidelity` vendors EuclideanRamsey.lean; `FidelityAlt` vendors EuclideanRamseySpherical.lean.
Both declare OAI.EuclideanRamsey.{Space, Congruent, Ramsey}, so they cannot share a build.
This script checks that (1) those definitions and their enclosing context are identical in
the two vendored files, and (2) `RamseyCosphericalStatement` has identical source text in
Fidelity/AlgebraicRamsey.lean and FidelityAlt/SphericalCheck.lean. With the kernel check in
FidelityAlt/SphericalCheck.lean, CL-1's forward hypothesis is then tied to OpenAI's statement.

For the `EndToEnd` library it also checks that (3) OpenAI's proof files define the ten
objects CL-1 uses exactly as the comparator does, and state `classification` and
`ramsey_cospherical` exactly as the comparators do; and (4) the proof block in
EndToEnd/AlgebraicRamsey.lean is a verbatim copy of the one in Fidelity/AlgebraicRamsey.lean.
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
# (3) OpenAI's proof files vs the comparator statements
MODEL = "OAI/Combinatorics/EuclideanRamsey/Model.lean"
model = open(MODEL).read()
for name in ["abbrev Space", "def Congruent", "def Ramsey", "def coordinateField", "abbrev Coeff",
             "abbrev TensorRing", "def coordinate", "def augmented", "def multiply",
             "def FieldCriterion"]:
    if block(a, name) != block(model, name):
        problems.append(f"`{name}` differs between {MODEL} and {A}")


def signature(src: str, header: str) -> str:
    m = re.search(r"^" + header + r"\b(.*?):=", src, re.M | re.S)
    if not m:
        sys.exit(f"missing `{header}`")
    return " ".join(m.group(1).split())


for header, comp, proof in [
        ("theorem classification", A, "OAI/Combinatorics/EuclideanRamsey/Main.lean"),
        ("theorem ramsey_cospherical", B, "OAI/Combinatorics/EuclideanRamsey/Spherical.lean")]:
    if signature(open(comp).read(), header) != signature(open(proof).read(), header):
        problems.append(f"`{header}` is stated differently in {proof} and {comp}")

# (4) the CL-1 proof block is copied verbatim into the end-to-end library
def fidelity_block(path: str) -> str:
    src = open(path).read()
    i, j = src.find("namespace Fidelity\n"), src.find("end Fidelity\n")
    if i < 0 or j < 0:
        sys.exit(f"missing Fidelity block in {path}")
    return src[i:j]


if fidelity_block("Fidelity/AlgebraicRamsey.lean") != fidelity_block("EndToEnd/AlgebraicRamsey.lean"):
    problems.append("the proof block in EndToEnd/AlgebraicRamsey.lean is not a verbatim copy")

if problems:
    sys.exit("TEXT CHECK FAILED:\n- " + "\n- ".join(problems))
print("OK: shared definitions, their context, RamseyCosphericalStatement, OpenAI's proof-file\n"
      "definitions and statements, and the end-to-end proof block are all byte-identical")
