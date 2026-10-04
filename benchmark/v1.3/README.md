# Benchmark v1.3: skill 1.2.0 vs 1.3.0

What changed in 1.3.0, and whether it helped. This is a small, cheap A/B check (3 prompts), not a replacement for the larger with-skill vs without-skill benchmark in [`../README.md`](../README.md).

## What 1.3.0 adds

| Addition | Where |
|---|---|
| Three.js shader background, particle field and bloom, with CSS fallback, mobile gate, DPR cap and visibility pause | [`shared/webgl.md`](../../skills/premium-saas-web/shared/webgl.md) |
| Timing & easing table (hover 120-180 ms, reveals 0.8-1.0 s, ...) | `shared/motion.md` |
| `gsap.matchMedia()` pattern for reduced motion and mobile | `shared/motion.md` |
| GSAP gotchas: `containerAnimation` ease, one ScrollTrigger per timeline, `immediateRender`, SplitText masks clipping accents | `shared/motion.md` |
| Native CSS scroll-driven motion, `@starting-style`, view transitions (progressive enhancement) | `shared/motion.md` |
| Accent-safe hero type (Á, Ő, Ű): line-height and mask rules | `directions/noir-spotlight/style.md` |
| Two new checklist items (motion via matchMedia + timing table, WebGL safeguards) | `SKILL.md` |

Ideas came from the Three.js, GSAP, motion-design and genjutsu skills; only techniques that fit this skill's look were taken.

## Method

- **Prompts (3):** Flowpilot (Ember Dark, SaaS), Bence Kovács portfolio (Noir Spotlight; this prompt adds "dark, moody look with a WebGL shader background in the hero" so the WebGL recipe is actually exercised), Clipnest (Warm Playful, control that must not get worse).
- **Configurations:** skill 1.2.0 (snapshot) vs 1.3.0, one run each, then a second run of 1.3.0 after two fixes found in round 1 (see below). Subagents ran on Claude Sonnet, each reading only its own skill folder. These are not the isolated `claude -p` runs of the main benchmark.
- **Scoring:** [`check_motion.py`](check_motion.py) (Playwright, no model calls) counts what the skill's checklist forbids: no reduced-motion handling, `transition: all`, `scale(0)`, width/height tweens, console errors, mobile overflow, CSS loops running under reduced motion, a hidden h1 under reduced motion, and for WebGL pages: no visibility pause, no DPR cap, no mobile/low-core gate, no `try/catch`, blank canvas. Visual comparison was done by eye from 1440 px hero screenshots.

## Results

| Prompt | Skill | Issues | Tokens | Time | Notes |
|---|---|---|---|---|---|
| Noir portfolio (WebGL) | 1.2.0 | **2** | 103,620 | 105 s | no mobile/low-core gate, no `try/catch` around WebGL |
| | 1.3.0 | **0** | 106,927 | 101 s | gate, fallback and visibility pause present |
| | 1.3.0 + fixes | **0** | 105,493 | 92 s | accents fixed (see below) |
| Flowpilot | 1.2.0 | 0 | 127,549 | 192 s | |
| | 1.3.0 | 0 | 125,308 | 161 s | |
| | 1.3.0 + fixes | 0 | 114,077 | 129 s | |
| Clipnest (control) | 1.2.0 | 0 | 113,899 | 130 s | |
| | 1.3.0 | 0 | 118,036 | 128 s | |
| | 1.3.0 + fixes | 0 | 121,535 | 149 s | |

Raw data: [`results.json`](results.json); per run `outputs/<prompt>/<round>-<version>/` holds `index.html`, `checks_motion.json` and `timing.json`.

## What the screenshots show

Hero shots are in [`screenshots/`](screenshots/): `*-v1.2.0`, `*-v1.3.0`, `*-v1.3.0-fixes`.

- **Noir:** 1.2.0 puts the A-acute of KOVÁCS into the line above (line-height .8 plus a clipping mask); 1.3.0 has the same flaw and a full-bleed shader with visible grain; 1.3.0 + fixes shows the accent intact and a localized light.
- **Flowpilot:** the 1.2.0 run invented a "4.9/5 by 2,400+ teams" rating with fake avatars and a 14-day trial; both 1.3.0 runs leave out ratings and counts. The 1.3.0 + fixes run still writes "Start free trial" and "No card to start", which the prompt did not provide.
- **Clipnest:** all three versions are close; no regression.

## Fixes made after round 1

1. **Accent clipping:** `noir-spotlight/style.md` now requires line-height of at least .92 for names with accented capitals and forbids masking such lines; `motion.md` has the matching SplitText gotcha.
2. **Shader grain and coverage:** `webgl.md` lowers the grain from .03 to .014 and asks to keep the lit area to about half of the hero.

## Caveats

- One run per cell: a difference of one or two issues is a signal, not a statistic. For example, the slowest transition on the Noir page was 0.3 s in the first 1.3.0 run and 0.9 s in the second, so the timing table does not guarantee short hover transitions.
- The metric counts what the checklist forbids; it says nothing about taste. The visual notes above are one reviewer's judgement.
- Headless screenshots can differ from a real browser (grain, GPU shader output, hotlinked icon images that failed to load in the Flowpilot captures).
- Round-2 runs were not repeated for 1.2.0.

## Reproduce

```bash
pip install playwright && playwright install chromium
python check_motion.py <iteration-dir> "eval-*/*/outputs/index.html"   # writes checks_motion.json per page, prints a table
```
