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

# jord0.skills

**10 production-grade skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview).** Copy a folder, get a superpower.

By [jord0.cmd](https://github.com/jord0-cmd)

---

## The Skills

| Skill | What It Does | Prerequisites |
|-------|-------------|---------------|
| [**PORTAL**](skills/PORTAL/) | Save and restore session context across sessions and machines | None |
| [**STRICT**](skills/STRICT/) | Non-negotiable coding standards — 11 critical rules | None |
| [**FORGE**](skills/FORGE/) | Onboard any codebase — generates CLAUDE.md automatically | None |
| [**CONCLAVE**](skills/CONCLAVE/) | Multi-perspective structured debate (9 voices) | None |
| [**NOTIFY**](skills/NOTIFY/) | Cross-platform desktop notifications with interactive buttons | See below |
| [**RECON**](skills/RECON/) | Deep research that persists to a knowledge base | WebSearch access |
| [**RECALL**](skills/RECALL/) | Search your knowledge base before searching the web | Knowledge base |
| [**ECHO**](skills/ECHO/) | Capture decision reasoning — queryable ADR system | None |
| [**MIRROR**](skills/MIRROR/) | Force counterarguments against your own recommendations | None |
| [**SPARK**](skills/SPARK/) | Divergent thinking — break out of conventional solutions | None |

---

## Install

### Option 1: Plugin Marketplace (Recommended)

```
/plugin marketplace add jord0-cmd/jord0.skills
/plugin install jord0-skills@jord0-skills
```

All 10 skills install and update automatically. Skills are namespaced as `/jord0-skills:PORTAL`, `/jord0-skills:STRICT`, etc.

### Option 2: Direct Plugin

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
claude --plugin-dir ./jord0.skills
```

### Option 3: Copy Individual Skills

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/PORTAL ~/.claude/skills/PORTAL
```

No build step, no dependencies (except NOTIFY — see below), no configuration.

See [INSTALL.md](INSTALL.md) for detailed instructions.

---

## NOTIFY Prerequisites

NOTIFY is the only skill with external dependencies. It sends real desktop notifications from your Claude Code session.

| Platform | Requirement | Install |
|----------|------------|---------|
| **WSL** | BurntToast PowerShell module | `Install-Module -Name BurntToast -Force` (in PowerShell) |
| **Linux** | libnotify | `sudo apt install libnotify-bin` |
| **macOS** | None | Built-in osascript |

All other skills are zero-dependency.

---

## How Skills Work

Claude Code skills are markdown files that extend Claude's capabilities. When you invoke a skill (e.g., `/portal create my-project`), Claude reads the skill's `SKILL.md` and follows its instructions.

Each skill in this repo is a self-contained folder:

```
skills/
  PORTAL/
    SKILL.md          # The skill definition
  NOTIFY/
    SKILL.md          # The skill definition
    scripts/          # Supporting scripts (if any)
      toast.py
      notify.sh
```

Skills live in `~/.claude/skills/` and are automatically available in all Claude Code sessions.

---

## Compatibility

- **Claude Code** v1.0+
- **Models**: Works with all Claude models (Opus, Sonnet, Haiku). Best results with Opus/Sonnet.
- **Platforms**: Linux, macOS, WSL (Windows Subsystem for Linux)

---

## Philosophy

These skills were extracted from a production AI development environment. They've been used daily for months, refined through real work, and stress-tested on real projects.

The design principles:

1. **Self-contained** — each skill works by copying one folder
2. **No lock-in** — standard markdown, standard JSON, no proprietary formats
3. **Prerequisites are documented** — if a skill needs something, it tells you
4. **Quality over quantity** — 10 skills that work perfectly > 100 that kinda work

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting new skills or improvements.

---

## License

MIT — see [LICENSE](LICENSE)
