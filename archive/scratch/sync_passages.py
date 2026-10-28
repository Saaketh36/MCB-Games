#!/usr/bin/env python3
"""
Sync curated reading passages into full_games_catalog.json, full_games_catalog.js,
and content/class-*.js files so all players have access to rich reading comprehension.
"""

import json
import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from curriculum_reading_passages import READING_PASSAGES

def sync_full_games_catalog():
    cat_json_path = os.path.join(BASE_DIR, "full_games_catalog.json")
    cat_js_path = os.path.join(BASE_DIR, "full_games_catalog.js")

    with open(cat_json_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    updated_count = 0
    for game in catalog:
        gid = game.get("id")
        if gid in READING_PASSAGES:
            rp = READING_PASSAGES[gid]
            game["gameType"] = "Reading Comprehension"
            game["passage"] = rp["passage"]
            game["questions"] = rp["questions"]
            game["desc"] = f"Read the story/essay '{rp['passage']['title']}' and answer comprehension questions."
            game["topic"] = rp["passage"]["topic"]
            updated_count += 1
            print(f"Updated {gid} in full_games_catalog.json: {rp['passage']['title']}")

    with open(cat_json_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Wrote updated {cat_json_path} ({updated_count} passages updated).")

    # Now write full_games_catalog.js
    js_content = "// Full Games Catalog for MyClassboard Games Platform\n"
    js_content += "// 325 Curriculum Games with Full Multi-Modal Question Bank & Reading Studio\n\n"
    js_content += "const FULL_GAMES_CATALOG = " + json.dumps(catalog, indent=2, ensure_ascii=False) + ";\n\n"
    js_content += "if (typeof window !== 'undefined') {\n"
    js_content += "    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n"
    js_content += "    window.GamesCatalog = FULL_GAMES_CATALOG;\n"
    js_content += "}\n"

    with open(cat_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Wrote updated {cat_js_path}.")

def sync_content_files():
    # Sync for play.html content files
    for gid, rp in READING_PASSAGES.items():
        cls_roman = rp["class"]
        content_file = os.path.join(BASE_DIR, "content", f"class-{cls_roman}.js")
        if not os.path.exists(content_file):
            continue

        with open(content_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Find prefix GAME_CONTENT = { ... }
        # Convert passage & questions to JS object
        data_to_inject = {
            "passage": rp["passage"],
            "intro": "📖 " + rp["passage"]["title"] + " (" + rp["passage"]["topic"] + ")",
            "questions": [
                {
                    "q": q["prompt"],
                    "type": q.get("type", "mcq"),
                    "options": q.get("options", []),
                    "answer": q["answer"],
                    "keywords": q.get("keywords", []),
                    "evidenceParagraph": q.get("evidenceParagraph", 0),
                    "explain": q.get("explanation", "")
                }
                for q in rp["questions"]
            ]
        }

        # Check if key exists
        pattern = rf'"{gid}":\s*\{{[^}}]*"questions":\s*\[.*?\]\s*\}}'
        replacement = f'"{gid}": ' + json.dumps(data_to_inject, indent=2, ensure_ascii=False)
        
        # If regex matches, replace it
        if re.search(pattern, text, flags=re.DOTALL):
            new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)
            with open(content_file, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"Updated {gid} in {content_file}")
        else:
            # Fallback insertion
            print(f"Note: {gid} pattern not directly regex replaced in {content_file}, checking...")

if __name__ == "__main__":
    sync_full_games_catalog()
    sync_content_files()
