# NOTIFY

<span class="tag tag-system">system</span>

**Cross-platform desktop notifications. Claude taps you on the shoulder.**

Long-running task? NOTIFY pops a real desktop notification when it's done. Need a decision? Interactive buttons right on your desktop.

---

## Usage

### Simple notification

```
/notify "Build Complete" "All tests passing"
```

### With alarm sound

```
/notify "DEPLOY FAILED" "Production is down" --alarm
```

### Interactive choices

```
/notify "Migration Ready" --choices "Deploy Now" "Wait" "Abort"
```

Claude waits for your response and continues based on your choice.

### Progress bar

```
/notify "Processing..." --progress 0.75
```

---

## Platform Support

| Feature | WSL (Windows) | Linux | macOS |
|---------|:---:|:---:|:---:|
| Basic notifications | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Sound / alarm | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Interactive buttons | :white_check_mark: | Partial | :x: |
| Progress bar | :white_check_mark: | :x: | :x: |

WSL gets the best experience via BurntToast (PowerShell module). See [Installation](../getting-started/install.md#notify-setup) for platform setup.

---

## When to Use It

- Long-running builds or tests
- Deployment confirmations
- Any time you've walked away from the terminal
- Decision points that need human input

---

## Prerequisites

- Python 3.10+
- WSL: BurntToast PowerShell module
- Linux: `libnotify-bin`
- macOS: No additional dependencies

---

*Because sometimes Claude needs to get your attention.*
