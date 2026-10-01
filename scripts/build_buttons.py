"""Generate the clickable README buttons as standalone SVGs (assets/banners/btn-*.svg).

GitHub only lets a whole <img> be a link, so every button is its own image wrapped in <a>.
Styles mirror the skill's recipes: rainbow-border CTA with under-glow, white pill, glass ghost.
Usage: python scripts/build_buttons.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "banners"

SANS = "'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
CHAR_W = 8.35  # rough advance width at 16px, good enough to size the pill

ICONS = {
    "arrow": '<path d="M0 -6l6 6-6 6" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
    "play": '<path d="M-1 -6.5v13l10-6.5z" fill="{c}"/>',
    "download": '<path d="M4 -8v11M-1 -2l5 5 5-5M-3 7h14" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "chat": '<path d="M-2 -7h14a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H4l-5 4v-4h-1a3 3 0 0 1-3-3v-7a3 3 0 0 1 3-3z" fill="none" stroke="{c}" stroke-width="1.9" stroke-linejoin="round"/>',
    "star": '<path d="M5 -8l2.6 5.3 5.8.8-4.2 4.1 1 5.8L5 5.3 -.2 8l1-5.8-4.2-4.1 5.8-.8z" fill="{c}"/>',
}

BUTTONS = [
    # name, label, style, icon
    ("btn-hire", "Hire me · get a quote", "rainbow", "arrow"),
    ("btn-portfolio", "See my portfolio", "white", "arrow"),
    ("btn-demo", "Live before / after demo", "white", "play"),
    ("btn-install", "Install guide", "ghost", "download"),
    ("btn-telegram", "Message me on Telegram", "ghost", "chat"),
    ("btn-star", "Star this repo", "ghost", "star"),
]


def button(label, style, icon):
    h = 56
    text_w = len(label) * CHAR_W
    w = int(28 + text_w + 14 + 18 + 26)  # pad + text + gap + icon + pad
    pad = 14  # room for the glow
    W, H = w + pad * 2, h + pad * 2 + 6
    x, y = pad, pad
    tx = x + 28
    ix = x + 28 + text_w + 16
    defs, body = [], []
    if style == "rainbow":
        defs.append(
            '<linearGradient id="rb" x1="0" x2="1">'
            + "".join(
                f'<stop offset="{i/8:.3f}" stop-color="{c}"/>'
                for i, c in enumerate(["#FF4F8B", "#8B6CFF", "#30E3FF", "#8B6CFF", "#FF4F8B", "#8B6CFF", "#30E3FF", "#8B6CFF", "#FF4F8B"])
            )
            + "</linearGradient>"
            f'<clipPath id="c"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}"/></clipPath>'
            '<filter id="g" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="9"/></filter>'
            f'<linearGradient id="p" x1="0" x2="1"><stop offset="0" stop-color="#E4E1F0"/><stop offset=".72" stop-color="#fff"/></linearGradient>'
        )
        body.append(
            f'<g clip-path="url(#c)" filter="url(#g)" opacity=".85" transform="translate({w*0.1:.0f} {h*0.45:.0f}) scale(.8 .6)">'
            f'<rect class="rb" x="{x}" y="{y}" width="{w*2}" height="{h}" fill="url(#rb)"/></g>'
            f'<g clip-path="url(#c)"><rect class="rb" x="{x}" y="{y}" width="{w*2}" height="{h}" fill="url(#rb)"/></g>'
            f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" rx="{(h-4)/2}" fill="url(#p)"/>'
        )
        fg, weight = "#0E1018", 600
    elif style == "white":
        defs.append(
            '<linearGradient id="p" x1="0" x2="1"><stop offset="0" stop-color="#DBE2E6"/><stop offset=".72" stop-color="#fff"/></linearGradient>'
            '<linearGradient id="sg" x1="1" x2="0"><stop offset="0" stop-color="#5A9FFF"/><stop offset="1" stop-color="#FFFA6B" stop-opacity=".2"/></linearGradient>'
            '<filter id="g" x="-50%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="9"/></filter>'
        )
        body.append(
            f'<rect class="sg" x="{x+w-96}" y="{y+4}" width="96" height="{h-8}" rx="{(h-8)/2}" fill="url(#sg)" filter="url(#g)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="url(#p)"/>'
        )
        fg, weight = "#0D1017", 600
    else:  # ghost / glass
        body.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#191D2A"/>'
            f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{(h-1)/2}" fill="none" stroke="#fff" stroke-opacity=".16"/>'
            f'<rect x="{x+18}" y="{y+1}" width="{w-36}" height="1" fill="#fff" fill-opacity=".22"/>'
        )
        fg, weight = "#fff", 500
    body.append(
        f'<text x="{tx:.0f}" y="{y + h/2 + 6:.0f}" font-family="{SANS}" font-size="16.5" font-weight="{weight}" fill="{fg}">{label}</text>'
        f'<g class="ic" transform="translate({ix:.0f} {y + h/2:.0f})">{ICONS[icon].format(c=fg)}</g>'
    )
    css = (
        "<style>.rb{animation:rb 5s linear infinite}@keyframes rb{to{transform:translateX(-50%)}}"
        ".sg{animation:sg 3s ease-in-out infinite}@keyframes sg{50%{opacity:.55}}"
        ".ic{animation:ic 2.4s ease-in-out infinite}@keyframes ic{50%{translate:3px 0}}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
        f"<title>{label}</title>{css}<defs>{''.join(defs)}</defs>{''.join(body)}</svg>\n"
    )


if __name__ == "__main__":
    for name, label, style, icon in BUTTONS:
        (OUT / f"{name}.svg").write_text(button(label, style, icon), encoding="utf-8")
        print("wrote", name)
