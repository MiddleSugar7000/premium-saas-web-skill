# Video (only when the user supplies it)

**Read this file only if the user gave you a video file or URL.** The skill never needs video: every page has a complete media-free version (`shared/light.md`, `shared/product-proof.md`). Never invent a video URL, never hotlink a third-party clip you were not given, and never leave a broken `<video>` placeholder. If no video was supplied, build the CSS background and stop reading.

## The slot pattern: CSS first, video on top

The CSS background is the real hero; the video is an enhancement that paints over it. If the video is slow, blocked, or the visitor is on a phone or data saver, the page still looks finished.

```html
<div class="bg">
  <div class="bg-css"></div>                 <!-- aurora / mesh / glow, always rendered -->
  <video class="bg-video" muted playsinline preload="auto" aria-hidden="true" src="USER_SUPPLIED.mp4"></video>
</div>
```
```css
.bg{position:absolute;inset:0;overflow:hidden;background:#000}
.bg-css,.bg-video{position:absolute;inset:0;width:100%;height:100%}
.bg-video{object-fit:cover;opacity:0;transition:opacity .6s ease}
.bg-video.on{opacity:1}
```
```js
const v = document.querySelector('.bg-video');
const lite = matchMedia('(prefers-reduced-motion: reduce)').matches
  || (navigator.connection && navigator.connection.saveData)
  || matchMedia('(max-width: 700px)').matches;
if (v && !lite) {
  v.addEventListener('loadeddata', () => { v.classList.add('on'); v.play().catch(() => v.classList.remove('on')); }, { once: true });
  v.addEventListener('error', () => v.classList.remove('on'));
} else if (v) v.remove();
```
Use only user-supplied sources. Remind the user to check they have the rights to the footage and to keep it short and compressed (a few MB).

## Seamless loop

The browser's own `loop` flashes at the seam. Fade the video out for the last half second and restart it:
```js
v.removeAttribute('loop');
v.addEventListener('timeupdate', () => { if (v.duration - v.currentTime < 0.55) v.style.opacity = 0; });
v.addEventListener('ended', () => { v.currentTime = 0; v.play(); v.style.opacity = 1; });
```

## Click-driven clips (state transitions)

When a click plays a pre-made clip (A to B, then reverse):
- One persistent `<video>` per clip with a fixed `src`; never swap `src` on a visible element.
- Keep the previous frame visible while the next clip starts; reveal it only once a decoded frame of the new clip exists (`requestVideoFrameCallback` where available, with a `playing` + double rAF fallback). A timeout never counts as "decoded".
- Switch layers with `visibility`, not an opacity crossfade between two scene states.
- Stop slightly before the end (`duration - 0.08s`) and hold that frame; do not rely on `ended` alone.
- Lock input synchronously, token-guard every callback, release the lock exactly once (see `shared/pitfalls.md`).

## Pointer-scrubbed clip

A clip that never plays by itself and is turned by horizontal mouse travel:
```js
const SENS = 0.8, EPS = 0.04; let prevX = null, target = 0, seeking = false, asked = -1;
const dur = () => (isFinite(v.duration) && v.duration > 0 ? v.duration : 0);
function pump(){ if (seeking || Math.abs(target - v.currentTime) < EPS) return; seeking = true; asked = target; try { v.currentTime = target; } catch(e){ seeking = false; } }
v.addEventListener('seeked', () => { seeking = false; if (target !== asked) pump(); });   // compare with what was ASKED, not where the decoder landed
addEventListener('mousemove', e => { const d = dur(); if (prevX === null || !d) { prevX = e.clientX; return; }
  target = Math.min(d, Math.max(0, target + ((prevX - e.clientX) / innerWidth) * SENS * d)); prevX = e.clientX; pump(); }, { passive: true });
['mouseleave','blur'].forEach(t => addEventListener(t, () => prevX = null));
v.pause(); v.addEventListener('loadeddata', () => { target = v.currentTime; if (!v.currentTime) v.currentTime = 0.001; }, { once: true });   // paint a first frame
```
Only one seek may be in flight; the `seeked` event issues the next. Keep this in its own block so it still runs under reduced motion where entrance code returns early (reduced motion: `v.pause()` and stop; touch: autoplay loop instead). Encode scrub clips with a short keyframe interval (`ffmpeg -i in.mp4 -c:v libx264 -g 6 -bf 0 -movflags +faststart -an out.mp4`) or every seek decodes from frame 0.

## Blending a video into the page (cut-out look)

For a figure on a plain light background, make the rectangle disappear:
```css
.cutout{position:relative;overflow:hidden;background:var(--bg);
  -webkit-mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent),linear-gradient(to bottom,transparent,#000 9%);
  -webkit-mask-composite:source-in;
  mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent),linear-gradient(to bottom,transparent,#000 9%);
  mask-composite:intersect}
.cutout video{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply;filter:brightness(1.18) saturate(1.2)}
```
The video's backdrop must be light and even; `brightness` pushes it to white so `multiply` resolves it to the page color. It does not work on dark or busy footage.

## Verify

Screenshot after 6-10 s: the subject is visible, not cropped, not covered by the headline, and the page ground matches the video's edges. Test once with the video blocked: the CSS layer must look finished on its own.
