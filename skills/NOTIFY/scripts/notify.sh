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

# WSL: Use Windows toast notifications
send_wsl_toast() {
    local PS_EXE
    PS_EXE=$(command -v powershell.exe 2>/dev/null || echo "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
    "$PS_EXE" -Command "
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        \$textNodes = \$template.GetElementsByTagName('text')
        \$textNodes.Item(0).AppendChild(\$template.CreateTextNode('$TITLE')) | Out-Null
        \$textNodes.Item(1).AppendChild(\$template.CreateTextNode('$MESSAGE')) | Out-Null
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

# macOS: Use osascript
send_macos_notify() {
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"" 2>/dev/null
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
