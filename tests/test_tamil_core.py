# -*- coding: utf-8 -*-
"""Tests for the custom Tamil layout.  Run with:  python3 tests/test_tamil_core.py"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from tamil_core import Composer, type_text  # noqa: E402

FAILS = []


def check(label, got, want):
    if got != want:
        FAILS.append("%-28s got %r  want %r" % (label, got, want))


# ---------------------------------------------------------------- base layer
BASE_CASES = [
    ("q", "\u0BB5"), ("w", "\u0BB4"), ("e", "\u0BB3"), ("r", "\u0B99"),
    ("t", "\u0B9E"), ("y", "\u0BA3"), ("u", "\u0BA8"), ("i", "\u0BAE"),
    ("o", "\u0BA9"), ("p", "\u0B83"),
    ("a", "\u0B95"), ("s", "\u0B9A"), ("d", "\u0B9F"), ("f", "\u0BA4"),
    ("g", "\u0BAA"), ("h", "\u0BB1"), ("j", "\u0BAF"), ("k", "\u0BB0"),
    ("l", "\u0BB2"),
    ("z", "\u0B85"), ("x", "\u0B87"), ("c", "\u0B89"), ("v", "\u0B8E"),
    ("b", "\u0B92"), ("n", "\u0B90"), ("m", "\u0B94"),
]
for key, want in BASE_CASES:
    check("base %s" % key, type_text(key), want)

# ------------------------------------------------------------ shift layer
SHIFT_CASES = [
    ("~a", "\u0B95\u0BCD\u0BB7"),   # க்ஷ
    ("~s", "\u0BB8"),               # ஸ
    ("~d", "\u0BB7"),               # ஷ
    ("~f", "\u0B9C"),               # ஜ
    ("~g", "\u0BB9"),               # ஹ
    ("~z", "\u0BCD"),               # ்
]
for keys, want in SHIFT_CASES:
    check("shift %s" % keys, type_text(keys), want)

# --------------------------------------------------- மெய் + உயிர் table
# consonant key, and the seven short-vowel results from the spec table.
TABLE = [
    ("a", "க் கி கு கெ கொ கை கௌ"),
    ("r", "ங் ஙி ஙு ஙெ ஙொ ஙை ஙௌ"),
    ("s", "ச் சி சு செ சொ சை சௌ"),
    ("t", "ஞ் ஞி ஞு ஞெ ஞொ ஞை ஞௌ"),
    ("d", "ட் டி டு டெ டொ டை டௌ"),
    ("y", "ண் ணி ணு ணெ ணொ ணை ணௌ"),
    ("f", "த் தி து தெ தொ தை தௌ"),
    ("u", "ந் நி நு நெ நொ நை நௌ"),
    ("g", "ப் பி பு பெ பொ பை பௌ"),
    ("i", "ம் மி மு மெ மொ மை மௌ"),
    ("j", "ய் யி யு யெ யொ யை யௌ"),
    ("k", "ர் ரி ரு ரெ ரொ ரை ரௌ"),
    ("l", "ல் லி லு லெ லொ லை லௌ"),
    ("q", "வ் வி வு வெ வொ வை வௌ"),
    ("w", "ழ் ழி ழு ழெ ழொ ழை ழௌ"),
    ("e", "ள் ளி ளு ளெ ளொ ளை ளௌ"),
    ("h", "ற் றி று றெ றொ றை றௌ"),
    ("o", "ன் னி னு னெ னொ னை னௌ"),
]
VOWEL_KEYS = "zxc vbn".replace(" ", "")
for cons_key, row in TABLE:
    want = row.split()
    for vowel_key, expected in zip(VOWEL_KEYS, want):
        check("%s+%s" % (cons_key, vowel_key), type_text(cons_key + vowel_key), expected)

# ------------------------------------------------------- long vowels (caps)
LONG_CASES = [
    ("^z", "ஆ"), ("^x", "ஈ"), ("^c", "ஊ"), ("^v", "ஏ"), ("^b", "ஓ"),
    ("a^z", "கா"),          # க then Caps+அ
    ("q^z", "வா"),          # வ then Caps+அ
    ("q^c", "வூ"),          # வ then Caps+உ
    ("a^x", "கீ"),
    ("a^v", "கே"),
    ("a^b", "கோ"),
    ("s^x", "சீ"),
]
for keys, want in LONG_CASES:
    check("long %s" % keys, type_text(keys), want)

# --------------------------------------------------------------- behaviour
check("space clears pending", type_text("a z"), "க அ")
check("two consonants", type_text("aq"), "கவ")
check("vowel after vowel", type_text("zx"), "அஇ")
check("aytham clears pending", type_text("pz"), "ஃஅ")
check("punctuation passes", type_text("a,"), "க,")
check("digits pass", type_text("1a"), "1க")
check("kSha + vowel", type_text("~ax"), "க்ஷி")
check("stand-alone virama", type_text("~z"), "்")
check("uppercase letter still works", type_text("A"), "க")
check("caps + consonant", type_text("^a"), "க")
check("caps + shift grantha", type_text("^~s"), "ஸ")

# composer state is independent per instance
c1, c2 = Composer(), Composer()
c1.feed("a")
check("isolated state", c2.feed("x"), "இ")

# ------------------------------------------------------------------ report
if FAILS:
    print("\n".join(FAILS))
    print("\n%d test(s) FAILED" % len(FAILS))
    sys.exit(1)

total = len(BASE_CASES) + len(SHIFT_CASES) + len(TABLE) * 7 + len(LONG_CASES) + 13
print("all %d checks passed" % total)
