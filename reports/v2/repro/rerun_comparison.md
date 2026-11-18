# Rerun of the v2 final run: comparison with the archive

Reproducibility check, not a new result: the entry-12 readings stand as reported. Same code (`frozen-v2.1`), same seeds 6-11. Value classes were fixed before the rerun was read (see the script's docstring and `README.md`).

## Failures first

- Rerun errors: 0.
- Exact-class values that differ: **0**.
- Readings whose verdict changed on the rerun: none.

## Exact class (must match bit for bit)

| File | Corpora (archive / rerun) | Values compared | Differ |
|---|---|---|---|
| records | 240 / 240 | 12,048 | 0 |
| predictions | 240 / 240 | 301,395 | 0 |
| v1_sister | 240 / 240 | 26,112 | 0 |
| c4_records | 24 / 24 | 1,312 | 0 |

Corpora with the archived token count: finnish 48 of 48; latin 48 of 48; sanskrit 48 of 48; sumerian 48 of 48; tamil 0 of 48.

## Replication class (Old Tamil text changed upstream)

| File | Values compared | Identical | Differ |
|---|---|---|---|
| records | 19,536 | 14,501 | 5,035 |
| predictions | 718,002 | 260,944 | 457,058 |
| v1_sister | 12,585 | 8,358 | 4,227 |
| c4_records | 2,688 | 1,783 | 905 |

## The readings, archive and rerun

| Reading | Archive | Rerun |
|---|---|---|
| H1 | met: highest 40.5 (Kannada, alphabetic) | met: highest 30.8 (Malayalam, alphabetic) |
| H2a | met: +17.0; 11 of 12 | met: +17.0; 11 of 12 |
| H2b | met: +23.9; 11 of 12 | met: +10.5; 10 of 12 |
| H3 | **not met**: 3 of 8: Malayalam syllabic +6.2, 10/12, Estonian syllabic +8.7, 10/12, Estonian logosyllabic +5.4, 9/12 | **not met**: 3 of 8: Malayalam syllabic +5.1, 9/12, Estonian syllabic +8.7, 10/12, Estonian logosyllabic +5.4, 9/12 |
| H4 | met: 12 of 12 | met: 12 of 12 |
| H5 | met: Malayalam 27.8, Kannada 40.5 | met: Malayalam 30.8, Kannada 30.3 |
| H6 | met: 16.6 vs 26.3; 3.0 vs 16.3 | met: 16.6 vs 26.3; 3.0 vs 16.3 |
| H7 | met: Italian 12, Malayalam 0, Kannada 23 of 48 | met: Italian 12, Malayalam 0, Kannada 20 of 48 |
| H8 | met: 3,904 of 3,904 identical (24 corpora) | met: 3,904 of 3,904 identical (24 corpora) |
