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

*Why:* Text that "inks in" as you scroll rewards reading and paces the page. The premium version is a **soft opacity wave**: every word fades from dim to full ink on its own, and the next words are already starting while the previous ones finish, so the page *darkens* along the reading line instead of flipping from white to black. A hard per-line wipe or an instant color swap looks like a progress bar; the overlapping fade looks like ink soaking in.

```css
.fill-text{font-size:clamp(36px,6vw,90px);line-height:.98;letter-spacing:-.05em;color:var(--ink)}
.fill-text .w{display:inline-block;opacity:.18}   /* dim = opacity, so it works on any background, light or dark */
```
```js
// SplitText into words (autoSplit re-measures on resize), then ONE scrubbed timeline per block:
gsap.utils.toArray('.fill-text').forEach(el => SplitText.create(el, {
  type: 'words', wordsClass: 'w', autoSplit: true,
  onSplit: self => {
    const wave = 5;   // how many words are mid-fade at once: 3 = tight, 8 = dreamy
    return gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 35%', scrub: 0.6 } })
      .to(self.words, { opacity: 1, ease: 'sine.inOut', duration: wave, stagger: 1 });  // stagger 1 + duration `wave` = overlapping fades
  }
}));
```
*How the wave works:* each word's tween lasts `wave` units and the next word starts 1 unit later, so about `wave` words are at different stages of fading at any moment: the one at the front is barely lit, the one at the back is nearly ink. Because words fade in reading order, the wave still travels strictly left to right, line after line (no word on line 2 lights up before line 1 is done). `sine.inOut` on each word makes the fade ease in and out instead of ramping linearly; `scrub:0.6` adds inertia so it glides with the Lenis scroll rather than tracking the scrollbar 1:1.

Tuning: dimmer start (`.12`) = more drama, brighter start (`.3`) = calmer. Long block? Give the trigger more scroll distance (`end:'bottom 25%'`, or `+=` a multiple of the block height) so each word has time to fade. Playful extra, only for short statements (< ~40 words): `.fromTo(words,{opacity:.18,y:'.15em'},{opacity:1,y:0,…})`; avoid animating `filter:blur` on every word, it repaints every frame.

Don't do the old way: a hard-stop gradient wipe per line (`linear-gradient(to right,ink 50%,dim 50%)` + `background-position`) or a per-line ScrollTrigger. Hard stops read as a loading bar, and per-line triggers overlap (lines are one line-height apart) so two or three lines fill at once like a muddy wave.

Under `prefers-reduced-motion` the split never runs, so the text simply stays at full ink (the `.w` class only exists after splitting, which is why the dim opacity is on `.w`, not on `.fill-text`).
