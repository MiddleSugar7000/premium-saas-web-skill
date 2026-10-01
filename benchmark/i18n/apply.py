"""Apply hu ==> en text pairs to a demo page. Usage: python apply.py <page.html> <pairs.txt>
Lines look like `hungarian text ==> english text`. Longest source strings are applied first.
Prints pairs that matched nothing and any remaining Hungarian-accented text so misses are easy to spot."""
import re, sys
from pathlib import Path

page, pairs = Path(sys.argv[1]), Path(sys.argv[2])
src = page.read_text(encoding="utf-8")
items = []
for n, line in enumerate(pairs.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip() or line.startswith("#"):
        continue
    hu, sep, en = line.partition(" ==> ")
    if not sep:
        print("BAD LINE", n, line[:80]); continue
    items.append((hu, en))
items.sort(key=lambda p: -len(p[0]))
for hu, en in items:
    if hu not in src:
        print("NO MATCH:", hu[:90])
    src = src.replace(hu, en)
src = src.replace('<html lang="hu">', '<html lang="en">')
page.write_text(src, encoding="utf-8", newline="\n")
left = [(i + 1, l.strip()[:110]) for i, l in enumerate(src.splitlines()) if re.search(r"[áéíóöőúüűÁÉÍÓÖŐÚÜŰ]", l)]
print(f"{len(left)} lines still contain Hungarian accents")
for i, l in left[:60]:
    print(f"  {i}: {l}")
