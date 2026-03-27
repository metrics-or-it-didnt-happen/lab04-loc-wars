import subprocess
from pathlib import Path
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"

from loc_counter import count_lines, find_python_files

tags = ["v2.20.0", "v2.25.0", "v2.28.0", "v2.31.0"]
repo_path = Path("requests")
sloc_per_tag = []

for tag in tags:
    print(f"Processing ({tag}/{len(tags)}).")
    subprocess.run(["git", "checkout", tag], 
                   cwd=repo_path,
                   capture_output=True)

    py_files = find_python_files(repo_path)

    total_sloc = 0
    for file in py_files:
        stats = count_lines(file)
        total_sloc += stats.sloc
    sloc_per_tag.append(total_sloc)

# Przywróć główną gałąź
subprocess.run(["git", "checkout", "main"],
               cwd=repo_path,
               capture_output=True)

plt.figure(figsize=(10, 5))
plt.plot(tags, sloc_per_tag, marker="o", linewidth=2)
plt.xlabel("Wersja")
plt.ylabel("SLOC")
plt.title("Ewolucja rozmiaru projektu requests")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("loc_trend.png", dpi=150)
plt.show()