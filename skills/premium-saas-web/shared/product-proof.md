# Product proof: mockups and bento mini-UIs

## Browser-frame mockup fading into the page

*Why:* Every top SaaS template puts the actual product in the hero. Buyers trust what they can see. Build it in HTML so it's crisp and can be animated.

```html
<div class="mock-wrap">
  <div class="mock">
    <div class="mock-bar"><i></i><i></i><i></i><span class="mock-url">app.yourproduct.com</span></div>
    <div class="mock-body">…sidebar + chat/dashboard built in HTML…</div>
  </div>
  <div class="mock-fade"></div>
</div>
```
```css
.mock-wrap{position:relative;max-width:1288px;margin:64px auto 0}
.mock{border-radius:14px;overflow:hidden;background:#0B0E14;border:1px solid rgb(90 159 255/.5);
  box-shadow:0 0 0 1px rgb(90 159 255/.15),0 0 40px rgb(47 107 255/.45),0 0 120px rgb(47 107 255/.25)}
.mock-bar{display:flex;align-items:center;gap:8px;padding:12px 16px;border-bottom:1px solid var(--line)}
.mock-bar i{width:11px;height:11px;border-radius:50%;background:#FF5F57}.mock-bar i:nth-child(2){background:#FEBC2E}.mock-bar i:nth-child(3){background:#28C840}
.mock-url{margin-inline:auto;padding:4px 80px;border-radius:6px;background:var(--bg-2);font-size:12px;color:rgb(255 255 255/.5)}
.mock-fade{position:absolute;inset:auto 0 -2% 0;height:min(465px,45%);background:linear-gradient(180deg,transparent,var(--bg-0) 94%);pointer-events:none}
```
Animate it in with a slight 3D tilt: `gsap.from('.mock',{rotateX:18,y:80,opacity:0,duration:1.4,ease:'power3.out',transformPerspective:1200})`. On light directions, swap the neon edge glow for a soft layered shadow and a 1px `--line` border.

## Bento grid with mini-UIs and corner light leaks

*Why:* Feature icons are interchangeable; a tiny working-looking UI proves the feature exists. Unequal cell sizes create a magazine rhythm.

```css
.bento{display:grid;gap:16px;grid-template-columns:repeat(6,1fr);grid-auto-rows:minmax(220px,auto)}
.bento>.c1{grid-column:span 2;grid-row:span 2}.bento>.c2{grid-column:span 4}.bento>.c3{grid-column:span 2}.bento>.c4{grid-column:span 2}
.cell{position:relative;overflow:hidden;border-radius:20px;background:var(--bg-2);border:1px solid var(--line);padding:28px;display:flex;flex-direction:column;justify-content:flex-end}
.cell::before{content:"";position:absolute;top:-30%;right:-20%;width:60%;height:60%;border-radius:50%;
  background:radial-gradient(circle,rgb(90 159 255/.55),transparent 70%);filter:blur(40px);opacity:.7}   /* corner light leak */
.cell h3{font-size:20px;letter-spacing:-.02em}.cell p{color:rgb(255 255 255/.6);font-size:14px}
@media(max-width:900px){.bento{grid-template-columns:1fr}.bento>*{grid-column:auto!important;grid-row:auto!important}}
```
Mini-UI ideas (build each in ~10–20 lines of HTML): workflow nodes connected by a dashed SVG path with a dot traveling along it (`offset-path`, see `shared/motion.md`), chat bubbles typing, toggle switches flipping on a loop, a sparkline drawing itself (SVG `stroke-dashoffset`), color chips, a "Process → Sync → Grow" pill flow, a notification stack, a code snippet with a blinking cursor, a radial progress ring, an integrations orbit (real logos, `shared/logos.md`). Give the mini-UI its own muted panel (`background:rgb(255 255 255/.03); border:1px solid var(--line); border-radius:12px`).

Highlighted card among equals (e.g. 1 of 4 services): `background:linear-gradient(160deg,#3B5BFF,#1C2A8C)`, others stay neutral.
