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
    loc: int = 0       # All lines
    sloc: int = 0      # Code (non-blank, non-comment)
    comments: int = 0  # Comments (# and docstrings)
    blank: int = 0     # Blank lines
    # Invariant: loc == sloc + comments + blank


def count_lines(filepath: Path) -> FileStats:
    """Count LOC, SLOC, comments, and blank lines in a Python file.

    Handles:
    - Single-line comments (lines starting with #, after stripping whitespace)
    - Multi-line docstrings/strings (triple quotes: ''' or \""")
    - Blank lines
    - Inline comments (x = 1  # comment) -> counted as SLOC

    Design decisions:
    - Shebangs (#!/usr/bin/env python3) are counted as comments (they start with #)
    - Triple-quoted strings that start at the beginning of a (stripped) line are
      treated as docstrings/comments, matching cloc behaviour for most cases
    - Triple-quoted strings assigned to variables (e.g. x = \"""...\""") are NOT
      detected as comments because the stripped line doesn't start with triple quotes.
      This is a known limitation of line-by-line parsing without full tokenization.
    """
    stats = FileStats(path=str(filepath))

    try:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return stats

    in_docstring = False
    docstring_quote = None

    for line in lines:
        stats.loc += 1
        stripped = line.strip()

        if not stripped:
            stats.blank += 1
            continue

        # Inside a multi-line docstring
        if in_docstring and docstring_quote is not None:
            stats.comments += 1
            if docstring_quote in stripped:
                # Check that the closing quotes aren't the opening ones again
                # (i.e. the line actually closes the docstring)
                after_close = stripped.split(docstring_quote, 1)[1]
                # If there's no second occurrence, docstring ends here
                if docstring_quote not in after_close:
                    in_docstring = False
                    docstring_quote = None
            continue

        # Check for triple-quoted string opening at start of line
        if stripped.startswith('"""') or stripped.startswith("'''"):
            quote = stripped[:3]
            stats.comments += 1
            # Check if it closes on the same line (after the opening quotes)
            rest = stripped[3:]
            if quote in rest:
                # Single-line docstring like """hello"""
                pass
            else:
                # Multi-line docstring begins
                in_docstring = True
                docstring_quote = quote
            continue

        # Single-line comment
        if stripped.startswith("#"):
            stats.comments += 1
            continue

        # Everything else is source code (including lines with inline comments)
        stats.sloc += 1

    return stats


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all .py files, skipping excluded directories."""
    result: list[Path] = []
    for path in sorted(directory.rglob("*.py")):
        if any(excluded in path.parts for excluded in EXCLUDED_DIRS):
            continue
        result.append(path)
    return result


def print_report(files_stats: list[FileStats]) -> None:
    """Print formatted report."""
    print(f"{'File':<60} {'LOC':>6} {'SLOC':>6} {'Comm':>6} {'Blank':>6}")
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
    print(f"{'TOTAL':<60} {total_loc:>6} {total_sloc:>6} "
          f"{total_comments:>6} {total_blank:>6}")
    print(f"\nFiles: {len(files_stats)}")
    if total_loc > 0:
        print(f"Comments/code: {total_comments/total_sloc:.1%}" if total_sloc else "")
        print(f"Blank/total:   {total_blank/total_loc:.1%}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python loc_counter.py <directory>")
        sys.exit(1)

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Directory not found: {directory}")
        sys.exit(1)

    py_files = find_python_files(directory)
    print(f"Found {len(py_files)} .py files\n")

    stats = [count_lines(f) for f in py_files]
    stats = [s for s in stats if s.loc > 0]

    print_report(stats)


if __name__ == "__main__":
    main()
