# Installation

Three ways in. Pick your poison.

---

## Option 1: Plugin Marketplace (Recommended)

Inside a Claude Code session:

```
/plugin marketplace add jord0-cmd/jord0.skills
/plugin install jord0-skills@jord0-skills
```

All 10 skills install at once. Skills are namespaced as `/jord0-skills:PORTAL`, `/jord0-skills:STRICT`, etc. Updates automatically with `/plugin update`.

To uninstall:
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

This loads all 10 skills for the current session. Make it permanent with a shell alias:

```bash
alias claude='claude --plugin-dir ~/path/to/jord0.skills'
```

---

## Option 3: Copy Individual Skills

### All skills at once

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/* ~/.claude/skills/
```

### Just one skill

```bash
git clone https://github.com/jord0-cmd/jord0.skills.git
cp -r jord0.skills/skills/PORTAL ~/.claude/skills/PORTAL
```

### Without cloning (curl)

```bash
mkdir -p ~/.claude/skills/PORTAL
curl -sL https://raw.githubusercontent.com/jord0-cmd/jord0.skills/main/skills/PORTAL/SKILL.md \
  -o ~/.claude/skills/PORTAL/SKILL.md
```

---

## Verify Installation

Start a Claude Code session and run:

```
/help
```

Your installed skills should appear in the available skills list. Test one:

```
/strict
```

Should respond acknowledging the coding standards are loaded.

---

## NOTIFY Setup

NOTIFY is the only skill with external dependencies. It sends real desktop notifications from Claude Code.

=== "WSL (Windows)"

    1. Open **PowerShell as Administrator**
    2. Install BurntToast:
    ```powershell
    Install-Module -Name BurntToast -Force
    ```
    3. Verify:
    ```powershell
    Get-Module -ListAvailable BurntToast
    ```
    Requires Windows 10 1903+ or Windows 11.

=== "Ubuntu / Debian"

    ```bash
    sudo apt install libnotify-bin
    ```

=== "Fedora"

    ```bash
    sudo dnf install libnotify
    ```

=== "Arch"

    ```bash
    sudo pacman -S libnotify
    ```

=== "macOS"

    No dependencies needed. Basic notifications only (no interactive buttons or progress bars).

### Test NOTIFY

```bash
python3 ~/.claude/skills/NOTIFY/scripts/toast.py "Test" "NOTIFY is working"
```

You should see a desktop notification appear.

---

## Storage Directories

Some skills create local directories for persistent data. These are created automatically on first use:

| Skill | Directory | What's Stored |
|-------|-----------|---------------|
| PORTAL | `portals/` | Context snapshots |
| RECON | `knowledge/research/` | Research reports |
| RECALL | `knowledge/` | Knowledge base index |
| ECHO | `echoes/` | Decision records |

!!! tip "Cross-machine sync"
    Put these directories in a git-tracked location and they'll sync across machines. See the [Cross-Machine Workflow](../recipes/cross-machine.md) recipe for details.
