# SafeLock-CSV

This tool takes the CSV created in the SafeLock Stellar One console from the
Stellar Enforce scan tool to make the whitelist.

This tool requires Python 3.9+ and has no runtime dependencies — it uses only
the Python standard library (`csv`, `pathlib`, `argparse`, `logging`).

## Installation

No installation is required beyond a Python 3.9+ interpreter. If you plan to
run the test suite, install the dev dependencies:

```bash
pip install -r requirements-dev.txt
```

Two folders are used by default:
- `approve-list-csv` — the raw CSVs exported from Stellar Enforce
- `approve-list-done` — the cleaned CSVs written by this tool (created
  automatically if it doesn't exist)

## Usage

```bash
python main.py
```

By default this reads CSVs from `./approve-list-csv` and writes cleaned CSVs
to `./approve-list-done`. Both locations can be overridden:

```bash
python main.py --input-dir /path/to/raw-csv --output-dir /path/to/output
```

| Flag           | Default              | Description                                  |
| -------------- | --------------------- | --------------------------------------------- |
| `--input-dir`  | `./approve-list-csv`  | Directory containing raw Stellar Enforce CSVs |
| `--output-dir` | `./approve-list-done` | Directory to write cleaned CSVs into          |

If the input directory is missing or contains no CSV files, the tool logs a
message and exits cleanly instead of crashing. If an individual CSV fails to
process, it is skipped (with a logged error) and the rest of the batch
continues.

## Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the README as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
