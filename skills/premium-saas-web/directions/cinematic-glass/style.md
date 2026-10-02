# Cinematic Glass (from dark agency/studio sites with video backdrops)

**Why it works:** Pure black lets a moving backdrop carry the mood, while near-invisible glass chips with a lit edge sit on top without ever blocking it. A tight italic serif headline against a light sans body gives the page a film-title voice. Everything is sparse: one headline, one line, two actions.

**Media is optional.** The backdrop is a CSS aurora by default and works with no image or video at all. If the user supplies a video, it paints over the same slot (`shared/video.md`). Never ship a page that depends on a clip that was not provided.

## Tokens

```css
:root{
  --bg:#000; --fg:#fff; --fg-2:rgb(255 255 255/.8); --fg-3:rgb(255 255 255/.6);
  --accent:#9fd3ff;                 /* optional, used on <5% of the page; swap to the brand hue */
  --glow-a:#3a2fa0; --glow-b:#0f6a8a; --glow-c:#7a2b6a;   /* backdrop only, desaturated and dark */
  --font-display:"Instrument Serif",serif; --font-body:"Barlow",system-ui,sans-serif;
  --r-pill:999px; --r-card:20px; --r-icon:12px;
}
```
- **Fonts:** headings Instrument Serif italic 56-88px (desktop up to 96px), tracking -0.045em, `line-height:.8` (`shared/typography.md`, "Serif italic display"); body Barlow 300-500, 14-16px, `line-height:1.25`.
- **Surfaces:** `.glass` / `.glass-strong` from `shared/components.md`. Radii: pills 999px, cards 20px, icon wells 12px.
- **Nav:** a detached glass circle (monogram) on the left, a centered glass pill with the links and a white CTA, an empty spacer on the right. Does not need to be three columns on mobile: hide the links and keep the monogram and CTA.

## CSS aurora backdrop (the default, no media)

```css
.bg-css{position:absolute;inset:0;overflow:hidden;background:#000}
.bg-css::before,.bg-css::after{content:"";position:absolute;width:70vmax;height:70vmax;border-radius:50%;filter:blur(90px);opacity:.55;will-change:transform}
.bg-css::before{left:-15vmax;top:-20vmax;background:radial-gradient(circle,var(--glow-a),transparent 65%);animation:drift 28s ease-in-out infinite alternate}
.bg-css::after{right:-20vmax;bottom:-25vmax;background:radial-gradient(circle,var(--glow-b),transparent 65%);animation:drift 34s ease-in-out infinite alternate-reverse}
.bg-css i{position:absolute;left:30%;top:40%;width:50vmax;height:50vmax;border-radius:50%;filter:blur(110px);opacity:.3;background:radial-gradient(circle,var(--glow-c),transparent 65%);animation:drift 40s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate3d(8vmax,6vmax,0) scale(1.08)}}
@media (prefers-reduced-motion:reduce){.bg-css::before,.bg-css::after,.bg-css i{animation:none}}
@media (max-width:700px){.bg-css::before,.bg-css::after,.bg-css i{filter:blur(60px)}}
```
Add a faint grain (`shared/light.md`, Backgrounds) and a bottom fade `linear-gradient(transparent, #000)` so the next section starts clean. The glass chips need this motion behind them to read as glass.

## Hero composition

- Centered: glass badge ("New" in a white mini pill + one line), serif headline via blur-in (`shared/motion.md`), one sentence of light body copy (max ~42rem), then the primary `.glass-strong` CTA with an arrow and a plain-text secondary action.
- Two small glass stat cards under the CTA (icon well, number in serif italic 36px, one line label) and a trust line with 4-5 names in serif italic. Use the brand's own name-style text logos; for real third-party brands follow `shared/logos.md`.
- All hero elements enter together with the same blur-up (`filter:blur(10px)`, `y:20`, 0.8s, ease out) staggered by 0.2-0.3s. One hero moment.

## Second section: capabilities

A full-height section on the same black ground (and a second backdrop slot), a small `// Label` in 14px at 80%, a 6rem serif heading, then three equal `.glass` cards with `min-height:360px`: icon well + right-aligned tag chips on top, a flex spacer, then serif title and 32ch of light copy at the bottom. Equal cards are acceptable here because the backdrop, not the grid, carries the interest; vary the tag count per card.

## Do not

- Do not add a dark overlay over the backdrop to "fix" legibility: dim the glow tokens instead.
- Do not put glass on a flat color; it needs motion or color behind it.
- Do not use more than one accent hue, and never a purple-to-blue gradient as the backdrop (keep the glows desaturated and separated by black).
- Do not rely on a video, image or any external asset to make the hero look finished.
