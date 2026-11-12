#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Generate layout-chart.html straight from tamil_core.py, so the chart can
never drift away from what the engine actually types."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))

from tamil_core import BASE, SHIFT, VIRAMA, type_text  # noqa: E402

ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

LONG_NAME = {"z": "ஆ", "x": "ஈ", "c": "ஊ", "v": "ஏ", "b": "ஓ", "n": "ஐ", "m": "ஔ"}

CONSONANT_KEYS = [
    ("a", "க"), ("r", "ங"), ("s", "ச"), ("t", "ஞ"), ("d", "ட"), ("y", "ண"),
    ("f", "த"), ("u", "ந"), ("g", "ப"), ("i", "ம"), ("j", "ய"), ("k", "ர"),
    ("l", "ல"), ("q", "வ"), ("w", "ழ"), ("e", "ள"), ("h", "ற"), ("o", "ன"),
]
VOWEL_COLS = [("z", "அ", ""), ("x", "இ", ""), ("c", "உ", ""), ("v", "எ", ""),
              ("b", "ஒ", ""), ("n", "ஐ", ""), ("m", "ஔ", ""),
              ("^z", "ஆ", "long"), ("^x", "ஈ", "long"), ("^c", "ஊ", "long"),
              ("^v", "ஏ", "long"), ("^b", "ஓ", "long")]


def keycap(latin, main, extra=""):
    badge = ('<span class="shift">%s</span>' % extra) if extra else ""
    return (
        '<div class="key"><span class="latin">%s</span>'
        '<span class="tamil">%s</span>%s</div>' % (latin, main, badge)
    )


def build_keyboard():
    out = []
    for index, row in enumerate(ROWS):
        caps = []
        for latin in row:
            main = BASE[latin]
            extra = ""
            if latin in SHIFT:
                extra = "⇧ " + SHIFT[latin]
            if latin in LONG_NAME and LONG_NAME[latin] != main:
                extra = (extra + " " if extra else "") + "^ " + LONG_NAME[latin]
            caps.append(keycap(latin.upper(), main, extra.strip()))
        out.append('<div class="kbdrow r%d">%s</div>' % (index, "".join(caps)))
    return "\n".join(out)


def build_table():
    head = "".join(
        '<th class="%s">%s%s</th>' % (kind, name, '<br><small>^</small>' if kind == "long" else "")
        for _, name, kind in VOWEL_COLS
    )
    rows = []
    for key, cons in CONSONANT_KEYS:
        cells = []
        for vkey, _, kind in VOWEL_COLS:
            text = type_text(key + vkey)
            cells.append('<td class="%s">%s</td>' % (kind, text))
        rows.append(
            '<tr><th class="cons">%s<small>%s</small></th>%s</tr>'
            % (cons, key, "".join(cells))
        )
    return (
        '<table class="matrix"><thead><tr><th class="corner">மெய் \\ உயிர்</th>%s</tr></thead>'
        "<tbody>%s</tbody></table>" % (head, "".join(rows))
    )


EXAMPLES = [
    ("az", "க"), ("sz", "ச்"), ("sx", "சி"), ("q^z", "வா"),
    ("q^c", "வூ"), ("^z", "ஆ"), ("~az", "க்ஷ்"), ("~ax", "க்ஷி"),
    ("p", "ஃ"), ("~z", "்"),
]

example_rows = "".join(
    '<tr><td class="mono">%s</td><td class="arrow">→</td><td class="out">%s</td></tr>'
    % (keys.replace("^", "Caps+").replace("~", "Shift+").replace("+", " + "), out)
    for keys, out in EXAMPLES
)

HTML = """<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tamil keyboard layout - AlmaLinux</title>
<style>
  :root {
    --ink: #1b1b1f;
    --muted: #6b6b76;
    --line: #dcdce3;
    --paper: #f6f5f2;
    --card: #ffffff;
    --accent: #a8451f;
    --accent-soft: #f6e6df;
    --long: #eef2f8;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 40px 24px 64px;
    background: var(--paper); color: var(--ink);
    font-family: "Noto Sans Tamil", "Latha", "Nirmala UI", "Tamil Sangam MN",
                 -apple-system, "Segoe UI", Roboto, sans-serif;
    line-height: 1.5;
  }
  .wrap { max-width: 1120px; margin: 0 auto; }
  header { border-bottom: 2px solid var(--ink); padding-bottom: 18px; margin-bottom: 34px; }
  h1 { font-size: 30px; margin: 0 0 6px; letter-spacing: -0.2px; }
  .meta { list-style: none; display: flex; flex-wrap: wrap; gap: 26px; margin: 12px 0 0; padding: 0; }
  .meta li { display: flex; flex-direction: column; gap: 1px; }
  .meta span { color: var(--muted); font-size: 10.5px; text-transform: uppercase; letter-spacing: 1px; }
  .meta b { color: var(--ink); font-weight: 600; font-size: 13.5px; }
  h2 {
    font-size: 15px; text-transform: uppercase; letter-spacing: 1.4px;
    color: var(--accent); margin: 44px 0 14px; font-weight: 700;
  }
  h2 span { color: var(--muted); text-transform: none; letter-spacing: 0; font-weight: 400; }
  .kbd {
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    padding: 18px; display: inline-block;
  }
  .kbdrow { display: flex; gap: 8px; margin-bottom: 8px; }
  .kbdrow.r1 { padding-left: 22px; }
  .kbdrow.r2 { padding-left: 40px; }
  .kbdrow:last-child { margin-bottom: 0; }
  .key {
    position: relative; width: 84px; height: 76px; border-radius: 10px;
    background: #fff; border: 1px solid var(--line);
    box-shadow: 0 2px 0 #d8d8de;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
  }
  .key .latin { position: absolute; top: 4px; left: 7px; font-size: 10px; color: #a3a3ad; font-family: ui-monospace, monospace; }
  .key .tamil { font-size: 27px; line-height: 1; }
  .key .shift { font-size: 10px; color: var(--muted); margin-top: 3px; }
  .legendtab { margin-top: 14px; font-size: 12.5px; color: var(--muted); }
  .legendtab td { padding: 2px 16px 2px 0; vertical-align: top; }
  .legendtab td.mono { color: var(--ink); font-family: ui-monospace, monospace; white-space: nowrap; }
  table { border-collapse: collapse; background: var(--card); font-size: 16px; }
  .matrix { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
  .matrix th, .matrix td {
    border: 1px solid var(--line); padding: 7px 12px; text-align: center; white-space: nowrap;
  }
  .matrix thead th { background: #f1efe9; font-weight: 600; font-size: 15px; }
  .matrix thead th small { color: var(--accent); font-size: 10px; }
  .matrix th.cons { background: #f1efe9; font-size: 20px; position: relative; }
  .matrix th.cons small {
    position: absolute; top: 2px; left: 4px; font-size: 9px; color: #a3a3ad;
    font-family: ui-monospace, monospace; font-weight: 400;
  }
  .matrix th.corner { font-size: 12px; color: var(--muted); font-weight: 500; }
  .matrix td.long, .matrix th.long { background: var(--long); }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; align-items: start; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 18px 20px; }
  .card h3 { margin: 0 0 10px; font-size: 14px; letter-spacing: .4px; text-transform: uppercase; color: var(--muted); }
  ul.rules { margin: 0; padding-left: 20px; font-size: 14.5px; }
  ul.rules li { margin-bottom: 9px; }
  ul.rules code, .mono { font-family: ui-monospace, "DejaVu Sans Mono", monospace; }
  ul.rules code { background: #f1efe9; padding: 1px 5px; border-radius: 4px; font-size: 13px; }
  table.ex { width: 100%; font-size: 15px; }
  table.ex td { border-bottom: 1px dashed var(--line); padding: 6px 8px; }
  table.ex td.mono { font-size: 12.5px; color: var(--muted); width: 44%; }
  table.ex td.arrow { color: var(--accent); width: 8%; }
  table.ex td.out { font-size: 20px; }
  footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--line); font-size: 12.5px; color: var(--muted); }
  @media (max-width: 900px) { .grid2 { grid-template-columns: 1fr; } .kbd { overflow-x: auto; max-width: 100%; } }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>தமிழ் விசைப்பலகை &mdash; Tamil Keyboard Layout</h1>
    <ul class="meta">
      <li><span>System</span><b>AlmaLinux 8 / 9 / 10 &middot; IBus</b></li>
      <li><span>Layout name</span><b>Tamil (custom) &middot; ta</b></li>
      <li><span>Engine id</span><b>tamil-custom</b></li>
      <li><span>Switch</span><b>Super + Space</b></li>
    </ul>
  </header>

  <h2>1 &middot; Key map <span>qwerty &rarr; தமிழ்</span></h2>
  <div class="kbd">
    __KEYBOARD__
  </div>
  <table class="legendtab"><tbody>
    <tr><td class="mono">grey corner</td><td>physical key you press</td></tr>
    <tr><td class="mono">⇧</td><td>hold Shift</td></tr>
    <tr><td class="mono">^</td><td>Caps Lock on (நெடில்)</td></tr>
  </tbody></table>

  <h2>2 &middot; மெய் + உயிர் <span>consonant + vowel &rarr; one letter</span></h2>
  <div class="kbd" style="padding:22px">
    __MATRIX__
  </div>
  <table class="legendtab"><tbody>
    <tr><td class="mono">white</td><td>consonant key, then the vowel key</td></tr>
    <tr><td class="mono">blue</td><td>same, with Caps Lock on (நெடில்)</td></tr>
  </tbody></table>

  <div class="grid2" style="margin-top:44px">
    <div class="card">
      <h3>Rules</h3>
      <ul class="rules">
        <li>A consonant key alone gives the bare letter: <code>a</code> &rarr; க</li>
        <li>The <b>next</b> vowel key becomes its sign: <code>a</code> <code>x</code> &rarr; கி</li>
        <li><code>அ</code> after a consonant gives the pulli: <code>a</code> <code>z</code> &rarr; க்</li>
        <li><b>Caps Lock</b> makes the vowel long: <code>^z</code> &rarr; ஆ, <code>q</code> <code>^z</code> &rarr; வா</li>
        <li><b>Shift</b> gives the grantha letters: ஸ ஷ ஜ ஹ க்ஷ, and <code>⇧z</code> is a lone ்</li>
        <li>Space, digits, punctuation and Ctrl/Alt shortcuts pass straight through</li>
      </ul>
    </div>
    <div class="card">
      <h3>Examples</h3>
      <table class="ex"><tbody>__EXAMPLES__</tbody></table>
    </div>
  </div>

  <footer>
    <ul>
      <li>Generated from <span class="mono">tamil_core.py</span></li>
      <li>Every cell above is produced by the same code the engine runs</li>
      <li>Full install and usage tables: <span class="mono">README.md</span></li>
    </ul>
  </footer>
</div>
</body>
</html>
"""


def main():
    html = (
        HTML.replace("__KEYBOARD__", build_keyboard())
        .replace("__MATRIX__", build_table())
        .replace("__EXAMPLES__", example_rows)
    )
    out = os.path.join(ROOT, "layout-chart.html")
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(html)
    print("wrote %s (%d bytes)" % (out, len(html.encode("utf-8"))))


if __name__ == "__main__":
    main()
