"""Builds japanese/jlpt-n5-vocabulary.ankipan from n5.csv.

n5.csv is src/n5.csv from https://github.com/jamsinclair/open-anki-jlpt-decks
(MIT, see LICENSE-open-anki-jlpt-decks), itself based on tanos.co.uk.

Run from the repository root: python3 sources/jlpt/build.py

The package id and version are kept from the existing file, and every row keeps
the upstream guid, so learners' progress carries over to a rebuilt version.
Bump "version" by hand when publishing a change.
"""
import csv, json, os, re, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "japanese", "jlpt-n5-vocabulary.ankipan")

old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}

notes = []
for r in csv.DictReader(open(os.path.join(HERE, "n5.csv"), encoding="utf-8-sig")):
    word, reading, meaning = (r[k].strip() for k in ("expression", "reading", "meaning"))
    # する-verbs: "べんきょう (する)" → reading べんきょう, note it on the meaning.
    if re.search(r"\s*\(する\)$", reading):
        reading = re.sub(r"\s*\(する\)$", "", reading)
        meaning += " (～する)"
    # Readings are typed and read aloud: no "(〜を)" hints or affix tildes.
    reading = re.sub(r"^\(〜を\)\s*", "", reading)
    reading = re.sub(r"[～〜~]", "", reading).strip()
    notes.append({"guid": r["guid"], "values": [word, reading, meaning]})

pkg = {
    "format": 1,
    "id": old.get("id", str(uuid.uuid4())),
    "version": old.get("version", 1),
    "name": "JLPT N5 Vocabulary",
    "description": f"All {len(notes)} JLPT N5 words with kana readings and English meanings. Word list from tanos.co.uk via github.com/jamsinclair/open-anki-jlpt-decks (MIT).",
    "homepage": "https://github.com/fanzeyi/ankipan-cards",
    "tags": "jlpt n5",
    "icon": {"symbol": "character.book.closed", "tint": "orange"},
    "fields": [
        {"name": "Word", "language": "ja-JP", "options": {"pronounceWith": "Reading"}},
        {"name": "Reading", "language": "ja-JP", "options": {"script": "kana"}},
        {"name": "Meaning", "language": "en-US"},
    ],
    "kinds": [
        {"ord": 0, "name": "Recognition", "prompt": ["Word"], "answer": ["Reading", "Meaning"],
         "read": {"back": "Reading"}},
        {"ord": 1, "name": "Production", "prompt": ["Meaning"], "answer": ["Word", "Reading"],
         "check": {"field": "Reading", "mode": "typed", "alsoAccept": ["Word"]}, "read": {"back": "Word"}},
    ],
    "notes": notes,
}

# One column / kind / note per line, so diffs between versions stay readable.
def line(x):
    return json.dumps(x, ensure_ascii=False)

head = {k: v for k, v in pkg.items() if k not in ("fields", "kinds", "notes")}
parts = [json.dumps(head, ensure_ascii=False, indent=2)[:-2] + ","]
for key in ("fields", "kinds", "notes"):
    items = pkg[key]
    parts.append(f'  "{key}": [')
    parts += [f"    {line(x)}" + ("," if i < len(items) - 1 else "") for i, x in enumerate(items)]
    parts.append("  ]" + ("," if key != "notes" else ""))
parts.append("}")
open(OUT, "w", encoding="utf-8").write("\n".join(parts) + "\n")
print(f"{OUT}: {len(notes)} rows, version {pkg['version']}")
