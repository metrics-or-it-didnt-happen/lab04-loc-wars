import sys
from dataclasses import dataclass, field
from pathlib import Path
from pathspec import PathSpec


@dataclass
class FileStats:
    """Line count statistics for a single file."""
    path: str
    loc: int = 0
    sloc: int = 0
    comments: int = 0
    blank: int = 0


def is_blank(line: str) -> bool:
    """Check if a line is blank (only whitespace)."""
    return not line.strip()


def is_comment(line: str) -> bool:
    """Check if a line is a comment (starts with # after stripping, shebangs included)."""
    return line.strip().startswith("#")


def is_code_with_comment(line: str) -> bool:
    """Check if a line contains code followed by an inline comment."""
    stripped = line.strip()
    return "#" in stripped and not stripped.startswith("#") and not is_blank(line)


def is_single_line_docstring(line: str) -> bool:
    """Check if a line is a single-line docstring (triple quotes on the same line)."""
    stripped = line.strip()
    return (
            (stripped.startswith('"""') and stripped.endswith('"""') and len(stripped) > 6)
            or
            (stripped.startswith("'''") and stripped.endswith("'''") and len(stripped) > 6)
    )


def is_docstring_start(line: str) -> bool:
    """Check if a line starts a multi-line docstring (triple quotes)."""
    stripped = line.strip()
    return (
            (stripped.startswith('"""') and not stripped.endswith('"""'))
            or
            (stripped.startswith("'''") and not stripped.endswith("'''"))
            or stripped == '"""'
            or stripped == "'''"
    )


def is_docstring_end(line: str) -> bool:
    """Check if a line ends a multi-line docstring (triple quotes)."""
    stripped = line.strip()
    return (
            (stripped.endswith('"""') and not stripped.startswith('"""'))
            or
            (stripped.endswith("'''") and not stripped.startswith("'''"))
            or stripped == '"""'
            or stripped == "'''"
    )


def count_lines(filepath: Path) -> FileStats:
    """Count LOC, SLOC, comments, and blank lines in a Python file.

    Handles:
    - Single-line comments (lines starting with #)
    - Multi-line strings used as docstrings (triple quotes)
    - Blank lines
    - Inline comments (line has code AND comment)

    """
    stats = FileStats(path=str(filepath))

    # TODO: Twój kod tutaj
    # Wskazówki:
    # - Czytaj plik linia po linii
    # - Śledź czy jesteś wewnątrz docstringa (triple quotes)
    # - Linia może być: pusta, komentarz, kod, lub kod+komentarz
    # - Docstringi: ''' lub """ otwierają i zamykają
    #   Uwaga: mogą być jednoliniowe! np. """This is a docstring."""
    in_docstring = False

    with open(filepath, "r", encoding="utf-8") as infile:
        for line in infile:
            stats.loc += 1

            if in_docstring:
                stats.comments += 1
                if is_docstring_end(line):
                    in_docstring = False
                continue

            if is_blank(line):
                stats.blank += 1
            elif is_code_with_comment(line):
                stats.sloc += 1
                stats.comments += 1
            elif is_comment(line):
                stats.comments += 1
            elif is_single_line_docstring(line):
                stats.comments += 1
            elif is_docstring_start(line):
                stats.comments += 1
                in_docstring = True
            else:
                stats.sloc += 1

    return stats


def load_gitignore(directory: Path) -> PathSpec:
    gitignore = directory / ".gitignore"
    if not gitignore.exists():
        return PathSpec.from_lines("gitwildmatch", [])
    return PathSpec.from_lines("gitwildmatch", gitignore.read_text().splitlines())


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all .py files in a directory. Ignore .gitignore patterns."""
    spec = load_gitignore(directory)

    files = []
    for path in directory.rglob("*.py"):
        rel_path = path.relative_to(directory).as_posix()
        if not spec.match_file(rel_path):
            files.append(path)

    return sorted(files)


def compare_with_cloc(cloc_report_path: Path, files_stats: list[FileStats]) -> None:
    """Compare results with cloc report."""
    import csv
    cloc_results = {
        "blank": 0,
        "comment": 0,
        "code": 0,
    }
    with open(cloc_report_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == "SUM:":
                break
            cloc_results["blank"] = int(row[2])
            cloc_results["comment"] = int(row[3])
            cloc_results["code"] = int(row[4])

    total_loc = sum([v for k, v in cloc_results.items()])
    total_sloc = cloc_results["code"]
    total_comments = cloc_results["comment"]
    total_blank = cloc_results["blank"]
    print("-" * 86)
    print(f"{' ':<60} {'LOC':>6} {'SLOC':>6} {'Comm':>6} {'Blank':>6}")
    print(f"{'RAZEM':<60} {total_loc:>6} {total_sloc:>6} "
          f"{total_comments:>6} {total_blank:>6}")
    print(f"\nPlików: {len(files_stats)}")
    if total_loc > 0:
        print(f"Komentarze/kod: {total_comments / total_sloc:.1%}" if total_sloc else "")
        print(f"Puste/całość:   {total_blank / total_loc:.1%}")


def print_report(files_stats: list[FileStats]) -> None:
    """Print formatted report."""
    print(f"{'Plik':<60} {'LOC':>6} {'SLOC':>6} {'Comm':>6} {'Blank':>6}")
    print("-" * 86)

    for fs in files_stats:
        short_path = fs.path if len(fs.path) < 58 else "..." + fs.path[-55:]
        print(f"{short_path:<60} {fs.loc:>6} {fs.sloc:>6} "
              f"{fs.comments:>6} {fs.blank:>6}")

    # Podsumowanie
    total_loc = sum(f.loc for f in files_stats)
    total_sloc = sum(f.sloc for f in files_stats)
    total_comments = sum(f.comments for f in files_stats)
    total_blank = sum(f.blank for f in files_stats)

    print("-" * 86)
    print(f"{'RAZEM':<60} {total_loc:>6} {total_sloc:>6} "
          f"{total_comments:>6} {total_blank:>6}")
    print(f"\nPlików: {len(files_stats)}")
    if total_loc > 0:
        print(f"Komentarze/kod: {total_comments / total_sloc:.1%}" if total_sloc else "")
        print(f"Puste/całość:   {total_blank / total_loc:.1%}")

    print("\nPorównanie z cloc (jeśli dostępny):")
    cloc_report = Path("cloc_report.csv")
    if cloc_report.exists():
        compare_with_cloc(cloc_report, files_stats)
    else:
        print("Brak raportu cloc_report.csv do porównania.")


def main():
    if len(sys.argv) < 2:
        print("Użycie: python loc_counter.py <katalog>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Nie znaleziono katalogu: {directory}")
        sys.exit(1)

    py_files = find_python_files(directory)
    print(f"Znaleziono {len(py_files)} plików .py\n")

    stats = [count_lines(f) for f in py_files]
    stats = [s for s in stats if s.loc > 0]  # Pomiń puste pliki

    print_report(stats)


if __name__ == "__main__":
    main()
