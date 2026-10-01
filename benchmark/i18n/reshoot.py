"""Re-capture the demo screenshots after the pages were translated to English.
Usage: python reshoot.py <port>   (serve the repo root first: python -m http.server <port>)
Writes docs/demos/<name>/full-desktop.jpg, full-mobile.jpg and the 1440x900 hero crops in assets/screenshots/ and docs/img/."""
import sys, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PORT = sys.argv[1] if len(sys.argv) > 1 else "8791"
NAMES = ["flowpilot", "northlane", "portfolio", "invoicing"]
FINISH_JS = """() => {
  try { if (window.gsap) { gsap.globalTimeline.getChildren(true, true, true).forEach(t => { if (!t.scrollTrigger || !t.vars.scrub) t.progress(1); }); } } catch (e) {}
  try { if (window.ScrollTrigger) ScrollTrigger.refresh(); } catch (e) {}
}"""

def shoot(page, url, width, height, full_out, crop_out=None):
    page.set_viewport_size({"width": width, "height": height})
    resp = page.goto(url, wait_until="networkidle", timeout=90000)
    if not resp or resp.status != 200:
        raise RuntimeError(f"{url} returned {resp.status if resp else None}")
    page.wait_for_timeout(3500)
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.mouse.wheel(0, height * 0.8)
        page.wait_for_timeout(250)
        y += height * 0.8
        total = page.evaluate("document.documentElement.scrollHeight")
    page.wait_for_timeout(1200)
    page.evaluate(FINISH_JS)
    page.mouse.wheel(0, -total * 2)
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(1800)
    page.screenshot(path=str(full_out), full_page=True, type="jpeg", quality=72)
    if crop_out:
        page.screenshot(path=str(crop_out), type="jpeg", quality=82, clip={"x": 0, "y": 0, "width": width, "height": height})

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for n in NAMES:
        for kind in ("before", "after"):
            d = ROOT / "docs" / "demos" / f"{n}-{kind}"
            url = f"http://127.0.0.1:{PORT}/docs/demos/{n}-{kind}/index.html"
            ctx = b.new_context(device_scale_factor=1)
            page = ctx.new_page()
            crop = ROOT / "assets" / "screenshots" / f"{n}-{kind}.jpg"
            shoot(page, url, 1440, 900, d / "full-desktop.jpg", crop)
            shutil.copyfile(crop, ROOT / "docs" / "img" / f"{n}-{kind}.jpg")
            shoot(page, url, 390, 844, d / "full-mobile.jpg")
            ctx.close()
            print("ok", n, kind)
    b.close()
