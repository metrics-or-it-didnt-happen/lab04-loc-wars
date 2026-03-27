# Lab 04 - Answers

## Task 1: cloc Analysis

### cloc results summary (Python only)

| Project  | Files | Blank | Comment | Code (SLOC) | Total |
|----------|------:|------:|--------:|------------:|------:|
| requests |    35 | 2,053 |   2,072 |       7,040 | 11,165 |
| flask    |    80 | 4,273 |   3,666 |      10,451 | 18,390 |
| httpx    |    57 | 3,377 |   2,189 |      12,187 | 17,753 |

### Q1: Which project is the "largest" (by SLOC)?

**httpx** is the largest with 12,187 SLOC, followed by flask (10,451) and requests (7,040).

This is somewhat surprising given that requests is arguably the most well-known Python HTTP library. However, httpx supports both sync and async APIs, HTTP/2, and implements more of the HTTP stack itself (rather than wrapping urllib3 like requests does), which explains the larger codebase.

### Q2: Which has the best comment-to-code ratio?

| Project  | Comment/Code ratio |
|----------|--------------------|
| requests | 29.4%              |
| flask    | 35.1%              |
| httpx    | 18.0%              |

**flask** has the best comment-to-code ratio at 35.1%. This reflects Flask's emphasis on thorough documentation and docstrings — it's a framework designed to be approachable, and the code reflects that. httpx has the lowest ratio at 18.0%.

### Q3: What percentage are blank lines?

| Project  | Blank/Total |
|----------|-------------|
| requests | 18.4%       |
| flask    | 23.2%       |
| httpx    | 19.0%       |

Blank lines range from 18-23% across all three projects, which is fairly typical for Python code. flask has slightly more, likely due to PEP 8 conventions around class/function separation in a larger file count (80 files).

### Q4: Are the results surprising?

The main surprise is the relative sizes. requests feels like a "big" library given its ubiquity, but at ~7K SLOC it's actually quite lean — most of the heavy lifting is delegated to urllib3. flask at ~10.5K SLOC is larger than expected for a "micro-framework", but much of that is in the test suite and CLI tooling. httpx being the largest makes sense once you consider it implements both sync/async clients, HTTP/2, and its own transport layer.

---

## Task 2: loc_counter vs cloc Comparison

### Results comparison (requests project, Python files only)

|          | loc_counter | cloc  | Difference |
|----------|------------:|------:|-----------:|
| Files    |          35 |    35 |          0 |
| Blank    |       2,053 | 2,053 |          0 |
| Comments |       2,788 | 2,072 |       +716 |
| Code     |       6,324 | 7,040 |       -716 |

Blank lines match exactly. The entire discrepancy (716 lines) is a shift from code → comments.

### Results comparison (flask)

|          | loc_counter | cloc   | Difference |
|----------|------------:|-------:|-----------:|
| Comments |       3,687 |  3,666 |        +21 |
| Code     |      10,430 | 10,451 |        -21 |

### Results comparison (httpx)

|          | loc_counter | cloc   | Difference |
|----------|------------:|-------:|-----------:|
| Comments |       2,161 |  2,189 |        -28 |
| Code     |      12,215 | 12,187 |        +28 |

flask and httpx have much smaller discrepancies (21 and 28 lines respectively). The requests difference is dominated by a single file.

### Why the differences?

**The main cause: closing triple-quotes on their own line after `variable = """`.**

Our parser only enters "docstring mode" when a stripped line *starts* with `"""` or `'''`. When a triple-quoted string is assigned to a variable (e.g. `content = """`), the opening line starts with `content`, so the parser doesn't detect it. However, the closing `"""` appears on its own line — and the parser misinterprets it as *opening* a new docstring. From that point, all subsequent code lines are incorrectly counted as comments until the next `"""` is encountered.

The biggest offender is `tests/test_utils.py`:
- loc_counter: 498 comments, 353 SLOC
- cloc: 54 comments, 797 SLOC
- **444 lines** misclassified due to a single `content = """..."""` pattern at line 397

This is a known limitation of line-by-line parsing without full tokenization. The Python `tokenize` module would solve this by providing proper token boundaries for strings.

**Secondary causes:**
- cloc counts shebangs (`#!/usr/bin/env python3`) as code; our parser counts them as comments (they start with `#`). This accounts for a small number of lines.
- cloc has more sophisticated heuristics for detecting triple-quoted strings mid-line (e.g. `x = """..."""`), which our simple `startswith` check misses.

### Design decisions

- **Shebangs** (`#!/usr/bin/env python3`): counted as comments (they start with `#`). cloc counts them as code. Our choice is defensible since shebangs are metadata, not executable logic.
- **Triple-quoted strings assigned to variables**: not detected as comments by our parser (the line doesn't start with `"""`). cloc treats all triple-quoted strings as comments regardless of context. This is a deliberate simplification — without full tokenization, trying to detect mid-line `"""` introduces more bugs than it solves.
- **Inline comments** (`x = 1  # comment`): counted as SLOC, matching cloc's behavior.

---

## Task 3: Trend Analysis

The chart (`loc_trend.png`) tracks SLOC across 9 versions of requests (v2.0.0 through v2.33.0).

Key observations:
- **v2.0.0 → v2.10.0**: Steady growth from ~10K to ~13K SLOC as features were added
- **v2.15.0**: Massive spike to ~25K SLOC — this version bundled vendored dependencies (urllib3, chardet, etc.) directly in the source tree
- **v2.20.0**: Sharp drop back to ~5K SLOC — vendored packages were removed, and the project restructured to use `src/` layout
- **v2.20.0 → v2.33.0**: Gradual, steady growth from ~5K to ~6.3K SLOC

This demonstrates why LOC is a tricky metric: the v2.15.0 spike doesn't represent a doubling of functionality, just a change in how dependencies were distributed. Context matters.
