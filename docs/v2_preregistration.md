# v2 pre-registration

Status: written 2026-10-09 on branch `v2`, before any v2 final run. Every entry here enters the
`frozen-v2` tag. Entries are added before the run they govern and never edited after it; a later
change is a new, dated entry that says what it replaces and why.

## 1. EM language-selection rule (Tasks C and D)

**Declaration.** For v2 final runs, the primary EM solver is the **revised selection rule**
(`knight2006_em`, `rule = "revised"`). The **original rule** (`knight2006_em_original`) is reported
beside it as secondary in every table where EM appears. The v1 paper is unchanged: there the original
rule stays primary.

**What the two rules are** (code unchanged since `frozen-v1`, `src/ibdb/methods/decipher.py`):
- Original: the pooled rare-unit state (OTHER) has learned emissions and unpinned mass, and the
  candidate language is chosen by raw log-likelihood per sign bigram.
- Revised: OTHER emits uniformly and its mass is pinned at 3% for every reference, and the candidate
  is chosen by the gain over a unigram-only model of the same reference, divided by the reference's
  own bigram mutual information.

**Reason.** The original rule's choice is dominated by one reference language, Sumerian, whatever the
hidden language is:
- **v1 main runs, `candidates` tier, all language corpora:** it picks Sumerian for 91% of corpora
  (652/720, sampler A) and 71% (299/420, sampler B). The revised rule picks Sumerian for 0% and 1%.
- **Ugaritic-Hebrew anchor (`reports/v2/ugaritic/results.md`):** in `candidates` (Hebrew plus the
  five v1 languages) the original rule picks Sumerian in all 5 conditions and scores 0% on Task D. The
  revised rule picks Hebrew in all 5 and scores 25-32% of tokens.

**Known weakness of the revised rule, stated now so it cannot be discovered later and explained away.**
It is not unbiased: in v1 sampler A it picks Latin for 58% of corpora (416/720) and Finnish for 33%.
It picks the true sister more often than the original rule (36% vs 28% of corpora, sampler A; 57% vs
47%, sampler B), but far from always. v2 reports which reference each rule picks, by hidden language,
beside every Task C rate.

**Status of the evidence.** The revised rule was written during v1 development after the original
rule was seen to pick Sumerian for almost every corpus (v1 paper, Section 3.7). It is therefore post hoc with
respect to v1. The Ugaritic anchor is the first data it had not been tuned on, and there it picked the
right language in every condition. That is one real case, not a validation.

**What this does not change.** Task D scores stay "before the cognate step". Thresholds (50% of
tokens) and tiers are unchanged. No other method parameter changes.
