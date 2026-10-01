"""Syntax-check every inline <script> in the demo pages with node --check."""
import re, subprocess, sys, tempfile, pathlib
for f in sorted(pathlib.Path(sys.argv[1]).glob("*/index.html")):
    s = f.read_text(encoding="utf-8")
    for n, m in enumerate(re.finditer(r"<script>(.*?)</script>", s, re.S)):
        t = pathlib.Path(tempfile.mkstemp(suffix=".js")[1]); t.write_text(m.group(1), encoding="utf-8")
        r = subprocess.run(["node", "--check", str(t)], capture_output=True, text=True)
        print(f.parent.name, n, "OK" if r.returncode == 0 else "ERR " + r.stderr[:300])
