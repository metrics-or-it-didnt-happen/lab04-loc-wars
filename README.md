# Lab 04: LOC Wars — ile linii to za dużo?

## Czy wiesz, że...

Według badań (które właśnie wymyśliłem), Windows XP miał 45 milionów linii kodu. Nikt do dziś nie wie, ile z nich to komentarze w stylu `// TODO: fix this later`. Podejrzewam, że sporo.

## Kontekst

Metryki rozmiaru kodu to najstarsza i najprostsza forma pomiaru oprogramowania. LOC (Lines of Code) brzmi banalnie — "policz linie, gotowe" — ale diabeł tkwi w szczegółach. Czy pusta linia się liczy? A komentarz? A docstring? A import? Okazuje się, że "ile linii ma ten projekt" nie ma jednej poprawnej odpowiedzi.

W praktyce metryki rozmiaru służą do: szacowania złożoności projektu, porównywania projektów, śledzenia wzrostu kodu w czasie, normalizacji innych metryk (np. "bugi na 1000 LOC"), i jako input do modeli predykcji. Dlatego ważne jest, żeby rozumieć co dokładnie mierzymy.

## Cel laboratorium

Po tym laboratorium będziesz potrafić:
- używać narzędzia `cloc` do analizy rozmiaru projektów,
- napisać własny licznik LOC w Pythonie (parsujący komentarze i docstringi),
- porównywać projekty pod kątem rozmiaru i struktury kodu,
- krytycznie ocenić LOC jako metrykę.

## Wymagania wstępne

- Python 3.9+
- `cloc` zainstalowany (`sudo apt install cloc` lub `brew install cloc`)
- matplotlib (do opcjonalnej wizualizacji)
- Sklonowane 3 projekty open-source (najlepiej w Pythonie)

## Zadania

### Zadanie 1: cloc w akcji (30 min)

`cloc` (Count Lines of Code) to sprawdzone narzędzie do liczenia linii kodu. Obsługuje dziesiątki języków i odróżnia kod, komentarze i puste linie.

**Krok 1:** Zainstaluj cloc (jeśli jeszcze nie masz):

```bash
# Linux
sudo apt install cloc

# Mac
brew install cloc

# Albo z Dockera (lab03):
docker run -it --rm code-analyzer
```

**Krok 2:** Sklonuj 3 projekty open-source (Pythonowe, dla porównania):

```bash
git clone https://github.com/psf/requests.git
git clone https://github.com/pallets/flask.git
git clone https://github.com/encode/httpx.git
```

Możesz wybrać inne — ważne żeby były w Pythonie i miały co najmniej kilka tysięcy linii.

**Krok 3:** Przeanalizuj każdy projekt:

```bash
cloc requests/
cloc flask/
cloc httpx/
```

**Krok 4:** Porównanie w jednym poleceniu:

```bash
cloc requests/ flask/ httpx/ --by-file --include-lang=Python --csv --out=comparison.csv
```

**Krok 5:** Odpowiedz na pytania (zapiszcie):

1. Który projekt jest "największy" (wg SLOC)?
2. Który ma najlepszy stosunek komentarzy do kodu?
3. Ile procent stanowią puste linie?
4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?

### Zadanie 2: Własny LOC counter (60 min)

`cloc` jest fajny, ale to czarna skrzynka. Czas napisać własny licznik, żeby zrozumieć co właściwie liczymy.

**Co skrypt ma robić:**

Napisz `loc_counter.py`, który:

1. Przyjmuje ścieżkę do katalogu jako argument
2. Znajduje wszystkie pliki `.py`
3. Dla każdego pliku liczy:
   - **LOC** — wszystkie linie (łącznie z pustymi i komentarzami)
   - **SLOC** — source lines of code (niepuste, niekomentarzowe)
   - **Comments** — linie z komentarzami (# i docstringi)
   - **Blank** — puste linie
4. Generuje raport per-plik i podsumowanie
5. Porównuje swoje wyniki z `cloc`

**Punkt startowy:**

```python
#!/usr/bin/env python3
"""LOC Counter - counting lines of code for Python files."""

import sys
from dataclasses import dataclass, field
from pathlib import Path


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

    # TODO: Twój kod tutaj
    # Wskazówki:
    # - Czytaj plik linia po linii
    # - Śledź czy jesteś wewnątrz docstringa (triple quotes)
    # - Linia może być: pusta, komentarz, kod, lub kod+komentarz
    # - Docstringi: ''' lub """ otwierają i zamykają
    #   Uwaga: mogą być jednoliniowe! np. """This is a docstring."""

    return stats


def find_python_files(directory: Path) -> list[Path]:
    """Recursively find all .py files in a directory."""
    return sorted(directory.rglob("*.py"))


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
```

**Oczekiwany output (przykład):**

```
Znaleziono 42 plików .py

Plik                                                          LOC   SLOC   Comm  Blank
--------------------------------------------------------------------------------------
src/requests/__init__.py                                      178    112     38     28
src/requests/api.py                                           157    102     32     23
src/requests/models.py                                        987    714    143    130
...
--------------------------------------------------------------------------------------
RAZEM                                                        8234   5891   1287   1056

Plików: 42
Komentarze/kod: 21.8%
Puste/całość:   12.8%
```

**Krok końcowy:** Porównaj wyniki z `cloc`:

```bash
cloc requests/ --include-lang=Python --csv
python loc_counter.py requests/
```

Czy wyniki się zgadzają? Jeśli nie — dlaczego? (Podpowiedź: docstringi, `__init__.py`, różne definicje "komentarza".)

### Zadanie 3: Analiza trendów (45 min) — dla ambitnych

Jak zmieniał się rozmiar projektu w czasie? Sprawdźmy.

**Do zrobienia:**
- Weź projekt ze stabilnymi tagami/wersjami (np. `requests` ma tagi `v2.20.0`, `v2.25.0`, `v2.28.0`, `v2.31.0`)
- Dla każdego tagu: checkout, uruchom `loc_counter.py`, zapisz wyniki
- Narysuj wykres: oś X = wersja, oś Y = SLOC

```python
import subprocess
import matplotlib.pyplot as plt

tags = ["v2.20.0", "v2.25.0", "v2.28.0", "v2.31.0"]
repo_path = "requests"
sloc_per_tag = []

for tag in tags:
    subprocess.run(["git", "checkout", tag], cwd=repo_path,
                   capture_output=True)
    # Uruchom loc_counter i zbierz wynik (lub importuj jako moduł)
    # ...
    sloc_per_tag.append(total_sloc)

# Przywróć główną gałąź
subprocess.run(["git", "checkout", "main"], cwd=repo_path,
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
```

## Co oddajecie

W swoim branchu `lab04_nazwisko1_nazwisko2`:

1. **`loc_counter.py`** — działający licznik LOC z zadania 2
2. **`comparison.csv`** — wyniki cloc dla 3 projektów z zadania 1
3. **`answers.md`** — odpowiedzi na pytania z zadania 1 + porównanie wyników loc_counter vs cloc
4. *(opcjonalnie)* **`loc_trend.png`** — wykres trendów z zadania 3

## Kryteria oceny

- `loc_counter.py` poprawnie liczy LOC, SLOC, komentarze i puste linie
- Docstringi (triple quotes) są poprawnie zliczane jako komentarze
- Raport zawiera podsumowanie per-plik i ogólne
- Porównanie z cloc: student opisuje różnice i wyjaśnia przyczyny
- Analiza 3 projektów z zadania 1 zawiera konkretne wnioski

## FAQ

**P: Mój loc_counter daje inne wyniki niż cloc. Kto ma rację?**
O: Prawdopodobnie oboje macie rację, ale liczycie co innego. `cloc` ma swoją definicję komentarza (np. inline comments po kodzie traktuje jako kod). Opisz różnice — to jest wartość edukacyjna tego zadania.

**P: Jak obsłużyć docstringi, które zaczynają się i kończą w jednej linii?**
O: `"""Krótki docstring."""` — to jedna linia komentarza. Sprawdź czy linia zawiera otwierający I zamykający triple quote (po usunięciu otwierającego).

**P: Czy `# type: ignore` to komentarz?**
O: Technicznie tak — zaczyna się od `#`. Ale to adnotacja dla mypy, nie komentarz dla człowieka. Na potrzeby tego laba liczymy jako komentarz.

**P: A co z shebangs (`#!/usr/bin/env python3`)?**
O: cloc liczy to jako kod. Możesz traktować jak chcesz, ale udokumentuj swoją decyzję.

**P: Mogę użyć modułu `ast` zamiast parsowania linia po linii?**
O: `ast` nie daje informacji o komentarzach i pustych liniach (bo je ignoruje przy parsowaniu). Do pełnego LOC counter musisz czytać plik jako tekst. Ale `tokenize` z biblioteki standardowej może pomóc.

## Przydatne linki

- [cloc — GitHub](https://github.com/AlDanial/cloc)
- [Python tokenize module](https://docs.python.org/3/library/tokenize.html)
- [Software Size Metrics (Wikipedia)](https://en.wikipedia.org/wiki/Source_lines_of_code)
- [Why Lines of Code is a Stupid Metric](https://blog.codinghorror.com/diseconomies-of-scale-and-lines-of-code/) — Jeff Atwood

---
*"Mierzenie postępu programowania liczbą linii kodu jest jak mierzenie postępu budowy samolotu jego wagą."* — Bill Gates (podobno)
