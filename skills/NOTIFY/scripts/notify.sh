#!/bin/bash
#
# NOTIFY - Cross-platform desktop notifications
# Works on: WSL (Windows toast), Native Linux (notify-send), macOS (osascript)
#
# Usage: notify.sh "Title" "Message"
#

TITLE="${1:-NOTIFY}"
MESSAGE="${2:-Notification}"

# Detect environment
is_wsl() {
    grep -qiE "(microsoft|wsl)" /proc/version 2>/dev/null
}

is_linux_desktop() {
    [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]
}

is_macos() {
    [ "$(uname)" = "Darwin" ]
}

# Escape a string for PowerShell single-quoted strings (double up single quotes)
escape_ps_string() {
    printf '%s' "$1" | sed "s/'/''/g"
}

# WSL: Use Windows toast notifications
send_wsl_toast() {
    local PS_EXE
    PS_EXE=$(command -v powershell.exe 2>/dev/null || echo "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
    local SAFE_TITLE
    local SAFE_MESSAGE
    SAFE_TITLE=$(escape_ps_string "$TITLE")
    SAFE_MESSAGE=$(escape_ps_string "$MESSAGE")
    "$PS_EXE" -Command "
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        \$textNodes = \$template.GetElementsByTagName('text')
        \$textNodes.Item(0).AppendChild(\$template.CreateTextNode('$SAFE_TITLE')) | Out-Null
        \$textNodes.Item(1).AppendChild(\$template.CreateTextNode('$SAFE_MESSAGE')) | Out-Null
        \$toast = [Windows.UI.Notifications.ToastNotification]::new(\$template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('NOTIFY').Show(\$toast)
    " 2>/dev/null
    return $?
}

# Native Linux: Use notify-send
send_linux_notify() {
    if command -v notify-send &>/dev/null; then
        notify-send "$TITLE" "$MESSAGE" --app-name="NOTIFY" 2>/dev/null
        return $?
    fi
    return 1
}

# macOS: Use osascript with stdin to prevent shell injection
# Piping AppleScript via stdin avoids all shell escaping issues with -e flag
send_macos_notify() {
    osascript <<APPLESCRIPT 2>/dev/null
set theTitle to "$(printf '%s' "$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g')"
set theMessage to "$(printf '%s' "$MESSAGE" | sed 's/\\/\\\\/g; s/"/\\"/g')"
display notification theMessage with title theTitle
APPLESCRIPT
    return $?
}

# Main logic
if is_wsl; then
    send_wsl_toast
    exit $?
elif is_macos; then
    send_macos_notify
    exit $?
elif is_linux_desktop; then
    send_linux_notify
    exit $?
else
    # No display / headless - silent fail
    exit 0
fi
