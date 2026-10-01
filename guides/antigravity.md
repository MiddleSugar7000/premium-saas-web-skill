# Install premium-saas-web in Google Antigravity

Antigravity supports the open Agent Skills standard. It reads **global** skills from `~/.gemini/antigravity/skills/` and **workspace** skills from `<workspace>/.agents/skills/` (the older `.agent/skills/` still works). The agent loads a skill when your request matches its description.

[← Back to README](../README.md) · [Claude Code](claude-code.md) · [Codex](codex.md) · [Cursor](cursor.md)

## Option 1: skills CLI

```bash
npx skills add MiddleSugar7000/premium-saas-web-skill
```

Pick **Antigravity** when asked. Add `-g` for a global install.

## Option 2: copy the folder

**Workspace** (commit it so collaborators get it):

```bash
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill /tmp/psw
mkdir -p .agents/skills
cp -r /tmp/psw/skills/premium-saas-web .agents/skills/
```

**Global, macOS / Linux:**

```bash
mkdir -p ~/.gemini/antigravity/skills
cp -r /tmp/psw/skills/premium-saas-web ~/.gemini/antigravity/skills/
```

**Global, Windows (PowerShell):**

```powershell
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill $env:TEMP\psw
New-Item -ItemType Directory -Force "$HOME\.gemini\antigravity\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\psw\skills\premium-saas-web" "$HOME\.gemini\antigravity\skills\"
```

The final layout must be `.../skills/premium-saas-web/SKILL.md`, with `references/` next to it.

## Check it works

Open a new agent conversation and ask *"Which skills can you use?"* It should list `premium-saas-web`.

## Use it

```
Use the premium-saas-web skill to build a landing page for Flowpilot, an AI agent that automates Slack, Notion and Gmail.
```

Tips:

- Antigravity's built-in browser agent is a great fit for the skill's self-review step: it screenshots the page at 1440px and 390px and fixes what it sees.
- It works with any model you pick in Antigravity; the benchmark in this repo was run with Claude Opus 5.5.

## Uninstall

Delete `premium-saas-web` from `~/.gemini/antigravity/skills/` or `.agents/skills/`.

---

Need a site built by a human? **[Hire MiddleSugar7000](https://middlesugar7000.xyz/?utm_source=github&utm_medium=guide&utm_campaign=premium-saas-web#contact)**, a full-stack developer: landing pages from $450, SaaS MVPs from $950.
