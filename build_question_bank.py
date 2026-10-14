"""
Question bank builder for MyClassboard Games.

Replaces the old keyword-matching generator (which collapsed all 325 activities
onto ~20 recycled question pairs). Content now comes from explicit, hand-authored
fact banks in `question_content.py`, keyed by (subject, skill_area).

Each fact yields up to two distinct questions:
  form 0 - direct:      "<question>"                     -> pick the term
  form 1 - clue-based:  "Which term matches: <why>"      -> pick the term

Activities are assigned facts deterministically, so rebuilding the bank always
produces byte-identical output (no random churn between runs).
"""

import hashlib
import json
import os

from games_data import CURRICULUM_DATA
from question_content import FACT_BANK, SUBJECT_FALLBACK
from listening_content import get_audio, get_story, has_story, LISTENING_STORIES
from odd_one_out_build import build_questions as build_odd_questions

QUESTIONS_PER_ACTIVITY = 3
BANK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "question_bank.js")


def _seed(*parts):
    return int(hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:12], 16)


def _pool_for(subject, skill_area):
    return FACT_BANK.get((subject, skill_area)) or SUBJECT_FALLBACK.get(subject) or []


def _is_listening(activity):
    haystack = " ".join([
        activity.get("skill_area", ""),
        activity.get("sub_skill_area", ""),
        activity.get("activity_name", ""),
    ]).lower()
    return any(k in haystack for k in (
        "listen", "hearing", "announcement", "podcast", "audio",
        "sound", "radio", "news", "speech",
    ))


def _make_question(activity, fact, form, pool_whys):
    cls = activity["class"]
    subject = activity["subject"]
    sub = activity["sub_skill_area"]
    name = activity["activity_name"]
    tag = f"[{cls} {subject} - {name}]"

    if form == 0:
        stem = f"{tag} {fact['q']}"
        options, answer = _shuffled_options(_seed(cls, subject, sub, name, fact["t"], 0), fact["t"], fact["d"])
        explanation = fact["w"]
    elif fact["t"] in fact["w"]:
        # Cloze form: blank the term inside its own explanation so the stem
        # never spells out the answer.
        cloze = fact["w"].replace(fact["t"], "_____", 1)
        stem = f"{tag} Complete the statement: {cloze}"
        options, answer = _shuffled_options(_seed(cls, subject, sub, name, fact["t"], 1), fact["t"], fact["d"])
        explanation = fact["w"]
    else:
        # The explanation does not contain the term, so quoting it as a clue
        # cannot give the answer away.
        stem = f"{tag} Which term matches this description? {fact['w']}"
        options, answer = _shuffled_options(_seed(cls, subject, sub, name, fact["t"], 1), fact["t"], fact["d"])
        explanation = fact["w"]

    return {
        "question": stem,
        "options": options,
        "answer": answer,
        "explanation": explanation,
    }


def _shuffled_options(rng_seed, correct, distractors):
    """Place the correct answer at a varying position so 'always A' is not learnable."""
    items = [correct] + list(distractors)
    r = rng_seed % len(items)
    rotated = items[r:] + items[:r]
    labels = ["A", "B", "C", "D"]
    options = [f"Option {labels[i]}: {t}" for i, t in enumerate(rotated)]
    answer = f"Option {labels[rotated.index(correct)]}: {correct}"
    return options, answer


def build_bank():
    """Return {bank_key: payload} for every curriculum activity."""
    groups = {}
    for a in CURRICULUM_DATA:
        groups.setdefault((a["subject"], a["skill_area"]), []).append(a)

    bank = {}
    for (subject, skill_area), activities in groups.items():
        pool = _pool_for(subject, skill_area)
        activities = sorted(activities, key=lambda a: (a["class"], a["activity_name"]))

        for activity in activities:
            # An Odd One Out activity is a picture task, not a fact-bank quiz:
            # the student taps the picture that does not belong.
            odd_q = build_odd_questions(activity)
            if odd_q:
                bank[_key(activity)] = _payload(activity, odd_q)
                continue
            # A listening activity with an authored passage uses that passage
            # and its own comprehension questions.
            if _is_listening(activity) and has_story(activity["activity_name"]):
                payload = _story_questions(activity)
                if payload:
                    bank[_key(activity)] = payload

        pending = [a for a in activities if _key(a) not in bank]
        if not pending:
            continue

        if not pool:
            for a in pending:
                bank[_key(a)] = _placeholder(a)
            continue

        # Each fact yields two distinct questions (direct form and clue form).
        # Build (fact, form) slots so every distinct question is used once before
        # anything repeats - this keeps sibling activities genuinely different.
        slots = [(i, form) for i in range(len(pool)) for form in (0, 1)]
        slots.sort(key=lambda s: _seed(subject, skill_area, s[0], s[1]))
        pool_whys = [f["w"] for f in pool]

        cursor = 0
        for activity in pending:
            questions = []
            for _ in range(QUESTIONS_PER_ACTIVITY):
                if cursor >= len(slots):
                    cursor = 0
                fact_index, form = slots[cursor]
                cursor += 1
                questions.append(_make_question(activity, pool[fact_index], form, pool_whys))
            bank[_key(activity)] = _payload(activity, questions)

    return bank


def _story_questions(activity):
    """Listening activities use a real passage and questions taken from it."""
    story, questions = get_story(activity["activity_name"])
    if not story:
        return None
    cls = activity["class"]
    subject = activity["subject"]
    name = activity["activity_name"]
    tag = f"[{cls} {subject} - {name}]"
    # Picture questions are too abstract for the youngest classes, so Class I
    # and Class II get the plain text questions only.
    show_image = cls not in ("Class I", "Class II")
    built = []
    for q in questions:
        options, answer = _shuffled_options(
            _seed(cls, subject, name, q["question"]),
            q["answer"],
            [o for o in q["options"] if o != q["answer"]],
        )
        built.append({
            "question": f"{tag} {q['question']}",
            "options": options,
            "answer": answer,
            "explanation": q["explanation"],
            "image": q.get("image", "") if show_image else "",
        })
    return {
        "title": name,
        "audio_script": story,
        "audio": get_audio(name),
        "audio_seconds": LISTENING_STORIES[name].get("audio_seconds", 0),
        "instructions": LISTENING_STORIES[name].get("instructions", []),
        "questions": built,
    }


def _key(a):
    return f"{a['class']}|||{a['subject']}|||{a['activity_name']}"


def _payload(activity, questions):
    audio = ""
    if _is_listening(activity):
        cls = activity["class"]
        name = activity["activity_name"]
        audio = (
            f"Attention students of {cls}. This is the listening task for {name}. "
            "Listen carefully to every detail before you answer the questions."
        )
    return {
        "title": activity["activity_name"],
        "audio_script": audio,
        "questions": questions,
    }


def _placeholder(activity):
    """No authored content for this bucket - surface it instead of faking it."""
    return {
        "title": activity["activity_name"],
        "audio_script": "",
        "questions": [],
        "content_missing": True,
    }


def generate_activity_questions(item):
    """Entry point used by ai_helper.py."""
    bank = build_bank()
    return bank.get(_key(item), _placeholder(item))


def write_js(bank, path=BANK_PATH):
    body = json.dumps(bank, indent=2, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("const QUESTION_BANK = " + body + ";\n")
    return path


if __name__ == "__main__":
    built = build_bank()
    write_js(built)
    total = sum(len(p.get("questions", [])) for p in built.values())
    empty = [k for k, p in built.items() if not p.get("questions")]
    print(f"activities written : {len(built)}")
    print(f"questions written  : {total}")
    print(f"activities w/o content: {len(empty)}")