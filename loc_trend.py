#!/usr/bin/env python3
"""Trend analysis: SLOC over versions for the requests library."""

import subprocess
from pathlib import Path

import altair as alt

from loc_counter import count_lines, find_python_files

TAGS = [
    "v2.0.0", "v2.5.0", "v2.10.0", "v2.15.0",
    "v2.20.0", "v2.25.0", "v2.28.0", "v2.31.0", "v2.33.0",
]
REPO = Path("oss/requests")


def main():
    records: list[dict[str, str | int]] = []

    for tag in TAGS:
        subprocess.run(
            ["git", "checkout", tag],
            cwd=REPO,
            capture_output=True,
        )
        py_files = find_python_files(REPO)
        total_sloc = sum(count_lines(f).sloc for f in py_files)
        total_comments = sum(count_lines(f).comments for f in py_files)
        total_blank = sum(count_lines(f).blank for f in py_files)
        print(f"{tag}: {total_sloc} SLOC, {total_comments} comments, {total_blank} blank")
        records.append({
            "version": tag,
            "SLOC": total_sloc,
            "Comments": total_comments,
            "Blank": total_blank,
        })

    # Restore main branch
    subprocess.run(["git", "checkout", "main"], cwd=REPO, capture_output=True)

    chart = (
        alt.Chart(alt.Data(values=records))
        .mark_line(point=True)
        .encode(
            x=alt.X("version:N", title="Version", sort=TAGS),
            y=alt.Y("SLOC:Q", title="Source Lines of Code"),
            tooltip=["version:N", "SLOC:Q", "Comments:Q", "Blank:Q"],
        )
        .properties(
            title="Evolution of requests project size (SLOC)",
            width=600,
            height=350,
        )
    )
    chart.save("loc_trend.png", scale_factor=2)
    print("\nSaved loc_trend.png")


if __name__ == "__main__":
    main()
