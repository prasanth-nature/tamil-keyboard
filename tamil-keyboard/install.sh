#!/usr/bin/env bash
# Install the custom Tamil keyboard layout.
#
#   ./install.sh                 install (asks for sudo once, for the component file)
#   ./install.sh --add-source    also add the layout to the GNOME input sources
#   ./install.sh --no-sudo       install everything under $HOME (needs a re-login)
#   ./install.sh --system        engine in /usr/local/share for every user
#
# Why sudo is needed: IBus only scans /usr/share/ibus/component. The
# user-level directory ~/.local/share/ibus/component is compiled out of
# ibusregistry.c, so a component file placed there is never loaded.

set -euo pipefail

APP="tamil-keyboard"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_NAME="tamil-custom"
COMPONENT_NAME="${ENGINE_NAME}.xml"
SYSTEM_COMPONENT_DIR="/usr/share/ibus/component"

blue() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!!\033[0m  %s\n' "$*"; }
die()  { printf '\033[1;31mxx\033[0m  %s\n' "$*" >&2; exit 1; }

ADD_SOURCE=0
SYSTEM=0
NO_SUDO=0
for arg in "$@"; do
  case "$arg" in
    --add-source) ADD_SOURCE=1 ;;
    --system)     SYSTEM=1 ;;
    --no-sudo)    NO_SUDO=1 ;;
    -h|--help)    sed -n '2,13p' "$0"; exit 0 ;;
    *)            die "unknown option: $arg" ;;
  esac
done

# ------------------------------------------------------------------ checks
command -v python3 >/dev/null 2>&1 || die "python3 is required."

python3 - <<'PY' || die "IBus Python bindings missing. Run:  sudo dnf install -y ibus ibus-libs python3-gobject"
import gi
gi.require_version("IBus", "1.0")
from gi.repository import IBus  # noqa: F401
PY

command -v ibus >/dev/null 2>&1 || die "the ibus command is missing:  sudo dnf install -y ibus"

# ------------------------------------------------------------------ paths
if [ "$SYSTEM" -eq 1 ]; then
  DEST="/usr/local/share/${APP}"
else
  DEST="${HOME}/.local/share/${APP}"
fi
ENGINE="${DEST}/ibus-engine-tamil-custom"

# ------------------------------------------------------------------ engine
blue "Installing engine into ${DEST}"
if [ "$SYSTEM" -eq 1 ]; then
  sudo mkdir -p "$DEST"
  sudo install -m 0755 "${HERE}/src/ibus-engine-tamil-custom" "${ENGINE}"
  sudo install -m 0644 "${HERE}/src/tamil_core.py"           "${DEST}/tamil_core.py"
  sudo install -m 0755 "${HERE}/doctor.sh"                   "${DEST}/doctor.sh"
else
  mkdir -p "$DEST"
  install -m 0755 "${HERE}/src/ibus-engine-tamil-custom" "${ENGINE}"
  install -m 0644 "${HERE}/src/tamil_core.py"           "${DEST}/tamil_core.py"
  install -m 0755 "${HERE}/doctor.sh"                   "${DEST}/doctor.sh"
fi

# ------------------------------------------------------------------ component
TMP_XML="$(mktemp)"
trap 'rm -f "${TMP_XML}"' EXIT
sed -e "s|@ENGINE_EXEC@|${ENGINE} --ibus|g" \
    "${HERE}/component/tamil-custom.xml.in" > "${TMP_XML}"

installed_where=""
install_component_system() {
  sudo mkdir -p "${SYSTEM_COMPONENT_DIR}" &&
  sudo install -m 0644 "${TMP_XML}" "${SYSTEM_COMPONENT_DIR}/${COMPONENT_NAME}"
}

install_component_user() {
  local dir="${HOME}/.local/share/ibus/component"
  mkdir -p "${dir}" "${HOME}/.config/environment.d"
  install -m 0644 "${TMP_XML}" "${dir}/${COMPONENT_NAME}"
  printf 'IBUS_COMPONENT_PATH=%s:/usr/share/ibus/component\n' "${dir}" \
    > "${HOME}/.config/environment.d/ibus-${ENGINE_NAME}.conf"
}

if [ "$NO_SUDO" -eq 1 ]; then
  blue "Installing component into \$HOME (no-sudo mode)"
  install_component_user
  installed_where="user"
elif install_component_system; then
  blue "Installing component into ${SYSTEM_COMPONENT_DIR}"
  installed_where="system"
else
  warn "could not write ${SYSTEM_COMPONENT_DIR} - falling back to a user-level install"
  install_component_user
  installed_where="user"
fi

# ------------------------------------------------------------------ verify
blue "Running layout self-test"
"${ENGINE}" --selftest || die "self-test failed - engine not installed correctly"

# ------------------------------------------------------------------ cache
blue "Rebuilding the IBus registry cache"
rm -rf "${HOME}/.cache/ibus/bus/registry"
ibus write-cache >/dev/null 2>&1 || warn "ibus write-cache failed (not fatal)"

blue "Restarting IBus"
ibus restart >/dev/null 2>&1 || ibus-daemon -drx >/dev/null 2>&1 || \
  warn "could not restart ibus-daemon; log out and back in"

blue "Checking that IBus can see the layout"
if ibus list-engine 2>/dev/null | grep -q "${ENGINE_NAME}"; then
  ibus list-engine 2>/dev/null | grep "${ENGINE_NAME}" | sed 's/^/     /'
else
  warn "IBus still does not list '${ENGINE_NAME}'."
  if [ "$installed_where" = "user" ]; then
    warn "user-level install: LOG OUT AND BACK IN so the session picks up"
    warn "IBUS_COMPONENT_PATH, then run: ibus list-engine | grep ${ENGINE_NAME}"
  else
    warn "run: ${HERE}/doctor.sh"
  fi
fi

# ------------------------------------------------------------------ GNOME
if [ "$ADD_SOURCE" -eq 1 ] && command -v gsettings >/dev/null 2>&1; then
  blue "Adding the layout to GNOME input sources"
  current="$(gsettings get org.gnome.desktop.input-sources sources)"
  case "$current" in
    *"'${ENGINE_NAME}'"*)
      blue "Already present in input sources" ;;
    "@a(ss) []"|"[]")
      gsettings set org.gnome.desktop.input-sources sources "[('ibus', '${ENGINE_NAME}')]" ;;
    *)
      gsettings set org.gnome.desktop.input-sources sources \
        "${current%]}, ('ibus', '${ENGINE_NAME}')]" ;;
  esac
fi

cat <<EOF

$(blue "Done")

Next steps
  1. Open IBus setup:            ibus-setup
     (or GNOME Settings -> Keyboard -> Input Sources -> + -> Other)
  2. Add / select:              "Tamil (custom)"  [ta]
  3. Switch layouts with:       Super + Space
  4. Quick CLI switch:          ibus engine ${ENGINE_NAME}

Type this to check it works:   az sx sz   ->  க சி ச்
Caps Lock + அ gives ஆ, Caps Lock + வ then அ gives வா.

If IBus still does not list the engine:
  ${HERE}/doctor.sh
  (user-level install? log out and back in first)

Listed but types nothing?     ${HERE}/doctor.sh
Engine log:                   ~/.cache/tamil-custom/engine.log
Uninstall with:               ${HERE}/uninstall.sh
EOF
