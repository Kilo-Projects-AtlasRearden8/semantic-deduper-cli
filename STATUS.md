# STATUS

## What was built

`semantic-deduper-cli` — a local-first Python CLI that finds near-duplicate
notes and ideas in local text files using fuzzy matching and groups the
candidates for review.

Components:
- `semantic_deduper/matcher.py` — fuzzy matching with `difflib.SequenceMatcher`
  (stdlib only), shingle pre-filter, length-ratio pre-filter, similarity
  thresholding
- `semantic_deduper/scanner.py` — recursive directory scan of `.txt`/`.md`
  files, binary/undecodable files skipped
- `semantic_deduper/grouping.py` — union-find clustering of matches into
  review groups
- `semantic_deduper/storage.py` — local JSON store of scan results
  (`--store`, default `.semantic_deduper_store.json`)
- `semantic_deduper/report.py` — CSV report export (`--output`)
- `semantic_deduper/cli.py` — `scan` and `report` subcommands via argparse
- `tests/` — 15 tests covering matcher, grouping, and scanner (pytest)
- `pyproject.toml` — installable package with `semantic-deduper` console script
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — usage docs crediting Asdale Dynamics, LLC

Local-first, no API keys, no secrets, no network, no external dependencies.

## How to run

```bash
cd /workspace/kilo-lab/semantic-deduper-cli
pip install -e . --break-system-packages   # or pip install .
semantic-deduper scan ./notes --threshold 0.85 --min-length 30
semantic-deduper report --store .semantic_deduper_store.json --output dupes.csv
# or without installing:
python3 -m semantic_deduper.cli scan .
```

Tests: `python3 -m pytest -q`

## Verification results

- `pip install -e .` succeeds; `semantic-deduper` entry point installed
- `python3 -m pytest -q`: 15 passed
- End-to-end: scanned 5 sample files (4 text + 1 binary), found 1 near-duplicate
  pair (a.txt vs b.txt, similarity 0.9899), produced 1 review group, wrote
  `report.csv` with columns group_id, file indexes, similarity, file_a, file_b
- `semantic-deduper --help` and `scan --help` render correctly
- No `.github/workflows` files; no secrets or personal data in repo
- LICENSE copyright line exactly: `Copyright (c) 2026 Asdale Dynamics, LLC`
- README credits Asdale Dynamics, LLC

Committed as `d34a819` on branch `master` (git identity: Dylan Asdale).
Not pushed; no remote created.

## Known gaps

- Store keeps file paths/metadata only, not contents; report needs the store
  from the same scan (paths are absolute, so moving files breaks them)
- No incremental/resume scan; rescan re-reads all files
- Quadratic pairwise comparison; fine for personal notes folders, slow for
  very large collections
- Default extensions `.txt` `.md` only; override with `--extensions`
- No GUI/interactive review workflow; CSV is the review artifact
- Tested with Python 3.13 and pytest 9.1.1; requires `--break-system-packages`
  on this externally managed Python environment
