#!/usr/bin/env python3
"""LOC Counter - counting lines of code for Python files."""

import sys
import subprocess
import re
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRS = {".venv", "venv", "__pycache__", ".git", "node_modules", ".tox", ".eggs"}


@dataclass
class FileStats:
    path: str
    loc: int = 0
    sloc: int = 0
    comments: int = 0
    blank: int = 0


def count_lines(filepath: Path) -> FileStats:
    """Count LOC, SLOC, comments, and blank lines in a Python file."""
    stats = FileStats(path=str(filepath))

    in_docstring = False
    docstring_delim = None  # ''' or """

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            stats.loc += 1
            stripped = line.strip()

            if not stripped:
                stats.blank += 1
                continue

            if in_docstring:
                stats.comments += 1
                if docstring_delim in stripped:
                    if stripped.count(docstring_delim) % 2 != 0:
                        in_docstring = False
                        docstring_delim = None
                continue

            if stripped.startswith(('"""', "'''")):
                stats.comments += 1

                if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                    continue

                in_docstring = True
                docstring_delim = stripped[:3]
                continue

            if stripped.startswith("#"):
                stats.comments += 1
                continue

            if "#" in stripped:
                code_part = stripped.split("#", 1)[0].strip()
                if code_part:
                    stats.sloc += 1
                else:
                    stats.comments += 1
                continue

            stats.sloc += 1

    return stats


def find_python_files(directory: Path) -> list[Path]:
    result = []
    for path in sorted(directory.rglob("*.py")):
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            continue
        result.append(path)
    return result


def print_report(files_stats: list[FileStats]) -> None:
    print(f"{'Plik':<60} {'LOC':>6} {'SLOC':>6} {'Comm':>6} {'Blank':>6}")
    print("-" * 86)

    for fs in files_stats:
        short_path = fs.path if len(fs.path) < 58 else "..." + fs.path[-55:]
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

    if total_sloc > 0:
        print(f"Komentarze/kod: {total_comments / total_sloc:.1%}")
    if total_loc > 0:
        print(f"Puste/całość:   {total_blank / total_loc:.1%}")


def run_cloc(directory: Path) -> dict:
    try:
        result = subprocess.run(
            ["cloc", str(directory), "--include-lang=Python"],
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("\n[!] cloc nie znaleziony w PATH")
        return {}

    output = result.stdout

    match = re.search(r"Python\s+\d+\s+(\d+)\s+(\d+)\s+(\d+)", output)
    if not match:
        print("\n[!] Nie udało się sparsować wyniku cloc")
        return {}

    blank, comments, code = map(int, match.groups())

    return {
        "blank": blank,
        "comments": comments,
        "code": code
    }


def compare_with_cloc(our_stats: list[FileStats], directory: Path) -> None:
    cloc_stats = run_cloc(directory)
    if not cloc_stats:
        return

    our_blank = sum(f.blank for f in our_stats)
    our_comments = sum(f.comments for f in our_stats)
    our_code = sum(f.sloc for f in our_stats)

    print("\n=== PORÓWNANIE Z CLOC ===")
    print(f"{'':<12}{'Twoje':>10}{'cloc':>10}{'Różnica':>12}")

    def diff(a, b):
        if b == 0:
            return "—"
        return f"{(a - b) / b:+.1%}"

    print(f"{'SLOC':<12}{our_code:>10}{cloc_stats['code']:>10}{diff(our_code, cloc_stats['code']):>12}")
    print(f"{'Comments':<12}{our_comments:>10}{cloc_stats['comments']:>10}{diff(our_comments, cloc_stats['comments']):>12}")
    print(f"{'Blank':<12}{our_blank:>10}{cloc_stats['blank']:>10}{diff(our_blank, cloc_stats['blank']):>12}")


def main():
    if len(sys.argv) < 2:
        print("Użycie: python loc_counter.py <katalog>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Nie znaleziono katalogu: {directory}")
        sys.exit(1)

    py_files = find_python_files(directory)

    stats = [count_lines(f) for f in py_files]
    stats = [s for s in stats if s.loc > 0]

    print(f"Znaleziono {len(stats)} plików .py\n")

    print_report(stats)

    compare_with_cloc(stats, directory)


if __name__ == "__main__":
    main()