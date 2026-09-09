#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a hunspell .dic from a word-frequency list.

Written for the Nigerian-language dictionaries (yo_NG, ig_NG, ha_Latn_NG),
whose source corpora are web-crawled.  Web text in these languages is heavily
contaminated with undiacriticised spellings -- "eko" for "Ẹ̀kọ́", "obi" for
"ọbị" -- and a .dic built by naively taking the top N tokens would teach the
checker to accept those misspellings as correct.  That is worse than shipping
no dictionary at all, so the filtering below is the point of this script, not
incidental to it.

Usage:
    build_dic.py --lang yo_NG --input yo-words.txt --min-count 3

Input format is auto-detected: "word<TAB>count", "word count", or
"count word", one entry per line.  Output is written to <lang>/<lang>.dic
with the hunspell entry count on line 1, and a report to stderr.
"""
import argparse, os, sys, unicodedata
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Marks that carry meaning in each orthography.  Stripping these from a word
# yields its "skeleton"; two words with the same skeleton are spellings of the
# same thing, one of which is likely wrong.
TONE = {"̀", "́", "̄"}          # grave, acute, macron
SUBDOT = {"̣", "̩"}                  # dot below, vertical line below

# Letters whose bare counterpart is a distinct letter, per language.  Folding
# these is what exposes an undiacriticised spelling.
FOLD = {
    "yo_NG": {"ẹ": "e", "Ẹ": "E", "ọ": "o", "Ọ": "O",
              "ṣ": "s", "Ṣ": "S"},
    "ig_NG": {"ị": "i", "Ị": "I", "ọ": "o", "Ọ": "O",
              "ụ": "u", "Ụ": "U", "ṅ": "n", "Ṅ": "N"},
    "ha_Latn_NG": {"ɓ": "b", "Ɓ": "B", "ɗ": "d", "Ɗ": "D",
                   "ƙ": "k", "Ƙ": "K", "ƴ": "y", "Ƴ": "Y"},
}


def alphabet_from_aff(lang):
    """The set of characters this language's own .aff declares as word
    characters, so the filter can never drift from the shipped affix file."""
    path = os.path.join(HERE, lang, lang + ".aff")
    chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("WORDCHARS "):
                chars |= set(line[len("WORDCHARS "):].rstrip("\n"))
    return chars


def skeleton(word, lang):
    """Strip tone marks and fold subdotted/hooked letters to their base."""
    d = unicodedata.normalize("NFD", word)
    d = "".join(c for c in d if c not in TONE and c not in SUBDOT)
    d = unicodedata.normalize("NFC", d)
    return "".join(FOLD[lang].get(c, c) for c in d).lower()


def has_marks(word, lang):
    d = unicodedata.normalize("NFD", word)
    return any(c in TONE or c in SUBDOT for c in d) or \
        any(c in FOLD[lang] for c in word)


def parse(path):
    """Yield (word, count) from a frequency list, detecting the column order."""
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.replace("\t", " ").split()
            if len(parts) == 1:
                rows.append((parts[0], 1))
            elif parts[0].isdigit() and not parts[-1].isdigit():
                rows.append((" ".join(parts[1:]), int(parts[0])))
            elif parts[-1].isdigit():
                rows.append((" ".join(parts[:-1]), int(parts[-1])))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True, choices=sorted(FOLD))
    ap.add_argument("--input", required=True)
    ap.add_argument("--min-count", type=int, default=3,
                    help="drop words seen fewer than this many times")
    ap.add_argument("--dominance", type=float, default=1.0,
                    help="drop an unmarked spelling when a marked spelling of "
                         "the same skeleton is at least this many times as "
                         "frequent; 0 disables the guard")
    ap.add_argument("--max-len", type=int, default=40)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    lang = args.lang
    allowed = alphabet_from_aff(lang)
    rows = parse(args.input)

    counts, dropped = {}, defaultdict(int)
    for word, n in rows:
        word = unicodedata.normalize("NFC", word)
        if n < args.min_count:
            dropped["below min-count"] += 1
        elif len(word) > args.max_len or not word:
            dropped["length"] += 1
        elif any(c.isdigit() for c in word):
            dropped["contains digit"] += 1
        elif not set(word) <= allowed:
            dropped["character outside WORDCHARS"] += 1
        else:
            counts[word] = counts.get(word, 0) + n

    # The diacritic guard.  Note it is deliberately NOT "drop every unmarked
    # word": mid tone is unmarked in Yoruba and tone is usually unwritten in
    # Igbo, so plenty of correct words carry no mark at all.  We only drop an
    # unmarked spelling when a marked spelling of the same skeleton is attested
    # and clearly more frequent -- that is the signature of a stripped form.
    kept = dict(counts)
    if args.dominance > 0:
        by_skel = defaultdict(list)
        for w, n in counts.items():
            by_skel[skeleton(w, lang)].append((w, n))
        for skel, forms in by_skel.items():
            marked = [(w, n) for w, n in forms if has_marks(w, lang)]
            unmarked = [(w, n) for w, n in forms if not has_marks(w, lang)]
            if not marked or not unmarked:
                continue
            best_marked = max(n for _, n in marked)
            for w, n in unmarked:
                if best_marked >= args.dominance * n:
                    kept.pop(w, None)
                    dropped["unmarked variant of a marked word"] += 1

    words = sorted(kept, key=lambda w: (w.lower(), w))
    print("lang=%s  input rows=%d  kept=%d" % (lang, len(rows), len(words)),
          file=sys.stderr)
    for reason, n in sorted(dropped.items(), key=lambda kv: -kv[1]):
        print("  dropped %7d  %s" % (n, reason), file=sys.stderr)

    if args.dry_run:
        return
    out = os.path.join(HERE, lang, lang + ".dic")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("%d\n" % len(words))
        for w in words:
            f.write(w + "\n")
    print("wrote %s" % out, file=sys.stderr)


if __name__ == "__main__":
    main()
