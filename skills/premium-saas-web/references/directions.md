# Directions: full token sets

Each direction gives tokens measured from a real top-selling template. Swap the accent hue to fit the brand; keep the *structure* (how many neutrals, which opacities, which radii) intact. That structure is what makes it work.

## Contents
1. Ember Dark (OptimAI)
2. Tactile Light (Aigocy)
3. Editorial Mono (Adon)
4. Noir Spotlight (Davies)
5. Swapping the accent

---

## 1. Ember Dark

**Why it works:** A near-black *blue-tinted* base (not pure #000) makes warm glows look like they're emitting light. The glow is carved into shape, so it reads as a light source, not a gradient. Text is one white at different opacities, so the page feels calm despite the fire.

```css
:root{
  --bg-0:#0D1017;   /* page base (section bg) */
  --bg-1:#11141D;   /* alt section */
  --bg-2:#191D2A;   /* cards, inputs, nav pill fill */
  --bg-3:#252A32;   /* raised chips, hover */
  --light-0:#F8F9FA; --light-1:#F1F4F6; --light-2:#E4EAEE; /* light sections */
  --line: rgb(148 163 184 / .18);   /* hairline borders (slate-ish) */
  --line-strong: rgb(148 163 184 / .32);
  --fg: #fff;  /* use with opacity: 1 / .9 / .8 / .6 / .5 */
  --accent:#FF7300; --accent-deep:#5E1818; --glow:#FF0000; /* orange/red ember */
  /* blue variant: --accent:#5A9FFF; --glow:#2F6BFF; */
  --rainbow: #30E3FF,#8765FF,#FFF181,#FF4C52,#734CFF;
}
```
- **Fonts:** Sora 400 for display (64px, −0.05em, lh 1.2); Inter Tight for body; IBM Plex Mono 500 16px for *button labels and tags*. The mono buttons are a signature: they read "technical" without trying.
- **Radii:** 6px buttons, 12px inputs/chips, 20px cards, 28px big panels, 999px pills/avatars.
- **Signature pieces:** sculpted red/orange hero glow, prompt-box hero (input + model/think/search dropdown chips), rainbow-border primary button with blurred rainbow under-glow, avatar stack + rating eyebrow, AI-model logo arc (center logo enlarged, glow behind), tilted image cards on an arc, browser-frame mockup with neon edge glow, bento with corner light leaks, integration logos on a blue radial spotlight band, dark/light section alternation.
- **Light sections:** `--light-0` bg, cards white with 1px `rgb(16 24 40 / .08)` border and `0 1px 4px rgb(16 24 40 / .1)` shadow; dark CTA buttons inside them keep the rainbow glow.

## 2. Tactile Light

**Why it works:** Everything looks physically pressable: a lit top edge, a darker bottom lip and a soft multi-layer shadow mimic real objects under a softbox. A single hot red against zinc grays is confident and expensive. The hero sits in an inset rounded "frame", like a product on a plinth.

```css
:root{
  --page:#EDECEC;       /* body behind the framed hero */
  --surface:#F4F4F5;    /* zinc-100: sections, cards */
  --surface-2:#FAFAFA;
  --ink:#09090B;        /* zinc-950 */
  --ink-2:#3F3F46; --ink-3:#52525B; --ink-4:#A1A1AA;
  --line:#D4D4D8;       /* zinc-300 */
  --dark-card:#272727; --dark-card-2:#18181B;
  --accent:#FD3A25; --accent-grad: linear-gradient(#EA2B16,#FF3B26);
  --heading-grad: linear-gradient(132deg,#43484D 11%,#292C2E 79%);
}
```
- **Fonts:** Urbanist (display 96px/600, −0.03em, lh 1.0; body 16–18px).
- **Radii:** 99px buttons/pills, 40px big cards & framed hero, 24px cards, 16/12/8 inner.
- **Signature pieces:** framed hero (`margin:12px; border-radius:40px; overflow:hidden`) with a 3D abstract render (glossy ribbon/glass) bleeding off one side; floating glass nav pill (white/50, blur 44px); eyebrow pill with accent icon; headline with an *inline pill shape* in accent color carrying 2–3 floating app icons (gently bobbing); tactile dark primary + tactile light secondary buttons; "Scroll for more" notch tab cut into the bottom of the hero frame; dark sheen card next to light sheen card; giant pale number (e.g. "120+" in zinc-300) as decoration; dot-matrix globe; grayscale logo marquee.
- **Headline gradient:** apply `--heading-grad` with `background-clip:text` on the strong line; the second line uses a lighter variant (`#9a9a9a → #d4d4d8`) so it fades away.

## 3. Editorial Mono

**Why it works:** Confidence through subtraction. Two colors, one huge grotesk, no shadows at all. The *hairline grid* (visible 1px column/row lines) makes the layout feel architected. Scroll-scrubbed text fill turns reading into an interaction.

```css
:root{
  --bg:#F0F0F0; --bg-2:#FFFFFF;
  --ink:#111111; --ink-body:#555555; --ink-mute:#999999;
  --line: rgb(17 17 17 / .10); --line-2: rgb(17 17 17 / .20);
  --dim: rgb(17 17 17 / .30);   /* un-filled scroll text, dimmed words */
}
```
- **Fonts:** a neo-grotesk for display (BDO Grotesk in the original; free near-matches: "Inter Tight", "Schibsted Grotesk", "Hanken Grotesk") at weight 400 (not bold!), DM Sans for body.
- **Type scale:** hero 140px / lh 120px / −0.07em (−9.8px); section 90px / lh 85px / −0.05em; small labels 14–16px, often in parentheses like "(2017)" or "(Click to play reel)".
- **Radii:** 20px media, 30px big media, 500px pills. **No box-shadows anywhere.**
- **Signature pieces:** layout framed by 1px vertical lines at the page edges and between header cells; nav as a plain vertical list inside a bordered cell; a dimmed word inside the hero headline ("marketing" at 30%); scroll-fill paragraphs at 90px; black progress bars of varying heights with % labels; big stats ("130+") in display type; showreel thumbnail with play circle; mix-blend-mode: exclusion custom cursor.

## 4. Noir Spotlight

**Why it works:** Pure black + one neon accent gives maximum contrast and a nightlife/tech feel. The giant name interacting with a photo (solid behind, outline in front) creates depth with zero 3D. Motion (shader ripple, marquee, stacking cards) does the heavy lifting.

```css
:root{
  --bg:#000; --bg-2:#0A0A0A; --card:#111; --card-2:#191919;
  --fg:#fff; --fg-2:rgb(255 255 255 / .6); --line: rgb(255 255 255 / .1);
  --accent:#07C42C;   /* neon green; alternatives: #D4FF3A lime, #2AC6F8 cyan */
}
```
- **Fonts:** Figtree (or Outfit) 500–600; hero word 260–300px, uppercase, tracking ~0; small caps nav at 11–12px with +0.04em tracking.
- **Signature pieces:** preloader with accent-colored vertical bars wiping away; hero = huge wordmark + B/W portrait in the middle, letters solid outside the photo and *outlined* (`-webkit-text-stroke:1px #fff; color:transparent`) where they cross it, achieved with two stacked copies, the front one clipped to the photo's rect; an accent block as a blinking "_" cursor after the name; brand names with a trailing underscore ("Nexbot_"); WebGL ripple/water background (Unicorn Studio embed, or a CSS/SVG turbulence fallback); "Selected Work ◎ Selected Work" marquee with a wireframe globe glyph; full-width project cards that *stack* (sticky) as you scroll; white pill CTA.

## 5. Swapping the accent

Keep lightness/chroma similar to the original and use OKLCH to rotate hue:
- Ember: orange `oklch(70% .2 50)` → blue `oklch(68% .17 255)` → violet `oklch(62% .22 295)` → green `oklch(75% .2 150)`.
- Always regenerate the *glow* color as a more saturated, darker sibling of the accent (glows look best at very high chroma because blur dilutes them).
- Re-check contrast of any text placed on the accent.
