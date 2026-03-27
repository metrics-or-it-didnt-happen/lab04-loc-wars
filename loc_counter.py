#!/usr/bin/env python3
"""LOC Counter - counting lines of code for Python files."""

import sys
from dataclasses import dataclass
from pathlib import Path
import tokenize
import subprocess
import csv
import tempfile

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

def mark_lines(filepath: Path) -> dict:
    ignored_types = [
        tokenize.ENCODING, # pierwsza linia (utf-8)
        tokenize.NL,       # nowa linia w środku konstrukcji (np. w nawiasach)
        tokenize.NEWLINE,  # koniec logicznej linii
        tokenize.ENDMARKER # koniec pliku
        ]
    
    line_info = {}
    with open(filepath, 'rb') as file:
        try:
            tokens = tokenize.tokenize(file.readline)

            for token in tokens:
                ttype = token.type
                if ttype in ignored_types:
                    continue

                token_str = token.string
                start_line = token.start[0]
                end_line = token.end[0]

                for line_no in range(start_line, end_line+1):
                    line_info.setdefault(line_no, {"code": False, "comment": False})

                    if ttype==tokenize.COMMENT:
                        line_info[line_no]["comment"] = True
                    elif ttype==tokenize.STRING:
                        if token_str.startswith("'''") or token_str.startswith('"""'):
                            line_info[line_no]["comment"] = True
                        else:
                            line_info[line_no]["code"] = True
                    else:
                        line_info[line_no]["code"] = True
        except tokenize.TokenError:
            pass

        return line_info

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

    sloc = 0
    comments = 0
    blank = 0

    line_info = mark_lines(filepath)

    with open(filepath, encoding="utf-8", errors="replace") as file:
        lines = file.readlines()

    loc = len(lines)
    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped=="":
            blank+=1
            continue

        info = line_info.get(line_no, {"code": False, "comment": False})
        if info["code"]: sloc+=1
        elif info["comment"]: comments+=1

    stats = FileStats(path=str(filepath))
    stats.loc      = loc
    stats.sloc     = sloc
    stats.comments = comments
    stats.blank    = blank

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

def run_cloc(directory: Path) -> dict:
    """Run cloc and return summary stats (LOC, SLOC, comments, blank)."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    cmd = [
        "cloc",
        str(directory),
        "--include-lang=Python",
        "--csv",
        f"--out={tmp_path}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = {}
    with open(tmp_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["language"] == "SUM":
                result = {
                    "files": int(row["files"]),
                    "blank": int(row["blank"]),
                    "comment": int(row["comment"]),
                    "code": int(row["code"]),
                    "loc": int(row["blank"]) + int(row["comment"]) + int(row["code"])
                }
    return result

def print_report(files_stats: list[FileStats], cloc_results: dict) -> None:
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
    
    print(f"{'CLOC':<60} {cloc_results["loc"]:>6} {cloc_results["code"]:>6} "
          f"{cloc_results["comment"]:>6} {cloc_results["blank"]:>6}")
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

    cloc_results = run_cloc(directory)
    print_report(stats, cloc_results)

if __name__ == "__main__":
    main()