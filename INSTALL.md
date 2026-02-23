# Installation Guide

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) CLI installed and configured
- A `~/.claude/skills/` directory (created automatically by Claude Code)

## Install All Skills

```bash
git clone https://github.com/jord0-cmd/jord0.skills.bat.git
cp -r jord0.skills.bat/skills/* ~/.claude/skills/
```

## Install a Single Skill

```bash
git clone https://github.com/jord0-cmd/jord0.skills.bat.git
cp -r jord0.skills.bat/skills/PORTAL ~/.claude/skills/PORTAL
```

Or without cloning:

```bash
# Download just one skill folder
# (Replace PORTAL with any skill name)
mkdir -p ~/.claude/skills/PORTAL
curl -sL https://raw.githubusercontent.com/jord0-cmd/jord0.skills.bat/main/skills/PORTAL/SKILL.md \
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
   cp -r jord0.skills.bat/skills/NOTIFY ~/.claude/skills/NOTIFY
   ```

**Requirements:** Windows 10 1903+ or Windows 11

### Linux (Debian/Ubuntu)

```bash
sudo apt install libnotify-bin
cp -r jord0.skills.bat/skills/NOTIFY ~/.claude/skills/NOTIFY
```

### Linux (Fedora)

```bash
sudo dnf install libnotify
cp -r jord0.skills.bat/skills/NOTIFY ~/.claude/skills/NOTIFY
```

### Linux (Arch)

```bash
sudo pacman -S libnotify
cp -r jord0.skills.bat/skills/NOTIFY ~/.claude/skills/NOTIFY
```

### macOS

No additional dependencies. Just copy:

```bash
cp -r jord0.skills.bat/skills/NOTIFY ~/.claude/skills/NOTIFY
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

Remove all batch skills:

```bash
rm -rf ~/.claude/skills/{PORTAL,STRICT,FORGE,CONCLAVE,NOTIFY,RECON,RECALL,ECHO,MIRROR,SPARK}
```
