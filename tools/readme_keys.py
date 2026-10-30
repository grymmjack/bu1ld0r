#!/usr/bin/env python3
"""The README's Keys section, made from the in-program HELP (UI/UI.BM).

    python3 tools/readme_keys.py          # print it
    python3 tools/readme_keys.py --write  # replace it in README.md (between the keys markers)

HELP is written as `HelpTopic "NAME"`, then `HelpAdd "KEYS|what it does"` rows
and `HelpAdd "#HEADING"` lines; each topic becomes a fold-out of tables.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- keys:start -->", "<!-- keys:end -->"


def keys_md():
    out, table = [], False

    def end_table():
        nonlocal table
        if table:
            out.append("")
            table = False

    for line in open(os.path.join(ROOT, "UI", "UI.BM"), encoding="utf-8"):
        m = re.match(r'\s*HelpTopic "(.*)"\s*$', line)
        if m:
            end_table()
            if out:
                out.append("</details>\n")
            out.append(f"<details>\n<summary><b>{m.group(1)}</b></summary>\n")
            continue
        m = re.match(r'\s*HelpAdd "(.*)"\s*$', line)
        if not m:
            continue
        s = m.group(1)
        if s.startswith("#"):
            end_table()
            out.append(f"#### {s[1:]}\n")
        elif "|" in s:
            k, t = s.split("|", 1)
            if not table:
                out.append("| Keys | What it does |\n|---|---|")
                table = True
            k = re.sub(r"\s{2,}", " / ", k.strip().replace("  or  ", " or "))
            out.append(f"| {k} | {t} |")
        else:
            end_table()
            out.append(s + "\n")
    end_table()
    out.append("</details>")
    return "\n".join(out)


if __name__ == "__main__":
    md = keys_md()
    if "--write" not in sys.argv:
        print(md)
        sys.exit(0)
    path = os.path.join(ROOT, "README.md")
    r = open(path, encoding="utf-8").read()
    a, b = r.find(START), r.find(END)
    if a < 0 or b < a:
        sys.exit(f"README.md has no {START} ... {END} markers")
    open(path, "w", encoding="utf-8").write(r[: a + len(START)] + "\n" + md + "\n" + r[b:])
    print("README.md: Keys section updated")
