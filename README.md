# semantic-deduper

A local-first Python CLI that finds near-duplicate notes and ideas in your text
files using fuzzy matching, then groups the candidates for review.

Built and published by **Asdale Dynamics, LLC** (Indiana, formed October 2026)
— beginner-friendly AI education, books, and practical local-first tools.
Learn more at dylanasdale.github.io.

No API keys. No cloud. No accounts. Everything runs on your machine with
Python's standard library only.

## What it does

- Scans a folder (recursively) for `.txt` and `.md` files
- Compares every pair of notes with `difflib` fuzzy matching (SequenceMatcher)
- Groups near-duplicates into review groups using union-find clustering
- Saves results to a local JSON store (`--store`)
- Exports a CSV report (`--output`) you can open in any spreadsheet

## Install

```bash
git clone <this repo>
cd semantic-deduper-cli
pip install .
```

Or run without installing:

```bash
python -m semantic_deduper.cli scan .
```

## Usage

Scan a folder for near-duplicates:

```bash
semantic-deduper scan ./notes --threshold 0.85 --min-length 30
```

Output:

```
Scanned 42 text file(s) in ./notes
Near-duplicate candidate pairs: 7
Review groups: 3
Local store written to .semantic_deduper_store.json
```

Export a CSV report from a saved store:

```bash
semantic-deduper report --store .semantic_deduper_store.json --output dupes.csv
```

The CSV has one row per candidate pair: group id, file indexes, similarity
score, and the two file paths. Review the groups, then decide what to keep,
merge, or delete.

### Options

`scan`
- `directory` — folder to scan (default: current directory)
- `--threshold` — similarity floor, 0.0–1.0 (default: 0.85)
- `--min-length` — ignore files shorter than this many characters (default: 20)
- `--extensions` — file extensions to include (default: `.txt .md`)
- `--store` — local JSON store path (default: `.semantic_deduper_store.json`)

`report`
- `--store` — local JSON store path (default: `.semantic_deduper_store.json`)
- `--output` — CSV report path (default: `dedupe_report.csv`)

## How it works

1. `scan` reads every text file in the folder.
2. Pairs too short or too different in length are skipped cheaply.
3. Remaining pairs get a shingle pre-filter, then an exact
   `difflib.SequenceMatcher` similarity score.
4. Pairs above the threshold are clustered into groups (if A matches B and B
   matches C, all three form one review group).
5. Results are saved locally as JSON; `report` renders them to CSV.

Everything stays on your machine. No data is ever uploaded, and no keys or
secrets are required.

## Tests

```bash
pip install pytest
pytest
```

Tests cover the fuzzy matcher, grouping logic, and directory scanner.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is an Indiana LLC founded by Dylan Asdale, a registered
nurse turned AI author and founder of ASDALE DYNAMICS, LLC. The LLC focuses on
beginner-friendly AI education, books and guides, and practical tools that can
be published or sold — from local AI utilities and prompt tools to small
business and author helpers. This CLI is one of those open-source tools: clear,
warm, polished, tested, local-first, and free of secrets or personal data.
