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
| Sproat non-linguistic symbol corpora, corpora.zip (richardsproat.com) | Held-out structured non-linguistic control family (Tasks A and B) | Used with the author's permission; XML files carry an Apache 2.0 header | data page (no licence stated); file headers (read 2026-10-08); author's permission | Cite Sproat (2014) and Wu, Solman, Linehan & Sproat (2012). IndusBarSeals not used; not redistributed |

**Before publishing anything derived from Sumerian:** CDLI permits academic reuse with citation but gives no formal open license. Publishing transformed sign-ID corpora for a research benchmark is plausibly within "common and fair academic practice". If you need certainty (for example for a Zenodo deposit under CC BY), ask CDLI or drop Sumerian from public rounds.

## Indus period and object-type tags: checked, NOT used (2026-10-04)

| Candidate source | What it holds | Terms we could establish | Status |
|---|---|---|---|
| CISI vol. 3, part 1 (Parpola, Pande & Koskikallio eds., 2010), data list | Per-object HARP designations; Kenoyer & Meadow (2010, p. 4 and fn. 4) state that each Harappa object was assigned a chronological period, and the catalogue records object type | Commercial, copyrighted book (Suomalainen Tiedeakatemia, ISBN 978-951-41-1040-5). No open license or data-reuse statement found. | Not used. Needs permission from the publisher and editors, or a tag list supplied by HARP. |
| harappa.com (HARP) | Articles, slides, images; the two papers above are hosted there | We could not read the site's own terms page: its Cloudflare protection blocks this environment, and we did not try to get around it. Search summaries of harappa.com's "image rights" and credits pages say images are copyrighted by HARP or the photographers, that commercial use and any Internet use need permission first, and that non-commercial educational use is allowed. These are unverified summaries. No statement about data or tag reuse was found. | Not used. Treat as all rights reserved until HARP says otherwise. |
| The two PDFs supplied by the project owner (Kenoyer & Meadow 2010; Kenoyer 2020a/b) | Text of the papers | Copyrighted publications | Read for citation only; short quotations with page references are used in configs and reports. The PDFs are not committed. |

Recommended route: ask J. M. Kenoyer / HARP for a per-object table (CISI or HARP id, object type,
period, sign sequence) with explicit permission to derive statistics and publish aggregates.

Attribution required by CC BY / CC BY-SA applies to any redistribution of derived corpora.
Synthetic corpora published in `challenge/` are transformed sign-ID sequences: a disguised sister
language written in invented signs, not readable text. Their keys (in `challenge/public/*/keys/`)
contain transformed units, and the public-tier keys carry these attributions:
DCS (CC BY 4.0, O. Hellwig), CDLI (academic reuse with citation, https://cdli.mpiwg-berlin.mpg.de), Project Madurai, Project Gutenberg, Sakana AI Kamon (CC BY-SA 4.0).
