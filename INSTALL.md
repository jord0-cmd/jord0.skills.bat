# Installation Guide

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) CLI installed and configured
- A `~/.claude/skills/` directory (created automatically by Claude Code)

---

## Option 1: Plugin Marketplace (Recommended)

The fastest way to install. Run these commands inside a Claude Code session:

```
/plugin marketplace add jord0-cmd/jord0.skills
/plugin install jord0-skills@jord0-skills
```

**What this does:**
- Registers the jord0-skills marketplace as a source
- Installs all 12 skills as the `jord0-skills` plugin
- Skills are namespaced: `/jord0-skills:PORTAL`, `/jord0-skills:STRICT`, etc.
- Updates automatically when you run `/plugin update`

**To uninstall:**
```
/plugin uninstall jord0-skills
```

---

## Option 2: Direct Plugin

Load the entire repo as a plugin directory:

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
claude --plugin-dir ./jord0.skills
```

This loads all 12 skills for the current session. Add `--plugin-dir` to your shell alias for persistence:

```bash
alias claude='claude --plugin-dir ~/path/to/jord0.skills'
```

---

## Option 3: Copy Individual Skills

### All Skills

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/* ~/.claude/skills/
```

### Single Skill

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/PORTAL ~/.claude/skills/PORTAL
```

### Without Cloning (curl)

```bash
# Download just one skill folder
# (Replace PORTAL with any skill name)
mkdir -p ~/.claude/skills/PORTAL
curl -sL https://raw.githubusercontent.com/jord0-cmd/jord0.skills/main/skills/PORTAL/SKILL.md \
  -o ~/.claude/skills/PORTAL/SKILL.md
```

## Verify Installation

Start a Claude Code session and check that skills are listed:

```
> /help
```

You should see your installed skills in the available skills list.

Test a skill:

```
> /strict
```

Should respond acknowledging the coding standards are loaded.

## NOTIFY Setup (Platform-Specific)

NOTIFY is the only skill requiring external dependencies.

### WSL (Windows Subsystem for Linux)

1. Open **PowerShell as Administrator** on Windows
2. Run:
   ```powershell
   Install-Module -Name BurntToast -Force
   ```
3. If prompted about PSGallery, type `Y`
4. Verify:
   ```powershell
   Get-Module -ListAvailable BurntToast
   ```
5. Copy the skill:
   ```bash
   cp -r jord0.skills/skills/NOTIFY ~/.claude/skills/NOTIFY
   ```

**Requirements:** Windows 10 1903+ or Windows 11

### Linux (Debian/Ubuntu)

```bash
sudo apt install libnotify-bin
cp -r jord0.skills/skills/NOTIFY ~/.claude/skills/NOTIFY
```

### Linux (Fedora)

```bash
sudo dnf install libnotify
cp -r jord0.skills/skills/NOTIFY ~/.claude/skills/NOTIFY
```

### Linux (Arch)

```bash
sudo pacman -S libnotify
cp -r jord0.skills/skills/NOTIFY ~/.claude/skills/NOTIFY
```

### macOS

No additional dependencies. Just copy:

```bash
cp -r jord0.skills/skills/NOTIFY ~/.claude/skills/NOTIFY
```

Note: macOS supports basic notifications only (no interactive buttons or progress bars).

### Test NOTIFY

```bash
python3 ~/.claude/skills/NOTIFY/scripts/toast.py "Test" "NOTIFY is working"
```

You should see a desktop notification.

## Skill Storage Directories

Some skills create local storage directories for persistent data:

| Skill | Storage | Purpose |
|-------|---------|---------|
| PORTAL | `portals/` | Portal context snapshots |
| RECON | `knowledge/research/` | Research reports |
| RECALL | `knowledge/` | Knowledge base index |
| ECHO | `echoes/` | Decision records |

These directories are created automatically on first use. You can place them:
- In your project root (per-project data)
- In `~/.claude/` (global data)
- In any git-tracked directory (for cross-machine sync)

## Uninstall

Remove individual skills:

```bash
rm -rf ~/.claude/skills/PORTAL
```

Remove all jord0 skills:

```bash
rm -rf ~/.claude/skills/{OPTIC,LOCUS,PORTAL,STRICT,FORGE,CONCLAVE,NOTIFY,RECON,RECALL,ECHO,MIRROR,SPARK}
```
