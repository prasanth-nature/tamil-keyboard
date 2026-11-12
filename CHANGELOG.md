# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- CI now validates the component XML identifiers and version against the engine.
  The previous workflow called the installed-system diagnostic and ignored its
  failure, so it did not actually test the repository template.

## [1.2.0] — 2026-11-12

### Fixed

- Component file is now installed to `/usr/share/ibus/component`, the only
  directory IBus scans. The previous `~/.local/share/ibus/component` location
  made the layout appear in Settings while typing did nothing.

### Added

- `doctor.sh` — eight-section diagnosis (session, bindings, component location,
  name match, layout logic, IBus registry, GNOME sources, engine log).
- `--no-sudo` install mode (`IBUS_COMPONENT_PATH` via `~/.config/environment.d`).
- `--system` install mode for all users.
- Engine log at `~/.cache/tamil-custom/engine.log`.
- Installer verifies `ibus list-engine` and reports the result.
- Registry cache is cleared and rebuilt on install and uninstall.

## [1.1.0] — 2026-11-12

### Fixed

- D-Bus name mismatch: the component declared `org.local.IBus.TamilCustom`
  while the engine claimed `org.freedesktop.IBus.TamilCustom`, so the daemon
  could never attach to the engine process.

### Added

- `--check` flag: prints the component `<name>` and the engine name side by side.
- Startup, name-ownership and first-key-event logging.

## [1.0.0] — 2026-11-12

### Added

- Tamil IBus engine: qwerty key map, consonant + vowel composition,
  Caps Lock long vowels, Shift grantha layer.
- Per-user and system installers.
- `layout-chart.html` generated from the layout data.
- 183-check test suite covering the full மெய் + உயிர் table.

[1.2.0]: https://github.com/prasanth-nature/tamil-keyboard/releases/tag/v1.2.0
[1.1.0]: https://github.com/prasanth-nature/tamil-keyboard/releases/tag/v1.1.0
[1.0.0]: https://github.com/prasanth-nature/tamil-keyboard/releases/tag/v1.0.0
