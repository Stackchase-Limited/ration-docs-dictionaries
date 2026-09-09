# Yorùbá (yo_NG)

Windows LCID **1130**. Latin script, 25 letters, Nigeria.

## Orthography notes

* Sub-dotted letters are `ẹ` U+1EB9, `ọ` U+1ECD, `ṣ` U+1E63 (and capitals
  U+1EB8 / U+1ECC / U+1E62).
* Tone is marked with U+0301 (high) and U+0300 (low). Mid tone is unmarked,
  so a word carrying no tone mark is **not** by itself evidence of a
  misspelling.
* `a e i o u` have precomposed tone-marked forms; `ẹ` and `ọ` do not, so
  `ẹ́` is two codepoints (U+1EB9 U+0301). All data here is NFC.

## Affix file

* `WORDCHARS` includes U+0300 and U+0301 so combining tone marks are not
  treated as word separators.
* `MAP` relates plain letters to their sub-dotted and tone-marked forms, which
  is what lets an undiacriticised input be *rejected* but still receive the
  correct suggestion.
* `ICONV` normalises legitimate non-NFC input onto the NFC dictionary forms:
  separately-typed dot below (U+0323), the vertical-line-below publishing
  convention (U+0329), and tone typed before the dot below.
* There is deliberately **no `IGNORE`** directive. Making the tone and dot
  marks ignorable would make the checker accept undiacriticised text as
  correct, which is the failure mode this dictionary exists to prevent.

## Wordlist (superseded -- see provenance below)

`yo_NG.dic` is not yet present — see `tools/build_dic.py` and the source
decision recorded on the `ration/9.4-languages` branch.

## Wordlist provenance

66,180 entries, built by `tools/build_dic.py` from two complementary sources:

* **Niger-Volta-LTI/yoruba-text** (GPL-3.0) -- 69,455 files, 14.3M tokens:
  Bibeli Mimo, JW300, Quran Mimo, Iroyin, Owe, TheYorubaBlog, UDHR and
  YorubaForAcademicPurpose. Professionally translated, properly diacriticised.
* **Lesika/yoruba_words_sorted.txt** -- a curated 41,584-word list from the
  same repository; 83% of entries carry diacritics.

Excluded deliberately: `LagosNWU/all_transcripts_no_diacritics.txt` (would
teach undiacriticised spellings), `jw300.en.txt` (English side of the parallel
corpus) and `Asubiaro_LangID` (deliberately mixed-language training data).

**Licence: GPL-3.0**, inherited from yoruba-text. Compatible with AGPL-3.0.
