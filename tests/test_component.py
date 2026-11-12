#!/usr/bin/env python3
"""Check that the IBus component template agrees with the engine metadata."""

import ast
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "src" / "ibus-engine-tamil-custom"
TEMPLATE = ROOT / "component" / "tamil-custom.xml.in"


def read_engine_constants():
    tree = ast.parse(ENGINE.read_text(encoding="utf-8"), filename=str(ENGINE))
    wanted = {"VERSION", "ENGINE_NAME", "BUS_NAME"}
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [target.id for target in node.targets
                 if isinstance(target, ast.Name) and target.id in wanted]
        if names:
            value = ast.literal_eval(node.value)
            for name in names:
                found[name] = value
    missing = wanted - found.keys()
    if missing:
        raise AssertionError("missing engine constants: " + ", ".join(sorted(missing)))
    return found


def main():
    constants = read_engine_constants()
    root = ET.parse(TEMPLATE).getroot()
    engines = root.findall("./engines/engine")

    checks = [
        (root.tag == "component", "template root is <component>"),
        (root.findtext("name") == constants["BUS_NAME"], "D-Bus component name matches BUS_NAME"),
        (len(engines) == 1, "template declares exactly one engine"),
        (len(engines) == 1 and engines[0].findtext("name") == constants["ENGINE_NAME"],
         "IBus engine name matches ENGINE_NAME"),
        (root.findtext("version") == constants["VERSION"], "component and engine versions match"),
        ("@ENGINE_EXEC@" in (root.findtext("exec") or ""), "installer placeholder is present"),
    ]

    failures = [label for passed, label in checks if not passed]
    if failures:
        for label in failures:
            print("FAIL: " + label)
        print("%d component check(s) failed" % len(failures))
        return 1

    print("all %d component checks passed" % len(checks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
