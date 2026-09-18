import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import process_directory  # noqa: E402


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))


def test_empty_input_dir_processes_nothing(tmp_path):
    input_dir = tmp_path / "approve-list-csv"
    output_dir = tmp_path / "approve-list-done"
    input_dir.mkdir()

    processed = process_directory(input_dir, output_dir)

    assert processed == 0


def test_missing_input_dir_does_not_crash(tmp_path):
    input_dir = tmp_path / "does-not-exist"
    output_dir = tmp_path / "approve-list-done"

    processed = process_directory(input_dir, output_dir)

    assert processed == 0
    assert not output_dir.exists()


def test_duplicate_paths_are_deduped(tmp_path):
    input_dir = tmp_path / "approve-list-csv"
    output_dir = tmp_path / "approve-list-done"
    input_dir.mkdir()

    csv_content = (
        "C:\\Program Files\\App\\app.exe\n"
        "C:\\Program Files\\App\\other.exe\n"
        "C:\\Windows\\System32\\cmd.exe\n"
    )
    (input_dir / "scan.csv").write_text(csv_content, encoding="utf-8")

    processed = process_directory(input_dir, output_dir)

    assert processed == 1
    out_file = output_dir / "done-scan.csv"
    assert out_file.exists()

    rows = read_csv(out_file)
    assert rows[0] == ["Full File Path"]
    data_rows = [row[0] for row in rows[1:]]
    assert data_rows == [
        "C:\\Program Files\\App",
        "C:\\Windows\\System32",
    ]


def test_malformed_row_is_skipped_not_fatal(tmp_path):
    input_dir = tmp_path / "approve-list-csv"
    output_dir = tmp_path / "approve-list-done"
    input_dir.mkdir()

    csv_content = (
        "C:\\Program Files\\App\\app.exe\n"
        "\n"
        "C:\\Windows\\System32\\cmd.exe\n"
    )
    (input_dir / "scan.csv").write_text(csv_content, encoding="utf-8")

    processed = process_directory(input_dir, output_dir)

    assert processed == 1
    out_file = output_dir / "done-scan.csv"
    rows = read_csv(out_file)
    data_rows = [row[0] for row in rows[1:]]
    assert data_rows == [
        "C:\\Program Files\\App",
        "C:\\Windows\\System32",
    ]


def test_row_without_directory_is_skipped_not_blank(tmp_path):
    input_dir = tmp_path / "approve-list-csv"
    output_dir = tmp_path / "approve-list-done"
    input_dir.mkdir()

    csv_content = (
        "C:\\Program Files\\App\\app.exe\n"
        "  \n"
        "bare-filename.exe\n"
        "C:\\Windows\\System32\\cmd.exe\n"
    )
    (input_dir / "scan.csv").write_text(csv_content, encoding="utf-8")

    processed = process_directory(input_dir, output_dir)

    assert processed == 1
    out_file = output_dir / "done-scan.csv"
    rows = read_csv(out_file)
    data_rows = [row[0] for row in rows[1:]]
    assert data_rows == [
        "C:\\Program Files\\App",
        "C:\\Windows\\System32",
    ]
    assert "" not in data_rows


def test_one_bad_file_does_not_stop_batch(tmp_path):
    input_dir = tmp_path / "approve-list-csv"
    output_dir = tmp_path / "approve-list-done"
    input_dir.mkdir()

    (input_dir / "good.csv").write_text(
        "C:\\Apps\\Good\\app.exe\n", encoding="utf-8"
    )
    # A file that will cause an exception path exercise: unreadable is hard to
    # simulate portably, so use a directory with a .csv suffix instead, which
    # will raise when opened as a file.
    bad_dir = input_dir / "bad.csv"
    bad_dir.mkdir()

    processed = process_directory(input_dir, output_dir)

    assert processed == 1
    assert (output_dir / "done-good.csv").exists()
    assert not (output_dir / "done-bad.csv").exists()
