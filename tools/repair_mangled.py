"""
Repairs the fact entries mangled by the earlier term/distractor swap.

Goal state for every repaired entry:

    F(<correct answer>, <question>, (<original wrong answer>, ...), <why>)

The correct answer is the distractor that the explanation names. The original
wrong answer is recovered from the @@...@@ marker left in the term position.

Run:  python tools\\repair_mangled.py [--dry]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "question_content.py")
MARKER = re.compile(r"@@(.*?)@@", re.S)


def flat(text):
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).split())


def lit(value):
    if '"' in value:
        return "'" + value + "'"
    return '"' + value + '"'


def split_args(text):
    args, buf, depth, quote = [], [], 0, None
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch in "([{":
            depth += 1
            buf.append(ch)
        elif ch in ")]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            args.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        args.append("".join(buf).strip())
    return args


def unquote(text):
    text = text.strip()
    if len(text) >= 2 and text[0] in "\"'" and text[-1] == text[0]:
        return text[1:-1].replace("\\" + text[0], text[0]).replace("\\\\", "\\")
    return text


def find_correct(why, items, old):
    """The distractor the explanation names is the intended answer."""
    why_flat = flat(why)
    for item in items:
        if item == old:
            continue
        f = flat(item)
        if f and f in why_flat:
            return item
    remaining = [i for i in items if i != old]
    return remaining[0] if len(remaining) == 1 else None


def paren_delta(text):
    """Net bracket depth, ignoring brackets that appear inside string literals."""
    depth = 0
    quote = None
    for ch in text:
        if quote:
            if ch == "\\":
                continue
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
    return depth


def main():
    dry = "--dry" in sys.argv
    lines = open(TARGET, encoding="utf-8").readlines()

    out = []
    i = 0
    fixed = skipped = 0

    while i < len(lines):
        line = lines[i]
        if not re.match(r"^\s*F\(", line):
            out.append(line)
            i += 1
            continue

        # Gather the whole call across lines.
        chunk = [line]
        depth = paren_delta(line)
        j = i
        while depth > 0 and j + 1 < len(lines):
            j += 1
            chunk.append(lines[j])
            depth += paren_delta(chunk[-1])
        call = "".join(chunk)

        m = re.search(r"F\((.*)\),\s*$", call, re.S)
        body = m.group(1) if m else call[call.index("(") + 1:call.rindex(")")]
        args = split_args(body)

        if len(args) >= 4:
            term_raw = args[0]
            marker = MARKER.search(term_raw)
            q_text = unquote(args[1])
            items = [x or y for x, y in
                     re.findall(r'"([^"]*)"|\'([^\']*)\'', args[2])]
            why = unquote(args[3])

            old = unquote(marker.group(1)) if marker else unquote(term_raw)
            needs = marker is not None or (old in items)
            if needs and items:
                correct = find_correct(why, items, old)
                if correct:
                    new_items = [old] + [c for c in items if c != correct]
                    rebuilt = (
                        f"    F({lit(correct)},\n"
                        f"      {args[1].strip()},\n"
                        f"      (" + ", ".join(lit(s) for s in new_items) + "),\n"
                        f"      {args[3].strip()}),\n"
                    )
                    out.append(rebuilt)
                    fixed += 1
                    i = j + 1
                    continue
                skipped += 1
        else:
            skipped += 1

        out.extend(chunk)
        i = j + 1

    print(f"repaired: {fixed}   skipped: {skipped}")
    if not dry:
        open(TARGET, "w", encoding="utf-8").writelines(out)
        print("written")


if __name__ == "__main__":
    main()