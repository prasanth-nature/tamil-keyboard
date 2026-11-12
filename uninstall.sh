#!/usr/bin/env bash
# Remove the custom Tamil keyboard layout.

set -euo pipefail

APP="tamil-keyboard"
ENGINE_NAME="tamil-custom"
COMPONENT_NAME="${ENGINE_NAME}.xml"
SYSTEM_COMPONENT="${COMPONENT_DIR:-/usr/share/ibus/component}/${COMPONENT_NAME}"

SYSTEM=0
[ "${1:-}" = "--system" ] && SYSTEM=1

if [ "$SYSTEM" -eq 1 ]; then
  DEST="/usr/local/share/${APP}"
  sudo rm -rf "$DEST"
else
  DEST="${HOME}/.local/share/${APP}"
  rm -rf "$DEST"
fi

if [ -f "$SYSTEM_COMPONENT" ]; then
  sudo rm -f "$SYSTEM_COMPONENT"
fi
rm -f "${HOME}/.local/share/ibus/component/${COMPONENT_NAME}"
rm -f "${HOME}/.config/environment.d/ibus-${ENGINE_NAME}.conf"

if command -v gsettings >/dev/null 2>&1; then
  current="$(gsettings get org.gnome.desktop.input-sources sources)"
  case "$current" in
    *"'${ENGINE_NAME}'"*)
      cleaned="$(printf '%s' "$current" | sed -e "s/, ('ibus', '${ENGINE_NAME}')//" -e "s/('ibus', '${ENGINE_NAME}'), //")"
      gsettings set org.gnome.desktop.input-sources sources "$cleaned" || true ;;
  esac
fi

rm -rf "${HOME}/.cache/ibus/bus/registry"
command -v ibus >/dev/null 2>&1 && { ibus write-cache >/dev/null 2>&1 || true; ibus restart >/dev/null 2>&1 || true; }

echo "Removed the custom Tamil layout. Restart your session if it is still listed."
