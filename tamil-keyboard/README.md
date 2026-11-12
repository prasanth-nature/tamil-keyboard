# தமிழ் விசைப்பலகை · Tamil Keyboard Layout

**A custom Tamil IBus input method for AlmaLinux, RHEL, and Fedora. It uses a dedicated QWERTY-based composition map rather than Tamil99.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-AlmaLinux%20%7C%20RHEL%20%7C%20Fedora-informational)](https://almalinux.org)
[![Input method](https://img.shields.io/badge/input%20method-IBus-green)](https://github.com/ibus/ibus)
[![Tests](https://github.com/prasanth-nature/tamil-keyboard/actions/workflows/tests.yml/badge.svg)](https://github.com/prasanth-nature/tamil-keyboard/actions/workflows/tests.yml)

---

## Table of contents

| § | Section |
| --- | --- |
| 1 | [What it is](#1--what-it-is) |
| 2 | [Key map](#2--key-map) |
| 3 | [How typing works](#3--how-typing-works) |
| 4 | [மெய் + உயிர் table](#4--மெய்--உயிர்-table) |
| 5 | [Caps Lock and Shift](#5--caps-lock-and-shift) |
| 6 | [Install](#6--install) |
| 7 | [Switching layouts](#7--switching-layouts) |
| 8 | [Troubleshooting](#8--troubleshooting) |
| 9 | [Why an IBus engine and not an XKB layout](#9--why-an-ibus-engine-and-not-an-xkb-layout) |
| 10 | [Development](#10--development) |
| 11 | [Repository layout](#11--repository-layout) |
| 12 | [License](#12--license) |

---

## 1 · What it is

| Item | Value |
| --- | --- |
| Engine id | `tamil-custom` |
| Name in settings | **Tamil (custom)** — language `ta` |
| Type | IBus input method |
| Designed for | AlmaLinux 8 / 9 / 10, RHEL 8+, Fedora, and GNOME on Wayland or X11 |
| Packages needed | `ibus`, `ibus-libs`, `python3-gobject` |
| Root needed | once — one file in `/usr/share/ibus/component/` |
| Does not work in | plain TTY / console (IBus needs a graphical session) |
| Visual reference | [`layout-chart.html`](layout-chart.html) |

- The 26 QWERTY letter keys cover the 18 Tamil consonants, all 12 vowels, and ஃ; Shift adds ஸ, ஷ, ஜ, ஹ, க்ஷ, and a stand-alone pulli.
- A consonant followed by a vowel key becomes one letter — no virama juggling.
- Caps Lock is the long-vowel switch (நெடில்), alone or after a consonant.
- The layout is data, not code: four dictionaries in [`src/tamil_core.py`](src/tamil_core.py).

---

## 2 · Key map

| Row | Physical keys | Tamil |
| --- | --- | --- |
| Top | `q w e r t y u i o p` | வ ழ ள ங ஞ ண ந ம ன ஃ |
| Home | `a s d f g h j k l` | க ச ட த ப ற ய ர ல |
| Bottom | `z x c v b n m` | அ இ உ எ ஒ ஐ ஔ |

| Key | Base | Shift | Caps Lock |
| --- | --- | --- | --- |
| `q` | வ | — | — |
| `w` | ழ | — | — |
| `e` | ள | — | — |
| `r` | ங | — | — |
| `t` | ஞ | — | — |
| `y` | ண | — | — |
| `u` | ந | — | — |
| `i` | ம | — | — |
| `o` | ன | — | — |
| `p` | ஃ | — | — |
| `a` | க | க்ஷ | — |
| `s` | ச | ஸ | — |
| `d` | ட | ஷ | — |
| `f` | த | ஜ | — |
| `g` | ப | ஹ | — |
| `h` | ற | — | — |
| `j` | ய | — | — |
| `k` | ர | — | — |
| `l` | ல | — | — |
| `z` | அ | ் (lone pulli) | ஆ |
| `x` | இ | — | ஈ |
| `c` | உ | — | ஊ |
| `v` | எ | — | ஏ |
| `b` | ஒ | — | ஓ |
| `n` | ஐ | — | ஐ |
| `m` | ஔ | — | ஔ |

---

## 3 · How typing works

| # | Rule | Example |
| --- | --- | --- |
| 1 | A consonant key types the bare letter | `a` → க |
| 2 | The **next** vowel key becomes that consonant's sign | `a` `x` → கி |
| 3 | `அ` after a consonant gives the pulli (virama) | `a` `z` → க் |
| 4 | **Caps Lock** makes the vowel long (நெடில்) | `^z` → ஆ · `q` `^z` → வா |
| 5 | **Shift** gives the grantha letters | `⇧s` → ஸ · `⇧a` → க்ஷ |
| 6 | `க்ஷ` behaves like a consonant | `⇧a` `x` → க்ஷி |
| 7 | Caps Lock never changes consonants | `^a` → க |
| 8 | Space, digits, punctuation, arrows and Ctrl/Alt clear the pending consonant and pass through | `a` `space` `z` → க அ |

> `^` in this README means "Caps Lock is on" — it is not a key you press.

---

## 4 · மெய் + உயிர் table

White = normal key. **Bold** = Caps Lock on.

| மெய் \ உயிர் | அ | இ | உ | எ | ஒ | ஐ | ஔ | **ஆ** | **ஈ** | **ஊ** | **ஏ** | **ஓ** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| க `a` | க் | கி | கு | கெ | கொ | கை | கௌ | **கா** | **கீ** | **கூ** | **கே** | **கோ** |
| ங `r` | ங் | ஙி | ஙு | ஙெ | ஙொ | ஙை | ஙௌ | **ஙா** | **ஙீ** | **ஙூ** | **ஙே** | **ஙோ** |
| ச `s` | ச் | சி | சு | செ | சொ | சை | சௌ | **சா** | **சீ** | **சூ** | **சே** | **சோ** |
| ஞ `t` | ஞ் | ஞி | ஞு | ஞெ | ஞொ | ஞை | ஞௌ | **ஞா** | **ஞீ** | **ஞூ** | **ஞே** | **ஞோ** |
| ட `d` | ட் | டி | டு | டெ | டொ | டை | டௌ | **டா** | **டீ** | **டூ** | **டே** | **டோ** |
| ண `y` | ண் | ணி | ணு | ணெ | ணொ | ணை | ணௌ | **ணா** | **ணீ** | **ணூ** | **ணே** | **ணோ** |
| த `f` | த் | தி | து | தெ | தொ | தை | தௌ | **தா** | **தீ** | **தூ** | **தே** | **தோ** |
| ந `u` | ந் | நி | நு | நெ | நொ | நை | நௌ | **நா** | **நீ** | **நூ** | **நே** | **நோ** |
| ப `g` | ப் | பி | பு | பெ | பொ | பை | பௌ | **பா** | **பீ** | **பூ** | **பே** | **போ** |
| ம `i` | ம் | மி | மு | மெ | மொ | மை | மௌ | **மா** | **மீ** | **மூ** | **மே** | **மோ** |
| ய `j` | ய் | யி | யு | யெ | யொ | யை | யௌ | **யா** | **யீ** | **யூ** | **யே** | **யோ** |
| ர `k` | ர் | ரி | ரு | ரெ | ரொ | ரை | ரௌ | **ரா** | **ரீ** | **ரூ** | **ரே** | **ரோ** |
| ல `l` | ல் | லி | லு | லெ | லொ | லை | லௌ | **லா** | **லீ** | **லூ** | **லே** | **லோ** |
| வ `q` | வ் | வி | வு | வெ | வொ | வை | வௌ | **வா** | **வீ** | **வூ** | **வே** | **வோ** |
| ழ `w` | ழ் | ழி | ழு | ழெ | ழொ | ழை | ழௌ | **ழா** | **ழீ** | **ழூ** | **ழே** | **ழோ** |
| ள `e` | ள் | ளி | ளு | ளெ | ளொ | ளை | ளௌ | **ளா** | **ளீ** | **ளூ** | **ளே** | **ளோ** |
| ற `h` | ற் | றி | று | றெ | றொ | றை | றௌ | **றா** | **றீ** | **றூ** | **றே** | **றோ** |
| ன `o` | ன் | னி | னு | னெ | னொ | னை | னௌ | **னா** | **னீ** | **னூ** | **னே** | **னோ** |

Every cell above is asserted in [`tests/test_tamil_core.py`](tests/test_tamil_core.py).

---

## 5 · Caps Lock and Shift

| Short | Long (Caps) | Sign after a consonant |
| --- | --- | --- |
| அ | ஆ | ா → கா |
| இ | ஈ | ீ → கீ |
| உ | ஊ | ூ → கூ |
| எ | ஏ | ே → கே |
| ஒ | ஓ | ோ → கோ |
| ஐ | ஐ | ை → கை |
| ஔ | ஔ | ௌ → கௌ |

| Shift + | Gives |
| --- | --- |
| `a` | க்ஷ |
| `s` | ஸ |
| `d` | ஷ |
| `f` | ஜ |
| `g` | ஹ |
| `z` | ் (stand-alone pulli) |

- ஷ ஸ ஜ ஹ க்ஷ had no keys in the original design, so they sit on the Shift layer of the phonetically closest keys.
- Move them by editing `SHIFT` in [`src/tamil_core.py`](src/tamil_core.py).

---

## 6 · Install

### Requirements

```bash
sudo dnf install -y ibus ibus-libs python3-gobject
```

Already present on a GNOME Workstation install.

### Steps

| # | Command / action |
| --- | --- |
| 1 | `git clone https://github.com/prasanth-nature/tamil-keyboard.git` |
| 2 | `cd tamil-keyboard` |
| 3 | `./install.sh --add-source` — asks for your password once |
| 4 | Settings → Keyboard → Input Sources → add **Tamil (custom)** |
| 5 | Type `az sx sz` → க சி ச் |

### Installer flags

| Flag | Effect |
| --- | --- |
| `--add-source` | also adds the layout to GNOME input sources |
| `--no-sudo` | everything under `$HOME` + `IBUS_COMPONENT_PATH` override; requires a re-login |
| `--system` | engine in `/usr/local/share`, for every user on the machine |

### What gets installed

| Path | Contents |
| --- | --- |
| `/usr/share/ibus/component/tamil-custom.xml` | registers the engine — the only directory IBus scans |
| `~/.local/share/tamil-keyboard/ibus-engine-tamil-custom` | the engine |
| `~/.local/share/tamil-keyboard/tamil_core.py` | the layout rules |
| `~/.local/share/tamil-keyboard/doctor.sh` | diagnostics |
| `~/.config/environment.d/ibus-tamil-custom.conf` | only in `--no-sudo` mode |
| `~/.cache/tamil-custom/engine.log` | runtime log |

---

## 7 · Switching layouts

| Action | How |
| --- | --- |
| Toggle | <kbd>Super</kbd> + <kbd>Space</kbd> |
| Jump directly | `ibus engine tamil-custom` |
| Confirm active | panel indicator shows **த** |

---

## 8 · Troubleshooting

Run this first — it checks all eight things that can break:

```bash
./doctor.sh
```

| Symptom | Cause | Fix |
| --- | --- | --- |
| `ibus list-engine` does not show `tamil-custom` | component is in `~/.local/share/ibus/component`, which IBus never scans | `sudo install -m 644 ~/.local/share/ibus/component/tamil-custom.xml /usr/share/ibus/component/` then `rm -rf ~/.cache/ibus/bus/registry && ibus write-cache && ibus restart` |
| Listed but typing does nothing | stale input-source entry | remove the source, `ibus restart`, add it again |
| Entry reads `tamil-custom`, not **Tamil (custom)** | component and engine disagree on the D-Bus name | reinstall v1.1 or newer |
| Nothing types at all | engine never started | `~/.local/share/tamil-keyboard/ibus-engine-tamil-custom --ibus` — it prints the reason |
| Types Latin letters | engine not selected | `ibus engine tamil-custom` |
| Terminal apps ignore the layout | missing IM env vars | `GTK_IM_MODULE=ibus`, `QT_IM_MODULE=ibus`, `XMODIFIERS=@im=ibus` |
| Caps Lock does nothing | Caps Lock remapped to Ctrl | Settings → Keyboard → View and Customise Shortcuts |
| Console / TTY | IBus needs a graphical session | not supported |

Engine log: `~/.cache/tamil-custom/engine.log`.

---

## 9 · Why an IBus engine and not an XKB layout

| Option | Verdict |
| --- | --- |
| XKB symbols file | cannot do it — a keypress must be remembered and combined with the next one (ச + இ → சி); XKB has no state machine |
| Compose file + dead keys | one dead key per consonant would need 18 custom keysyms, and Caps Lock as a long-vowel modifier still would not work |
| IBus engine (this repo) | full state machine, Caps Lock aware, ~150 lines of layout data plus a thin engine |

---

## 10 · Development

| Task | Command |
| --- | --- |
| Run the layout test suite (183 checks) | `python3 tests/test_tamil_core.py` |
| Engine self-test (no IBus needed) | `python3 src/ibus-engine-tamil-custom --selftest` |
| Validate component metadata (6 checks) | `python3 tests/test_component.py` |
| Check shell script syntax | `bash -n install.sh && bash -n uninstall.sh && bash -n doctor.sh` |
| Regenerate the visual chart | `python3 tools/build_chart.py` |
| Diagnose a live install | `./doctor.sh` |

### Editing the layout

| File | Dictionary | Controls |
| --- | --- | --- |
| `src/tamil_core.py` | `BASE` | qwerty key → Tamil letter |
| `src/tamil_core.py` | `SHIFT` | Shift layer |
| `src/tamil_core.py` | `INDEPENDENT` | short / long vowels |
| `src/tamil_core.py` | `SIGNS` | vowel signs (matras) |

- After editing: `./install.sh && ibus restart`.
- `layout-chart.html` is generated from the same code, so it cannot drift.
- CI runs the layout, engine, and component checks; it also checks shell syntax and fails if the committed chart is out of date.

---

## 11 · Repository layout

| Path | Purpose |
| --- | --- |
| `install.sh` | installer |
| `uninstall.sh` | remover |
| `doctor.sh` | 8-section diagnosis for "listed but does not type" |
| `component/tamil-custom.xml.in` | IBus component template |
| `src/tamil_core.py` | all layout rules, no IBus dependency |
| `src/ibus-engine-tamil-custom` | the IBus engine |
| `tests/test_tamil_core.py` | 183 layout checks, including the full மெய்+உயிர் table |
| `tests/test_component.py` | validates component XML identifiers and version against the engine |
| `tools/build_chart.py` | generates `layout-chart.html` |
| `layout-chart.html` | visual key map |
| `.github/workflows/tests.yml` | CI |

---

## 12 · License

MIT — see [LICENSE](LICENSE).

Changelog: [CHANGELOG.md](CHANGELOG.md).
