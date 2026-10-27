# v2 Tasks C and D: real relatives beside the synthetic references

Real relatives are the realistic `related` tier; the synthetic sisters (v1 sister, `harsh`) are optimistic upper references, not bounds (pre-registration entry 10). Real-relative tiers of 48 corpora are scored with the entry-10 rule (a no-source gold row is unknown, not lost); `reports/v2/cd/entry10.md` has the old values.

Records: `/home/user/indus-blind-benchmark/runs/results/v2_cd` (0 corpora with errors). Methods frozen (`frozen-v2`); scoring entry 2 (strict primary, lenient secondary, before the cognate step); the v1 sister rows use the v1 scorer before the cognate step (entry 4). Each cell: mean % of sign tokens over 6 corpora (seeds 0-2, samplers A and B), then corpora at or above 50%. Beside: Ugaritic-Hebrew, natural text, related tier: 33.9% (EM original), 32.0% (EM revised).

## Task D, `related` tier, EM revised (primary) (strict)

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 16.1 (0/6) | 54.9 (3/6) | 4.2 (0/6) | 56.9 (5/6) |
| sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.5 (0/6) | 7.3 (0/6) | 1.2 (0/6) | 29.1 (0/6) |
| tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 26.7 (0/6) | 19.0 (0/6) | 42.5 (2/6) |
| tamil | kannada | sister | 0.0 (0/6) | 3.3 (0/6) | 2.9 (0/6) | 32.2 (0/6) |
| tamil | malayalam | descendant | 0.0 (0/6) | 6.2 (0/6) | 5.9 (0/6) | 30.4 (1/6) |
| tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.1 (0/6) | 6.2 (0/6) | 5.9 (0/6) | 16.4 (0/6) |
| sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 3.7 (0/6) | 5.7 (0/6) | 4.5 (0/6) | 29.6 (1/6) |
| sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 1.1 (0/6) | 1.0 (0/6) | 2.5 (0/6) | 12.0 (0/6) |
| latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 1.4 (0/6) | 32.2 (1/6) | 9.8 (0/6) | 45.4 (2/6) |
| latin | italian | descendant | 0.0 (0/6) | 6.0 (0/6) | 1.5 (0/6) | 16.9 (1/6) |
| latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 1.5 (0/6) | 24.4 (0/6) | 4.6 (0/6) | 36.1 (1/6) |
| finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 1.0 (0/6) | 43.6 (3/6) | 21.2 (0/6) | 65.3 (5/6) |
| finnish | estonian (weak gold: 10 word pairs, 13 of 27 letters) | sister | 0.0 (0/6) | 9.3 (0/6) | 3.7 (0/6) | 29.8 (0/6) |
| finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 19.9 (0/6) | 8.6 (0/6) | 35.9 (0/6) |

## Task D, `related` tier, EM original (strict)

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.6 (0/6) | 53.2 (3/6) | 4.0 (0/6) | 58.5 (6/6) |
| sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 7.4 (0/6) | 2.0 (0/6) | 29.2 (0/6) |
| tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 28.1 (0/6) | 18.7 (0/6) | 43.1 (2/6) |
| tamil | kannada | sister | 0.0 (0/6) | 3.4 (0/6) | 2.5 (0/6) | 33.5 (0/6) |
| tamil | malayalam | descendant | 0.0 (0/6) | 5.9 (0/6) | 6.6 (0/6) | 30.4 (1/6) |
| tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 8.4 (0/6) | 5.4 (0/6) | 17.3 (0/6) |
| sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 2.3 (0/6) | 3.8 (0/6) | 2.6 (0/6) | 28.7 (1/6) |
| sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 1.1 (0/6) | 1.4 (0/6) | 1.6 (0/6) | 11.9 (0/6) |
| latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 29.5 (1/6) | 9.5 (0/6) | 45.7 (2/6) |
| latin | italian | descendant | 0.0 (0/6) | 6.0 (0/6) | 1.7 (0/6) | 17.1 (0/6) |
| latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.1 (0/6) | 24.0 (0/6) | 4.3 (0/6) | 35.8 (1/6) |
| finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 46.2 (3/6) | 21.0 (0/6) | 65.7 (5/6) |
| finnish | estonian (weak gold: 10 word pairs, 13 of 27 letters) | sister | 0.0 (0/6) | 9.7 (0/6) | 3.5 (0/6) | 30.0 (0/6) |
| finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 20.2 (0/6) | 8.9 (0/6) | 37.6 (1/6) |

## Task D, `related` tier, frequency rank (strict)

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 14.3 (0/6) | 3.3 (0/6) | 0.5 (0/6) | 10.5 (0/6) |
| sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 4.1 (0/6) | 0.6 (0/6) | 8.4 (0/6) |
| tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.6 (0/6) | 1.4 (0/6) | 4.8 (0/6) |
| tamil | kannada | sister | 0.0 (0/6) | 1.3 (0/6) | 1.4 (0/6) | 6.3 (0/6) |
| tamil | malayalam | descendant | 0.0 (0/6) | 2.2 (0/6) | 1.9 (0/6) | 3.5 (0/6) |
| tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.8 (0/6) | 0.3 (0/6) | 4.3 (0/6) |
| sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.1 (0/6) | 1.0 (0/6) | 0.7 (0/6) | 9.6 (0/6) |
| sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.7 (0/6) | 0.0 (0/6) | 1.0 (0/6) | 6.5 (0/6) |
| latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 5.9 (0/6) | 4.0 (0/6) | 0.9 (0/6) | 7.5 (0/6) |
| latin | italian | descendant | 0.0 (0/6) | 4.9 (0/6) | 2.4 (0/6) | 7.8 (0/6) |
| latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 11.0 (0/6) | 7.1 (0/6) | 2.2 (0/6) | 9.2 (0/6) |
| finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.8 (0/6) | 8.4 (0/6) | 1.8 (0/6) | 7.4 (0/6) |
| finnish | estonian (weak gold: 10 word pairs, 13 of 27 letters) | sister | 0.0 (0/6) | 1.8 (0/6) | 0.6 (0/6) | 3.0 (0/6) |
| finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 1.1 (0/6) | 7.1 (0/6) | 1.2 (0/6) | 7.4 (0/6) |

## Task D, `candidates` tier, EM revised (primary) (strict)

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 54.9 (3/6) | 1.7 (0/6) | 13.0 (0/6) |
| sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.4 (0/6) | 1.7 (0/6) | 0.6 (0/6) | 9.8 (0/6) |
| tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 19.7 (0/6) | 17.6 (0/6) | 20.2 (1/6) |
| tamil | kannada | sister | 0.0 (0/6) | 2.4 (0/6) | 2.9 (0/6) | 11.8 (0/6) |
| tamil | malayalam | descendant | 0.0 (0/6) | 2.3 (0/6) | 2.2 (0/6) | 12.2 (0/6) |
| tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.1 (0/6) | 2.1 (0/6) | 1.0 (0/6) | 8.8 (0/6) |
| sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.7 (0/6) | 0.6 (0/6) | 7.4 (0/6) |
| sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 1.1 (0/6) | 0.8 (0/6) | 0.6 (0/6) | 7.5 (0/6) |
| latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.8 (0/6) | 32.2 (1/6) | 9.8 (0/6) | 45.4 (2/6) |
| latin | italian | descendant | 0.0 (0/6) | 7.1 (0/6) | 1.2 (0/6) | 15.1 (0/6) |
| latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.7 (0/6) | 18.6 (0/6) | 1.1 (0/6) | 35.1 (1/6) |
| finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.1 (0/6) | 43.6 (3/6) | 19.5 (0/6) | 54.7 (4/6) |
| finnish | estonian (weak gold: 10 word pairs, 13 of 27 letters) | sister | 0.0 (0/6) | 9.3 (0/6) | 3.7 (0/6) | 23.0 (0/6) |
| finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 15.4 (0/6) | 5.4 (0/6) | 25.2 (0/6) |

## Task D, `candidates` tier, EM original (strict)

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 30.6 (3/6) | 0.1 (0/6) | 15.2 (0/6) |
| sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.0 (0/6) | 0.1 (0/6) | 12.2 (0/6) |
| tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 13.8 (0/6) | 7.3 (0/6) | 13.4 (0/6) |
| tamil | kannada | sister | 0.0 (0/6) | 0.4 (0/6) | 0.1 (0/6) | 16.7 (0/6) |
| tamil | malayalam | descendant | 0.0 (0/6) | 0.6 (0/6) | 0.2 (0/6) | 18.2 (0/6) |
| tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.0 (0/6) | 0.1 (0/6) | 11.4 (0/6) |
| sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 2.3 (0/6) | 3.8 (0/6) | 2.6 (0/6) | 28.7 (1/6) |
| sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 1.1 (0/6) | 1.4 (0/6) | 1.6 (0/6) | 11.9 (0/6) |
| latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 15.8 (0/6) | 0.2 (0/6) | 9.5 (0/6) |
| latin | italian | descendant | 0.0 (0/6) | 1.1 (0/6) | 0.2 (0/6) | 9.5 (0/6) |
| latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.7 (0/6) | 0.1 (0/6) | 7.2 (0/6) |
| finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.4 (0/6) | 0.1 (0/6) | 9.6 (0/6) |
| finnish | estonian (weak gold: 10 word pairs, 13 of 27 letters) | sister | 0.0 (0/6) | 0.4 (0/6) | 0.1 (0/6) | 9.5 (0/6) |
| finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.4 (0/6) | 0.0 (0/6) | 5.7 (0/6) |

## Task D, `candidates` tier, frequency rank (strict)

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 2.1 (0/6) | 3.3 (0/6) | 0.7 (0/6) | 5.3 (0/6) |
| sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.5 (0/6) | 0.1 (0/6) | 8.4 (0/6) |
| tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.6 (0/6) | 0.7 (0/6) | 7.1 (0/6) |
| tamil | kannada | sister | 0.0 (0/6) | 0.3 (0/6) | 0.7 (0/6) | 10.7 (0/6) |
| tamil | malayalam | descendant | 0.0 (0/6) | 1.8 (0/6) | 0.8 (0/6) | 3.5 (0/6) |
| tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.0 (0/6) | 0.2 (0/6) | 2.2 (0/6) |
| sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.2 (0/6) | 0.0 (0/6) | 9.6 (0/6) |
| sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 0.2 (0/6) | 0.0 (0/6) | 6.5 (0/6) |
| latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 5.9 (0/6) | 3.8 (0/6) | 0.6 (0/6) | 5.7 (0/6) |
| latin | italian | descendant | 0.0 (0/6) | 3.1 (0/6) | 0.7 (0/6) | 5.7 (0/6) |
| latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 11.0 (0/6) | 3.1 (0/6) | 0.3 (0/6) | 9.2 (0/6) |
| finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 6.2 (0/6) | 0.9 (0/6) | 3.6 (0/6) |
| finnish | estonian (weak gold: 10 word pairs, 13 of 27 letters) | sister | 0.0 (0/6) | 2.6 (0/6) | 0.2 (0/6) | 3.0 (0/6) |
| finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0/6) | 2.6 (0/6) | 0.2 (0/6) | 7.4 (0/6) |

## Task D, secondary columns (EM revised): lenient score and the strict ceiling

Ceiling: share of tokens with a strict reflex at all (unrecoverable: no reflex, no cognate for a logogram, determinatives).

| Hidden | Tier | logographic: lenient / ceiling | syllabic: lenient / ceiling | logosyllabic: lenient / ceiling | alphabetic: lenient / ceiling |
|---|---|---|---|---|---|
| sanskrit | candidates_harsh | 0.4 / 16.4 | 1.7 / 100.0 | 0.6 / 43.4 | 11.4 / 100.0 |
| sanskrit | related_harsh | 0.5 / 16.4 | 10.2 / 100.0 | 1.6 / 43.4 | 30.1 / 100.0 |
| tamil | candidates_harsh | 0.1 / 20.5 | 2.5 / 100.0 | 1.9 / 72.0 | 10.3 / 100.0 |
| tamil | candidates_real:kannada | 0.0 / 24.0 | 3.9 / 100.0 | 3.9 / 72.5 | 16.7 / 100.0 |
| tamil | candidates_real:malayalam | 0.0 / 17.0 | 3.4 / 100.0 | 2.7 / 72.8 | 14.0 / 100.0 |
| tamil | related_harsh | 0.1 / 20.5 | 8.2 / 100.0 | 7.1 / 72.0 | 19.2 / 100.0 |
| tamil | related_real:kannada | 0.0 / 24.0 | 4.8 / 100.0 | 3.9 / 72.5 | 34.2 / 100.0 |
| tamil | related_real:malayalam | 0.0 / 17.0 | 9.8 / 100.0 | 8.4 / 72.8 | 33.6 / 100.0 |
| sumerian | candidates_harsh | 1.1 / 40.9 | 0.8 / 100.0 | 1.0 / 61.0 | 9.2 / 100.0 |
| sumerian | related_harsh | 1.1 / 40.9 | 1.2 / 100.0 | 2.8 / 61.0 | 14.4 / 100.0 |
| latin | candidates_harsh | 0.7 / 46.4 | 18.6 / 100.0 | 1.1 / 74.8 | 35.1 / 100.0 |
| latin | candidates_real:italian | 0.0 / 51.4 | 9.0 / 100.0 | 2.3 / 80.4 | 21.7 / 99.1 |
| latin | related_harsh | 1.5 / 46.4 | 24.4 / 100.0 | 4.6 / 74.8 | 36.1 / 100.0 |
| latin | related_real:italian | 0.1 / 51.4 | 7.5 / 100.0 | 2.6 / 80.4 | 22.6 / 99.1 |
| finnish | candidates_harsh | 0.0 / 15.4 | 20.3 / 100.0 | 7.5 / 60.9 | 29.9 / 100.0 |
| finnish | candidates_real:estonian | 0.0 / 15.5 | 11.0 / 82.9 | 5.0 / 50.5 | 33.8 / 86.5 |
| finnish | related_harsh | 0.0 / 15.4 | 27.5 / 100.0 | 11.5 / 60.9 | 44.1 / 100.0 |
| finnish | related_real:estonian | 0.0 / 15.5 | 11.0 / 82.9 | 5.0 / 50.5 | 39.8 / 86.5 |

## Task C (`candidates` tiers): right family, % of corpora (all script types pooled), and the reference chosen

| Hidden | Tier | EM revised (primary) | EM original | frequency rank | References chosen by EM revised |
|---|---|---|---|---|---|
| sanskrit | v1 sister (synthetic, optimistic upper reference) | 75.0 (24) | 12.5 (24) | 54.2 (24) | latin 10, sanskrit-sister 8, finnish 6 |
| sanskrit | candidates_harsh | 62.5 (24) | 0.0 (24) | 58.3 (24) | latin 13, finnish 9, sanskrit-sister-harsh 2 |
| tamil | v1 sister (synthetic, optimistic upper reference) | 33.3 (24) | 12.5 (24) | 12.5 (24) | latin 13, tamil-sister 8, finnish 3 |
| tamil | candidates_harsh | 12.5 (24) | 0.0 (24) | 29.2 (24) | latin 14, finnish 7, tamil-sister-harsh 3 |
| tamil | candidates_real:kannada | 37.5 (24) | 0.0 (24) | 8.3 (24) | latin 10, kannada 9, finnish 5 |
| tamil | candidates_real:malayalam | 0.0 (24) | 0.0 (24) | 37.5 (24) | latin 16, finnish 8 |
| sumerian | v1 sister (synthetic, optimistic upper reference) | 4.2 (24) | 100.0 (24) | 25.0 (24) | finnish 12, latin 11, sumerian-sister 1 |
| sumerian | candidates_harsh | 25.0 (24) | 100.0 (24) | 25.0 (24) | latin 11, finnish 7, sumerian-sister-harsh 6 |
| latin | v1 sister (synthetic, optimistic upper reference) | 95.8 (24) | 8.3 (24) | 62.5 (24) | latin-sister 23, finnish 1 |
| latin | candidates_harsh | 54.2 (24) | 0.0 (24) | 70.8 (24) | latin-sister-harsh 12, finnish 11, sanskrit 1 |
| latin | candidates_real:italian | 25.0 (24) | 0.0 (24) | 50.0 (24) | finnish 18, italian 6 |
| finnish | v1 sister (synthetic, optimistic upper reference) | 70.8 (24) | 0.0 (24) | 25.0 (24) | finnish-sister 17, latin 6, tamil 1 |
| finnish | candidates_harsh | 70.8 (24) | 0.0 (24) | 37.5 (24) | finnish-sister-harsh 17, latin 7 |
| finnish | candidates_real:estonian | 62.5 (24) | 0.0 (24) | 29.2 (24) | estonian 15, latin 7, sanskrit 1, tamil 1 |

