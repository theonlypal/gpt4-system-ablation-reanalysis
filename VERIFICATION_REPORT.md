# Verification report

Phase 1 source audit: PASS. Final revised PDF and clean-clone validation pending. No new model calls were performed.

The pinned CSV and original ZIP SHA-256 values matched. The complete raw audit checked 31,430 final trials, 31,484 retained raw attempts, 54 nonfinal attempts, and 62,968 event hashes. Frozen request/schedule reconstruction and classifier replay passed. Independent classification of 17,005 successful OpenAI responses agreed, with no returned-model mismatch.

`tables.py --csv inputs/trial_level.csv` regenerated every result table and figure. Prompt hashes matched the frozen archive. The setting-matched focal contrast is 298/300 V0 versus 0/90 across ablations; the 919/930 census and 890/900 core composite remain separate. The latter includes both budgets, not the low-budget subset alone.

All checks are offline evidence verification, not new provider execution. The original verified PDF is preserved for the final release.
