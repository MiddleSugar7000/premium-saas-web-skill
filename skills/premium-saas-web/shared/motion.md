# Motion: GSAP + Lenis setup

All five reference sites use GSAP + ScrollTrigger + SplitText. Three of them also use a smooth-scroll layer (Lenis or ScrollSmoother). Since GSAP 3.13 every plugin, including SplitText, is free and on the public CDN.

## Principles (why motion feels premium)
- **Ease out, never linear** (except scrubbed and infinite loops). `power3.out` / `expo.out` for entrances, `power2.inOut` for state changes.
- **Short distances, longer durations.** Move 24–60px over 0.8–1.2s. Big moves look cheap.
- **Stagger is the luxury.** 0.04–0.08s between words/cards creates a cascade that reads as craft.
- **One hero moment.** The headline reveal + product mockup entrance are the most choreographed thing on the page; everything else is a quiet fade-up.
- **Respect `prefers-reduced-motion`.** Skip all of it, show final states.

## Boilerplate

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/SplitText.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js"></script>
<script>
gsap.registerPlugin(ScrollTrigger, SplitText);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reduce) {
  // Smooth scroll, synced with ScrollTrigger
  const lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}

document.fonts.ready.then(() => { if (!reduce) initMotion(); });

function initMotion() {
  // 1. Hero headline: words rise from below a mask, slight 3D tilt
  const h = SplitText.create('.hero h1', { type: 'words,lines', mask: 'lines' });
  gsap.from(h.words, { yPercent: 110, rotateX: -40, opacity: 0, transformOrigin: '50% 100%',
    duration: 1.1, ease: 'expo.out', stagger: 0.06, delay: 0.15 });
  gsap.from('.hero [data-fade]', { y: 24, opacity: 0, duration: 0.9, ease: 'power3.out', stagger: 0.08, delay: 0.5 });
  gsap.from('.mock', { y: 80, rotateX: 18, opacity: 0, transformPerspective: 1200, duration: 1.4, ease: 'power3.out', delay: 0.7 });

  // 2. Generic reveal: any [data-reveal] container fades its children up with stagger
  gsap.utils.toArray('[data-reveal]').forEach(group => {
    gsap.from(group.children, { y: 40, opacity: 0, duration: 0.9, ease: 'power3.out', stagger: 0.08,
      scrollTrigger: { trigger: group, start: 'top 82%' } });
  });

  // 3. Section headings: line-by-line mask reveal
  gsap.utils.toArray('[data-split]').forEach(el => {
    const s = SplitText.create(el, { type: 'lines', mask: 'lines' });
    gsap.from(s.lines, { yPercent: 100, duration: 1, ease: 'expo.out', stagger: 0.1,
      scrollTrigger: { trigger: el, start: 'top 85%' } });
  });

  // 4. Scroll-fill text: ONE trigger + sequential timeline, lines fill strictly one after another.
  //    (A ScrollTrigger per line overlaps and fills several lines at once - don't.) CSS in shared/typography.md.
  gsap.utils.toArray('.fill-text').forEach(el => SplitText.create(el, {
    type: 'lines', linesClass: 'line', autoSplit: true,
    onSplit: self => {
      const tl = gsap.timeline({ defaults: { ease: 'none' },
        scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 40%', scrub: 0.5 } });
      self.lines.forEach(l => tl.to(l, { backgroundPosition: '0% 0', duration: 1 }));
      return tl;
    }
  }));

  // 5. Counters
  gsap.utils.toArray('[data-count]').forEach(el => {
    const end = +el.dataset.count, suffix = el.dataset.suffix || '';
    const o = { v: 0 };
    gsap.to(o, { v: end, duration: 2, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 85%' },
      onUpdate: () => el.textContent = Math.round(o.v).toLocaleString() + suffix });
  });

  // 6. Parallax for decorative layers
  gsap.utils.toArray('[data-speed]').forEach(el => {
    gsap.to(el, { yPercent: -20 * +el.dataset.speed, ease: 'none',
      scrollTrigger: { trigger: el.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });
}
</script>
```

## Gotchas found in testing
- **Gradient text + SplitText:** `background-clip:text` on the parent stops working once SplitText wraps words/lines in their own elements, and the headline turns invisible. Apply the gradient to the split pieces instead (`wordsClass:'w'` + `.display-metal .w{background:inherit;-webkit-background-clip:text;background-clip:text;color:transparent}`), or use a plain color for split headlines. Scroll-fill text (`shared/typography.md`) already applies its gradient per line for this reason.
- **SplitText lines + responsive:** lines are measured once. Create splits with `autoSplit:true` and build the animation in `onSplit(self){ return gsap.from(self.lines, …) }` so they re-measure on resize; otherwise headings break one word per line after a width change.
- **Dimming stacked cards:** use `filter:brightness()`, never `opacity`, or the card underneath bleeds through.

## Signature sequences

**Stacking cards** (Davies projects, "how it works" steps):
```css
.stack-card{position:sticky;top:96px}  /* each card; give each a slightly larger top: 96px, 112px, 128px for a peek effect */
```
```js
gsap.utils.toArray('.stack-card').forEach((card, i, all) => {
  if (i === all.length - 1) return;
  // dim with brightness, NOT opacity: a semi-transparent card lets the next card's text bleed through
  // fromTo with an explicit brightness(1): tweening from the default `filter:none`, GSAP starts at brightness(0),
  // so the card snaps to near-black the moment the trigger starts.
  gsap.fromTo(card, { scale: 1, filter: 'brightness(1)' },
    { scale: 0.95, filter: 'brightness(0.7)', ease: 'power1.in',
      scrollTrigger: { trigger: all[i + 1], start: 'top 45%', end: 'top 96px', scrub: true } });
});
```
**Always tween `filter` with `fromTo` (or set `filter:'brightness(1)'` in CSS).** From `none`, GSAP interpolates from `brightness(0)`: the card goes black instantly and then *lightens* toward the target. This is the main reason stacked cards "go dark way too early".

**Don't dim too early or too hard.** The card being covered is still the one the visitor is reading. Starting the dim at `start:'top bottom'` (the moment the next card peeks in at the bottom of the screen) with `brightness(.45)` turns it dark almost as soon as it pins, so its text becomes unreadable mid-read. Start only once the next card has covered roughly half the viewport (`top 45%`), stop at its pinned top, keep brightness ≥ .65, and use an ease-in so most of the darkening happens in the last stretch, when the card is already mostly hidden.

**Pinned horizontal scroll** (features or case studies):
```js
const track = document.querySelector('.h-track');
gsap.to(track, { x: () => -(track.scrollWidth - innerWidth + 64), ease: 'none',
  scrollTrigger: { trigger: '.h-pin', pin: true, scrub: 1, end: () => '+=' + track.scrollWidth, invalidateOnRefresh: true } });
```

**Traveling dot on a connector** (bento workflow): SVG path + `<circle>` with CSS `offset-path: path('…'); animation: travel 3s linear infinite;` `@keyframes travel{to{offset-distance:100%}}`.

**Self-drawing line/sparkline**: `stroke-dasharray: L; stroke-dashoffset: L;` → animate to 0 on enter.

Direction-specific motion lives with its direction: logo arc in `directions/ember-dark/`, preloader and custom cursor in `directions/noir-spotlight/` (cursor also in `editorial-mono/`).

## Hover micro-interactions
- Buttons: arrow `translateX(3px)`, glow blur tightens (14→10px), tactile buttons sink 1px on `:active`.
- Cards: `translateY(-4px)` + border alpha 0.18 → 0.32 + cursor spotlight. 300ms `cubic-bezier(.2,.8,.2,1)`.
- Links: underline grows from left (`background-size: 0 1px → 100% 1px`).
- Images in cards: `scale(1.04)` over 700ms inside an `overflow:hidden` wrapper.

## Performance
- Animate only `transform` and `opacity` (and `background-position` for the fill effect).
- Big `filter: blur()` blobs are expensive. Keep them static or drift them slowly; add `will-change: transform` only to things that actually move.
- On mobile (`max-width: 768px`): halve blur radii, disable magnetic/cursor effects, keep reveals.
- Call `ScrollTrigger.refresh()` after images load if layout shifts.


## Blur-in words

*Why:* Words that sharpen out of a blur as they rise read as focus pulling, softer and more cinematic than a plain fade-up.
```js
const s = SplitText.create('[data-blurin]', { type: 'words' });
gsap.from(s.words, { filter: 'blur(10px)', opacity: 0, y: 50, duration: 0.7, ease: 'power3.out',
  stagger: 0.1, scrollTrigger: { trigger: '[data-blurin]', start: 'top 85%' } });
```
Add `display:inline-block` to the words (SplitText does this) and use it on one headline per section, not on body copy.

## Sticky stage with scroll-progress

*Why:* A section taller than the viewport with a sticky inner stage lets scroll drive a small choreography (words sliding in, opacity rising) without any pinning plugin.
```html
<section class="stage-wrap" style="height:120vh"><div class="stage" style="position:sticky;top:0;height:100vh">…</div></section>
```
```js
const wrap = document.querySelector('.stage-wrap'), words = [...document.querySelectorAll('[data-slide]')];
const k = innerWidth < 768 ? .5 : 1;
function tick(){ const r = wrap.getBoundingClientRect();
  const p = Math.min(1, Math.max(0, -r.top / (wrap.offsetHeight - innerHeight)));
  words.forEach((w, i) => { const dir = w.dataset.slide === 'l' ? -1 : 1;
    w.style.transform = `translateX(${dir * (60 + i * 40) * k * (1 - p)}px)`; w.style.opacity = .35 + p * .65; }); }
addEventListener('scroll', tick, { passive: true }); addEventListener('resize', tick); tick();
```

## Entrance with a safety net

*Why:* A hidden-until-animated page is a blank page if the script fails. Gate the hidden state behind an attribute that an inline script sets, and remove it on a timer if the animation never completes.
```html
<script>(function(){var d=document.documentElement;if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  d.setAttribute('data-anim','pending');window.__guard=setTimeout(function(){d.removeAttribute('data-anim')},4000);})();</script>
```
```css
html[data-anim="pending"] .hero [data-in]{opacity:0;translate:0 12px}
```
Start the timeline after `document.fonts.ready` (and after any media you wait for), then `clearTimeout(window.__guard)` and remove the attribute when it finishes. Skip elements whose computed `display` is `none`. No script means no attribute means nothing hidden. See `shared/pitfalls.md`.
