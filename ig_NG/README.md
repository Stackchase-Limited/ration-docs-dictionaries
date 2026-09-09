# Igbo (ig_NG)

Windows LCID **1136**. Latin script, Ọnwụ orthography, Nigeria.

## Orthography notes

* Sub-dotted letters are `ị` U+1ECB, `ọ` U+1ECD, `ụ` U+1EE5; `ṅ` is U+1E45
  (and capitals U+1ECA / U+1ECC / U+1EE4 / U+1E44).
* Tone (acute, grave) and downstep (macron) are usually left unwritten in
  running text but are written in teaching and reference material, so they
  must not break tokenisation.
* The apostrophe is orthographic (`n'ime`, `n'ihi`) and is a word character.
* All data here is NFC; tone-marked sub-dotted vowels are two codepoints.

## Affix file

Same design as `yo_NG` — `WORDCHARS` covers U+0300/U+0301/U+0304, `MAP`
relates plain to sub-dotted forms for suggestions, `ICONV` folds
separately-typed dot below (U+0323), dot above (U+0307), the
vertical-line-below convention (U+0329) and tone-before-dot orderings onto NFC.
No `IGNORE`: dropping the subdot would collapse distinct words and accept
misspellings.

## Wordlist

`ig_NG.dic` is not yet present — see `tools/build_dic.py`.
