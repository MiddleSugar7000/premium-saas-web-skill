"""Robustness checks for generated pages: the things grade.py's regexes cannot see.

Static checks read the HTML; browser checks load it in Chrome via Playwright.
Usage:
    python check_robust.py page.html [more.html ...]       # one row per file
    python check_robust.py --demos                          # docs/demos/*-before and *-after
    python check_robust.py --hero-only page.html            # adds single-hero checks
Add --json out.json to save the results.
"""
import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# effective-opacity walk over every visible text node: share of characters a visitor cannot see
HIDDEN_JS = """() => {
  let total = 0, hidden = 0;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const t = w.currentNode, n = t.nodeValue.trim().length;
    if (!n || /^(SCRIPT|STYLE|NOSCRIPT)$/.test(t.parentElement.tagName)) continue;
    let el = t.parentElement, op = 1, vis = true;
    while (el && el !== document.documentElement) {
      const cs = getComputedStyle(el);
      op *= parseFloat(cs.opacity);
      if (cs.visibility === 'hidden' || cs.display === 'none') vis = false;
      el = el.parentElement;
    }
    if (!vis) continue;           // display:none / hidden by design (menus, tabs): not counted
    total += n;
    if (op < 0.05) hidden += n;
  }
  return { total, hidden };
}"""


def static_checks(h):
    out = {}
    no_video = "<video" not in h.lower()
    empty_img = re.findall(r"<img\b(?![^>]*\bsrc=[\"'](?!#)[^\"']+[\"'])[^>]*>", h, re.I)
    bad_img = [i for i in empty_img if "srcset" not in i and "data-src" not in i]
    out["No <video> and no <img> without a real src (no invented media)"] = no_video and not bad_img
    out["Uses dvh/svh wherever 100vh is used"] = ("100vh" not in h) or bool(re.search(r"\d+[ds]vh", h))
    out["Has :focus-visible styling"] = ":focus-visible" in h or "focus-visible:" in h
    uses_bf = "backdrop-filter" in h or "backdrop-blur" in h
    out["backdrop-filter has -webkit- fallback"] = (not uses_bf) or ("-webkit-backdrop-filter" in h) or ("backdrop-blur" in h)
    return out


def hidden_frac(page):
    r = page.evaluate(HIDDEN_JS)
    return (r["hidden"] / r["total"]) if r["total"] else 1.0, r["total"]


def browser_checks(browser, url, hero_only=False):
    out = {}
    errors = []

    def new_page(width=1440, height=900, js=True, reduced=False):
        ctx = browser.new_context(viewport={"width": width, "height": height}, java_script_enabled=js,
                                  reduced_motion="reduce" if reduced else "no-preference")
        pg = ctx.new_page()
        if js:
            pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(url, wait_until="load", timeout=60000)
        pg.wait_for_timeout(3000)
        return ctx, pg

    # 1. no horizontal overflow at 390 and 320
    for w in (390, 320):
        ctx, pg = new_page(w, 800)
        ow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        out[f"No sideways overflow at {w}px"] = ow <= 1
        ctx.close()

    # 2. no JS exceptions on load + scroll
    ctx, pg = new_page()
    for _ in range(6):
        pg.mouse.wheel(0, 700); pg.wait_for_timeout(150)
    pg.wait_for_timeout(500)
    out["No JavaScript exceptions"] = not errors
    # 3. broken images
    broken = pg.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0 && !i.src.startsWith('data:') && !/\\.svg(\\?|$)/.test(i.src)).length")
    out["No broken images"] = broken == 0
    if hero_only:
        n = pg.evaluate("[document.querySelectorAll('section').length, document.querySelectorAll('footer').length]")
        out["Hero-only: at most one <section>, no <footer>"] = n[0] <= 1 and n[1] == 0
        st = pg.evaluate("document.documentElement.scrollHeight / innerHeight")
        out["Hero-only: page is at most ~1.3 screens tall"] = st <= 1.3
    ctx.close()

    # 4. no-JS: nothing hidden
    ctx, pg = new_page(js=False)
    frac, total = hidden_frac(pg)
    out["Without JS, <10% of text is invisible (and page has text)"] = frac < 0.10 and total > 200
    ctx.close()

    # 5. reduced motion: nothing hidden after load, without scrolling
    ctx, pg = new_page(reduced=True)
    frac, total = hidden_frac(pg)
    out["With reduced motion, <10% of text is invisible"] = frac < 0.10 and total > 200
    ctx.close()
    return out


def run(files, hero_only_names=("halden",), save=None):
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for f in files:
            f = Path(f).resolve()
            h = f.read_text(encoding="utf-8", errors="ignore")
            hero = any(n in str(f).lower() for n in hero_only_names) or "--hero-only" in sys.argv
            res = static_checks(h)
            try:
                res.update(browser_checks(b, f.as_uri(), hero))
            except Exception as e:
                res["Browser checks ran"] = False
                print("ERR", f, e)
            results[str(f)] = res
            ok = sum(res.values())
            label = "/".join(f.parts[-5:-2]) if f.parent.name == "outputs" else f.parent.name + "/" + f.name
            print(f"{ok}/{len(res)}  {label}")
            for k, v in res.items():
                if not v:
                    print("      FAIL:", k)
        b.close()
    if save:
        Path(save).write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    save = None
    if "--json" in sys.argv:
        i = sys.argv.index("--json"); save = sys.argv[i + 1]; args = [a for a in args if a != save]
    if "--demos" in sys.argv:
        root = Path(__file__).resolve().parent.parent / "docs" / "demos"
        args = [str(p) for p in sorted(root.glob("*/index.html"))]
    run(args, save=save)
