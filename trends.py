import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt

# Zaimportuj swój loc_counter jako moduł
# (loc_counter.py musi być w tym samym katalogu lub w PYTHONPATH)
from loc_counter import find_python_files, count_lines

tags = ["3.1.0", "3.1.1", "3.1.2","3.1.3"]
repo_path = Path("/tmp/flask")
sloc_per_tag = []

for tag in tags:
    subprocess.run(["git", "checkout", tag], cwd=repo_path,
                   capture_output=True)
    py_files = find_python_files(repo_path)
    total_sloc = sum(count_lines(f).sloc for f in py_files)
    sloc_per_tag.append(total_sloc)
    print(f"{tag}: {total_sloc} SLOC")

# Przywróć główną gałąź
subprocess.run(["git", "checkout", "main"], cwd=repo_path,
               capture_output=True)

plt.figure(figsize=(10, 5))
plt.plot(tags, sloc_per_tag, marker="o", linewidth=2)
plt.xlabel("Wersja")
plt.ylabel("SLOC")
plt.title("Ewolucja rozmiaru projektu flask")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("loc_trend.png", dpi=150)
plt.show()