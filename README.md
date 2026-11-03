# semantic-deduper

A friendly, local-first Python CLI that finds near-duplicate notes and ideas in
your text files using fuzzy matching, then groups the candidates so you can
review them in a spreadsheet.

Built by **Asdale Dynamics, LLC** (Indiana, formed October 2026) —
beginner-friendly AI education, books, and practical local-first tools.
Learn more at dylanasdale.github.io.

No API keys. No cloud. No accounts. No personal data leaves your computer.
Everything runs on your machine with Python's standard library only.

## Who this is for

You keep notes, ideas, meeting summaries, or drafts in `.txt` and `.md` files.
Over time, duplicates creep in — the same thought saved twice, a near-identical
meeting recap, a paragraph you reused. This tool finds those near-duplicates
and groups them so you can decide what to keep, merge, or delete.

No AI background needed. If you can open a terminal, you can use this.

## Install

```bash
git clone <this repo>
cd semantic-deduper-cli
pip install .
```

That installs the `semantic-deduper` command. If your Python installation
blocks installs (some systems do), add `--break-system-packages`:

```bash
pip install . --break-system-packages
```

Or run without installing:

```bash
python3 -m semantic_deduper scan .
```

## Step 1: Scan your notes

Pick a folder full of notes and scan it:

```bash
semantic-deduper scan ./notes --threshold 0.85 --min-length 30
```

You will see something like:

```
Scanned 42 text file(s) in ./notes
Near-duplicate candidate pairs: 7
Review groups: 3
Local store written to .semantic_deduper_store.json
```

### What the options mean

- `./notes` — the folder to scan (defaults to the current folder).
- `--threshold 0.85` — how similar two notes must be to count as a match,
  from 0.0 to 1.0. Higher means stricter. Default: 0.85.
- `--min-length 30` — skip files shorter than this many characters.
  Default: 20. Use this to ignore tiny fragments.
- `--extensions .txt .md` — file types to include. Default: `.txt .md`.
- `--store` — where to save the local results file.
  Default: `.semantic_deduper_store.json`.

## Step 2: Export a CSV report

Turn the saved results into a spreadsheet-friendly report:

```bash
semantic-deduper report --store .semantic_deduper_store.json --output dupes.csv
```

Open `dupes.csv` in Excel, Google Sheets, Numbers, or any text editor. Each row
is one candidate pair:

| group_id | file_a_index | file_b_index | similarity | file_a | file_b |
|----------|--------------|--------------|------------|--------|--------|
| 1 | 3 | 7 | 0.9899 | ./notes/meeting.md | ./notes/meeting_copy.md |

- `group_id` — notes linked together (if A matches B and B matches C, they all
  share one group id).
- `similarity` — how alike the two notes are, from 0.0 to 1.0.
- `file_a` / `file_b` — the two file paths to compare.

Review the groups, then keep, merge, or delete as you like.

## How it works

1. `scan` reads every `.txt` and `.md` file in your folder.
2. It skips files too short or too different in size to possibly match.
3. Remaining pairs get a fast shingle check, then an exact
   `difflib.SequenceMatcher` similarity score.
4. Pairs above your threshold are clustered into groups (A matches B, B
   matches C → all three in one group).
5. Results are saved locally as JSON; `report` writes them to CSV.

Everything stays on your machine. Nothing is uploaded. No keys or secrets are
ever needed.

## Tests

```bash
pip install pytest
pytest
```

Tests cover the fuzzy matcher, the grouping logic, and the directory scanner.
15 tests, all passing.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is an Indiana LLC founded by Dylan Asdale, a registered
nurse turned AI author and founder of ASDALE DYNAMICS, LLC. Dylan's book
*The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a
friend would": plain English, step by step, never condescending.

The LLC focuses on beginner-friendly AI education, books and guides, and
practical tools it can publish or sell — from local AI utilities and prompt
tools to small business and author helpers. This CLI is one of those tools:
clear, warm, polished, tested, local-first, and free of secrets or personal
data.
