# Install premium-saas-web in OpenAI Codex

Codex CLI (and the Codex IDE extension) reads Agent Skills from `~/.codex/skills/` (personal, every project) and `.codex/skills/` (one project). If you set `CODEX_HOME`, the personal folder is `$CODEX_HOME/skills/`. Codex loads a skill automatically when your request matches its description, or when you mention it with `$premium-saas-web`.

[← Back to README](../README.md) · [Claude Code](claude-code.md) · [Cursor](cursor.md) · [Antigravity](antigravity.md)

## Option 1: skills CLI

```bash
npx skills add MiddleSugar7000/premium-saas-web-skill
```

Pick **Codex** when asked. Add `-g` for a global install.

## Option 2: copy the folder

**macOS / Linux**

```bash
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill /tmp/psw
mkdir -p ~/.codex/skills
cp -r /tmp/psw/skills/premium-saas-web ~/.codex/skills/
```

**Windows (PowerShell)**

```powershell
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill $env:TEMP\psw
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\psw\skills\premium-saas-web" "$HOME\.codex\skills\"
```

For one repository, use `<repo>/.codex/skills/premium-saas-web/` and commit it.

## Check it works

Restart Codex, then type `$` and look for `premium-saas-web` in the list, or ask *"Which skills are available?"*

## Use it

```
$premium-saas-web Build a landing page for Flowpilot, an AI agent that automates Slack, Notion and Gmail. One index.html.
```

Or just describe the page; the skill triggers on landing pages, homepages, pricing pages and portfolios for SaaS / AI / tech / agency brands.

Tips:

- Codex runs sandboxed by default. The skill loads GSAP, Lenis and Google Fonts from public CDNs **in the page**, which doesn't need network access during generation, but the self-review step (opening the page in a browser) only runs if your setup allows it.
- Name a direction to steer it: *"Editorial Mono"*, *"Noir Spotlight with a lime accent"*.

## Uninstall

```bash
rm -rf ~/.codex/skills/premium-saas-web
```

---

Need a site built by a human? **[Hire MiddleSugar7000](https://middlesugar7000.xyz/?utm_source=github&utm_medium=guide&utm_campaign=premium-saas-web#contact)**, a full-stack developer: landing pages from $450, SaaS MVPs from $950.
