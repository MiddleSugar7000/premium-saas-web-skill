---
name: premium-saas-web
description: Build premium, ThemeForest-top-seller-grade websites for SaaS, AI products, agencies, startups and tech portfolios — sculpted color glows, animated gradient borders, tactile glossy buttons, glass navs, bento grids with mini product UIs, giant tight-tracked headlines, scroll-scrubbed text reveals, smooth scroll and GSAP motion. Use this skill whenever the user asks for a landing page, homepage, marketing site, pricing page, waitlist page, product page or portfolio for a SaaS / AI / tech / agency / startup brand, or says things like "make it look premium / expensive / modern / like a top template", "Vercel/Linear/Framer style", "dark glowing hero", "glassmorphism" — in any language, and even if they don't name a style. Also use it when redesigning an existing tech/SaaS page to look higher-end.
---

# Premium SaaS Web

This skill encodes what makes the best-selling SaaS/AI/agency templates feel expensive. It was distilled by inspecting five reference sites at the CSS level (OptimAI, Aigocy, Adon, Davies, an AI image generator demo) and measuring the actual values they use. The recipes are the real techniques, not guesses.

**File layout.** Load only what the task needs:
- `directions/<name>/style.md`: one file per visual direction (tokens, fonts, signature pieces, techniques only that direction uses). Read **only the one you pick**.
- `shared/*.md`: techniques every direction uses, split by topic. Read the ones for the sections you are building (map in step 3).

## The core insight: premium = controlled light + restraint + motion

Cheap pages and premium pages often use the *same* components (hero, logos, features, pricing, FAQ, CTA). The difference is in four layers of finish:

1. **Light** — surfaces look lit, not filled. Glows are sculpted from blurred shapes; cards have a top-left sheen; buttons have an inner highlight and an inner bottom edge; borders are hairlines at 6–20% opacity. Real light falls off, so nothing is a flat block of color.
2. **Restraint** — one accent color, used on ≤5% of the page. Text hierarchy comes from *opacity of one color* (100 / 80 / 60 / 50%), not from many grays. Two fonts max (+ an optional mono for labels). Zero decoration that doesn't carry meaning.
3. **Typography with tension** — display type is big and *tightly tracked* (letter-spacing −2% to −7%), line-height ≈ 1.0–1.2. Half of a headline is often dimmed (`opacity .5` or a lighter gradient) so the eye reads the strong half first.
4. **Motion with weight** — smooth scroll (Lenis), headlines that rise word-by-word, text that fills as you scroll, counters that roll, marquees that never stop, cards that stack. Everything eases out (no linear), nothing bounces, and it all respects `prefers-reduced-motion`.

If an output only has the components but not these four layers, it will look like a free Bootstrap theme no matter how many sections it has.

## Workflow

### 1. Read the brief, pick ONE direction

Choose a direction from this table, then read its `directions/<folder>/style.md` (full token set + its signature techniques). Don't read the other directions.

| Direction (folder) | Feel | Best for | Source |
|---|---|---|---|
| **Ember Dark** (`ember-dark`) | Deep navy-black, sculpted orange/red or blue glow, rainbow-border CTA, mono button labels | AI tools, dev tools, SaaS apps | OptimAI |
| **Tactile Light** (`tactile-light`) | Zinc/off-white, glossy skeuomorphic buttons, sheen cards, one hot accent (red), framed hero with 3D render | AI agencies, B2B SaaS, consultancies | Aigocy |
| **Editorial Mono** (`editorial-mono`) | Pure #111 on #F0F0F0, 140px grotesk at −7% tracking, hairline grid, scroll-fill text, no shadows | Agencies, studios, premium services | Adon |
| **Noir Spotlight** (`noir-spotlight`) | Black, one neon accent, giant word interacting with a photo, shader/WebGL bg, stacking project cards | Personal brands, portfolios, creative tech | Davies |
| **Cinematic Glass** (`cinematic-glass`) | Black, drifting CSS aurora (or a supplied video), near-invisible glass chips with a lit edge, tight italic serif headline | Design/dev studios, agencies, creative AI | Dark studio sites |

If the user didn't specify and it's SaaS/AI, default to **Ember Dark**. Mixing directions is how pages get muddy. Borrowing one *technique* from another direction is fine, as long as the palette and type stay coherent.

Tell the user in one line which direction you picked and why, so they can redirect early. If the brand needs a different accent hue, see "Swapping the accent" in `directions/README.md`.

### 2. Plan the page as a rhythm, not a list

**Match the brief's size.** If the user asks for a single hero, a one-screen page or "only X", build exactly that and do not add logo strips, stats, cards or footers. Adding sections nobody asked for is the most common way to ruin a tight brief.

**Hero visual, in this order of preference** (the page must look finished at every level, because most users supply no media):
1. **Product UI in HTML/CSS** (mockup, prompt box, dashboard tiles). Default for SaaS and AI products.
2. **CSS/SVG visual**: sculpted glow or aurora, mini UIs, grain, dot globe, a large typographic composition (`shared/light.md`, `shared/product-proof.md`, `shared/typography.md`).
3. **User-supplied image or video**, only if the user provided one: layer it over the CSS visual, never in place of it (`shared/video.md`). Never invent URLs, hotlink third-party assets you were not given, or leave a broken placeholder.

Premium pages alternate density and tone. A typical SaaS home that works:

1. **Hero**: eyebrow badge (avatar stack + "Rated 4.9 by 7,000+ users" or a pill like "✦ AI-Driven Agency"), 2-line headline with a dimmed half, 1–2 line subcopy at 60% opacity, primary + secondary CTA, then **the product itself** (browser-framed mockup or an interactive prompt box) bleeding into the next section via a gradient fade.
2. **Logo strip**: grayscale logos, infinite marquee, masked edges.
3. **Bento feature grid**: 5–7 cells of unequal size, each with a *mini UI illustration* built in HTML/CSS (workflow nodes, chat bubbles, toggles, charts, color chips), not stock icons.
4. **Scroll-fill statement**: one big sentence that fills from 30% → 100% as you scroll. The fill runs strictly line by line (one scrubbed timeline per block, lines back-to-back), never several lines at once. See `shared/typography.md`.
5. **Numbers**: 3–4 stats with rolling counters; one giant faded number as decoration.
6. **How it works / tabs** or **stacking cards**.
7. **Testimonials**: real-feeling quotes, avatar + name + role, maybe a vertical marquee of cards.
8. **Pricing**: 3 tiers, middle one lifted with the accent border/glow, monthly/yearly toggle.
9. **FAQ** accordion.
10. **Final CTA** with the strongest glow on the page, then a calm footer with a huge wordmark.

Alternate dark/light (or bg-1/bg-2) section backgrounds to create rhythm. Section padding is generous: 120–176px vertical on desktop.

### 3. Build with the recipes

The recipes are copy-ready CSS/HTML/JS. Your direction's `style.md` already holds its signature techniques (e.g. rainbow border for Ember, tactile buttons and sheen cards for Tactile). For everything else, read the shared file that matches what you are building:

| Building… | Read |
|---|---|
| Hero light, glows, dot/grid/noise backgrounds, hairline grid & column guides | `shared/light.md` |
| Headlines (tight tracking, dimmed half, metallic gradient), scroll-fill statement | `shared/typography.md` |
| Product mockup in the hero, bento grid with mini-UIs | `shared/product-proof.md` |
| Glass nav, eyebrow badge & avatar stack, card spotlight, marquees, pricing, footer wordmark | `shared/components.md` |
| Any named brand with an icon (integrations, logo strip, orbit, "works with") | `shared/logos.md` |
| GSAP + Lenis boilerplate, reveals, counters, stacking cards, pinned scroll, hover, blur-in words, safe entrance, gotchas | `shared/motion.md` |
| Glass surfaces (gradient-stroke border), stacked drop-title, serif italic display | `shared/components.md`, `shared/typography.md` |
| Breakpoint strategy, mobile layouts, one-screen fluid hero | `shared/responsive.md` |
| A video the **user supplied** (backdrop, click clips, scrub, cut-out) | `shared/video.md` (skip entirely if there is no video) |
| Before handing over: browser-only traps, accessibility, acceptance pass | `shared/pitfalls.md` |

A full landing page usually needs all of them; a single section or a small edit needs only its row. All GSAP plugins incl. SplitText are free since 3.13, load them from jsDelivr.

### 4. Tech defaults

- Single-file HTML with Tailwind CDN (or the project's existing stack — follow it if there is one). Put design tokens in CSS custom properties on `:root` so a palette swap is one edit.
- Fonts from Google Fonts. Proven pairings from the references: **Sora + Inter Tight + IBM Plex Mono** (Ember), **Urbanist** (Tactile), **a grotesk like "Inter Tight"/"Schibsted Grotesk"/"Familjen Grotesk" + DM Sans** (Editorial), **Figtree/"Outfit"** (Noir).
- Icons: inline SVG (Lucide-style 1.5px stroke). Never emoji as icons.
- Images: if image generation is available, generate on-brand 3D renders / abstract objects; otherwise build visuals with CSS/SVG (glows, mini UIs, dot globes). Use `https://images.unsplash.com/...` photos only for people/portraits. A page with no visual anchor in the hero looks unfinished.
- **Real brand logos, never letter placeholders.** Whenever the page names an existing company, product or SaaS (integration chips, logo arcs/strips, "works with" bands, testimonials, comparison tables) and you show an icon next to it, use that brand's actual logo. A colored square with the initial ("F" for Figma, "S" for Slack) reads as a cheap template and breaks trust. Details and sources in `shared/logos.md`. If no real logo can be sourced, show the name as plain text with no icon at all; a fake icon is worse than none.
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
- [ ] Every real brand named on the page has its real logo (or no icon). No initial-letter squares.
- [ ] No lorem ipsum. Copy is specific to the product: concrete numbers, real-sounding features.
- [ ] Nothing overflows horizontally at 390px.
- [ ] Looks finished with zero images or videos: no broken media, no empty frames, no invented URLs.
- [ ] Ran the acceptance pass in `shared/pitfalls.md` (double-click, keyboard focus, reduced motion, no-JS, 320px).

## What to avoid (the "cheap template" tells)

- Purple-to-blue gradient on everything; multiple competing accent colors.
- Drop shadows like `0 4px 6px rgba(0,0,0,.3)` on dark backgrounds (shadows don't read on dark; use glows and borders instead).
- Centered everything with identical card grids of 3 icons + title + text.
- Glassmorphism without anything behind the glass to blur.
- Fake brand icons: a colored rounded square with a letter standing in for Figma, Slack, GitHub, etc.
- Bouncy/elastic easing, fade-ins that take >1s, animations on every element at once.
- Gradient text on body copy; more than one gradient-text phrase per viewport.
- Stock "AI brain" imagery. Show the product or an abstract render instead.
