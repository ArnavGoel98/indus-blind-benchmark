# Positive control: frozen EM on English letter-substitution ciphers

Knight et al. (2006, Sec. 3) setting: English letter bigrams with known word boundaries, 1:1 substitution of 26 letters, out-of-domain ciphertext. Their bigram EM/Viterbi baseline on a 417-letter article: 68 errors = 83.7% correct (2.4% error with trigrams, cubing and smoothing). Ours: frozen `frozen-v1` EM, benchmark settings (3 restarts, 60 iterations). Plaintext model from Pride and Prejudice + Moby Dick; ciphertext from On the Origin of Species (Project Gutenberg). 10 random passages and random keys per length. Letter accuracy = share of cipher letters decoded correctly.

| Plaintext-model data | Cipher length (letters) | Original rule: mean [min, max] | Revised rule: mean [min, max] |
|---|---|---|---|
| 70k chars | 100 | 71.7% [55, 91] | 69.3% [46, 91] |
| 70k chars | 200 | 84.6% [53, 97] | 84.7% [60, 97] |
| 70k chars | 417 | 97.4% [93, 100] | 96.9% [90, 100] |
| 70k chars | 1,000 | 99.8% [99, 100] | 99.6% [99, 100] |
| 70k chars | 2,000 | 99.9% [100, 100] | 99.8% [100, 100] |
| 70k chars | 5,000 | 99.9% [100, 100] | 99.7% [99, 100] |
| 1.5M chars | 100 | 58.2% [13, 92] | 60.9% [13, 92] |
| 1.5M chars | 200 | 92.2% [81, 96] | 92.7% [81, 96] |
| 1.5M chars | 417 | 97.5% [90, 100] | 97.7% [91, 100] |
| 1.5M chars | 1,000 | 99.7% [98, 100] | 99.6% [98, 100] |
| 1.5M chars | 2,000 | 99.9% [100, 100] | 99.7% [99, 100] |
| 1.5M chars | 5,000 | 99.9% [100, 100] | 99.8% [100, 100] |

Reference point (Knight et al. 2006): bigram EM/Viterbi, 417 letters, 83.7% correct; best configuration 97.6%. Their decoding uses Viterbi over the whole text; ours maps each cipher letter to one plaintext letter (sign-level assignment), so the two are close but not identical measures.
