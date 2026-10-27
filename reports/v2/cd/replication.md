# v2 Task C/D: fresh-seed replication, seeds 3-5 (pre-registration entry 7)

Corpora: 120 of 120 (seeds 3-5, samplers A and B), frozen code (`frozen-v2`), the same tiers. Each cell: mean % of sign tokens over 6 corpora (number at or above 50%). Revised EM, strict, unless stated. The v1 sister is read from the v1 `sister_v2_repl` and `sister_v2_gen2_repl` records. Entry 10: Old Tamil real-relative values use the entry-10 rule (no source = unknown; old values in `entry10.md`); the synthetic sisters are optimistic upper references, not bounds.

## Task D, `related` tier

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| Sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 2.1 (0) | 40.8 (2) | 5.3 (0) | 53.7 (4) |
| Sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 10.0 (0) | 3.1 (0) | 3.0 (0) | 32.0 (0) |
| Old Tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 31.8 (1) | 23.6 (1) | 44.5 (2) |
| Old Tamil | Malayalam | descendant | 0.0 (0) | 15.1 (0) | 7.2 (0) | 30.5 (2) |
| Old Tamil | Kannada | sister | 0.0 (0) | 4.8 (0) | 5.0 (0) | 36.7 (1) |
| Old Tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 10.1 (0) | 6.6 (0) | 9.5 (0) |
| Sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 3.8 (0) | 2.7 (0) | 5.4 (0) | 24.6 (0) |
| Sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.2 (0) | 2.5 (0) | 1.4 (0) | 16.8 (0) |
| Latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 1.3 (0) | 26.4 (1) | 9.6 (0) | 47.2 (2) |
| Latin | Italian | descendant | 0.0 (0) | 2.4 (0) | 3.0 (0) | 23.8 (2) |
| Latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 4.7 (0) | 9.4 (0) | 2.6 (0) | 26.8 (0) |
| Finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 2.4 (0) | 43.2 (2) | 16.0 (0) | 64.6 (6) |
| Finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.2 (0) | 26.1 (0) | 14.0 (0) | 46.5 (2) |

## Task D, `candidates` tier

| Hidden | Relative | Relationship | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|---|
| Sanskrit | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 34.6 (2) | 0.4 (0) | 17.1 (0) |
| Sanskrit | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 1.4 (0) | 0.3 (0) | 15.7 (0) |
| Old Tamil | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 22.3 (1) | 21.4 (1) | 16.5 (0) |
| Old Tamil | Malayalam | descendant | 0.0 (0) | 1.8 (0) | 1.7 (0) | 15.1 (0) |
| Old Tamil | Kannada | sister | 0.0 (0) | 5.3 (0) | 4.8 (0) | 14.8 (0) |
| Old Tamil | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 0.9 (0) | 0.3 (0) | 10.2 (0) |
| Sumerian | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.0 (0) | 0.2 (0) | 0.2 (0) | 7.2 (0) |
| Sumerian | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.1 (0) | 0.2 (0) | 0.4 (0) | 8.2 (0) |
| Latin | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.6 (0) | 26.4 (1) | 9.9 (0) | 47.2 (2) |
| Latin | Italian | descendant | 0.0 (0) | 2.5 (0) | 1.7 (0) | 12.9 (0) |
| Latin | `harsh` (synthetic, optimistic upper reference) | synthetic | 3.0 (0) | 2.3 (0) | 1.1 (0) | 20.6 (0) |
| Finnish | v1 sister (synthetic, optimistic upper reference) | synthetic | 0.8 (0) | 43.2 (2) | 15.9 (0) | 45.1 (4) |
| Finnish | `harsh` (synthetic, optimistic upper reference) | synthetic | 0.2 (0) | 22.5 (0) | 8.0 (0) | 39.2 (2) |

## Replication checks (fixed in entry 7 before the run)

- R1. Every real-relative mean below 50%: **replicated**. Highest: kannada/alphabetic 36.7%.
- R2. Old Tamil alphabetic means within 22.0-42.0% (Ugaritic 32.0% ± 10): **replicated**. malayalam 30.5%, kannada 36.7%.
- R3. Italian below `harsh` for alphabetic and syllabic: **replicated**. alphabetic: Italian 23.8% against `harsh` 26.8%, syllabic: Italian 2.4% against `harsh` 9.4%.
- R4. Revised rule picks the real relative in fewer than half of the `candidates_real` corpora: **replicated**. malayalam 0 of 24, kannada 10 of 24, italian 6 of 24.

## Task C (`candidates`), right family, % of corpora, seeds 3-5

| Hidden | Relative offered | EM revised | EM original | Frequency rank | Chosen by EM revised |
|---|---|---|---|---|---|
| Old Tamil | Malayalam | 0% | 0% | 33% | finnish 14, latin 10 |
| Old Tamil | Kannada | 42% | 0% | 8% | kannada 10, finnish 8, latin 6 |
| Latin | Italian | 25% | 0% | 29% | finnish 17, italian 6, tamil 1 |

