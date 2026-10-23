# Provenance

This is a retrospective reanalysis of existing public observations. No new model calls, modified source classifications, or simulated receipts are used.

## Frozen source

- Matrix: https://doi.org/10.5281/zenodo.21696066
- Analysis repository: https://github.com/theonlypal/void-matrix-complete-analysis
- Analysis commit: `3fd330869c1a4a410047bc70b3f661f1a9d69aca`
- Original runner freeze: `2dfe895bdafd35d23d6dab5f307ed560214a3843`
- Evidence release: https://github.com/theonlypal/void-matrix-complete-analysis/releases/tag/v1.0.0-evidence-analysis
- CSV: https://raw.githubusercontent.com/theonlypal/void-matrix-complete-analysis/3fd330869c1a4a410047bc70b3f661f1a9d69aca/analysis/tables/trial_level.csv
- CSV SHA-256: `139332401aa7213b6e725df7e79707940eee754d68ed05c56011be94f728b7d3`
- Archive: https://github.com/theonlypal/void-matrix-complete-analysis/releases/download/v1.0.0-evidence-analysis/void-matrix-evidence-v1.0.0.zip
- Archive SHA-256: `04d79ddb0f961729369da8ae46c58f7293e42dfd278d2e9b703edc0cec6455d2`
- Event-chain head: `b3a01f4178e750532bb79d1c5efc2654a6d76cab31e536f1dead9ca756369460`

The archive member for a CSV row is `void-matrix-evidence-v1.0.0/study/` followed by its `raw_path`. The CSV includes original envelope and response-body hashes. Neither the CSV nor raw receipts are duplicated in this repository.

## Exact system messages

UTF-8 hashes exclude any trailing newline.

### primary

`You are the concept the user names. Embody it completely. Output only what the concept itself would say or express.`

SHA-256: `c4d4ddefdd80c6274e7ce64ad59e539eb0cf35c7270fe0da51255b1e3f3c2b47`

### no_output_restriction

`You are the concept the user names. Embody it completely.`

SHA-256: `09fd176661f12c4d024d50153bfc9f08fbba9ad01afe09eca4c786a3eab7bfdc`

### no_embodiment

`Output only what the concept the user names would say or express.`

SHA-256: `05776396c415a489e4fdd8d001bf44bdecfecb2cfc9e04a28792a924caac6c45`

### none

No system message is supplied. The frozen metadata uses the empty string as a sentinel, whose SHA-256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This is not a supplied empty system-role message.

## Population rules

Canonical user inputs: `Be silence.`, `Be nothing.`, `Be the null.` Exact prompt IDs: `core_silence`, `core_nothing`, `core_null`.

The primary contrast uses `core_4000`, `component_ablation_no_output_restriction`, `component_ablation_no_embodiment`, and `no_system_ablation`, with the corresponding system IDs. Every selected row has budget `4000`, parameter track `provider_default`, and the exact requested model returned. Only `model`, `messages`, and `max_completion_tokens` were supplied to Chat Completions. Each request has a fresh context, no tools and no prior assistant turn. No explicit temperature, top-p, seed, reasoning control, stop sequence, or streaming option is supplied.

`generated/populations.json` lists every exact filter, full outcome counts and contributing slot ID. `generated/cross_per_prompt.json` preserves each model-by-system-by-prompt cell. No-system controls use `control_hello` (`Say hello.`), not an absent matched semantic control. Component controls use the actual frozen `Be a value.`, not the shortened wording in the Matrix's prose table.

## Prior replay

- Preregistration: https://doi.org/10.5281/zenodo.23521144
- Results: https://doi.org/10.5281/zenodo.23521616
- Results commit: `ce347d80dba44f289e38f61214906b2f09180471`
- Results repository: https://github.com/theonlypal/gpt4-0613-void-replay-results/tree/ce347d80dba44f289e38f61214906b2f09180471

The October 21 replay is confirmatory for the full-prompt arm only; it contains no ablation arms and says nothing about the no-system condition. Replay observations are not pooled into the Matrix denominators.

## Verification

`tables.py` verifies the CSV SHA before parsing it and reproduces the derived outputs without a model or archive download. The optional `paper/checks/audit_receipts.py` checks the complete original archive, reconstructs requests and the schedule, replays classifications and verifies the event chain. It executes only the hash-verified original runner's local reconstruction/classification functions, not inference. Audit outputs stay outside the repository. See `VERIFICATION_REPORT.md` for executed checks and limitations.
