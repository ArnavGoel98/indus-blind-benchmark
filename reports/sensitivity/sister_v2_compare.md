# Sensitivity sweep: sister-v2 primary vs sister-v1 upper bound

Generator v1, Indus point, 6 x 5 grid, seeds 0-2, methods frozen. Cell means of Task D token accuracy. Box = duplicates 0.2-0.4 x inventory 400-700. S = seals-only region (duplicates 0.0); T = tablets-only region (duplicates 0.4-0.5); prediction, not measurement.

## sister-v2, primary (before cognate)

- Records: 1800; status {'ok': 1451, 'length_distorted': 116, 'unreachable_low': 85, 'unreachable_high': 126, 'tolerance_miss': 22}; strict panel 7 combinations; box panel 10 combinations.
- Candidates, original rule, box panel: 2.9-4.2%; all corpora in box: 1.7-4.5%.
- Within-combination spread across the box (original): median 2.1 points, max 7.5 (sumerian/alphabetic), 0 of 10 >= 10 points.
- Same, revised rule (post hoc): median 5.9, max 43.8 points.
- Candidates, revised rule, box panel: 5.6-14.2%.
- No relative, box panel max cell: original 3.7%, revised 4.3%; whole grid max cell: original 4.6%, revised 6.3%.
- Archaeology (all panel), original: S 2.8-7.0% vs T 0.6-3.0%; revised: S 6.5-24.4% vs T 2.5-11.7%; none tier max 6.3%.
- Archaeology (balanced panel), original: S 0.6-4.3% vs T 0.4-1.1%; revised: S 7.1-22.5% vs T 1.6-7.1%; none tier max 2.4%.

## sister-v2, with oracle sound correspondences

- Records: 1800; status {'ok': 1451, 'length_distorted': 116, 'unreachable_low': 85, 'unreachable_high': 126, 'tolerance_miss': 22}; strict panel 7 combinations; box panel 10 combinations.
- Candidates, original rule, box panel: 2.9-4.5%; all corpora in box: 1.9-4.5%.
- Within-combination spread across the box (original): median 2.7 points, max 6.7 (sumerian/alphabetic), 0 of 10 >= 10 points.
- Same, revised rule (post hoc): median 5.9, max 67.1 points.
- Candidates, revised rule, box panel: 7.4-20.6%.
- No relative, box panel max cell: original 3.7%, revised 4.3%; whole grid max cell: original 4.6%, revised 6.3%.
- Archaeology (all panel), original: S 2.8-8.4% vs T 0.7-3.3%; revised: S 8.9-37.2% vs T 3.6-15.4%; none tier max 6.3%.
- Archaeology (balanced panel), original: S 0.6-6.6% vs T 0.5-1.5%; revised: S 10.5-41.2% vs T 2.3-10.9%; none tier max 2.4%.

## upper bound (sister-v1, known overlap), with oracle sound correspondences

- Records: 1800; status {'ok': 1454, 'unreachable_low': 87, 'unreachable_high': 127, 'length_distorted': 117, 'tolerance_miss': 15}; strict panel 5 combinations; box panel 10 combinations.
- Candidates, original rule, box panel: 3.5-5.1%; all corpora in box: 2.2-5.2%.
- Within-combination spread across the box (original): median 2.1 points, max 7.6 (sumerian/alphabetic), 0 of 10 >= 10 points.
- Same, revised rule (post hoc): median 5.5, max 61.8 points.
- Candidates, revised rule, box panel: 8.7-21.8%.
- No relative, box panel max cell: original 3.2%, revised 4.3%; whole grid max cell: original 4.6%, revised 7.1%.
- Archaeology (all panel), original: S 3.5-14.5% vs T 0.4-4.9%; revised: S 10.9-38.6% vs T 4.2-17.3%; none tier max 7.1%.
- Archaeology (balanced panel), original: S 0.7-20.5% vs T 0.0-1.4%; revised: S 13.0-41.7% vs T 2.6-15.7%; none tier max 2.2%.

No relative, sister-v2 sweep, every valid corpus: best 26.5%, corpora >= 50%: 0 of 2902 (both rules).

## Generator-v2 corpora inside the plausible box (Indus point, sister-v2 runs, seeds 0-5)

- primary: 37 corpora, mean 11.9%, max 72.0%
- with oracle sound correspondences: 37 corpora, mean 18.0%, max 93.9%
