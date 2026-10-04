"""Free (no-model) motion/perf/robustness checks for A/B runs of premium-saas-web.
Usage: python check_motion.py <iteration-dir> [pattern]      default pattern: eval-*/*/outputs/index.html
Writes <run>/checks_motion.json next to each index.html, then prints a per-eval old-vs-new table.
Each check is one line of evidence; `issues` counts what the skill's checklist says must not happen."""
import sys, re, json, io
from pathlib import Path
from playwright.sync_api import sync_playwright

try:
    from PIL import Image, ImageStat
except ImportError:
    Image = None

def static(src):
    s = {}
    s["reduced_motion_css"] = "prefers-reduced-motion" in src
    s["gsap_matchmedia"] = bool(re.search(r"gsap\.matchMedia\s*\(", src))
    s["transition_all"] = len(re.findall(r"transition\s*:\s*all\b", src))
    s["scale0"] = len(re.findall(r"scale\(\s*0\s*\)|scale\s*:\s*0\b", src))
    s["layout_tween"] = len(re.findall(r"gsap\.(?:to|from|fromTo|set)\([^;]{0,200}?\b(?:width|height|top|left)\s*:", src))
    s["linear_spatial"] = len(re.findall(r"gsap\.(?:to|from)\([^;]{0,200}?\b(?:x|y|xPercent|yPercent)\s*:[^;]{0,200}?ease\s*:\s*['\"]none['\"][^;]{0,120}(?!scrub)", src))
    webgl = bool(re.search(r"WebGLRenderer|getContext\(['\"](?:webgl|experimental-webgl)", src))
    s["webgl"] = webgl
    if webgl:
        s["webgl_visibility_pause"] = "IntersectionObserver" in src
        s["webgl_dpr_cap"] = bool(re.search(r"Math\.min\([^)]*devicePixelRatio", src))
        s["webgl_lite_gate"] = bool(re.search(r"hardwareConcurrency|max-width\s*:\s*\d+px\)[^;]{0,80}(?:return|if)", src))
        s["webgl_try_catch"] = bool(re.search(r"try\s*\{[^}]{0,3000}WebGLRenderer|WebGLRenderer[^}]{0,3000}catch", src, re.S))
    return s

def runtime(url, browser):
    r, errs = {}, []
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:120]))
    pg.on("console", lambda m: errs.append("console: " + m.text[:120]) if m.type == "error" else None)
    pg.goto(url, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(1500)
    r["console_errors"] = errs[:6]
    r["canvas"] = pg.evaluate("document.querySelectorAll('canvas').length")
    if r["canvas"] and Image:
        try:
            png = pg.locator("canvas").first.screenshot()
            r["canvas_stddev"] = round(sum(ImageStat.Stat(Image.open(io.BytesIO(png)).convert("L")).stddev), 2)  # ~0 = blank
        except Exception as e:
            r["canvas_stddev"] = f"err {str(e)[:60]}"
    r["hover_transition_max_s"] = pg.evaluate("""() => Math.max(0, ...[...document.querySelectorAll('a,button')].map(e =>
        Math.max(0, ...getComputedStyle(e).transitionDuration.split(',').map(parseFloat))))""")
    ctx.close()
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); pg.goto(url, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(1200)
    r["mobile_overflow_px"] = pg.evaluate("Math.max(0, document.documentElement.scrollWidth - innerWidth)")
    r["mobile_canvas_rendering"] = pg.evaluate("document.querySelectorAll('canvas').length")
    ctx.close()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page(); pg.goto(url, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(1500)
    r["rm_infinite_css_anims"] = pg.evaluate("document.getAnimations().filter(a => a.effect && a.effect.getComputedTiming().iterations === Infinity && a.playState === 'running').length")
    r["rm_h1_opacity"] = pg.evaluate("""() => { const h = document.querySelector('h1'); if (!h) return null; let o = 1, e = h;
        while (e && e.nodeType === 1) { o *= +getComputedStyle(e).opacity; e = e.parentElement; } return +o.toFixed(2); }""")
    ctx.close()
    return r

def issues(s, r):
    n = []
    if not s["reduced_motion_css"] and not s["gsap_matchmedia"]: n.append("no reduced-motion handling")
    n += ["transition:all x%d" % s["transition_all"]] * (s["transition_all"] > 0)
    n += ["scale(0) x%d" % s["scale0"]] * (s["scale0"] > 0)
    n += ["layout-prop tween x%d" % s["layout_tween"]] * (s["layout_tween"] > 0)
    if r.get("console_errors"): n.append("console errors")
    if r.get("mobile_overflow_px"): n.append("mobile overflow %dpx" % r["mobile_overflow_px"])
    if r.get("rm_infinite_css_anims"): n.append("%d CSS loops still run under reduced-motion" % r["rm_infinite_css_anims"])
    if r.get("rm_h1_opacity") is not None and r["rm_h1_opacity"] < 0.9: n.append("h1 hidden under reduced-motion")
    if s["webgl"]:
        for k in ("webgl_visibility_pause", "webgl_dpr_cap", "webgl_lite_gate", "webgl_try_catch"):
            if not s[k]: n.append(k + " missing")
        if isinstance(r.get("canvas_stddev"), float) and r["canvas_stddev"] < 1: n.append("canvas blank")
    return n

def main():
    it = Path(sys.argv[1]); pat = sys.argv[2] if len(sys.argv) > 2 else "eval-*/*/outputs/index.html"
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for f in sorted(it.glob(pat)):
            run = f.parent.parent
            s = static(f.read_text(encoding="utf-8", errors="ignore"))
            try: r = runtime(f.resolve().as_uri(), b)
            except Exception as e: r = {"error": repr(e)[:200]}
            iss = issues(s, r)
            (f.parent / "checks_motion.json").write_text(json.dumps({"static": s, "runtime": r, "issues": iss}, indent=1), encoding="utf-8")
            rel = f.relative_to(it).parts[:-2]            # (eval, config[, run-N])
            rows.append((rel[0], "/".join(rel[1:]), len(iss), iss, s["webgl"]))
        b.close()
    print(f"{'eval':32}{'config':20}{'issues':>7}  webgl  details")
    for ev, cfg, n, iss, w in rows: print(f"{ev:32}{cfg:20}{n:>7}  {'yes' if w else 'no ':5}  {'; '.join(iss)}")

if __name__ == "__main__":
    main()
