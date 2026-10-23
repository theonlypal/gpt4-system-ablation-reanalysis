# Verified evidence for the system-prompt ablation paper

CSV SHA-256: `139332401aa7213b6e725df7e79707940eee754d68ed05c56011be94f728b7d3`
Public commit: `3fd330869c1a4a410047bc70b3f661f1a9d69aca`

CSV: https://github.com/theonlypal/void-matrix-complete-analysis/blob/3fd330869c1a4a410047bc70b3f661f1a9d69aca/analysis/tables/trial_level.csv
Direct CSV: https://raw.githubusercontent.com/theonlypal/void-matrix-complete-analysis/3fd330869c1a4a410047bc70b3f661f1a9d69aca/analysis/tables/trial_level.csv
Original paper: https://doi.org/10.5281/zenodo.21696066
Raw archive: https://github.com/theonlypal/void-matrix-complete-analysis/releases/download/v1.0.0-evidence-analysis/void-matrix-evidence-v1.0.0.zip

## Primary census

| Study | Ceiling | Sampling | Silence V0/N | Nothing V0/N | Null V0/N | NV | Total V0/N |
|---|---:|---|---:|---:|---:|---:|---:|
| core_100 | 100 | default | 100/100 | 100/100 | 95/100 | 5 | 295/300 |
| core_100 | 100 | temp. zero | 100/100 | 100/100 | 97/100 | 3 | 297/300 |
| core_4000 | 4000 | default | 100/100 | 100/100 | 98/100 | 2 | 298/300 |
| equivalence_9 | 4000 | default | 10/10 | 10/10 | 9/10 | 1 | 29/30 |
| All primary | mixed | mixed | 310/310 | 310/310 | 299/310 | 11 | 919/930 |

The primary census pools settings; it is not the setting-matched ablation baseline. The old core composite includes both token ceilings, not just the low ceiling.

## Setting-matched GPT-4 cells

| System | Prompt | N | V0 | NV | R | Other |
|---|---|---:|---:|---:|---:|---:|
| Full prompt | Be silence. | 100 | 100 | 0 | 0 | 0 |
|  | Be nothing. | 100 | 100 | 0 | 0 | 0 |
|  | Be the null. | 100 | 98 | 2 | 0 | 0 |
|  | Total | 300 | 298 | 2 | 0 | 0 |
| No output restriction | Be silence. | 10 | 0 | 0 | 10 | 0 |
|  | Be nothing. | 10 | 0 | 0 | 10 | 0 |
|  | Be the null. | 10 | 0 | 0 | 10 | 0 |
|  | Total | 30 | 0 | 0 | 30 | 0 |
| No embodiment | Be silence. | 10 | 0 | 7 | 3 | 0 |
|  | Be nothing. | 10 | 0 | 0 | 10 | 0 |
|  | Be the null. | 10 | 0 | 6 | 4 | 0 |
|  | Total | 30 | 0 | 13 | 17 | 0 |
| No system | Be silence. | 10 | 0 | 0 | 10 | 0 |
|  | Be nothing. | 10 | 0 | 0 | 10 | 0 |
|  | Be the null. | 10 | 0 | 0 | 10 | 0 |
|  | Total | 30 | 0 | 0 | 30 | 0 |

## Cross-model comparison

| Model | Full V0/N | No output restriction | No embodiment | No system |
|---|---:|---:|---:|---:|
| gpt-4-0613 | 298/300 | 0/30 | 0/30 | 0/30 |
| gpt-5.2-2025-12-11 | 282/300 | 16/30 | 9/30 | 0/30 |
| gpt-5.5-2026-04-23 | 287/300 | 20/30 | 21/30 | 20/30 |
| gpt-5.6-luna | 199/300 | 19/30 | 18/30 | 20/30 |
| gpt-5.6-sol | 115/300 | 4/30 | 4/30 | 14/30 |
| gpt-5.6-terra | 227/300 | 22/30 | 22/30 | 19/30 |

## Interpretation boundaries

- Retrospective reanalysis, not a newly preregistered hypothesis.
- Full-prompt and ablation comparisons use the same ceiling and parameter track but different sample sizes.
- No-embodiment is a tested rewrite retaining the output restriction, not an independent deletion of each sentence.
- NV includes nonempty ellipsis strings; it must not be merged with V0 or relabeled ordinary prose.
- Requested/returned snapshot identity is observable. Frozen provider weights, native EOS logits, and internal mechanisms are not.
- Later-model behavior is heterogeneous; GPT-5.2 also has no no-system Voids in these canonical cells.
- No-system controls are Say hello., not the paired speech/something/value panel used in the other studies.

## No-system controls

| Model | N | Voids | NV | R | R/N |
|---|---:|---:|---:|---:|---:|
| gpt-4-0613 | 10 | 0 | 0 | 10 | 10/10 |
| gpt-5.2-2025-12-11 | 10 | 0 | 0 | 10 | 10/10 |
| gpt-5.5-2026-04-23 | 10 | 0 | 0 | 10 | 10/10 |
| gpt-5.6-luna | 10 | 0 | 0 | 10 | 10/10 |
| gpt-5.6-sol | 10 | 0 | 0 | 10 | 10/10 |
| gpt-5.6-terra | 10 | 0 | 0 | 10 | 10/10 |