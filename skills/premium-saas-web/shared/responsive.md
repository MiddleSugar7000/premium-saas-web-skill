# Responsive principles

Beyond "one column under 768px". Pick the trigger that actually governs each decision instead of one catch-all breakpoint.

## Four independent switches

1. **Input device** decides touch accommodations (burger menu, bigger hit areas, disabling hover/cursor effects):
   ```css
   @media (pointer:coarse), (max-width:999px){ .burger{display:grid} .nav-links{display:none} }
   @media (hover:hover) and (pointer:fine){ .cursor{display:block} }
   ```
   Viewport width cannot tell you what is pointing at the screen: a laptop with OS display scaling reports 1070px wide and still has a mouse.
2. **Aspect ratio** decides composition (side-by-side vs stacked), not width. A 1100×1000 window and a 1100×600 window need different hero layouts:
   ```css
   @media (max-aspect-ratio:13/10){ .hero{flex-direction:column} }
   ```
3. **Width** decides type size and grid columns (`clamp()` plus a column collapse).
4. **Height** decides vertical rhythm. Short landscape phones need the hero copy moved and shrunk: `@media (max-height:520px) and (orientation:landscape)`.

Keep these as separate media queries. Merging them makes every fix break another case.

## Fluid hero unit (one-screen heroes only)

For a hero that must be exactly one screen and never scroll or collide, scale everything from a reference frame:
```css
html{ font-size:min(calc(100vw / 1440), calc(100vh / 900)); }  /* 1rem = 1 reference px */
@supports (height:100dvh){ html{ font-size:min(calc(100vw / 1440), calc(100dvh / 900)); } }
.title{ font-size:96rem; top:200rem; }
```
Because the unit takes the smaller of the two ratios, the layout is a uniform scale or the reference pulled apart, never compressed. Do not use this for long pages.

## Redraw, don't shrink

Below about 520px, do not keep scaling the desktop frame down (body copy ends up at 13px, tap targets at 22px). Switch to a second, phone-sized frame and use literal `px` for tap targets (min 44px).

## Mobile checklist

- Display type via `clamp()`; headlines wrap to 2–3 lines and never cross the focal point of an image.
- Big blurs and glows shrink; cursor effects off; marquees keep running.
- Test 390×844, 320×568 and a short landscape phone.
