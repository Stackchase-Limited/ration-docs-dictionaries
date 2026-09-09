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

## Wordlist (superseded -- see provenance below)

`ha_Latn_NG.dic` is not yet present — see `tools/build_dic.py`.

## Wordlist provenance

78,696 entries, built by `tools/build_dic.py` from:

* **Hausa Wikipedia** (CC BY-SA 4.0) -- 123,004 pages, 60.0M tokens.

No curated Hausa lexicon was found in open form; An Crubadan holds one
(speller status "yes", derived from Bargery) but crubadan.org is offline.

**Licence: CC BY-SA 4.0.**

### Known limitation -- READ BEFORE SHIPPING

Hausa Wikipedia is heavily contaminated with unhooked spellings: writers
without a Hausa keyboard type `kasa` for `ƙasa`, `daya` for `ɗaya`. 2,199
hooked words had their unhooked spelling attested too, most at over 83% of the
correct form's frequency -- so frequency alone cannot separate them.

`--dominance 1.2` drops the clearest cases (`wadanda`, `kasar`), but this is a
blunt instrument: it cannot distinguish a keyboard shortcut from a genuine
minimal pair. `kasa` ("to fail") and `ƙasa` ("land") are different words, and
the guard may have removed one. **A Hausa speaker must review this list before
it ships.** Of the three languages here, Hausa has the weakest source.
