# Typography: display type and scroll-fill text

## Display type: tight tracking, dimmed half, metallic gradient

*Why:* Large type at default tracking looks loose and amateur. Tightening by 3–7% makes words read as shapes, the way a logo does. Dimming half the headline creates a reading order.

```css
.display{font-family:var(--font-display);font-weight:400;font-size:clamp(44px,6.5vw,96px);line-height:1.05;letter-spacing:-.05em;text-wrap:balance}
.display .dim{color:rgb(255 255 255/.5)}                 /* "Automate <span class=dim>smarter,</span> grow faster." */
.display-metal{background:linear-gradient(132deg,#43484D 11%,#292C2E 79%);-webkit-background-clip:text;background-clip:text;color:transparent}
.display-fade{background:linear-gradient(180deg,#fff 30%,rgb(255 255 255/.35));-webkit-background-clip:text;background-clip:text;color:transparent}
.eyebrow-num{font:500 13px/1 "IBM Plex Mono",monospace;letter-spacing:.04em;text-transform:uppercase;color:rgb(255 255 255/.5)}
```
Letter-spacing guide: 48px → −0.04em, 64px → −0.05em, 96px → −0.03 to −0.05em, 140px → −0.07em. Body text stays at 0.

If the headline is split with SplitText, put the gradient on the split pieces, not the parent (see Gotchas in `shared/motion.md`).

## Scroll-fill text

*Why:* Text that "inks in" as you scroll rewards reading and paces the page. Adon does it with a hard-stop gradient clipped to text, so it's crisp per line, not a blurry fade.

```css
.fill-text{font-size:clamp(36px,6vw,90px);line-height:.95;letter-spacing:-.05em}
.fill-text .line{
  background:linear-gradient(to right,var(--ink) 50%,var(--dim) 50%);
  background-size:200% 100%;background-position:100% 0;
  -webkit-background-clip:text;background-clip:text;color:transparent;display:inline}
```
```js
// split into lines (SplitText, autoSplit so it re-measures on resize), then ONE sequential timeline per block:
gsap.utils.toArray('.fill-text').forEach(el => SplitText.create(el, {
  type: 'lines', linesClass: 'line', autoSplit: true,
  onSplit: self => {
    const tl = gsap.timeline({ defaults: { ease: 'none' },
      scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 40%', scrub: 0.5 } });
    self.lines.forEach(l => tl.to(l, { backgroundPosition: '0% 0', duration: 1 }));  // equal slices, one after another
    return tl;
  }
}));
```
**Strictly line by line, never several at once.** Do NOT give each line its own ScrollTrigger: neighbouring lines are only one line-height apart, so their start/end ranges overlap and two or three lines fill simultaneously, which reads as a muddy wave instead of reading. One trigger on the whole block + a timeline of back-to-back tweens (`duration:1`, no overlap, no position offsets) guarantees line N is fully inked before line N+1 begins. `scrub:0.5` adds a little inertia so the fill glides instead of tracking the scrollbar 1:1. For a longer block, give the trigger more scroll distance (`end:'bottom 30%'` or `+=` a multiple of the block height) so each line has room to breathe. Weight each line's `duration` by its character count if line lengths vary a lot, so the fill speed stays constant.

Optional soft leading edge (still one line at a time): `background:linear-gradient(to right,var(--ink) 45%,var(--dim) 55%)`, so the ink edge feathers instead of cutting hard.

On dark: `--ink:#fff; --dim:rgb(255 255 255/.2)`.


## Serif italic display (tight)

*Why:* A high-contrast italic serif at very tight tracking and a sub-1 line-height gives a cinematic, editorial voice, a good counterweight to a light sans body.
```css
.display-serif{font-family:"Instrument Serif",serif;font-style:italic;font-weight:400;
  font-size:clamp(56px,8vw,88px);line-height:.8;letter-spacing:-.045em;text-wrap:balance}
```
Pair with Barlow 300/400 for body (`font-weight:300; line-height:1.25`). Tight tracking plus `line-height:.8` needs room: add padding-bottom so descenders are not clipped by a mask reveal.

## Stacked drop-title

*Why:* Four copies of one word, each a different color and nudged down a few pixels, make a retro layered shadow with zero images. Works for one big word per page.
```html
<h1 class="stack" aria-label="BEYOND"><span aria-hidden="true">BEYOND</span><span aria-hidden="true">BEYOND</span><span aria-hidden="true">BEYOND</span><span aria-hidden="true">BEYOND</span></h1>
```
```css
.stack{position:relative;font-size:clamp(7.5rem,30vw,28rem);line-height:.85;letter-spacing:-.02em}
.stack span{position:absolute;inset:0;display:block;text-align:center}
.stack span:nth-child(1){color:#89CFF0;transform:translateY(36px)}   /* back */
.stack span:nth-child(2){color:var(--bg);transform:translateY(24px)} /* gap = page color */
.stack span:nth-child(3){color:#90EE90;transform:translateY(12px)}
.stack span:nth-child(4){position:relative;color:#fff}               /* front, sizes the box */
@media (max-width:767px){.stack span:nth-child(1){transform:translateY(18px)}.stack span:nth-child(2){transform:translateY(12px)}.stack span:nth-child(3){transform:translateY(6px)}}
```
This is the one place a multi-color palette is deliberate; keep the rest of the page to the neutrals plus one accent. Put a cut-out subject in front (higher `z-index`) to add depth.
