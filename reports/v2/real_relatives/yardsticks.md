# Rank 6b: Ugaritic-Hebrew yardsticks on real related languages (pre-registration entry 5)

No tuning, no targets. Shared code (`src/ibdb/yardsticks.py`); sample sizes matched to the anchor. Normalised spelling is primary. Every pair is labelled sister or descendant.

**Cross-script comparisons are indicative only.** Shared word forms (and word pairs) are not directly comparable between a consonant-only script (Ugaritic-Hebrew) and scripts that write vowels (all other rows): a consonant skeleton matches far more easily than a full word, even after the chance correction. Comparisons within one script type are the meaningful ones.

| Pair | Relationship | Script type | Spelling | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Mergers |
|---|---|---|---|---|---|---|---|---|
| Ugaritic-Hebrew | sister | consonant-only (abjad) | as written | 0.166 | 46.8% | 1.5% | 0.8% | 7 |
| Ugaritic-Hebrew | sister | consonant-only (abjad) | vowel letters removed | 0.089 | 58.4% | 4.6% | 0.8% | 7 |
| **latin-italian** | descendant | alphabet (vowels written) | as written | 0.117 | 11.8% | 0.6% | 1.9% | 9 + h no reflex |
| **latin-italian** | descendant | alphabet (vowels written) | normalised (primary) | 0.104 | 11.8% | 0.6% | 1.9% | 9 + h no reflex |
| **tamil-malayalam** | descendant | abugida (vowels written) | as written | 0.176 | 5.5% | 0.0% | 1.8% | 3 + h, s, ḵ, ṣ no reflex |
| **tamil-malayalam** | descendant | abugida (vowels written) | normalised (primary) | 0.139 | 5.7% | 0.0% | 1.8% | 3 + h, s, ḵ, ṣ no reflex |
| **tamil-kannada** | sister | abugida (vowels written) | as written | 0.309 | 3.1% | 0.0% | 0.2% | 4 + h, s, ḵ, ṣ no reflex |
| **tamil-kannada** | sister | abugida (vowels written) | normalised (primary) | 0.180 | 4.7% | 0.0% | 1.0% | 4 + h, s, ḵ, ṣ no reflex |
| latin, v1-like sister (upper bound) | synthetic | as hidden | - | 0.006 | 53.1% | 7.1% | 12.4% | 0 |
| latin, `harsh` (lower bound) | synthetic | as hidden | - | 0.135 | 7.8% | 1.1% | 2.4% | 24% of consonants |
| tamil, v1-like sister (upper bound) | synthetic | as hidden | - | 0.002 | 57.6% | 8.5% | 17.8% | 0 |
| tamil, `harsh` (lower bound) | synthetic | as hidden | - | 0.185 | 3.6% | 0.1% | 1.8% | 24% of consonants |

**Bootstrap over the relative's lines (normalised; 200 replicates, 5 draws each): point / bootstrap mean / 95% interval**

| Pair | jsd_above_floor | cognate_types_cc | word_pairs_types_cc | verbatim_6plus |
|---|---|---|---|---|
| latin-italian | 0.104 / 0.104 / 0.101-0.108 | 11.8% / 10.6% / 9.6%-11.5% | 0.6% / 0.4% / 0.1%-0.7% | 1.9% / 1.9% / 0.7%-3.3% |
| tamil-malayalam | 0.139 / 0.141 / 0.137-0.145 | 5.7% / 4.6% / 4.0%-5.2% | 0.0% / 0.0% / 0.0%-0.0% | 1.8% / 1.3% / 0.4%-2.4% |
| tamil-kannada | 0.180 / 0.182 / 0.178-0.186 | 4.7% / 4.5% / 3.8%-5.1% | 0.0% / 0.0% / 0.0%-0.1% | 1.0% / 1.3% / 0.4%-2.4% |

**Sizes (normalised):** latin-italian: 14,233 lines, 101,601 words, 391,950 units; tamil-malayalam: 15,901 lines, 42,648 words, 479,851 units; tamil-kannada: 29,880 lines, 105,385 words, 857,617 units.
**Gold sources:** Latin-Italian, Grandgent (1907), section per row (`src/ibdb/data/relatives.py`); Tamil-Malayalam and Tamil-Kannada, Caldwell (1875), pages per row (`src/ibdb/data/dravidian.py`). Hidden side: the v1 hidden half of each source.
**Data notes:** Malayalam (Adhyatma Ramayanam Kilippattu, 126 section pages) and Kannada (Kumaravyasa Bharata) Wikisource texts: source edition unstated (accepted as clean by the project owner, 2026-10-15). Kannada coverage is partial: 93 of the 154 sandhi pages linked from the ten parva pages exist (61 red links), mostly Adi, Virata and Karna parvas; the 2 commentary (ಸಟೀಕಾ) pages are excluded. Each Kannada sandhi page opens with a short invocation that may be in Sanskrit; it was not removed. Revision ids and SHA-256 per page are in `data/raw/relatives/{ml,kn}/manifest.json`.

**Not measured:**

- finnish-estonian (sister): waiting for the Pajusalu (2012) PDF from the project owner
- sanskrit-pali (descendant): waiting on SuttaCentral; no OCR re-transcription
- sumerian: isolate; none tier only

