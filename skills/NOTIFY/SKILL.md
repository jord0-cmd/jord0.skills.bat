---
name: NOTIFY
description: |
  Cross-platform desktop notifications from Claude Code. Use when: a long task completes,
  you need to alert the user, asking a choice via toast buttons, showing progress, or any
  time a desktop notification would be helpful. Works on WSL (Windows BurntToast), native
  Linux (notify-send), and macOS (osascript).
user-invocable: true
allowed-tools: Bash, Read, Write
---

# NOTIFY

**Cross-platform desktop notifications from Claude Code.**

---

## Usage

```
/notify "Title" "Message"                          - Simple notification
/notify "Title" "Message" --alarm                  - Notification with sound
/notify "Question?" --choices "Yes" "No" "Maybe"   - Interactive with buttons
/notify "Building..." --progress 0.75              - Progress bar notification
```

---

## What This Is

NOTIFY sends real desktop notifications from your Claude Code session. When a long build finishes, when a test suite completes, when Claude needs your attention — a toast pops up on your desktop instead of sitting silently in the terminal.

---

## Platform Support

| Platform | Method | Interactive Buttons | Progress Bar |
|----------|--------|-------------------|--------------|
| **WSL** | BurntToast (PowerShell) | Yes (up to 5) | Yes |
| **Linux** | notify-send | Yes (if supported) | Text-based |
| **macOS** | osascript | No | No |

---

## How It Works

### Simple Notification
```bash
python3 scripts/toast.py "Build Complete" "All 47 tests passed"
```

### With Sound (Attention-Getter)
```bash
python3 scripts/toast.py "ALERT" "Deployment failed" --alarm
```

### Interactive Choices
```bash
python3 scripts/toast.py "Deploy?" --choices "Production" "Staging" "Cancel"
```
Returns the selected option number (1-indexed) or `None` on timeout.

### Progress Bar
```bash
python3 scripts/toast.py "Installing" --progress 0.6 --status "60% complete"
```

### JSON Output
Add `--json` flag for machine-readable output:
```bash
python3 scripts/toast.py "Choose" --choices "A" "B" --json
# {"choice": 1, "label": "A"}
```

---

## Programmatic Use (Python)

```python
from toast import send_toast, ask_choice, send_progress

# Simple notification
send_toast("Title", "Message")

# With icon/image
send_toast("Title", "Message", hero=True)

# Interactive choice (returns 1-indexed int or None)
choice = ask_choice("Deploy where?", ["Production", "Staging", "Cancel"])

# Progress bar (call repeatedly to update)
send_progress("Building", "Compiling...", 0.3)
send_progress("Building", "Linking...", 0.7)
send_progress("Building", "Done!", 1.0)
```

---

## AUTO-EXECUTE Protocol

When this skill is invoked:

### Step 0: Prerequisites Check (First Use Only)
Run this check the first time NOTIFY is used in a session:

```bash
# Detect platform
grep -qiE "(microsoft|wsl)" /proc/version 2>/dev/null && echo "PLATFORM=wsl" || \
  ([ "$(uname)" = "Darwin" ] && echo "PLATFORM=macos" || echo "PLATFORM=linux")
```

Then verify dependencies:
- **WSL:** `powershell.exe -Command "Get-Module -ListAvailable BurntToast"` — if not found, tell user: "NOTIFY requires BurntToast. Install it in PowerShell: `Install-Module -Name BurntToast -Force`"
- **Linux:** `which notify-send` — if not found, tell user: "NOTIFY requires libnotify. Install it: `sudo apt install libnotify-bin`"
- **macOS:** No check needed (osascript is built-in)

**If prerequisites are missing, tell the user exactly what to install and how. Do not silently fail.**

### Steps 1-4: Normal Operation
1. Detect the platform (WSL, Linux, macOS)
2. Use the appropriate notification method
3. For interactive choices, wait for the user's response (default 60s timeout)
4. Return the result to the conversation

**Proactive use:** When a long-running task completes (build, test suite, deployment), send a notification automatically so the user knows to come back.

---

## Prerequisites and Setup

### WSL (Windows)
1. Open **PowerShell as Administrator** on your Windows host
2. Install BurntToast: `Install-Module -Name BurntToast -Force`
3. If prompted about untrusted repository, type `Y`
4. Verify: `Get-Module -ListAvailable BurntToast` (should show version)
5. Copy `scripts/toast.py` and `scripts/notify.sh` to your skill directory

**Troubleshooting WSL:**
- If `powershell.exe` is not found, check `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/`
- If you have `appendWindowsPath=false` in `/etc/wsl.conf`, add the PowerShell path to your `$PATH`
- BurntToast requires Windows 10 1903+ or Windows 11

### Linux (Debian/Ubuntu)
```bash
sudo apt install libnotify-bin
```

### Linux (Fedora/RHEL)
```bash
sudo dnf install libnotify
```

### Linux (Arch)
```bash
sudo pacman -S libnotify
```

### macOS
No additional setup — uses built-in `osascript`. Interactive buttons are not supported on macOS; notifications are display-only.

### Verify Installation
```bash
# Quick test — should show a desktop notification
python3 scripts/toast.py "Test" "NOTIFY is working"
```

---

## Dependencies

- **Python 3.10+** (standard library only — no pip packages needed)
- **WSL:** BurntToast PowerShell module (Windows 10 1903+)
- **Linux:** `libnotify-bin` / `libnotify` package
- **macOS:** None (built-in osascript)

### Feature Matrix

| Feature | WSL + BurntToast | Linux + notify-send | macOS |
|---------|-----------------|-------------------|-------|
| Basic notification | Yes | Yes | Yes |
| Custom sound | Yes (multiple) | No | Default only |
| Alarm/urgent | Yes | Yes (critical urgency) | No |
| Interactive buttons | Yes (up to 5) | Yes (if DE supports) | No |
| Progress bar | Yes (native) | Yes (text-based) | No |
| App icon | Yes | Yes | No |
| Notification replacement | No | Yes | No |

---

*Don't make them watch the terminal. Tap them on the shoulder.*
