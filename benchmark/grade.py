"""Programmatic grader for premium-saas-web eval outputs. Usage: python grade.py <iteration-dir>"""
import json, re, sys
from pathlib import Path

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

def blur_px(html):
    return [int(float(m)) for m in re.findall(r"blur\(\s*([\d.]+)px", html)] + \
           [int(float(m)) * 16 for m in re.findall(r"blur\(\s*([\d.]+)rem", html)]

COMMON = [
    ("Design tokens defined as CSS custom properties on :root",
     lambda h: bool(re.search(r":root\s*\{[^}]*--[\w-]+\s*:", h))),
    ("Display type uses negative letter-spacing",
     lambda h: bool(re.search(r"letter-spacing\s*:\s*-\s*[\d.]", h)) or "tracking-tight" in h or "tracking-[-" in h),
    ("Has large-blur light/glow elements (blur >= 60px)",
     lambda h: any(b >= 60 for b in blur_px(h)) or bool(re.search(r"blur-\[(6\d|[7-9]\d|1\d\d)px\]|blur-3xl", h))),
    ("Uses hairline borders with transparency (1px + alpha color)",
     lambda h: bool(re.search(r"1px solid (rgba?\([^)]*(,|/)\s*0?\.\d+\)|var\(--[\w-]*line)", h))),
    ("Uses scroll-driven motion (GSAP ScrollTrigger or IntersectionObserver)",
     lambda h: "ScrollTrigger" in h or "IntersectionObserver" in h),
    ("Respects prefers-reduced-motion",
     lambda h: "prefers-reduced-motion" in h),
    ("Has an infinite marquee/ticker animation",
     lambda h: bool(re.search(r"marquee|ticker|infinite-scroll", h, re.I)) and "infinite" in h),
    ("Has responsive breakpoints (media queries or Tailwind md:/lg:)",
     lambda h: "@media" in h or " md:" in h or " lg:" in h),
    ("No lorem ipsum placeholder copy",
     lambda h: "lorem ipsum" not in h.lower()),
    ("No emoji used as icons (<= 2 emoji characters)",
     lambda h: len(EMOJI.findall(re.sub(r"<script.*?</script>", "", h, flags=re.S))) <= 2),
]

SPECIFIC = {
    "flowpilot-ai-saas": [
        ("Hero shows a product UI / mockup (browser frame, app window, prompt box or dashboard)",
         lambda h: bool(re.search(r"mock|browser|app-window|dashboard|prompt", h, re.I))),
        ("Has a pricing section with tiers",
         lambda h: bool(re.search(r"pricing|árazás|csomag", h, re.I)) and len(re.findall(r"/\s*(hó|month|mo)\b", h, re.I)) >= 2),
        ("Uses glass effect (backdrop-filter)",
         lambda h: "backdrop-filter" in h or "backdrop-blur" in h),
    ],
    "northlane-light-agency": [
        ("Tactile buttons: inset box-shadows for top highlight / bottom lip",
         lambda h: len(re.findall(r"inset\s+0\s+-?\d", h)) >= 2),
        ("Light base background (page bg is light)",
         lambda h: bool(re.search(r"--(bg|page|surface)[\w-]*\s*:\s*#(f[0-9a-f]{5}|e[0-9a-f]{5}|fff)\b", h, re.I))),
        ("Animated number counters for results",
         lambda h: bool(re.search(r"data-count|countUp|counter", h, re.I))),
    ],
    "bence-portfolio-noir": [
        ("Giant display type (>= 120px or >= 12vw)",
         lambda h: any(int(x) >= 120 for x in re.findall(r"font-size\s*:\s*(?:clamp\([^,]+,\s*[\d.]+vw\s*,\s*)?(\d{3})px", h))
                   or any(float(x) >= 12 for x in re.findall(r"([\d.]+)vw", h))),
        ("Outline / stroked text used for contrast",
         lambda h: "text-stroke" in h),
        ("Pure/near-black base background",
         lambda h: bool(re.search(r"--(bg|black|base)[\w-]*\s*:\s*#(000|0[0-9a-f]0[0-9a-f]0[0-9a-f])\b", h, re.I)) or "background:#000" in h.replace(" ", "")),
    ],
}

def main(it):
    it = Path(it)
    for ev in sorted(p for p in it.iterdir() if p.is_dir()):
        for cfg in ("with_skill", "without_skill"):
            run = ev / cfg / "run-1"
            f = run / "outputs" / "index.html"
            h = f.read_text(encoding="utf-8", errors="ignore") if f.exists() else ""
            exps = []
            for text, fn in COMMON + SPECIFIC.get(ev.name.split("-",2)[2], []):
                ok = bool(h) and fn(h)
                exps.append({"text": text, "passed": ok, "evidence": ("index.html " + str(len(h)) + " chars; check " + ("matched" if ok else "not matched")) if h else "index.html missing"})
            passed = sum(e["passed"] for e in exps)
            grading = {"expectations": exps,
                       "summary": {"passed": passed, "failed": len(exps) - passed, "total": len(exps), "pass_rate": round(passed / len(exps), 3)}}
            (run / "grading.json").write_text(json.dumps(grading, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"{ev.name:28} {cfg:14} {passed}/{len(exps)}")

if __name__ == "__main__":
    main(sys.argv[1])
