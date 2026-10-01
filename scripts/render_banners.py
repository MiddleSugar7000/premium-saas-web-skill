"""Render the SVG banners the way GitHub shows them (inside <img>) and export PNG copies.

Usage: python scripts/render_banners.py [name ...]
Needs: pip install playwright && playwright install chromium

PNGs are used for the social preview / Open Graph image and for previewing the SVGs.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BANNERS = ROOT / "assets" / "banners"
OUT = ROOT / "assets" / "png"


def main(names):
    OUT.mkdir(exist_ok=True)
    svgs = [BANNERS / f"{n}.svg" for n in names] if names else sorted(BANNERS.glob("*.svg"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for svg in svgs:
            page = browser.new_page(device_scale_factor=2)
            page.set_content(
                f'<html><body style="margin:0;background:#0d1117">'
                f'<img id="i" src="data:image/svg+xml;base64,{__import__("base64").b64encode(svg.read_bytes()).decode()}"></body></html>'
            )
            page.wait_for_timeout(2600)
            box = page.locator("#i").bounding_box()
            page.set_viewport_size({"width": int(box["width"]), "height": int(box["height"])})
            page.locator("#i").screenshot(path=str(OUT / f"{svg.stem}.png"), omit_background=True)
            print("rendered", svg.name)
            page.close()
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1:])
