#!/usr/bin/env python3
"""
NOTIFY Toast System - Cross-Platform Desktop Notifications

Send desktop notifications from CLI/AI coding sessions.
Works on WSL (Windows BurntToast), native Linux (notify-send), and macOS (osascript).

Usage:
    # Simple notification
    python toast.py "Title" "Message"

    # With alarm sound
    python toast.py "Title" "Message" --alarm

    # Interactive with choices (returns selected option)
    python toast.py "Question?" --choices "Option 1" "Option 2" "Option 3"

    # Progress bar
    python toast.py "Building" --progress 0.75 --status "75% complete"

    # Programmatic
    from toast import send_toast, ask_choice, send_progress
    send_toast("Title", "Message")
    choice = ask_choice("What next?", ["This", "That", "Other"])
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

APP_NAME = "NOTIFY"


def is_wsl() -> bool:
    """Check if running in WSL."""
    try:
        with open("/proc/version", "r") as f:
            content = f.read().lower()
            return "microsoft" in content or "wsl" in content
    except FileNotFoundError:
        return False


def is_linux_desktop() -> bool:
    """Check if running on Linux with a desktop environment."""
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def is_macos() -> bool:
    """Check if running on macOS."""
    import platform
    return platform.system() == "Darwin"


def check_notify_send_capabilities() -> dict[str, bool]:
    """Check what features notify-send supports on this system."""
    capabilities = {
        "available": False,
        "actions": False,
        "icons": False,
        "hints": False,
        "replace": False,
    }
    try:
        result = subprocess.run(
            ["notify-send", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        help_text = result.stdout + result.stderr
        capabilities["available"] = True
        capabilities["actions"] = "--action" in help_text or "-A" in help_text
        capabilities["icons"] = "--icon" in help_text or "-i" in help_text
        capabilities["hints"] = "--hint" in help_text or "-h" in help_text
        capabilities["replace"] = "--replace-id" in help_text or "-r" in help_text
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return capabilities


# Environment detection
IS_WSL = is_wsl()
IS_LINUX = not IS_WSL and is_linux_desktop()
IS_MACOS = not IS_WSL and not IS_LINUX and is_macos()
LINUX_CAPS = check_notify_send_capabilities() if IS_LINUX else {}

# Windows paths (only valid in WSL)
def get_windows_temp() -> str:
    """Get Windows temp directory path from WSL."""
    if not IS_WSL:
        return "/tmp"
    try:
        cmd_exe = shutil.which("cmd.exe") or "/mnt/c/Windows/System32/cmd.exe"
        result = subprocess.run(
            [cmd_exe, "/c", "echo %TEMP%"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            win_temp = result.stdout.strip()
            if win_temp.startswith("C:"):
                return "/mnt/c" + win_temp[2:].replace("\\", "/")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return "/tmp"


WIN_TEMP = get_windows_temp()
CHOICE_FILE = f"{WIN_TEMP}/notify_choice.txt"

# PowerShell path - needed when appendWindowsPath=false in wsl.conf
POWERSHELL_EXE = (
    shutil.which("powershell.exe")
    or "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
)

# Progress notification state (for replacement)
_progress_notification_id: int = 9999


def _send_linux_notify(
    title: str,
    message: str,
    icon: str | None = None,
    urgency: str = "normal",
    replace_id: int | None = None,
) -> bool:
    """Send notification via notify-send on Linux."""
    if not IS_LINUX or not LINUX_CAPS.get("available"):
        return False
    try:
        body = message.replace(" | ", "\n").replace("|", "\n")
        cmd = ["notify-send", title, body, f"--app-name={APP_NAME}"]
        cmd.extend(["-u", urgency])
        if icon and LINUX_CAPS.get("icons"):
            cmd.extend(["-i", icon])
        if replace_id is not None and LINUX_CAPS.get("replace"):
            cmd.extend(["-r", str(replace_id)])
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"Failed to send Linux notification: {e}")
        return False


def _send_macos_notify(title: str, message: str, sound: bool = False) -> bool:
    """Send notification via osascript on macOS."""
    if not IS_MACOS:
        return False
    try:
        escaped_title = title.replace('"', '\\"')
        escaped_msg = message.replace('"', '\\"')
        sound_str = ' sound name "default"' if sound else ""
        script = f'display notification "{escaped_msg}" with title "{escaped_title}"{sound_str}'
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"Failed to send macOS notification: {e}")
        return False


def _ask_linux_choice(
    question: str,
    options: list[str],
    icon: str | None = None,
    urgency: str = "normal",
    timeout: float = 60.0,
) -> int | None:
    """Show interactive notification with action buttons on Linux."""
    if not IS_LINUX or not LINUX_CAPS.get("actions"):
        _send_linux_notify(APP_NAME, question, icon=icon, urgency=urgency)
        return None
    try:
        cmd = [
            "notify-send", APP_NAME, question,
            f"--app-name={APP_NAME}", "--wait", "-u", urgency,
        ]
        if icon and LINUX_CAPS.get("icons"):
            cmd.extend(["-i", icon])
        for i, opt in enumerate(options, 1):
            cmd.extend(["-A", f"{i}={i}. {opt}"])
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                return int(result.stdout.strip())
            except ValueError:
                return None
        return None
    except subprocess.TimeoutExpired:
        return None
    except (FileNotFoundError, OSError) as e:
        logger.warning(f"Failed to show Linux choice: {e}")
        return None


def ensure_choice_scripts(count: int = 5) -> None:
    """Create batch files for each choice option. WSL only."""
    if not IS_WSL:
        return
    ps_script = f'''
$tempDir = $env:TEMP
1..{count} | ForEach-Object {{
    $content = "@echo off`r`necho $_ > $tempDir\\notify_choice.txt"
    $path = "$tempDir\\notify_choice_$_.bat"
    if (-not (Test-Path $path)) {{
        $content | Out-File -FilePath $path -Encoding ASCII -NoNewline
    }}
}}
'''
    try:
        subprocess.run(
            [POWERSHELL_EXE, "-Command", ps_script],
            capture_output=True,
            timeout=10,
        )
    except FileNotFoundError:
        pass


def clear_choice() -> None:
    """Clear any existing choice file."""
    choice_path = Path(CHOICE_FILE)
    if choice_path.exists():
        choice_path.unlink()


def read_choice(timeout: float = 30.0) -> Optional[int]:
    """Wait for and read user's choice from button click."""
    choice_path = Path(CHOICE_FILE)
    start = time.time()
    while time.time() - start < timeout:
        if choice_path.exists():
            try:
                content = choice_path.read_text().strip()
                first_line = content.split("\n")[0].strip()
                return int(first_line)
            except (ValueError, IOError):
                pass
        time.sleep(0.2)
    return None


def send_toast(
    title: str,
    message: str,
    line3: str | None = None,
    hero: bool = False,
    alarm: bool = False,
    sound: str | None = None,
) -> bool:
    """Send a simple toast notification.

    Args:
        title: Toast title (line 1, bold).
        message: Toast body (line 2).
        line3: Optional third line for additional info.
        hero: Include app icon (WSL AppLogo).
        alarm: Play alarm sound / use critical urgency.
        sound: Override sound (Default, IM, Mail, Alarm, etc.) - None = silent.

    Returns:
        True if toast was sent successfully.
    """
    if IS_LINUX:
        urgency = "critical" if alarm else "normal"
        full_message = f"{message} | {line3}" if line3 else message
        return _send_linux_notify(title, full_message, urgency=urgency)

    if IS_MACOS:
        full_message = f"{message}\n{line3}" if line3 else message
        return _send_macos_notify(title, full_message, sound=alarm)

    if not IS_WSL:
        return False

    title_escaped = title.replace("'", "''")
    message_escaped = message.replace("'", "''")
    line3_escaped = line3.replace("'", "''") if line3 else None

    sound_param = "-Silent"
    if alarm:
        sound_param = "-Sound Alarm"
    elif sound:
        sound_param = f"-Sound {sound}"

    if line3_escaped:
        text_param = f"-Text '{title_escaped}', '{message_escaped}', '{line3_escaped}'"
    else:
        text_param = f"-Text '{title_escaped}', '{message_escaped}'"

    ps_script = f"""
Import-Module BurntToast
New-BurntToastNotification `
    {text_param} `
    {sound_param}
"""
    try:
        result = subprocess.run(
            [POWERSHELL_EXE, "-Command", ps_script],
            capture_output=True,
            timeout=15,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def ask_choice(
    question: str,
    options: list[str],
    hero: bool = True,
    timeout: float = 60.0,
    urgent: bool = True,
    alarm: bool = False,
) -> int | None:
    """Show an interactive toast with button choices.

    Args:
        question: The question to ask.
        options: List of option labels (max 5).
        hero: Include app icon.
        timeout: Seconds to wait for response.
        urgent: Make toast persistent (stays visible longer).
        alarm: Play alarm sound.

    Returns:
        1-indexed choice number, or None if timeout/cancelled.
    """
    if IS_LINUX:
        urgency = "critical" if (alarm or urgent) else "normal"
        return _ask_linux_choice(question, options, urgency=urgency, timeout=timeout)

    if IS_MACOS:
        _send_macos_notify(APP_NAME, question, sound=alarm)
        return None  # macOS doesn't support interactive buttons via osascript

    if not IS_WSL:
        return None

    if len(options) > 5:
        options = options[:5]

    ensure_choice_scripts(len(options))
    clear_choice()

    buttons = []
    for i, opt in enumerate(options, 1):
        opt_escaped = opt.replace("'", "''")
        buttons.append(
            f"$btn{i} = New-BTButton -Content '{i}. {opt_escaped}' "
            f'-Arguments "$env:TEMP\\notify_choice_{i}.bat"'
        )

    button_vars = ", ".join(f"$btn{i}" for i in range(1, len(options) + 1))
    button_creation = "\n".join(buttons)

    urgent_param = "-Urgent" if urgent else ""
    sound_param = "-Sound Alarm" if alarm else ""
    question_escaped = question.replace("'", "''")

    ps_script = f"""
Import-Module BurntToast

{button_creation}

$Expire = (Get-Date).AddHours(1)

New-BurntToastNotification `
    -Text '{APP_NAME}', '{question_escaped}' `
    -Button {button_vars} `
    {urgent_param} {sound_param} `
    -ExpirationTime $Expire
"""
    try:
        result = subprocess.run(
            [POWERSHELL_EXE, "-Command", ps_script],
            capture_output=True,
            timeout=15,
        )
        if result.returncode != 0:
            return None
        return read_choice(timeout)
    except FileNotFoundError:
        return None


def send_progress(
    title: str,
    status: str,
    value: float,
    hero: bool = False,
) -> bool:
    """Send a toast with a progress bar.

    Args:
        title: Toast title.
        status: Progress status text.
        value: Progress value 0.0 to 1.0.
        hero: Include app icon.

    Returns:
        True if sent successfully.
    """
    value_clamped = max(0.0, min(1.0, value))
    pct = int(value_clamped * 100)

    if IS_LINUX:
        bar_width = 20
        filled = int(bar_width * value_clamped)
        bar = "\u2588" * filled + "\u2591" * (bar_width - filled)
        message = f"{status} | [{bar}] {pct}%"
        return _send_linux_notify(
            title, message, replace_id=_progress_notification_id
        )

    if IS_MACOS:
        return _send_macos_notify(title, f"{status} — {pct}%")

    if not IS_WSL:
        return False

    title_escaped = title.replace("'", "''")
    status_escaped = status.replace("'", "''")

    ps_script = f"""
Import-Module BurntToast
$Progress = New-BTProgressBar -Status '{status_escaped}' -Value {value_clamped}
New-BurntToastNotification `
    -Text '{title_escaped}' `
    -ProgressBar $Progress
"""
    try:
        result = subprocess.run(
            [POWERSHELL_EXE, "-Command", ps_script],
            capture_output=True,
            timeout=15,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} — Desktop Notifications")
    parser.add_argument("title", nargs="?", default=APP_NAME, help="Toast title")
    parser.add_argument("message", nargs="?", default="", help="Toast message")
    parser.add_argument("line3", nargs="?", default=None, help="Optional third line")
    parser.add_argument("--hero", action="store_true", help="Include app icon")
    parser.add_argument("--alarm", action="store_true", help="Play alarm sound")
    parser.add_argument("--choices", nargs="+", help="Interactive choices")
    parser.add_argument("--progress", type=float, help="Show progress bar (0-1)")
    parser.add_argument("--status", default="Working...", help="Progress status text")
    parser.add_argument("--timeout", type=float, default=60.0, help="Choice timeout")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.choices:
        choice = ask_choice(
            args.title,
            args.choices,
            hero=args.hero,
            timeout=args.timeout,
            alarm=args.alarm,
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "choice": choice,
                        "label": args.choices[choice - 1] if choice else None,
                    }
                )
            )
        else:
            if choice:
                print(f"Choice: {choice} ({args.choices[choice - 1]})")
            else:
                print("No choice made (timeout)")

    elif args.progress is not None:
        success = send_progress(
            args.title, args.status, args.progress, hero=args.hero
        )
        if args.json:
            print(json.dumps({"success": success}))
        else:
            print("Progress toast sent" if success else "Failed to send")

    elif args.message:
        success = send_toast(
            args.title, args.message, line3=args.line3, hero=args.hero, alarm=args.alarm
        )
        if args.json:
            print(json.dumps({"success": success}))
        else:
            print("Toast sent" if success else "Failed to send")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
