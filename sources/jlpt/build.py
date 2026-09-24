"""Builds japanese/jlpt-n{5..1}-vocabulary.ankipan from n{5..1}.csv.

The CSVs are src/n*.csv from https://github.com/jamsinclair/open-anki-jlpt-decks
at 1ad6673 (MIT, see LICENSE-open-anki-jlpt-decks), itself based on tanos.co.uk.

Run from anywhere: python3 sources/jlpt/build.py [5 4 ...]

Each package keeps its id and version from the existing file, and every row
keeps the upstream guid, so learners' progress carries over to a rebuilt
version. Bump "version" in the .ankipan by hand before rebuilding a change.
"""
import csv, html, json, os, re, sys, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "..", "japanese")
TINTS = {5: "orange", 4: "yellow", 3: "green", 2: "blue", 1: "purple"}

# Upstream rows whose word/reading carry hints the rules below can't sort out:
# expression -> (word, reading, text appended to the meaning).
OVERRIDES = {
    "パート (タイム)": ("パート(タイム)", "パート; パートタイム", ""),
    "スーパー (マーケット)": ("スーパー(マーケット)", "スーパー; スーパーマーケット", ""),
    "ミリ (メートル)": ("ミリ(メートル)", "ミリ; ミリメートル", ""),
    "コンタクト (レンズ)": ("コンタクト(レンズ)", "コンタクト; コンタクトレンズ", ""),
    "～(て) しまう": ("～てしまう", "てしまう", ""),
    "～(に) よると": ("～によると", "によると", ""),
    "～(に) ついて": ("～について", "について", ""),
    "いただく": ("いただく", "いただく", ""),  # upstream reading is 頂く
    "しいんと (する)": ("しいんと", "しいんと", " (～する)"),
    "〜 (まる) ごと": ("～ごと", "ごと", " (e.g. まるごと)"),
    "〜(日本) 式": ("～式", "しき", " (e.g. 日本式)"),
    "～いち (にほんいち)": ("～いち", "いち", " (e.g. にほんいち)"),
    "(かさを～) さす": ("さす", "さす", " (かさを～)"),
    "(花を〜) 生ける, 活ける": ("生ける; 活ける", "いける", " (はなを～)"),
    "こつ (をつかむ)": ("こつ", "こつ", " (～をつかむ)"),
    "とげ (をさす)": ("とげ", "とげ", " (～をさす)"),
    "かく (はじを)": ("かく", "かく", " (はじを～)"),
}

# Upstream meanings that are cut off: expression -> meaning.
MEANINGS = {
    "〜(日本) 式": "~ style",  # upstream: "custom,"
}


def clean(word, reading, meaning):
    meaning = re.sub(r"\s+", " ", html.unescape(meaning)).strip()
    meaning = MEANINGS.get(word, meaning)
    if word in OVERRIDES:
        word, reading, extra = OVERRIDES[word]
        return word, reading, meaning + extra
    if not reading:
        reading = word  # kana-only words with an empty reading
    # "べんきょう (する)", "げひん(な)": a hint about how the word is used.
    m = re.search(r"\s*\((する|な)\)$", reading)
    if m:
        reading = reading[: m.start()]
        meaning += f" (～{m.group(1)})"
    # "しまった (かん)": 感動詞, an interjection.
    if reading.endswith(" (かん)"):
        reading = reading[: -len(" (かん)")]
        word = re.sub(r"\s*\(かん\)$", "", word)
        meaning += " (interjection)"
    # Kana-only words with a usage hint or synonym: "しわ (かおの～)", "さきに (いぜん)".
    m = re.fullmatch(r"(.+?)\s*\((.+)\)", reading)
    if m and word.replace(" ", "") == reading.replace(" ", ""):
        word = reading = m.group(1)
        meaning += f" ({m.group(2)})"
    # Readings are typed and read aloud: no "(〜を)" hints or affix tildes.
    reading = re.sub(r"^\(〜を\)\s*", "", reading)
    reading = re.sub(r"[～〜~]", "", reading).strip()
    return word.strip(), reading, meaning


def build(level):
    out = os.path.join(OUT_DIR, f"jlpt-n{level}-vocabulary.ankipan")
    old = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}

    notes, seen, dropped = [], set(), []
    for r in csv.DictReader(open(os.path.join(HERE, f"n{level}.csv"), encoding="utf-8-sig")):
        values = list(clean(*(r[k].strip() for k in ("expression", "reading", "meaning"))))
        if tuple(values) in seen:  # the app would skip it anyway
            dropped.append(values[0])
            continue
        seen.add(tuple(values))
        notes.append({"guid": r["guid"], "values": values})

    pkg = {
        "format": 1,
        "id": old.get("id", str(uuid.uuid4())),
        "version": old.get("version", 1),
        "name": f"JLPT N{level} Vocabulary",
        "description": f"All {len(notes)} JLPT N{level} words with kana readings and English meanings. Word list from tanos.co.uk via github.com/jamsinclair/open-anki-jlpt-decks (MIT).",
        "homepage": "https://github.com/fanzeyi/ankipan-cards",
        "tags": f"jlpt n{level}",
        "icon": {"symbol": "character.book.closed", "tint": TINTS[level]},
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
            {"ord": 2, "name": "Listening", "prompt": ["Word"], "hidden": ["Word"], "read": {"front": "Word"},
             "answer": ["Meaning", "Word", "Reading"]},
            {"ord": 3, "name": "Speaking", "prompt": ["Word"], "answer": ["Reading", "Meaning"],
             "check": {"field": "Word", "mode": "spoken", "alsoAccept": ["Reading"]}},
        ],
        "notes": notes,
    }

    # One column / kind / note per line, so diffs between versions stay readable.
    head = {k: v for k, v in pkg.items() if k not in ("fields", "kinds", "notes")}
    parts = [json.dumps(head, ensure_ascii=False, indent=2)[:-2] + ","]
    for key in ("fields", "kinds", "notes"):
        items = pkg[key]
        parts.append(f'  "{key}": [')
        parts += [f"    {json.dumps(x, ensure_ascii=False)}" + ("," if i < len(items) - 1 else "") for i, x in enumerate(items)]
        parts.append("  ]" + ("," if key != "notes" else ""))
    parts.append("}")
    open(out, "w", encoding="utf-8").write("\n".join(parts) + "\n")
    print(f"{os.path.relpath(out)}: {len(notes)} rows, version {pkg['version']}"
          + (f", dropped repeated rows: {dropped}" if dropped else ""))


for level in [int(a) for a in sys.argv[1:]] or [5, 4, 3, 2, 1]:
    build(level)
