# Components: nav, badges, cards, marquees, pricing, footer

## Glass floating nav

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

## Eyebrow badges & avatar stack

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

## Cursor spotlight on cards (dark themes)

A cheap way to add life:
```css
.spot{--x:50%;--y:50%;background:radial-gradient(400px circle at var(--x) var(--y),rgb(255 255 255/.06),transparent 40%),var(--bg-2)}
```
```js
document.querySelectorAll('.spot').forEach(c=>c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect();c.style.setProperty('--x',e.clientX-r.left+'px');c.style.setProperty('--y',e.clientY-r.top+'px')}));
```

## Marquees with masked edges

```css
.marquee{overflow:hidden;mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.marquee-track{display:flex;gap:64px;width:max-content;animation:marquee 40s linear infinite}
.marquee:hover .marquee-track{animation-play-state:paused}
@keyframes marquee{to{transform:translateX(-50%)}}   /* duplicate the items once inside the track */
```
Logo strips use real brand logos, desaturated until hover (`shared/logos.md`).
Vertical testimonial columns: same idea with `flex-direction:column` and `translateY(-50%)`, two or three columns at different speeds (30s/40s/35s), the middle one reversed.

## Pricing highlight

```css
.price-card{border-radius:24px;padding:32px;background:var(--bg-2);border:1px solid var(--line)}
.price-card.featured{position:relative;background:linear-gradient(var(--bg-2),var(--bg-2)) padding-box,
  linear-gradient(160deg,var(--accent),transparent 60%) border-box;border:1px solid transparent;
  box-shadow:0 30px 80px -20px color-mix(in oklab,var(--accent) 45%,transparent);translate:0 -12px}
.price{font-size:56px;letter-spacing:-.04em}.price small{font-size:16px;color:rgb(255 255 255/.5)}
```
Use NumberFlow or a GSAP tween for the monthly/yearly switch so digits roll instead of snapping.

## Footer wordmark

A huge brand name spanning the full width at the very bottom (`font-size:20vw; line-height:.8; letter-spacing:-.06em`), partially cropped by `overflow:hidden`, filled with a vertical fade (`linear-gradient(#fff 0%, transparent 90%)` clipped to text, or `--line` color on light themes). It ends the page with a signature instead of a list of links.


## Liquid glass (gradient-stroke border)

*Why:* A glass surface reads as expensive when its edge catches light: a 1px stroke that is bright at the top and bottom and invisible at the sides, with a near-transparent fill. The stroke is drawn with a masked pseudo-element so it can be a gradient, which `border` cannot do. Needs something colorful or moving behind it to blur.

```css
.glass{position:relative;overflow:hidden;background:rgb(255 255 255/.01);background-blend-mode:luminosity;
  backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);box-shadow:inset 0 1px 1px rgb(255 255 255/.1)}
.glass::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.4px;pointer-events:none;
  background:linear-gradient(180deg,rgb(255 255 255/.45) 0%,rgb(255 255 255/.15) 20%,transparent 40%,transparent 60%,rgb(255 255 255/.15) 80%,rgb(255 255 255/.45) 100%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;
  mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);mask-composite:exclude}
.glass-strong{backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);box-shadow:4px 4px 4px rgb(0 0 0/.05),inset 0 1px 1px rgb(255 255 255/.15)}
```
Use `.glass` for chips, nav pills and cards, `.glass-strong` for the one primary CTA. Nest a smaller `.glass` square for icon wells inside cards.

Variant with a moving highlight (controllers, toggles): add a radial layer to `::after` whose origin follows the pointer through `--glass-x/--glass-y`, set from a `pointermove` listener (no re-render, no layout work), and a conic-gradient edge accent at 25-30% opacity (`#7fe3ff, white, #ffd7e6`) for a hint of dispersion. Keep it an accent, never a rainbow fill, and keep `backdrop-filter` local to small elements.
