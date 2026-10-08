# Install premium-saas-web in Claude Code

Claude Code reads Agent Skills from `~/.claude/skills/` (every project) and `.claude/skills/` (one project). It loads the skill when your request matches its description, or when you call it with `/premium-saas-web`.

[← Back to README](../README.md) · [Codex](codex.md) · [Cursor](cursor.md) · [Antigravity](antigravity.md)

## Option 1: plugin marketplace (recommended)

Inside Claude Code:

```
/plugin marketplace add MiddleSugar7000/premium-saas-web-skill
/plugin install premium-saas-web@middlesugar7000
```

Restart Claude Code if it was already running. Update later with `/plugin marketplace update middlesugar7000`.

## Option 2: skills CLI

```bash
npx skills add MiddleSugar7000/premium-saas-web-skill
```

Pick **Claude Code** when asked. Add `-g` to install it globally instead of into the current project.

## Option 3: copy the folder

**macOS / Linux**

```bash
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill /tmp/psw
mkdir -p ~/.claude/skills
cp -r /tmp/psw/skills/premium-saas-web ~/.claude/skills/
```

**Windows (PowerShell)**

```powershell
git clone --depth 1 https://github.com/MiddleSugar7000/premium-saas-web-skill $env:TEMP\psw
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\psw\skills\premium-saas-web" "$HOME\.claude\skills\"
```

For a single project, copy into `<project>/.claude/skills/` instead and commit it, so your whole team gets it.

## Check it works

Start a new session and run:

```
/premium-saas-web
```

If the command autocompletes, the skill is installed. You can also ask *"What skills do you have?"*

## Use it

```
Build a landing page for Flowpilot, an AI agent that automates Slack, Notion and Gmail.
```

Claude picks a design direction, tells you which in one line, builds the page and, if a browser tool is available, screenshots it at desktop and mobile width to fix problems before handing over.

Tips:

- Name a direction if you have one in mind: *"use Tactile Light with a blue accent"*.
- In an existing Next.js / React / Vue project, the skill follows your stack instead of writing a single HTML file.
- Image generation tools (if you have any connected) are used for 3D renders; otherwise visuals are built in CSS/SVG.

## Uninstall

```bash
rm -rf ~/.claude/skills/premium-saas-web
```

or `/plugin uninstall premium-saas-web@middlesugar7000`.

---

Want a studio to build it instead? **[Vantle](https://vantle.studio/?utm_source=github&utm_medium=guide&utm_campaign=premium-saas-web#start)**, the team behind this skill, designs and builds brands, websites and software products.
