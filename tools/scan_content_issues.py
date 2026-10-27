import json
import re
import os
import sys

for s in (sys.stdout, sys.stderr):
    if hasattr(s, 'reconfigure'):
        s.reconfigure(encoding='utf-8', errors='replace')

metadata_prefix_pattern = re.compile(r'\[(?:Class\s*)?[IVXLCDM\d\s\-_:\/|a-zA-Z]+\]', re.IGNORECASE)
duplicate_clue_pattern = re.compile(r'(?:visual\s*clue|hint)[\s\S]*?(?:visual\s*clue|hint)', re.IGNORECASE)
placeholder_pattern = re.compile(r'primary\s*fact|group\s*[ab]|category\s*[ab]|application\s*\d', re.IGNORECASE)

# Let's inspect content/ files
for cfile in os.listdir("content"):
    if cfile.endswith(".js"):
        p = os.path.join("content", cfile)
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            cnt = f.read()
            m = metadata_prefix_pattern.findall(cnt)
            if m:
                print(f"Metadata tags found in {cfile}: {len(m)} (e.g. {m[:5]})")
            ph = placeholder_pattern.findall(cnt)
            if ph:
                print(f"Placeholders found in {cfile}: {len(ph)} (e.g. {ph[:5]})")

# Let's check question_bank.js
if os.path.exists("question_bank.js"):
    with open("question_bank.js", "r", encoding="utf-8", errors="ignore") as f:
        cnt = f.read()
        m = metadata_prefix_pattern.findall(cnt)
        if m:
            print(f"Metadata tags found in question_bank.js: {len(m)} (e.g. {m[:5]})")
        ph = placeholder_pattern.findall(cnt)
        if ph:
            print(f"Placeholders found in question_bank.js: {len(ph)} (e.g. {ph[:5]})")
