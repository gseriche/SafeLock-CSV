"""SafeLock-CSV

Reads CSV files exported from Stellar Enforce (an application allow-listing
product) out of an input folder, strips the filename from each row's full
path (keeping only the directory), dedupes the paths while preserving order,
and writes a cleaned CSV per input file into an output folder.
"""

import argparse
import csv
import logging
from pathlib import Path
from typing import List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

HEADER = ["Full File Path"]


def extract_directories(csv_file: Path) -> List[str]:
    """Read a Stellar Enforce CSV and return deduped directory paths.

    Each row's first column is a Windows-style full file path
    (backslash-separated). The filename (last segment) is dropped, keeping
    only the directory path. Order is preserved and duplicates removed.
    Malformed rows (empty or missing the first column) are skipped with a
    warning instead of raising.
    """
    directories: List[str] = []
    with csv_file.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh, delimiter=",")
        for line_number, row in enumerate(reader, start=1):
            if not row or not row[0].strip():
                logger.warning(
                    "Skipping malformed row %d in %s: %r",
                    line_number,
                    csv_file.name,
                    row,
                )
                continue
            path = row[0].strip()
            if "\\" not in path:
                logger.warning(
                    "Skipping row %d in %s: no directory component in %r",
                    line_number,
                    csv_file.name,
                    row,
                )
                continue
            parts = path.split("\\")
            parts.pop()
            directory = "\\".join(parts)
            directories.append(directory)

    # Dedupe while preserving order.
    return list(dict.fromkeys(directories))


def process_directory(input_dir: Path, output_dir: Path) -> int:
    """Process every CSV in input_dir, writing cleaned CSVs to output_dir.

    Returns the number of files successfully processed. Missing/empty input
    directories and per-file errors are logged and do not raise.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.is_dir():
        logger.error("Input directory does not exist: %s", input_dir)
        return 0

    csv_files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() == ".csv")
    if not csv_files:
        logger.warning("No CSV files found in input directory: %s", input_dir)
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)

    processed = 0
    for csv_file in csv_files:
        try:
            directories = extract_directories(csv_file)
            out_path = output_dir / f"done-{csv_file.name}"
            with out_path.open("w", newline="", encoding="utf-8") as out_fh:
                writer = csv.writer(out_fh)
                writer.writerow(HEADER)
                writer.writerows([d] for d in directories)
            logger.info(
                "Processed %s -> %s (%d unique paths)",
                csv_file.name,
                out_path.name,
                len(directories),
            )
            processed += 1
        except Exception as exc:  # noqa: BLE001 - keep batch running on any per-file failure
            logger.error("Failed to process %s: %s", csv_file.name, exc)
            continue

    return processed


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Clean Stellar Enforce approve-list CSV exports by deduping "
            "directory paths (dropping the filename from each row)."
        )
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("./approve-list-csv"),
        help="Directory containing raw Stellar Enforce CSV exports (default: ./approve-list-csv)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./approve-list-done"),
        help="Directory to write cleaned CSV files to (default: ./approve-list-done)",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    processed = process_directory(args.input_dir, args.output_dir)
    logger.info("Done. %d file(s) processed.", processed)


if __name__ == "__main__":
    main()
