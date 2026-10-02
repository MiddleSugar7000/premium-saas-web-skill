# Benchmark: premium-saas-web vs plain Claude

**Model:** Claude Opus 5.5 (`claude-opus-5-5`) · **Date:** 2026-10-01 · **Runs:** 4 prompts × 2 configurations

## Method

- **Prompts**: four one-line requests with no style instructions, written the way a normal person types them. They were in Hungarian (`prompt_used` in [`evals.json`](evals.json)); English translations are next to them. The generated pages were therefore in Hungarian. The demo pages in `docs/demos/` were translated to English afterwards (text only, using the pair lists in [`i18n/`](i18n/) and `i18n/apply.py`), nothing was re-generated, and the scores below come from the original Hungarian pages. Two names were anglicized in the translated pages: Számlakör is shown as Billcircle and Bence Kovács as Ben Kovacs.
- **Isolation**: each run is a separate `claude -p` process in its own empty folder, which is its own git repo, outside any directory with Claude memory. Neither configuration sees memory, other skills or conversation history. Transcripts were checked afterwards to confirm this.
- **With skill**: the prompt is prefixed with `/premium-saas-web`.
- **Without skill**: the identical prompt, with the `Skill` tool disabled (`--disallowedTools Skill`).
- **Scoring**: [`grade.py`](grade.py) runs 10 mechanical checks on each `index.html`: design tokens on `:root`, negative display tracking, a large-blur light source, hairline borders with alpha, scroll-driven motion, `prefers-reduced-motion`, an infinite marquee, responsive breakpoints, no lorem ipsum, and no emoji icons. Visual quality is judged from the screenshots and live pages in the [demo](https://middlesugar7000.github.io/premium-saas-web-skill/).

## Results

| Prompt | With skill | Without skill |
|---|---|---|
| Flowpilot (AI automation SaaS) | 10/10 | 7/10 |
| Northlane (AI consulting) | 10/10 | 8/10 |
| UX/UI designer portfolio | 9/10 | 8/10 |
| Billcircle / Számlakör (invoicing SaaS) | 10/10 | 7/10 |
| **Pass rate** | **97.5%** | **75%** |

| Mean per page | With skill | Without skill |
|---|---|---|
| Wall time | 644 s | 137 s |
| API cost | $2.66 | $0.72 |
| Agent turns | ~30 | ~2 |

Per-run details are in [`results/`](results/) (`grading.json` lists every check with pass/fail; `timing.json` has duration, tokens and cost).

## Reproduce

```bash
# needs: claude CLI, Python 3, playwright (for screenshots)
bash run_isolated.sh iteration-1        # 8 isolated generations
python grade.py iteration-1             # writes grading.json per run
python shoot.py iteration-1 8791        # full-page screenshots (serve iteration-1 on :8791 first)
```

Set `PSW_ISO_DIR` to a folder outside any git repo where you use Claude memory.

## Limitations

- Four prompts, one run each, so this is a smoke test, not a statistically strong study.
- Mechanical checks reward techniques the skill teaches; they can't measure taste. Look at the pages.
- The skill-built pages tend to share one long section skeleton (bento → statement → stats → steps → testimonials → pricing → FAQ). Making page structure adapt to page type is on the roadmap.

## Robustness checks (`check_robust.py`)

`grade.py` is regex-only and tops out at 10/10, so it cannot see browser-level problems. `check_robust.py` adds 10 checks that load the page in Chrome (Playwright): no `<video>` or empty `<img>` (no invented media), `dvh` next to `100vh`, `:focus-visible`, `-webkit-backdrop-filter`, no sideways overflow at 390 and 320 px, no JavaScript exceptions, no broken images, and almost no invisible text with JavaScript off or with reduced motion on. For single-hero prompts it also checks that the page has at most one `<section>`, no `<footer>` and is about one screen tall.

```bash
python check_robust.py --demos --json robust-baseline.json   # the before/after demo pages
python check_robust.py path/to/index.html --hero-only
```

Baseline on the demo pages (generated with the first version of the skill, 2026-10-01): with skill 9/10, 10/10, 10/10, 10/10; without skill 5/10, 8/10, 8/10, 8/10 (see [`robust-baseline.json`](robust-baseline.json)).

## Iteration 2: an extended skill variant that was tried and not adopted (2026-10-02)

An extended variant of the skill (a fifth direction, `shared/pitfalls.md`, `shared/responsive.md`, `shared/video.md`, media-optional hero rules) was tried. Five pages generated with it, one run each: the four original prompts plus a new single-hero prompt (`5-halden`: a small web design studio, no images or videos, hero only), and a no-skill baseline for the hero-only prompt. Pages are in [`results-v2/`](results-v2/).

**Not comparable to iteration 1 in rigor.** These runs were made by sub-agents inside a Claude Code session (model alias `opus`), not by isolated `claude -p` processes, so memory and the surrounding environment were not fully excluded; there is one run per cell, and no timing or cost was recorded. Three of the five agents could not open the page in a browser while building.

| Page | `grade.py` (10 checks) | `check_robust.py` (10-12 checks) |
|---|---|---|
| Flowpilot, with skill | 9/10 | 10/10 |
| Northlane, with skill | 9/10 | 8/10 (sideways overflow at 390 and 320 px) |
| Portfolio, with skill | 10/10 | 10/10 |
| Számlakör, with skill | 9/10 | 10/10 |
| Halden hero-only, with skill | 7/10 | 12/12 |
| Halden hero-only, no skill | 9/10 | 12/12 |

What this shows, and what it does not:
- The three 9/10 scores come from one check, "no emoji used as icons": the pages use `★` (U+2605) rating glyphs and one `✓`, which the grader's character range counts as emoji. Iteration 1 pages did not use them. The grader was left unchanged.
- The Halden hero-only page loses three `grade.py` checks (hairline borders, scroll-driven motion, marquee) simply because a one-screen hero does not need them; they are not failures of the brief.
- The robustness checks found one real bug: Northlane's `.statement-glow` (a 420 px blurred circle) widened the page on phones. That led to a new rule in `shared/pitfalls.md` (clip sections that contain wide glows).
- On the single-hero prompt the skill and the baseline were indistinguishable on these checks. The checks do not measure visual quality, so this says nothing about which page looks better.

**Outcome:** the extended variant did not beat the published skill on these checks (92.5% vs 97.5% on `grade.py`, indistinguishable from the baseline on the hero-only prompt) and added about 700 lines of context, so it was not adopted. The published skill is unchanged from before this experiment. The variant is kept on the `experiment/cinematic-glass-pitfalls` branch; the robustness checker stays because it found a real overflow bug.
