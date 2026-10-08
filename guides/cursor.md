# Install premium-saas-web in Cursor

Cursor's agent discovers Agent Skills (`SKILL.md` folders) in `~/.cursor/skills/` (personal, every project) and in `.cursor/skills/` or `.agents/skills/` inside a project. Skills load automatically when your request matches, and you can call one with `/premium-saas-web` in the agent chat.

[← Back to README](../README.md) · [Claude Code](claude-code.md) · [Codex](codex.md) · [Antigravity](antigravity.md)

## Option 1: skills CLI

```bash
npx skills add MiddleSugar7000/premium-saas-web-skill
```

Pick **Cursor** when asked. Add `-g` for a global install.

## Option 2: copy the folder

**Per project** (commit it so your team gets it):

```bash
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill /tmp/psw
mkdir -p .cursor/skills
cp -r /tmp/psw/skills/premium-saas-web .cursor/skills/
```

**Global, macOS / Linux:**

```bash
mkdir -p ~/.cursor/skills
cp -r /tmp/psw/skills/premium-saas-web ~/.cursor/skills/
```

**Global, Windows (PowerShell):**

```powershell
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill $env:TEMP\psw
New-Item -ItemType Directory -Force "$HOME\.cursor\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\psw\skills\premium-saas-web" "$HOME\.cursor\skills\"
```

## Check it works

Reload the window (**Ctrl/Cmd+Shift+P → Developer: Reload Window**), open the agent chat and type `/`. `premium-saas-web` should appear in the list. Installed skills are also listed in Cursor Settings.

## Use it

In **Agent** mode:

```
/premium-saas-web Build a landing page for Flowpilot, an AI agent that automates Slack, Notion and Gmail.
```

Tips:

- Use Agent mode (not Ask), so it can write files and run the browser self-check.
- In an existing Next.js / React project the skill follows your stack and Tailwind config.
- **Older Cursor versions without skill support:** create `.cursor/rules/premium-saas-web.mdc` with `alwaysApply: false` and a description, paste the body of `SKILL.md` into it, and keep the `directions/` and `shared/` folders next to it at `.cursor/rules/premium-saas-web/`. Then mention `@premium-saas-web` in chat.

## Uninstall

Delete the `premium-saas-web` folder from `.cursor/skills/` or `~/.cursor/skills/`.

---

Want a studio to build it instead? **[Vantle](https://vantle.studio/?utm_source=github&utm_medium=guide&utm_campaign=premium-saas-web#start)**, the team behind this skill, designs and builds brands, websites and software products.
