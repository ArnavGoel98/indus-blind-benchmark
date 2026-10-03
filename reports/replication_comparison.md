# Replication (seeds 3-5) vs main run (seeds 0-2), generator v1

Same frozen methods. Raw comparison output from the analysis script; 95% cluster-bootstrap CIs in brackets.

```
(a) Task D, candidates tier, EM revised | EM original | baseline
     500 x  4.6 (tokens    2300): main 0.102 [0.03,0.19] | 0.027 | 0.032   rep 0.087 [0.02,0.17] | 0.027 | 0.045
    2906 x  4.6 (tokens   13367): main 0.146 [0.05,0.24] | 0.021 | 0.029   rep 0.136 [0.05,0.23] | 0.033 | 0.037
   10000 x  4.6 (tokens   46000): main 0.190 [0.07,0.32] | 0.044 | 0.042   rep 0.187 [0.09,0.30] | 0.031 | 0.041
   50000 x  4.6 (tokens  229999): main 0.169 [0.06,0.29] | 0.051 | 0.034   rep 0.162 [0.07,0.26] | 0.059 | 0.033
    2906 x  3.0 (tokens    8718): main 0.086 [0.02,0.17] | 0.026 | 0.024   rep 0.085 [0.03,0.15] | 0.026 | 0.026
    2906 x  6.0 (tokens   17436): main 0.193 [0.06,0.33] | 0.071 | 0.039   rep 0.192 [0.08,0.31] | 0.071 | 0.048
    2906 x 10.0 (tokens   29060): main 0.332 [0.16,0.49] | 0.326 | 0.039   rep 0.289 [0.14,0.43] | 0.286 | 0.038
    2906 x 20.0 (tokens   58120): main 0.438 [0.20,0.64] | 0.436 | 0.055   rep 0.438 [0.21,0.64] | 0.450 | 0.062
  none tier EM revised at Indus: {'main': '0.033 [0.02,0.05]', 'rep': '0.030 [0.02,0.05]'}
  related tier EM revised at Indus: {'main': '0.258 [0.13,0.38]', 'rep': '0.259 [0.15,0.37]'}
  related, length 20: {'main': '0.485 [0.28,0.67]', 'rep': '0.502 [0.29,0.69]'}

(b) entropy ratio at Indus point: i.i.d. control vs languages
  main full  : iid 0.470 | languages 0.477 [p10 0.35, p90 0.67]
  main top100: iid 0.696 | languages 0.605 [p10 0.48, p90 0.74]
  main Rao band bal.acc full 0.77 [0.57,0.90] | holdout 0.57 [0.32,0.81]
  main FPR Rao on families: {'language': 0.7, 'heraldry': 0.0, 'emblem_markov': 0.0, 'admin_tags': 0.0, 'adversarial': 0.0, 'rao_type1': 1.0, 'rao_type2': 0.0, 'kamon': 1.0}
  rep  full  : iid 0.467 | languages 0.476 [p10 0.33, p90 0.67]
  rep  top100: iid 0.696 | languages 0.601 [p10 0.46, p90 0.74]
  rep  Rao band bal.acc full 0.77 [0.56,0.90] | holdout 0.49 [0.25,0.75]
  rep  FPR Rao on families: {'language': 0.7, 'heraldry': 0.0, 'admin_tags': 0.0, 'emblem_markov': 0.0, 'adversarial': 0.0, 'rao_type1': 1.0, 'rao_type2': 0.0, 'kamon': 1.0}

(c) no script-type oracle, Indus point: mean token acc, share of corpora >=50%
  main candidates knight2006_em            0.119 [0.03,0.21]  >=50%: 0.07 [0.00,0.15]
  main candidates knight2006_em_original   0.016 [0.00,0.03]  >=50%: 0.00 [0.00,0.00]
  main candidates em_cognate_matcher       0.016 [0.01,0.03]  >=50%: 0.00 [0.00,0.00]
  main none       knight2006_em            0.028 [0.01,0.04]  >=50%: 0.00 [0.00,0.00]
  main none       knight2006_em_original   0.015 [0.00,0.03]  >=50%: 0.00 [0.00,0.00]
  main none       em_cognate_matcher       0.009 [0.00,0.02]  >=50%: 0.00 [0.00,0.00]
  main related    knight2006_em            0.214 [0.10,0.33]  >=50%: 0.20 [0.05,0.35]
  main related    knight2006_em_original   0.208 [0.09,0.32]  >=50%: 0.20 [0.05,0.35]
  main related    em_cognate_matcher       0.050 [0.02,0.08]  >=50%: 0.00 [0.00,0.00]
  main script type predicted correctly: 0.43
  rep  candidates knight2006_em            0.106 [0.03,0.20]  >=50%: 0.10 [0.02,0.22]
  rep  candidates knight2006_em_original   0.022 [0.01,0.04]  >=50%: 0.00 [0.00,0.00]
  rep  candidates em_cognate_matcher       0.020 [0.01,0.03]  >=50%: 0.00 [0.00,0.00]
  rep  none       knight2006_em            0.027 [0.01,0.05]  >=50%: 0.00 [0.00,0.00]
  rep  none       knight2006_em_original   0.018 [0.00,0.04]  >=50%: 0.00 [0.00,0.00]
  rep  none       em_cognate_matcher       0.015 [0.00,0.03]  >=50%: 0.00 [0.00,0.00]
  rep  related    knight2006_em            0.213 [0.11,0.32]  >=50%: 0.23 [0.08,0.40]
  rep  related    knight2006_em_original   0.203 [0.10,0.32]  >=50%: 0.22 [0.08,0.37]
  rep  related    em_cognate_matcher       0.048 [0.02,0.08]  >=50%: 0.00 [0.00,0.00]
  rep  script type predicted correctly: 0.43

Task A best / B best / C at Indus:
  main {'rao2009_entropy': 0.77, 'yadav2010_markov': 0.66, 'fuls_positional': 0.65, 'lee2010_tree': 0.65, 'ling_classifier_lr': 0.55} | B {'script_type_inventory_rule': 0.25, 'script_type_lr': 0.43, 'segmentation_branching': 0.22} | C cand {'baseline_frequency_rank': 0.42, 'knight2006_em': 0.45, 'knight2006_em_original': 0.2, 'em_cognate_matcher': 0.23}
  rep {'rao2009_entropy': 0.77, 'yadav2010_markov': 0.64, 'fuls_positional': 0.67, 'lee2010_tree': 0.72, 'ling_classifier_lr': 0.66} | B {'script_type_inventory_rule': 0.25, 'script_type_lr': 0.43, 'segmentation_branching': 0.25} | C cand {'baseline_frequency_rank': 0.4, 'knight2006_em': 0.38, 'knight2006_em_original': 0.2, 'em_cognate_matcher': 0.15}
```

See reports/generator_comparison.md for generator v1 vs v2 on seeds 0-2.
