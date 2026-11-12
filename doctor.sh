#!/usr/bin/env bash
# Diagnose "the layout is listed but typing does nothing".
#   ./doctor.sh
# Every line is PASS / FAIL / INFO.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_NAME="tamil-custom"
BUS_NAME="org.local.IBus.TamilCustom"
ENGINE="${HOME}/.local/share/tamil-keyboard/ibus-engine-tamil-custom"
[ -x "/usr/local/share/tamil-keyboard/ibus-engine-tamil-custom" ] && \
  ENGINE="/usr/local/share/tamil-keyboard/ibus-engine-tamil-custom"
SYS_COMPONENT="/usr/share/ibus/component/${ENGINE_NAME}.xml"
USR_COMPONENT="${HOME}/.local/share/ibus/component/${ENGINE_NAME}.xml"
LOG="${HOME}/.cache/tamil-custom/engine.log"

pass() { printf 'PASS  %s\n' "$*"; }
fail() { printf 'FAIL  %s\n' "$*"; }
info() { printf 'INFO  %s\n' "$*"; }
head2() { printf '\n== %s ==\n' "$*"; }

head2 "session"
info "XDG_SESSION_TYPE=${XDG_SESSION_TYPE:-unknown}"
info "DESKTOP=${XDG_CURRENT_DESKTOP:-unknown}"
if command -v ibus >/dev/null 2>&1; then
  info "ibus version: $(ibus version 2>/dev/null | head -1)"
else
  fail "ibus command not found (sudo dnf install -y ibus)"
fi
pgrep -x ibus-daemon >/dev/null 2>&1 && pass "ibus-daemon is running" \
  || fail "ibus-daemon is NOT running (ibus-daemon -drx)"

head2 "python bindings"
if python3 - <<'PY' >/dev/null 2>&1
import gi
gi.require_version("IBus", "1.0")
from gi.repository import IBus
PY
then pass "IBus Python bindings load"
else fail "IBus Python bindings missing (sudo dnf install -y ibus ibus-libs python3-gobject)"
fi

head2 "component location"
# IBus only scans /usr/share/ibus/component unless IBUS_COMPONENT_PATH says
# otherwise. The ~/.local/share/ibus/component scan is compiled out.
if [ -f "$SYS_COMPONENT" ]; then
  pass "system component: $SYS_COMPONENT"
elif [ -f "$USR_COMPONENT" ]; then
  fail "component is ONLY in $USR_COMPONENT - IBus does not scan that directory"
  info "fix: sudo install -m 644 \"$USR_COMPONENT\" \"$SYS_COMPONENT\""
  info "     then: rm -rf ~/.cache/ibus/bus/registry && ibus write-cache && ibus restart"
else
  fail "no component file found in $SYS_COMPONENT or $USR_COMPONENT"
  info "fix: re-run ./install.sh"
fi
info "IBUS_COMPONENT_PATH=${IBUS_COMPONENT_PATH:-<unset>}"
if grep -rqs "IBUS_COMPONENT_PATH" "${HOME}/.config/environment.d/" 2>/dev/null; then
  info "environment.d override present (needs a re-login to take effect):"
  grep -rhs "IBUS_COMPONENT_PATH" "${HOME}/.config/environment.d/" 2>/dev/null | sed 's/^/      /'
fi

head2 "installed files"
[ -f "$ENGINE" ] && pass "engine present: $ENGINE" || fail "engine missing: $ENGINE"
[ -x "$ENGINE" ] && pass "engine is executable" || fail "engine is not executable (chmod +x \"$ENGINE\")"

head2 "component vs engine name (must match)"
[ -x "$ENGINE" ] && "$ENGINE" --check 2>&1 | sed 's/^/      /'

head2 "layout logic"
[ -x "$ENGINE" ] && "$ENGINE" --selftest 2>&1 | sed 's/^/      /'

head2 "IBus registry"
if command -v ibus >/dev/null 2>&1; then
  if ibus list-engine 2>/dev/null | grep -q "${ENGINE_NAME}"; then
    pass "IBus lists the engine:"
    ibus list-engine 2>/dev/null | grep "${ENGINE_NAME}" | sed 's/^/      /'
  else
    fail "IBus does not list '${ENGINE_NAME}'"
    info "try, in this order:"
    info "  1. sudo install -m 644 $SYS_COMPONENT /usr/share/ibus/component/   (if only user-level)"
    info "  2. rm -rf ~/.cache/ibus/bus/registry"
    info "  3. ibus write-cache"
    info "  4. ibus restart"
    info "  5. log out and back in"
  fi
  info "current engine: $(ibus engine 2>/dev/null)"
  info "cache entries: $(ibus read-cache 2>/dev/null | grep -c "${ENGINE_NAME}" || true)"
fi

head2 "GNOME input sources"
command -v gsettings >/dev/null 2>&1 && \
  gsettings get org.gnome.desktop.input-sources sources 2>/dev/null | sed 's/^/      /'

head2 "engine log"
if [ -f "$LOG" ]; then
  tail -25 "$LOG" | sed 's/^/      /'
  grep -q "first key event reached the engine" "$LOG" \
    && pass "the engine HAS received key events" \
    || info "no key event logged yet - switch to the layout and type a few letters"
  grep -q "request_name.*-> False\|not connected" "$LOG" \
    && fail "the engine could not own ${BUS_NAME}"
else
  info "no log yet at $LOG (the engine has never started)"
fi

head2 "next"
info "Listed in Settings but nothing types? -> the entry is stale:"
info "  remove the input source, then: ibus engine ${ENGINE_NAME}"
info "Nothing in 'IBus registry'? -> component is in the wrong directory (see above)."
