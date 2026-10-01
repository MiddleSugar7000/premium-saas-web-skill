# Recipes: the finishing techniques

Each recipe comes with a one-line *why*, so you can adapt it instead of pasting it blindly. Values are the ones measured on the reference sites.

## Contents
1. Sculpted glow (hero light source)
2. Animated rainbow border + under-glow (primary CTA / prompt box)
3. Magnetic pill button with side glow
4. Tactile glossy buttons (light + dark)
5. Sheen surfaces (cards)
6. Glass floating nav
7. Hairline grid & column guides
8. Display type: tight tracking, dimmed half, metallic gradient
9. Scroll-fill text
10. Product proof: browser-frame mockup, prompt box, fade into page
11. Bento grid with mini-UIs and corner light leaks
12. Eyebrow badges & avatar stack
13. Marquees with masked edges
14. Backgrounds: dot grid, noise, radial spotlight band, dot globe
15. Outline-over-photo hero word
16. Framed hero with notch tab
17. Pricing highlight
18. Footer wordmark

---

## 1. Sculpted glow

*Why:* A single radial gradient looks like a gradient. Real light has shape. OptimAI stacks pure-hue blobs and then lays **bg-colored blobs on top** (also blurred) to carve the glow into a crescent or arch. That's why it feels like an eclipse, not a wallpaper.

```html
<section class="hero">
  <div class="glow" aria-hidden="true">
    <span class="g g1"></span><span class="g g2"></span>   <!-- light -->
    <span class="g e1"></span><span class="g e2"></span>   <!-- erasers -->
    <span class="g core"></span>                            <!-- hot core -->
  </div>
  ...content (position:relative; z-index:2)...
</section>
```
```css
.hero{position:relative;overflow:hidden;background:var(--bg-0);isolation:isolate}
.glow{position:absolute;inset:0;z-index:0;pointer-events:none}
.g{position:absolute;display:block}
.g1{top:-17%;left:50%;width:812px;height:488px;translate:-80% 0;background:var(--glow);filter:blur(100px)}
.g2{top:-5%;right:-4%;width:212px;height:288px;background:var(--glow);filter:blur(120px)}
.e1{top:-22%;left:50%;width:672px;height:488px;translate:-80% 0;border-radius:200px;background:var(--bg-0);filter:blur(100px);z-index:1}
.e2{bottom:-20%;left:50%;width:min(1812px,140vw);height:1040px;translate:-50% 0;border-radius:200px;background:var(--bg-0);filter:blur(142px);z-index:1}
.core{bottom:10%;left:50%;width:150px;height:180px;translate:-50% 0;border-radius:999px;background:linear-gradient(var(--accent-deep),var(--accent));filter:blur(78px);z-index:2}
@media (max-width:768px){.g{filter:blur(60px)!important;scale:.6}}
```
Tune by moving the erasers. Rule of thumb: light blobs at 100% saturation, erasers same size or bigger, blur 80–140px. Add a slow drift (`animation: drift 18s ease-in-out infinite alternate` on `.g1`, translating ±40px) for life.

A lighter variant for sections: one blob of accent at 25% opacity behind a heading, `filter:blur(120px)`.

## 2. Animated rainbow border + under-glow

*Why:* A moving gradient border signals "AI / live / special" and draws the eye to the one action that matters. The blurred copy underneath makes the button look like it's casting colored light onto the page. **Use it on one or two elements per page only.**

```css
.btn-rainbow{
  --fill: var(--bg-2);
  position:relative;isolation:isolate;
  display:inline-flex;align-items:center;gap:8px;
  padding:13px 24px;border-radius:6px;
  font:500 16px/1.4 "IBM Plex Mono",monospace;color:#fff;
  border:2px solid transparent;
  background:
    linear-gradient(var(--fill),var(--fill)) padding-box,
    linear-gradient(#121213 0%,rgb(18 18 19/.6) 80%,rgb(18 18 19/0)) border-box,
    linear-gradient(90deg,var(--fill),#8765FF,#FFF181,#FF4C52,#734CFF,#8765FF,#FFF181,#FF4C52,#734CFF,var(--fill)) border-box;
  background-size:400% 100%;
  animation:rainbow 15s linear infinite;
}
.btn-rainbow::before{               /* the colored light it casts */
  content:"";position:absolute;z-index:-1;
  left:50%;bottom:-25%;width:80%;height:40%;translate:-50% 0;
  background:linear-gradient(90deg,#30E3FF,#8765FF,#FFF181,#FF4C52,#734CFF,#30E3FF,#8765FF,#FFF181,#FF4C52,#734CFF,#30E3FF);
  background-size:400% 100%;animation:rainbow 15s linear infinite;
  filter:blur(14px);transition:filter .5s ease;
}
.btn-rainbow:hover::before{filter:blur(10px)}  /* light "focuses" on hover */
@keyframes rainbow{to{background-position:400% 0}}
```
The middle layer (dark→transparent, top→bottom) hides the rainbow on the top edge, so the color seems to come from *below*. For a prompt box, apply the same background stack to the input wrapper with `border-radius:999px`.

## 3. Magnetic pill button with side glow

*Why:* A white pill on dark is the clearest CTA there is. The blurred blue-yellow blob tucked behind its right edge reads as reflected light, and following the cursor makes it feel alive.

```html
<a class="btn-pill magnetic" href="#">Get started <svg>…chevron…</svg><span class="side-glow"></span></a>
```
```css
.btn-pill{position:relative;isolation:isolate;display:inline-flex;gap:7px;align-items:center;padding:13px 24px;border-radius:999px;
  background:linear-gradient(90deg,#DBE2E6 0%,#fff 71.6%);color:#0D1017;font:500 15px "IBM Plex Mono",monospace}
.side-glow{position:absolute;z-index:-1;right:0;top:50%;translate:0 -50%;width:88px;height:56px;border-radius:999px;
  background:linear-gradient(270deg,#5A9FFF 0%,rgb(255 250 107/.2) 95%);filter:blur(12px);transition:transform .5s}
.btn-pill:hover .side-glow{transform:translateX(6px) scale(1.1)}
.btn-pill svg{transition:transform .3s}.btn-pill:hover svg{transform:translateX(3px)}
```
Magnetic JS (desktop only):
```js
if(matchMedia('(pointer:fine)').matches)document.querySelectorAll('.magnetic').forEach(el=>{
  el.addEventListener('mousemove',e=>{const r=el.getBoundingClientRect();
    gsap.to(el,{x:(e.clientX-r.left-r.width/2)*.25,y:(e.clientY-r.top-r.height/2)*.35,duration:.4,ease:'power3.out'})});
  el.addEventListener('mouseleave',()=>gsap.to(el,{x:0,y:0,duration:.6,ease:'elastic.out(1,.4)'}));
});
```

## 4. Tactile glossy buttons

*Why:* Aigocy's buttons look like physical keys: a 1px inner highlight on top (light from above), a 3px darker inner lip at the bottom (thickness), and a 5-step shadow stack whose blur grows geometrically (a realistic contact shadow, not one blurry smudge).

```css
.btn-tactile-dark{
  padding:14px 26px;border-radius:99px;color:#fff;font-weight:500;
  background:
    radial-gradient(62.56% 62.56% at 28.14% -10.42%,rgb(255 255 255/.2) 0%,rgb(255 255 255/0) 100%),
    #272727;
  box-shadow:
    inset 0 -3px 0 #080808,
    inset 0 1px 0 rgb(255 255 255/.3),
    0 2.77px 2.21px rgb(0 0 0/.12),
    0 6.65px 5.32px rgb(0 0 0/.13),
    0 12.52px 10.02px rgb(0 0 0/.133),
    0 22.34px 17.87px rgb(0 0 0/.14),
    0 41.78px 33.42px rgb(0 0 0/.15);
  transition:transform .2s,box-shadow .2s;
}
.btn-tactile-dark:active{transform:translateY(1px);box-shadow:inset 0 -1px 0 #080808,inset 0 1px 0 rgb(255 255 255/.3),0 2px 3px rgb(0 0 0/.2)}
.btn-tactile-light{
  padding:14px 26px;border-radius:99px;color:#09090B;font-weight:500;
  background:radial-gradient(62.56% 62.56% at 28.14% -10.42%,rgb(255 255 255/.2),transparent),#F5F5F5;
  box-shadow:inset 0 -3px 0 #E9E9E9,inset 0 1px 0 rgb(255 255 255/.7),0 2.77px 2.21px rgb(0 0 0/.12),0 3px 3px rgb(0 0 0/.14);
}
.btn-accent{ /* hot accent version */
  background:linear-gradient(#EA2B16,#FF3B26);color:#fff;border-radius:99px;
  box-shadow:inset 0 -3px 0 rgb(0 0 0/.18),inset 0 1px 0 rgb(255 255 255/.35),0 8px 20px -6px rgb(253 58 37/.55);
}
```

## 5. Sheen surfaces (cards)

*Why:* The same radial highlight at the top-left corner on every card makes the whole page feel lit by one consistent light source. Consistency of light direction is what reads as "designed".

```css
.card-sheen{border-radius:24px;padding:28px;
  background:radial-gradient(62.56% 62.56% at 28.14% -10.42%,rgb(255 255 255/.2),transparent),var(--surface);
  box-shadow:0 7.77px 16px rgb(0 0 0/.06),0 3px 3px rgb(0 0 0/.1),inset 0 -8px 0 rgb(0 0 0/.05),inset 0 4px 0 rgb(255 255 255/.6);}
.card-sheen.dark{background:radial-gradient(62.56% 62.56% at 28.14% -10.42%,rgb(255 255 255/.1),transparent),#18181B;color:#fff;
  box-shadow:0 7.77px 2.21px rgb(0 0 0/.06),0 3px 3px rgb(0 0 0/.1),inset 0 -8px 0 #111,inset 0 4px 0 rgb(255 255 255/.1);}
```
Dark-theme card (Ember): `background:var(--bg-2); border:1px solid var(--line); border-radius:20px;` plus an optional top hairline highlight `box-shadow: inset 0 1px 0 rgb(255 255 255/.06)`.

**Cursor spotlight on cards** (dark themes), a cheap way to add life:
```css
.spot{--x:50%;--y:50%;background:radial-gradient(400px circle at var(--x) var(--y),rgb(255 255 255/.06),transparent 40%),var(--bg-2)}
```
```js
document.querySelectorAll('.spot').forEach(c=>c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect();c.style.setProperty('--x',e.clientX-r.left+'px');c.style.setProperty('--y',e.clientY-r.top+'px')}));
```

## 6. Glass floating nav

*Why:* A detached, centered pill that floats over content feels like an app, not a website. Glass only works when something colorful passes under it, so keep the hero glow behind it.

```css
.nav{position:fixed;top:20px;left:50%;translate:-50% 0;z-index:50;width:min(1200px,calc(100% - 32px));
  display:flex;align-items:center;justify-content:space-between;padding:10px 12px 10px 20px;border-radius:16px;
  background:rgb(255 255 255/.05);backdrop-filter:blur(25px);-webkit-backdrop-filter:blur(25px);
  border:1px solid rgb(255 255 255/.08)}
.nav.light{background:rgb(255 255 255/.5);backdrop-filter:blur(44px);border-radius:999px;border:0}
.nav a{font-size:14px;color:rgb(255 255 255/.7);transition:color .2s}.nav a:hover{color:#fff}
.nav.scrolled{background:rgb(13 16 23/.7)}  /* toggle with a scroll listener after ~40px */
```
Active link in light nav: accent color + a 1px underline offset 6px.

## 7. Hairline grid & column guides

*Why:* Visible structure lines (Adon, OptimAI's faint verticals) make a page feel engineered. They cost nothing and instantly elevate a plain layout.

```css
.frame{border-inline:1px solid var(--line);max-width:1440px;margin-inline:auto}
.cells{display:grid;grid-template-columns:1fr 1fr}
.cells>*{border-bottom:1px solid var(--line);padding:32px}
.cells>*+*{border-left:1px solid var(--line)}
/* faint column guides on a dark hero */
.guides{position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(90deg,transparent 0 calc(25% - 1px),rgb(255 255 255/.04) calc(25% - 1px) 25%);
  mask-image:linear-gradient(to bottom,#000 30%,transparent)}
```

## 8. Display type

*Why:* Large type at default tracking looks loose and amateur. Tightening by 3–7% makes words read as shapes, the way a logo does. Dimming half the headline creates a reading order.

```css
.display{font-family:var(--font-display);font-weight:400;font-size:clamp(44px,6.5vw,96px);line-height:1.05;letter-spacing:-.05em;text-wrap:balance}
.display .dim{color:rgb(255 255 255/.5)}                 /* Ember: "Automate <span class=dim>smarter,</span> grow faster." */
.display-metal{background:linear-gradient(132deg,#43484D 11%,#292C2E 79%);-webkit-background-clip:text;background-clip:text;color:transparent}
.display-fade{background:linear-gradient(180deg,#fff 30%,rgb(255 255 255/.35));-webkit-background-clip:text;background-clip:text;color:transparent}
.eyebrow-num{font:500 13px/1 "IBM Plex Mono",monospace;letter-spacing:.04em;text-transform:uppercase;color:rgb(255 255 255/.5)}
```
Letter-spacing guide: 48px → −0.04em, 64px → −0.05em, 96px → −0.03 to −0.05em, 140px → −0.07em. Body text stays at 0.

## 9. Scroll-fill text

*Why:* Text that "inks in" as you scroll rewards reading and paces the page. Adon does it with a hard-stop gradient clipped to text, so it's crisp per line, not a blurry fade.

```css
.fill-text{font-size:clamp(36px,6vw,90px);line-height:.95;letter-spacing:-.05em}
.fill-text .line{
  background:linear-gradient(to right,var(--ink) 50%,var(--dim) 50%);
  background-size:200% 100%;background-position:100% 0;
  -webkit-background-clip:text;background-clip:text;color:transparent;display:inline}
```
```js
// split into lines first (SplitText type:"lines", linesClass:"line"), then:
gsap.utils.toArray('.fill-text .line').forEach(l=>gsap.to(l,{backgroundPosition:'0% 0',ease:'none',
  scrollTrigger:{trigger:l,start:'top 85%',end:'bottom 45%',scrub:true}}));
```
On dark: `--ink:#fff; --dim:rgb(255 255 255/.2)`.

## 10. Product proof

*Why:* Every top SaaS template puts the actual product in the hero. Buyers trust what they can see. Build it in HTML so it's crisp and can be animated.

**Browser frame with edge glow, fading into the page:**
```html
<div class="mock-wrap">
  <div class="mock">
    <div class="mock-bar"><i></i><i></i><i></i><span class="mock-url">🔒 app.yourproduct.com</span></div>
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
Animate it in with a slight 3D tilt: `gsap.from('.mock',{rotateX:18,y:80,opacity:0,duration:1.4,ease:'power3.out',transformPerspective:1200})`.

**Prompt-box hero** (AI tools): rounded-full input (`background:var(--bg-2)` + rainbow border stack from §2 at reduced opacity), icons for voice/attach, a white circular send button, and under it a row of ghost dropdown chips (`Model ▾  Deep Search ▾  Think ▾  Edit Image ▾`) with 1px `--line` borders. Above it, a row of ✓ capability checks ("Text to Image · Photo to Text · …") at 60% opacity.

## 11. Bento grid with mini-UIs

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
Mini-UI ideas (build each in ~10–20 lines of HTML): workflow nodes connected by a dashed SVG path with a dot traveling along it (`offset-path`), chat bubbles typing, toggle switches flipping on a loop, a sparkline drawing itself (SVG `stroke-dashoffset`), color chips, a "Process → Sync → Grow" pill flow, a notification stack, a code snippet with a blinking cursor, a radial progress ring. Give the mini-UI its own muted panel (`background:rgb(255 255 255/.03); border:1px solid var(--line); border-radius:12px`).

Highlighted card among equals (e.g. 1 of 4 services): `background:linear-gradient(160deg,#3B5BFF,#1C2A8C)`, others stay neutral.

## 12. Eyebrow badges & avatar stack

```html
<div class="proof"><div class="avatars"><img …><img …><img …><img …></div><p>Rated 4.9/5 by<br>7,000+ users</p></div>
<span class="pill-eyebrow"><svg class="spark">…</svg> AI-Driven Agency</span>
```
```css
.avatars{display:flex}.avatars img{width:36px;height:36px;border-radius:50%;box-shadow:0 0 0 1.5px var(--bg-0);margin-left:-10px}.avatars img:first-child{margin-left:0}
.proof{display:inline-flex;align-items:center;gap:10px;font-size:13px;line-height:1.3;text-align:left}
.pill-eyebrow{display:inline-flex;gap:6px;align-items:center;padding:6px 12px;border-radius:8px;font-size:13px;color:var(--accent);
  background:#fff;box-shadow:inset 0 -2px 0 #ececec,0 1px 2px rgb(0 0 0/.08)}
.pill-eyebrow.dark{background:rgb(255 255 255/.05);border:1px solid var(--line);color:rgb(255 255 255/.8);backdrop-filter:blur(10px)}
```

## 13. Marquees with masked edges

```css
.marquee{overflow:hidden;mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.marquee-track{display:flex;gap:64px;width:max-content;animation:marquee 40s linear infinite}
.marquee:hover .marquee-track{animation-play-state:paused}
@keyframes marquee{to{transform:translateX(-50%)}}   /* duplicate the items once inside the track */
.logo{height:28px;opacity:.5;filter:grayscale(1);transition:opacity .3s}.logo:hover{opacity:1}
```
Vertical testimonial columns: same idea with `flex-direction:column` and `translateY(-50%)`, two or three columns at different speeds (30s/40s/35s), the middle one reversed.
Big-type marquee (Noir): "Selected Work ◎ Selected Work ◎" at 120px, 500 weight, with an inline SVG wireframe globe as separator.

## 14. Backgrounds

```css
.dots{background-image:radial-gradient(rgb(255 255 255/.12) 1px,transparent 1px);background-size:24px 24px;
  mask-image:radial-gradient(ellipse at center,#000 30%,transparent 75%)}
.grid-bg{background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:64px 64px;
  mask-image:radial-gradient(ellipse 60% 50% at 50% 0%,#000,transparent)}
.noise::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.06;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.spotlight-band{background:radial-gradient(60% 120% at 50% 100%,#3F7BFF 0%,#1B3A8F 40%,var(--bg-0) 75%)}  /* integrations strip */
```
Noise on top of glows removes gradient banding and adds a film-like richness. Use it on dark heroes.
Dot-matrix globe: a `<canvas>` drawing points on a sphere (lat/long loop, project with simple orthographic math, rotate slowly), or a pre-made SVG. Put it at the bottom of a dark card, half cropped.

## 15. Outline-over-photo hero word

```html
<div class="name-hero">
  <h1 class="word">DAVIES</h1>
  <img class="portrait" src="…bw portrait…" alt="">
  <h1 class="word outline" aria-hidden="true">DAVIES</h1>
</div>
```
```css
.name-hero{position:relative;display:grid;place-items:center}
.name-hero>*{grid-area:1/1}
.word{font-size:clamp(80px,21vw,300px);font-weight:500;line-height:.8;color:#fff;letter-spacing:-.02em}
.portrait{width:28%;aspect-ratio:3/4;object-fit:cover;filter:grayscale(1) contrast(1.1)}
.word.outline{color:transparent;-webkit-text-stroke:1px #fff;
  clip-path:inset(0 36% 0 36%)}   /* match the portrait's horizontal span */
```
Add the accent block after the word: `<span class="caret"></span>` with `width:.35em;height:.08em;background:var(--accent);animation:blink 1s steps(1) infinite`.

## 16. Framed hero with notch tab

```css
.hero-frame{margin:12px;border-radius:40px;overflow:hidden;position:relative;min-height:calc(100svh - 24px);
  background:radial-gradient(120% 80% at 70% 30%,#fff 0%,#E4E4E7 60%,#D4D4D8 100%)}
.notch{position:absolute;bottom:0;left:50%;translate:-50% 0;padding:14px 48px 12px;background:var(--page);
  border-radius:24px 24px 0 0;font-size:14px}
.notch::before,.notch::after{content:"";position:absolute;bottom:0;width:24px;height:24px;
  background:radial-gradient(circle at 0 0,transparent 23.5px,var(--page) 24px)}
.notch::before{left:-24px}
.notch::after{right:-24px;transform:scaleX(-1)}
```
The inverse-radius corners make the tab look *cut* into the frame. Put a 3D render (glossy ribbon, glass shape, chrome object) bleeding off the right side of the frame.

**Inline pill in headline** with bobbing icons: `<span class="h-pill"><img …><img …><img …></span>` with `display:inline-block;width:2.2em;height:.8em;border-radius:999px;background:var(--accent-grad);vertical-align:middle;position:relative` and the icons absolutely positioned, rotated ±12°, white rounded squares with shadow, `animation:bob 3s ease-in-out infinite` with staggered delays.

## 17. Pricing highlight

```css
.price-card{border-radius:24px;padding:32px;background:var(--bg-2);border:1px solid var(--line)}
.price-card.featured{position:relative;background:linear-gradient(var(--bg-2),var(--bg-2)) padding-box,
  linear-gradient(160deg,var(--accent),transparent 60%) border-box;border:1px solid transparent;
  box-shadow:0 30px 80px -20px color-mix(in oklab,var(--accent) 45%,transparent);translate:0 -12px}
.price{font-size:56px;letter-spacing:-.04em}.price small{font-size:16px;color:rgb(255 255 255/.5)}
```
Use NumberFlow or a GSAP tween for the monthly/yearly switch so digits roll instead of snapping.

## 18. Footer wordmark

A huge brand name spanning the full width at the very bottom (`font-size:20vw; line-height:.8; letter-spacing:-.06em`), partially cropped by `overflow:hidden`, filled with a vertical fade (`linear-gradient(#fff 0%, transparent 90%)` clipped to text, or `--line` color on light themes). It ends the page with a signature instead of a list of links.
