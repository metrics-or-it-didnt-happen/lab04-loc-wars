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
    loc: int = 0
    sloc: int = 0
    comments: int = 0
    blank: int = 0


def count_lines(filepath: Path) -> FileStats:
    """Count LOC, SLOC, comments, and blank lines in a Python file.

    Handles single-line comments (#), multi-line docstrings (triple quotes),
    blank lines. Inline comments (x = 1  # comment) are counted as SLOC.
    """
    stats = FileStats(path=str(filepath))
    in_docstring = False
    quote_char = None

    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except (OSError, PermissionError):
        return stats

    for line in lines:
        stats.loc += 1
        stripped = line.strip()

        if not stripped:
            stats.blank += 1
            continue

        if in_docstring:
            stats.comments += 1
            if quote_char in stripped:
                idx = stripped.find(quote_char)
                after = stripped[idx + 3:]
                if not after or not after.strip().replace(quote_char, ""):
                    in_docstring = False
                    quote_char = None
            continue

        # sprawdzamy czy linia otwiera docstring/triple-quoted string
        if stripped.startswith('"""') or stripped.startswith("'''"):
            qc = stripped[:3]
            stats.comments += 1
            rest = stripped[3:]
            # jednoliniowy docstring, np. """tekst"""
            if qc in rest:
                pass  # zamyka się w tej samej linii
            else:
                in_docstring = True
                quote_char = qc
            continue

        if stripped.startswith("#"):
            stats.comments += 1
            continue

        stats.sloc += 1

    return stats


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all .py files, skipping excluded directories."""
    result = []
    for path in sorted(directory.rglob("*.py")):
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            continue
        result.append(path)
    return result


def print_report(files_stats: list[FileStats], base_dir: Path) -> None:
    """Print formatted report."""
    print(f"{'Plik':<60} {'LOC':>6} {'SLOC':>6} {'Comm':>6} {'Blank':>6}")
    print("-" * 86)

    for fs in files_stats:
        try:
            rel = str(Path(fs.path).relative_to(base_dir))
        except ValueError:
            rel = fs.path
        short_path = rel if len(rel) < 58 else "..." + rel[-55:]
        print(f"{short_path:<60} {fs.loc:>6} {fs.sloc:>6} "
              f"{fs.comments:>6} {fs.blank:>6}")

    total_loc = sum(f.loc for f in files_stats)
    total_sloc = sum(f.sloc for f in files_stats)
    total_comments = sum(f.comments for f in files_stats)
    total_blank = sum(f.blank for f in files_stats)

    print("-" * 86)
    print(f"{'RAZEM':<60} {total_loc:>6} {total_sloc:>6} "
          f"{total_comments:>6} {total_blank:>6}")
    print(f"\nPlików: {len(files_stats)}")
    if total_loc > 0:
        if total_sloc:
            print(f"Komentarze/kod: {total_comments/total_sloc:.1%}")
        print(f"Puste/LOC:      {total_blank/total_loc:.1%}")


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
    stats = [s for s in stats if s.loc > 0]

    print_report(stats, directory)


if __name__ == "__main__":
    main()
