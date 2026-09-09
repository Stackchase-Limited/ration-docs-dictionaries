# Hausa (ha_Latn_NG)

Windows LCID **1128**. Boko (Latin) orthography, Nigeria.

## Orthography notes

* Hooked consonants are `ɓ` U+0253, `ɗ` U+0257, `ƙ` U+0199 (capitals U+0181 /
  U+018A / U+0198).
* The Nigerian standard writes the palatalised glottal as `'y`
  (apostrophe + y); Niger writes `ƴ` U+01B4. Both are accepted. They are
  treated as two national conventions, not as encodings of one another, so
  they are related through `MAP`/`REP` rather than rewritten by `ICONV`.
* The apostrophe is a letter here (`'yan`, `'ya'ya`, `sha'awa`) and is a word
  character; U+2019 and U+02BC are folded onto U+0027 on input.
* Tone and vowel length are unmarked in standard Boko but marked in
  pedagogical text, so those marks stay inside `WORDCHARS`.

## Affix file

`REP` covers the dominant real-world input error — typing the plain consonant
because the hooked letter is not on the keyboard — so `kasa` is rejected but
suggests `ƙasa`.

## Wordlist

`ha_Latn_NG.dic` is not yet present — see `tools/build_dic.py`.
