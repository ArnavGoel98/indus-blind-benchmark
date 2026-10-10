# Block-split test (pre-registration entry 3; dev seeds 90-91)

Halves: share of the source's clauses / word types kept by the hidden and the sister half.
Yardsticks: JSD above floor / shared word forms (cc) / word pairs (cc) / verbatim 6+.

| Language | Split | Hidden half | Sister half | v1-like sister | Mid setting |
|---|---|---|---|---|---|
| sanskrit | content | 50% / 78% | 50% / 78% | 0.005 / 75.5% / 26.9% / 39.7% | 0.169 / 9.7% / 1.1% / 6.7% |
| sanskrit | block250 | 50% / 68% | 50% / 68% | 0.004 / 69.0% / 16.9% / 25.3% | 0.154 / 9.7% / 0.8% / 5.9% |
| sanskrit | block1000 | 49% / 67% | 51% / 69% | 0.005 / 68.4% / 16.9% / 27.9% | 0.178 / 9.0% / 0.5% / 6.3% |
| sanskrit | block4000 | 51% / 67% | 49% / 67% | 0.008 / 66.6% / 15.5% / 25.3% | 0.152 / 11.9% / 2.0% / 6.3% |
| sanskrit | halves | 50% / 68% | 50% / 65% | 0.015 / 64.0% / 11.3% / 21.8% | 0.159 / 12.3% / 1.3% / 3.6% |
| tamil | content | 50% / 62% | 50% / 62% | 0.003 / 57.3% / 7.8% / 18.4% | 0.111 / 9.2% / 0.2% / 3.6% |
| tamil | block250 | 51% / 62% | 49% / 61% | 0.002 / 56.5% / 8.5% / 19.1% | 0.114 / 9.7% / 0.2% / 5.0% |
| tamil | block1000 | 53% / 66% | 47% / 56% | 0.005 / 51.5% / 6.1% / 16.7% | 0.127 / 7.7% / 0.2% / 3.2% |
| tamil | block4000 | 43% / 54% | 57% / 66% | 0.007 / 55.7% / 4.6% / 16.0% | 0.100 / 13.3% / 0.1% / 4.9% |
| tamil | halves | 50% / 64% | 50% / 55% | 0.010 / 47.3% / 3.3% / 13.5% | 0.115 / 7.3% / 0.0% / 3.8% |
| sumerian | content | 50% / 64% | 50% / 64% | 0.036 / 68.3% / 36.7% / 35.8% | 0.113 / 16.0% / 8.1% / 8.5% |
| sumerian | block250 | 50% / 66% | 50% / 65% | 0.027 / 71.6% / 41.1% / 44.6% | 0.115 / 20.4% / 8.2% / 9.9% |
| sumerian | block1000 | 49% / 63% | 51% / 67% | 0.032 / 71.8% / 41.5% / 45.5% | 0.108 / 18.6% / 7.3% / 8.7% |
| sumerian | block4000 | 52% / 68% | 48% / 58% | 0.031 / 66.8% / 39.6% / 40.4% | 0.103 / 19.1% / 8.8% / 7.9% |
| sumerian | halves | 50% / 64% | 50% / 60% | 0.082 / 44.5% / 20.3% / 21.8% | 0.153 / 16.7% / 5.6% / 6.9% |
| latin | content | 50% / 64% | 50% / 63% | 0.005 / 53.0% / 6.7% / 11.8% | 0.139 / 7.4% / 0.7% / 2.3% |
| latin | block250 | 53% / 63% | 47% / 62% | 0.005 / 51.5% / 7.8% / 13.7% | 0.146 / 5.8% / 0.8% / 3.2% |
| latin | block1000 | 57% / 67% | 43% / 56% | 0.009 / 47.9% / 6.3% / 9.7% | 0.146 / 6.2% / 0.7% / 1.7% |
| latin | block4000 | 0% / 0% | 100% / 100% | a half is (nearly) empty: too few blocks | a half is (nearly) empty: too few blocks |
| latin | halves | 50% / 41% | 50% / 71% | 0.029 / 41.7% / 5.1% / 9.7% | 0.169 / 5.9% / 0.4% / 1.3% |
| finnish | content | 51% / 62% | 49% / 62% | 0.004 / 53.8% / 9.2% / 19.2% | 0.155 / 4.7% / 0.3% / 3.4% |
| finnish | block250 | 48% / 61% | 52% / 63% | 0.003 / 53.2% / 14.2% / 21.6% | 0.138 / 6.2% / 0.5% / 3.3% |
| finnish | block1000 | 52% / 64% | 48% / 58% | 0.003 / 51.6% / 13.6% / 21.6% | 0.147 / 6.2% / 0.5% / 3.3% |
| finnish | block4000 | 30% / 40% | 70% / 80% | 0.004 / 57.5% / 15.0% / 25.1% | 0.142 / 4.7% / 0.6% / 3.0% |
| finnish | halves | 50% / 62% | 50% / 61% | 0.003 / 52.5% / 13.5% / 20.2% | 0.157 / 4.3% / 0.3% / 2.5% |

## Split chosen (entry 3 rule: largest block size, 250 / 1,000 / 4,000, whose halves each keep >= 40% of clauses and of word types)

| Language | Split |
|---|---|
| sanskrit | block4000 |
| tamil | block4000 |
| sumerian | block4000 |
| latin | block1000 |
| finnish | block1000 |

**Limitation (recorded as entry 3 requires).** Blocks do not remove shared formulaic text: for the v1-like sister, verbatim overlap stays far above the 2% constraint under every split (it falls only in Sanskrit and rises slightly in Sumerian). A real relative's texts differ in content as well as in language; a sister cut from the same source cannot reproduce that, so the verbatim constraint can only be met by changing word forms heavily.


