---
name: premium-saas-web
description: Build premium, ThemeForest-top-seller-grade websites for SaaS, AI products, agencies, startups and tech portfolios — sculpted color glows, animated gradient borders, tactile glossy buttons, glass navs, bento grids with mini product UIs, giant tight-tracked headlines, scroll-scrubbed text reveals, smooth scroll and GSAP motion. Use this skill whenever the user asks for a landing page, homepage, marketing site, pricing page, waitlist page, product page or portfolio for a SaaS / AI / tech / agency / startup brand, or says things like "make it look premium / expensive / modern / like a top template", "Vercel/Linear/Framer style", "dark glowing hero", "glassmorphism" — in any language, and even if they don't name a style. Also use it when redesigning an existing tech/SaaS page to look higher-end.
license: MIT
metadata:
  author: MiddleSugar7000
  homepage: https://github.com/MiddleSugar7000/premium-saas-web-skill
  version: "1.0.0"
---

# Premium SaaS Web

This skill encodes what makes the best-selling SaaS/AI/agency templates feel expensive. It was distilled by inspecting five reference sites at the CSS level (OptimAI, Aigocy, Adon, Davies, an AI image generator demo) and measuring the actual values they use. The recipes in `references/` are the real techniques, not guesses.

## The core insight: premium = controlled light + restraint + motion

Cheap pages and premium pages often use the *same* components (hero, logos, features, pricing, FAQ, CTA). The difference is in four layers of finish:

1. **Light** — surfaces look lit, not filled. Glows are sculpted from blurred shapes; cards have a top-left sheen; buttons have an inner highlight and an inner bottom edge; borders are hairlines at 6–20% opacity. Real light falls off, so nothing is a flat block of color.
2. **Restraint** — one accent color, used on ≤5% of the page. Text hierarchy comes from *opacity of one color* (100 / 80 / 60 / 50%), not from many grays. Two fonts max (+ an optional mono for labels). Zero decoration that doesn't carry meaning.
3. **Typography with tension** — display type is big and *tightly tracked* (letter-spacing −2% to −7%), line-height ≈ 1.0–1.2. Half of a headline is often dimmed (`opacity .5` or a lighter gradient) so the eye reads the strong half first.
4. **Motion with weight** — smooth scroll (Lenis), headlines that rise word-by-word, text that fills as you scroll, counters that roll, marquees that never stop, cards that stack. Everything eases out (no linear), nothing bounces, and it all respects `prefers-reduced-motion`.

If an output only has the components but not these four layers, it will look like a free Bootstrap theme no matter how many sections it has.

## Workflow

### 1. Read the brief, pick ONE direction

Choose a direction from `references/directions.md` (read it now — it has full token sets). Summary:

| Direction | Feel | Best for | Source |
|---|---|---|---|
| **Ember Dark** | Deep navy-black, sculpted orange/red or blue glow, rainbow-border CTA, mono button labels | AI tools, dev tools, SaaS apps | OptimAI |
| **Tactile Light** | Zinc/off-white, glossy skeuomorphic buttons, sheen cards, one hot accent (red), framed hero with 3D render | AI agencies, B2B SaaS, consultancies | Aigocy |
| **Editorial Mono** | Pure #111 on #F0F0F0, 140px grotesk at −7% tracking, hairline grid, scroll-fill text, no shadows | Agencies, studios, premium services | Adon |
| **Noir Spotlight** | Black, one neon accent, giant word interacting with a photo, shader/WebGL bg, stacking project cards | Personal brands, portfolios, creative tech | Davies |

If the user didn't specify and it's SaaS/AI, default to **Ember Dark**. Mixing directions is how pages get muddy. Borrowing one *technique* from another direction is fine, as long as the palette and type stay coherent.

Tell the user in one line which direction you picked and why, so they can redirect early.

### 2. Plan the page as a rhythm, not a list

Premium pages alternate density and tone. A typical SaaS home that works:

1. **Hero**: eyebrow badge (avatar stack + "Rated 4.9 by 7,000+ users" or a pill like "✦ AI-Driven Agency"), 2-line headline with a dimmed half, 1–2 line subcopy at 60% opacity, primary + secondary CTA, then **the product itself** (browser-framed mockup or an interactive prompt box) bleeding into the next section via a gradient fade.
2. **Logo strip**: grayscale logos, infinite marquee, masked edges.
3. **Bento feature grid**: 5–7 cells of unequal size, each with a *mini UI illustration* built in HTML/CSS (workflow nodes, chat bubbles, toggles, charts, color chips), not stock icons.
4. **Scroll-fill statement**: one big sentence that fills from 30% → 100% as you scroll.
5. **Numbers**: 3–4 stats with rolling counters; one giant faded number as decoration.
6. **How it works / tabs** or **stacking cards**.
7. **Testimonials**: real-feeling quotes, avatar + name + role, maybe a vertical marquee of cards.
8. **Pricing**: 3 tiers, middle one lifted with the accent border/glow, monthly/yearly toggle.
9. **FAQ** accordion.
10. **Final CTA** with the strongest glow on the page, then a calm footer with a huge wordmark.

Alternate dark/light (or bg-1/bg-2) section backgrounds to create rhythm. Section padding is generous: 120–176px vertical on desktop.

### 3. Build with the recipes

Read `references/recipes.md` and use the techniques that fit the direction. They are copy-ready CSS/HTML. Key ones:

- **Sculpted glow** (color blobs + same-as-bg "eraser" blobs, both blurred 80–140px)
- **Animated rainbow border** (3-layer background with `padding-box`/`border-box` clip, 400% size, 15s loop) + blurred under-glow
- **Tactile button** (inset bottom edge + inset top highlight + 5-step layered shadow)
- **Sheen card** (radial highlight at 28% −10% over a solid fill)
- **Glass nav** (floating pill, `backdrop-filter: blur(20–44px)`, white/5–50%)
- **Hairline grid** (1px rgba lines, 10% opacity, visible column guides)
- **Scroll-fill text** (`background-clip:text` + hard-stop 50/50 gradient, background-position scrubbed)
- **Browser-frame mockup** fading into the page
- **Bento mini-UIs**, **marquees with masked edges**, **dot/grid backgrounds**, **noise overlay**

Read `references/motion.md` for the GSAP + Lenis setup (all GSAP plugins incl. SplitText are free since 3.13 — load from jsDelivr).

### 4. Tech defaults

- Single-file HTML with Tailwind CDN (or the project's existing stack — follow it if there is one). Put design tokens in CSS custom properties on `:root` so a palette swap is one edit.
- Fonts from Google Fonts. Proven pairings from the references: **Sora + Inter Tight + IBM Plex Mono** (Ember), **Urbanist** (Tactile), **a grotesk like "Inter Tight"/"Schibsted Grotesk"/"Familjen Grotesk" + DM Sans** (Editorial), **Figtree/"Outfit"** (Noir).
- Icons: inline SVG (Lucide-style 1.5px stroke). Never emoji as icons.
- Images: if image generation is available, generate on-brand 3D renders / abstract objects; otherwise build visuals with CSS/SVG (glows, mini UIs, dot globes). Use `https://images.unsplash.com/...` photos only for people/portraits. A page with no visual anchor in the hero looks unfinished.
- Mobile: everything collapses to one column at <768px; display type scales with `clamp()`; glows shrink (big blurs are expensive on phones); disable cursor effects on touch.

### 5. Self-review before handing over

Open the page in a browser and screenshot at 1440px and 390px, if you can. Check against this list. These are the things that separate "AI-generated" from "top seller":

- [ ] Only one accent hue (plus neutrals). Gradients stay inside that hue family, except an intentional rainbow border.
- [ ] Display headline has negative letter-spacing and a dimmed half or gradient.
- [ ] Body/secondary text uses opacity steps of one color, and contrast still passes (≥4.5:1 for body).
- [ ] Hero shows the product (mockup, prompt box, UI), not just text over a gradient.
- [ ] At least one sculpted light source per dark section; no flat rectangles of pure color.
- [ ] Borders are hairlines (1px, 6–20% alpha), radii are consistent (pick a scale: 8/12/20/28/999).
- [ ] Buttons have hover states that change *light* (glow tightens, sheen shifts, arrow nudges 2–4px), not just color.
- [ ] Motion: hero text reveal, scroll-triggered fades with stagger, at least one scrubbed effect, marquee. All disabled under `prefers-reduced-motion`.
- [ ] No lorem ipsum. Copy is specific to the product: concrete numbers, real-sounding features.
- [ ] Nothing overflows horizontally at 390px.

## What to avoid (the "cheap template" tells)

- Purple-to-blue gradient on everything; multiple competing accent colors.
- Drop shadows like `0 4px 6px rgba(0,0,0,.3)` on dark backgrounds (shadows don't read on dark; use glows and borders instead).
- Centered everything with identical card grids of 3 icons + title + text.
- Glassmorphism without anything behind the glass to blur.
- Bouncy/elastic easing, fade-ins that take >1s, animations on every element at once.
- Gradient text on body copy; more than one gradient-text phrase per viewport.
- Stock "AI brain" imagery. Show the product or an abstract render instead.
