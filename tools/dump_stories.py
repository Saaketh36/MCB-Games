"""Dump LISTENING_STORIES to JSON so the PowerShell narrator can read it."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from listening_content import LISTENING_STORIES

out = {
    name: {
        "story": entry["story"],
        "audio": entry.get("audio", ""),
        "questions": len(entry["questions"]),
    }
    for name, entry in LISTENING_STORIES.items()
}

json.dump(out, sys.stdout, ensure_ascii=False, indent=1)