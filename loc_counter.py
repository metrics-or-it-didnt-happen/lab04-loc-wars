#!/usr/bin/env python3
"""LOC Counter - counting lines of code for Python files."""

import sys
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRS = {".venv", "venv", "__pycache__", ".git", "node_modules", ".tox", ".eggs"}


@dataclass
class FileStats:
    """Line count statistics for a single file."""
    path: str
    loc: int = 0       # Wszystkie linie
    sloc: int = 0      # Kod (niepuste, niekomentarzowe)
    comments: int = 0  # Komentarze (# oraz docstringi)
    blank: int = 0     # Puste linie
    # Invariant: loc == sloc + comments + blank
    


def count_lines(filepath: Path) -> FileStats:
    """Count LOC, SLOC, comments, and blank lines in a Python file.

    Handles:
    - Single-line comments (lines starting with #, after stripping whitespace)
    - Multi-line docstrings/strings (triple quotes: ''' lub \""")
    - Blank lines
    - Inline comments (x = 1  # comment) -> liczone jako SLOC

    Uwaga: triple-quoted strings przypisane do zmiennych (np. x = \"""...\""")
    to technicznie kod, nie komentarze. Ale cloc traktuje je jako komentarze.
    Wy zdecydujcie jak chcecie je liczyć — i uzasadnijcie w answers.md.
    """
    stats = FileStats(path=str(filepath))
    isInsideDoc = 0

    
    in_docstring = False
    docstring_delim = None  # """ or '''

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            stats.loc += 1
            stripped = line.strip()

            # 1. Blank line
            if not stripped:
                stats.blank += 1
                continue

            # 2. Inside docstring
            if in_docstring:
                stats.comments += 1
                if docstring_delim in stripped:
                    in_docstring = False
                    docstring_delim = None
                continue

            # 3. Start of docstring
            if stripped.startswith('"""') or stripped.startswith("'''"):
                delim = '"""' if stripped.startswith('"""') else "'''"

                # Check if it's a one-liner docstring
                if stripped.count(delim) >= 2:
                    stats.comments += 1
                else:
                    in_docstring = True
                    docstring_delim = delim
                    stats.comments += 1
                continue

            # 4. Single-line comment
            if stripped.startswith("#"):
                stats.comments += 1
                continue

            # 5. Everything else = SLOC
            stats.sloc += 1

    # TODO: Twój kod tutaj
    # Wskazówki:
    # 1. Otwórz plik z encoding="utf-8" i errors="replace" (niektóre pliki
    #    mogą mieć dziwne kodowanie i bez tego dostaniesz UnicodeDecodeError)
    # 2. Czytaj plik linia po linii, śledź stan: czy jesteś wewnątrz
    #    docstringa (triple quotes)
    # 3. Dla każdej linii (po .strip()):
    #    - Pusta -> blank
    #    - Wewnątrz docstringa -> comments (sprawdź czy docstring się zamyka)
    #    - Zaczyna się od """ lub ''' -> comments (sprawdź czy jednoliniowy)
    #    - Zaczyna się od # -> comments
    #    - Wszystko inne -> sloc
    # 4. Docstringi: ''' lub """ otwierają i zamykają
    #    Uwaga: mogą być jednoliniowe! np. """This is a docstring."""
    #    Sprawdź czy po usunięciu otwierającego """ reszta zawiera zamykający.
    # 5. Pułapka: x = """ NIE zaczyna się od """ (po strip to "x = ...").
    #    Zamykający """ takiego stringa będzie osobną linią zaczynającą się
    #    od """ - twój parser może go pomylić z otwarciem nowego docstringa.
    #    To jest znane ograniczenie prostego parsera linia-po-linii.
    #    Opisz to w answers.md.

    return stats


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all .py files, skipping excluded directories."""
    result = []
    for path in sorted(directory.rglob("*.py")):
        # Pomiń pliki w wykluczonych katalogach
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