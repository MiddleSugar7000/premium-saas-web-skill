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
