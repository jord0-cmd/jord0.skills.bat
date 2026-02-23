<div class="hero-ascii" markdown>

```
       ██╗ ██████╗ ██████╗ ██████╗  ██████╗
       ██║██╔═══██╗██╔══██╗██╔══██╗██╔═████╗
       ██║██║   ██║██████╔╝██║  ██║██║██╔██║
  ██   ██║██║   ██║██╔══██╗██║  ██║████╔╝██║
  ╚█████╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝
   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝

            C:\> jord0.skills
    10 production skills for Claude Code
```

</div>

---

# Copy a Folder. Get a Superpower.

**jord0.skills** is a collection of 10 production-grade skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview). No build step. No dependencies. No configuration.

## Install — Two Commands

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/* ~/.claude/skills/
```

That's it. All 10 skills are installed. Start a Claude Code session and use them immediately.

!!! note "NOTIFY is the only skill with dependencies"
    NOTIFY needs BurntToast (WSL) or libnotify (Linux) for desktop notifications. Everything else works out of the box. See the [Installation Guide](getting-started/install.md) for NOTIFY setup.

---

## The Arsenal

### Context & Memory

| Skill | What It Does |
|-------|-------------|
| [**PORTAL**](skills/portal.md) | Save and restore session context across sessions, projects, and machines. Never lose your place again. |
| [**ECHO**](skills/echo.md) | Decision records that persist. When future-you asks "why did we do it this way?" — ECHO has the answer. |

### Quality & Standards

| Skill | What It Does |
|-------|-------------|
| [**STRICT**](skills/strict.md) | 11 non-negotiable coding rules. Load at session start. No placeholders, no half-measures, no excuses. |
| [**FORGE**](skills/forge.md) | Deep project onboarding. Point it at a codebase, get a complete CLAUDE.md with architecture, patterns, conventions. |

### Cognitive Tools

| Skill | What It Does |
|-------|-------------|
| [**CONCLAVE**](skills/conclave.md) | 9-voice structured debate. Minimalist vs chaos agent vs philosopher. Let them fight before you decide. |
| [**MIRROR**](skills/mirror.md) | Force counterarguments against your own recommendations. 8 challenge frameworks. Find the blind spots. |
| [**SPARK**](skills/spark.md) | Divergent thinking engine. When standard approaches feel stale, SPARK explores the weird, wild long tail. |

### Research & Knowledge

| Skill | What It Does |
|-------|-------------|
| [**RECON**](skills/recon.md) | Deep technical research that auto-saves to a knowledge base. Never research the same thing twice. |
| [**RECALL**](skills/recall.md) | Search your knowledge base before searching the web. The retrieval half of RECON. |

### System

| Skill | What It Does |
|-------|-------------|
| [**NOTIFY**](skills/notify.md) | Cross-platform desktop notifications. Simple alerts, interactive buttons, progress bars. Claude taps you on the shoulder. |

---

## Why Skills?

Claude Code is powerful out of the box. But it forgets everything between sessions. It doesn't know your coding standards. It can't carry context across machines.

Skills fix that. They're markdown files that teach Claude new behaviors — persistent memory, structured debate, research pipelines, coding discipline. Each one is a single folder you can drop in and immediately use.

**No API keys.** **No external services.** **No configuration files.**

Just markdown and, occasionally, a bash script.

---

<p style="text-align: center; color: #555; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; margin-top: 3rem;">
Built by <a href="https://github.com/jord0-cmd">jord0.cmd</a> | MIT License
</p>
