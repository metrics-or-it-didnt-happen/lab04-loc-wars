"""LOC Counter - counting lines of code for Python files."""

import sys
from dataclasses import dataclass, field
from pathlib import Path

EXCLUDED_DIRS = {".venv", "venv", "__pycache__", ".git", "node_modules", ".tox", ".eggs"}

@dataclass
class FileStats:
    """Line count statistics for a single file."""
    path: str
    loc: int = 0
    sloc: int = 0
    comments: int = 0
    blank: int = 0


def count_lines(filepath: Path) -> FileStats:
    """Count LOC, SLOC, comments, and blank lines in a Python file.

    Handles:
    - Single-line comments (lines starting with #)
    - Multi-line strings used as docstrings (triple quotes)
    - Blank lines
    - Inline comments (line has code AND comment)
    """
    stats = FileStats(path=str(filepath))

    # Wskazówki:
    # - Czytaj plik linia po linii
    # - Śledź czy jesteś wewnątrz docstringa (triple quotes)
    # - Linia może być: pusta, komentarz, kod, lub kod+komentarz
    # - Docstringi: ''' lub """ otwierają i zamykają
    #   Uwaga: mogą być jednoliniowe! np. """This is a docstring."""
    in_multiline = False
    multiline_quote = ""

    try:
        with open(filepath, 'r') as f:
            for line in f:
                stats.loc += 1
                stripped = line.strip()

                # Puste linie
                if not stripped:
                    stats.blank += 1
                    continue

                # wewnątrz wielolinijkowego docstringu
                if in_multiline:
                    stats.comments += 1
                    # sprawdzenie czy tu docstring sie juz konczy
                    if multiline_quote in stripped:
                        in_multiline = False
                    continue

                # shebangs (#!/usr/bin/env python3), cloc traktuje jako kod, wiec my tez :)
                if stats.loc == 1 and stripped.startswith('#!'):
                    stats.sloc += 1
                    continue

                # zwykły komentarz
                if stripped.startswith("#"):
                    stats.comments += 1
                    continue

                # rozpoczecie docstringa, tutaj obejscie jakby byl f-string, albo raw-string albo jakis inny prefiks
                start = stripped.lower().lstrip('rubf')
                if start.startswith("'''") or start.startswith('"""'):
                    stats.comments += 1
                    quote = start[:3]
                    # test, czy to docstring jednolinijkowy
                    if start[3:].find(quote) != -1:
                        pass # tak, wzial i sie zamknal w tej samej linijce
                    else:
                        # multilinijkowy komentarz
                        in_multiline = True
                        multiline_quote = quote
                    continue

                # kod zwykly
                stats.sloc += 1

    except Exception as e:
        print("wybuch")

    return stats


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all .py files in a directory."""
    result = []
    for path in sorted(directory.rglob("*.py")):
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            continue
        result.append(path)
    return result


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
        print(f"Komentarze/kod: {total_comments/total_sloc:.1%}" if total_sloc else "")
        print(f"Puste/całość:   {total_blank/total_loc:.1%}")


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