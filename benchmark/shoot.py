"""Full-page screenshots of every run's index.html (desktop + mobile). Usage: python shoot.py <iteration-dir>"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

FINISH_JS = """() => {
  try { if (window.gsap) { gsap.globalTimeline.getChildren(true, true, true).forEach(t => { if (!t.scrollTrigger || !t.vars.scrub) t.progress(1); }); } } catch (e) {}
  try { if (window.ScrollTrigger) ScrollTrigger.refresh(); } catch (e) {}
}"""

def shoot(page, url, out, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:  # wheel-scroll so smooth-scroll libs and ScrollTriggers fire
        page.mouse.wheel(0, height * 0.8)
        page.wait_for_timeout(250)
        y += height * 0.8
        total = page.evaluate("document.documentElement.scrollHeight")
    page.wait_for_timeout(1200)
    page.evaluate(FINISH_JS)
    page.mouse.wheel(0, -total * 2)
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(1500)
    page.screenshot(path=str(out), full_page=True, type="jpeg", quality=72)

def main(it):
    it = Path(it)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for html in sorted(it.glob("eval-*/*/run-1/outputs/index.html")):
            ctx = b.new_context(device_scale_factor=1)
            page = ctx.new_page()
            for name, w, h in (("1-desktop-1440.jpg", 1440, 900), ("2-mobile-390.jpg", 390, 844)):
                try:
                    shoot(page, "http://127.0.0.1:" + (sys.argv[2] if len(sys.argv) > 2 else "8790") + "/" + html.relative_to(it).as_posix(), html.parent / name, w, h)
                    print("ok ", html.parent.parent.parent.parent.name, html.parent.parent.parent.name, name)
                except Exception as e:
                    print("ERR", html, name, e)
            ctx.close()
        b.close()

if __name__ == "__main__":
    main(sys.argv[1])
