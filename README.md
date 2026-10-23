# Alignment Is a System Property, Not Just a Model Property

**System-Prompt Ablation and Zero-Byte Continuation in GPT-4-0613.** Retrospective reanalysis of the frozen Cross-Vendor Semantic Void Matrix. Exact prompt cells, competing outcomes, controls, and cross-model comparisons are generated from a SHA-256-pinned public CSV. The setting-matched comparison is separate from the pooled primary census. No new inference is performed. [Results tables](generated/EVIDENCE_BRIEF.md) · [Provenance](PROVENANCE.md) · [Verification](VERIFICATION_REPORT.md) · [Related work](RELATED_WORK.md).

## Reproduce

Python 3.11 or later; ReportLab 4.4.9 for the deterministic figure.

```sh
python3 -m pip install reportlab==4.4.9
curl --fail --location 'https://raw.githubusercontent.com/theonlypal/void-matrix-complete-analysis/3fd330869c1a4a410047bc70b3f661f1a9d69aca/analysis/tables/trial_level.csv' --output /tmp/matrix-trial-level.csv
python3 tables.py --csv /tmp/matrix-trial-level.csv
(cd generated && shasum -a 256 -c SHA256SUMS)
CSV_PATH=/tmp/matrix-trial-level.csv python3 -m unittest discover -s paper/checks -p 'test_*.py' -v
```

Expected generated-output hashes: [generated/SHA256SUMS](generated/SHA256SUMS). Save that manifest before regeneration or use `git diff --exit-code -- generated` afterward to compare against the committed outputs. The generator rejects a mismatched input before writing outputs.

Source: [Matrix DOI](https://doi.org/10.5281/zenodo.21696066), [evidence release](https://github.com/theonlypal/void-matrix-complete-analysis/releases/tag/v1.0.0-evidence-analysis), [pinned CSV](https://raw.githubusercontent.com/theonlypal/void-matrix-complete-analysis/3fd330869c1a4a410047bc70b3f661f1a9d69aca/analysis/tables/trial_level.csv). Original data are linked, not repackaged.
