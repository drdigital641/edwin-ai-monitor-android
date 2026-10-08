import difflib, json, subprocess, sys
for f in sys.argv[1:]:
    old = subprocess.run(["git", "show", "HEAD:" + f], capture_output=True, text=True).stdout
    new = open(f, encoding="utf-8").read()
    a, b = old.splitlines(True), new.splitlines(True)
    edits = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal": continue
        lo, hi = i1, i2
        while True:
            o = "".join(a[lo:hi]); n = "".join(b[j1 - (i1 - lo):j2 + (hi - i2)])
            if o and old.count(o) == 1: break
            lo = max(0, lo - 1); hi = min(len(a), hi + 1)
        edits.append({"old_text": o, "new_text": n})
    # verify
    t = old
    for e in edits: t = t.replace(e["old_text"], e["new_text"], 1)
    assert t == new, f
    print("=== " + f); print(json.dumps(edits, ensure_ascii=False))
