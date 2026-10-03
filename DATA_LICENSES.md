# Data sources and licenses

No third-party text is committed to this repository. `ibdb fetch` downloads it into `data/raw/`
(git-ignored) and writes a `.meta.json` next to each file with URL, size, SHA-256, license and
fetch time.

| Source | Used as | License | Evidence | Notes |
|---|---|---|---|---|
| Digital Corpus of Sanskrit (O. Hellwig), Rāmāyaṇa CoNLL-U | Sanskrit plaintext | CC BY 4.0 | `dcs/data/readme.md`, "License" | Chosen over GRETIL, whose Mahābhārata file states "(C) BORI ... for reference purposes only" |
| Project Madurai, Sangam anthologies (17 root texts) | Old Tamil plaintext | Free distribution with header intact; texts public domain | file headers; FAQ 3.3 | |
| CDLI bulk ATF dump (Aug 2022), Sumerian only | Sumerian plaintext incl. 19,076 seal inscriptions | CDLI terms: "may be freely copied, aggregated and re-used according to common and fair academic practice"; cite CDLI. **Not a Creative Commons license.** | https://cdli.earth/terms-of-use (read 2026-10-03) | An earlier draft said CC BY 4.0; that covers CDLI's articles, not the data. ETCSL asserts copyright without an open license; ORACC was unreachable (TLS error) |
| Project Gutenberg #218, #229, #231 | Latin control | Public domain (USA) | Gutenberg headers | |
| Project Gutenberg #7000 (Kalevala) | Finnish control | Public domain (USA) | Gutenberg header | |
| Sakana AI Kamon, synthetic_examples.zip | NL-derived control | CC BY-SA 4.0 | dataset card | 122 MB; only the parsed text descriptions are used |

**Before publishing anything derived from Sumerian:** CDLI permits academic reuse with citation but gives no formal open license. Publishing transformed sign-ID corpora for a research benchmark is plausibly within "common and fair academic practice". If you need certainty (for example for a Zenodo deposit under CC BY), ask CDLI or drop Sumerian from public rounds.

Attribution required by CC BY / CC BY-SA applies to any redistribution of derived corpora.
Synthetic corpora published in `challenge/` are transformed sign-ID sequences: a disguised sister
language written in invented signs, not readable text. Their keys (in `challenge/public/*/keys/`)
contain transformed units, and the public-tier keys carry these attributions:
DCS (CC BY 4.0, O. Hellwig), CDLI (academic reuse with citation, https://cdli.mpiwg-berlin.mpg.de), Project Madurai, Project Gutenberg, Sakana AI Kamon (CC BY-SA 4.0).
