# Known pitfalls and robustness

These only show up in a real browser, so read this before handing over. Each one has cost a rebuild somewhere.

## CSS and layout

1. **Inline `left`/`width`/`transform` beat your state classes.** If JS sets `el.style.left`, a later `.collapsed{left:…}` rule never wins. Drive moving parts through CSS custom properties (`style.setProperty('--cap-left', …)`) and let the stylesheet read them.
2. **`position:fixed` inside a transformed parent is not fixed to the viewport.** Any ancestor with `transform`, `filter`, `perspective` or `backdrop-filter` becomes the containing block, so `top:57%` resolves against that ancestor. Offset from the ancestor instead, or move the element out.
3. **A transformed wrapper relocates absolutely positioned children.** If you animate a group, give the wrapper the same box as the stage (`position:absolute; inset:0`) for the duration of the animation.
4. **`100vh` is wrong on phones.** Use `height:100vh; height:100dvh;` (the second line wins where supported). Add `env(safe-area-inset-top)` to fixed headers.
5. **Overlay layers must not eat clicks.** Decorative layers (glows, grain, videos, hero copy wrappers) get `pointer-events:none`; re-enable it on the interactive children.
6. **Never crossfade two different states of the same scene.** It produces a muddy double image. Swap with `visibility`, or fade through the page background.
7. **Backdrop-filter is expensive.** Keep it on small surfaces (nav, chips, a controller), never on a full-screen layer. Always write `-webkit-backdrop-filter` next to it.

## State and async

8. **Lock input synchronously.** Set the "busy" flag and disable the buttons in the same tick as the click, before any `await`, or a double click starts two transitions.
9. **Guard every async callback with a token.** Capture `const token = ++current` when a transition starts; every timeout, event listener and promise continuation first checks `token === current` and returns if stale.
10. **Do not defer a CSS transition with `setTimeout`.** It races against early exits. Add both classes in the same style recalc and let `transition-delay` do the waiting.
11. **A timeout is not success.** If you wait for something to load or decode and give up after N seconds, show the error state. Never report the new state as reached.
12. **Pause timers while `document.hidden`.** Frame callbacks, rAF and media events freeze in background tabs; a naive deadline fires a false error.
13. **Never leave the UI permanently locked.** Every failure path releases the lock, keeps the last valid visual, and offers a retry.

## Accessibility that gets forgotten

14. **Disabling the focused button drops focus to `<body>`.** Remember whether it had focus before disabling, then `focus({preventScroll:true})` the element that replaces it.
15. **Hidden controls leave the tab order**: `tabindex="-1"` plus `aria-hidden="true"` (or `inert`) together, not just `opacity:0`.
16. **Announce state changes** (loading, done, error) in a visually hidden `aria-live="polite"` region.
17. **`prefers-reduced-motion`**: skip entrances, parallax and autoplay; drop blur filters; keep one-shot state changes working with ~1ms transitions.

## Progressive enhancement

18. **No JS must not mean a blank page.** Initial "hidden" states for entrance animations live behind an attribute that a tiny inline script in `<head>` sets (`<html data-anim>`). Without the script nothing is hidden. Add a 3–4 s safety timeout that removes the attribute if the animation never starts.
19. **Wait for fonts before measuring or splitting text** (`document.fonts.ready`). Split text with `autoSplit` so it re-measures on resize.
20. **Skip animating `display:none` elements.** The tween never paints and the final frame resolves late.

## Before you hand over: acceptance pass

- Open the page, load it at 1440×900 and 390×844, and screenshot both.
- Click every interactive element once, then twice quickly. Nothing queues, nothing strands an empty state.
- Tab through the page; every control shows a visible focus ring and focus never lands on a hidden element.
- Turn on reduced motion; the page is complete and usable.
- Resize through 1920, 1280, 768, 390, 320: nothing clips, overlaps or scrolls sideways.
