"""Turn Lean `error:` blocks in a lake build log into GitHub ::error annotations."""
import re, sys

log = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
pat = re.compile(r"^(?:error: )?([\w./-]+\.lean):(\d+):(\d+): error: ?(.*)$")
i, n = 0, 0
while i < len(log):
    m = pat.match(log[i].strip())
    if m:
        f, line, col, msg = m.groups()
        body = [msg]
        j = i + 1
        while j < len(log) and not pat.match(log[j].strip()) and not log[j].startswith(("✔", "⚠", "✖", "info:", "Some required")):
            body.append(log[j])
            j += 1
        text = "%0A".join(x.replace("%", "%25").replace("\r", "") for x in body)[:3500]
        print(f"::error file={f},line={line},col={col}::{text}")
        n += 1
        i = j
    else:
        i += 1
if n == 0:
    tail = "%0A".join(log[-40:]).replace("::", ": :")[:3500]
    print(f"::error file=build.log::no parsable Lean errors; log tail:%0A{tail}")
