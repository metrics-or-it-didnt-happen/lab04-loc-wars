# Lab 04: LOC Wars - ile linii to za dużo?

## Czy wiesz, że...

Według badań (które właśnie wymyśliłem), Windows XP miał 45 milionów linii kodu. Nikt do dziś nie wie, ile z nich to komentarze w stylu `// TODO: fix this later`. Podejrzewam, że sporo.

## Kontekst

Metryki rozmiaru kodu to najstarsza i najprostsza forma pomiaru oprogramowania. LOC (Lines of Code) brzmi banalnie - "policz linie, gotowe" - ale diabeł tkwi w szczegółach. Czy pusta linia się liczy? A komentarz? A docstring? A import? Okazuje się, że "ile linii ma ten projekt" nie ma jednej poprawnej odpowiedzi.

W praktyce metryki rozmiaru służą do: szacowania złożoności projektu, porównywania projektów, śledzenia wzrostu kodu w czasie, normalizacji innych metryk (np. "bugi na 1000 LOC"), i jako input do modeli predykcji. Dlatego ważne jest, żeby rozumieć co dokładnie mierzymy.

## Cel laboratorium

Po tym laboratorium będziesz potrafić:
- używać narzędzia `cloc` do analizy rozmiaru projektów,
- napisać własny licznik LOC w Pythonie (parsujący komentarze i docstringi),
- porównywać projekty pod kątem rozmiaru i struktury kodu,
- krytycznie ocenić LOC jako metrykę.

## Wymagania wstępne

- Python 3.9+
- `cloc` zainstalowany - to **narzędzie systemowe**, nie pakiet Pythonowy:
  - Linux: `sudo apt install cloc`
  - Mac: `brew install cloc`
  - Albo z Dockera z lab03 (tam cloc jest już zainstalowany w obrazie)
- matplotlib (`pip install matplotlib` - do opcjonalnej wizualizacji)

## Zadania

### Zadanie 1: cloc w akcji (30 min)

`cloc` (Count Lines of Code) to sprawdzone narzędzie do liczenia linii kodu. Obsługuje dziesiątki języków i odróżnia kod, komentarze i puste linie.

**Krok 1:** Zainstaluj cloc (jeśli jeszcze nie masz):

```bash
# Linux
sudo apt install cloc

# Mac
brew install cloc

# Albo z Dockera (lab03) - obraz budowany przez docker compose:
docker compose run --rm analyzer
```

**Krok 2:** Sklonuj 3 projekty open-source do katalogu tymczasowego:

> **WAŻNE:** Klonujcie repozytoria do `/tmp` albo innego katalogu POZA waszym repozytorium labowym. Jeśli sklonujecie je do katalogu roboczego i zrobicie `git add .`, commitniecie tysiące cudzych plików. Nie chcecie tego. Nikt tego nie chce.

```bash
cd /tmp
git clone https://github.com/psf/requests.git
git clone https://github.com/pallets/flask.git
git clone https://github.com/encode/httpx.git
```

Możesz wybrać inne - ważne żeby były w Pythonie i miały co najmniej kilka tysięcy linii.

**Krok 3:** Przeanalizuj każdy projekt:

```bash
cloc /tmp/requests/
cloc /tmp/flask/
cloc /tmp/httpx/
```

**Krok 4:** Wygeneruj CSV z wynikami:

```bash
# Osobno per projekt - wtedy widać który jest największy
cloc /tmp/requests/ --include-lang=Python --csv --out=requests.csv
cloc /tmp/flask/    --include-lang=Python --csv --out=flask.csv
cloc /tmp/httpx/    --include-lang=Python --csv --out=httpx.csv

# Albo wszystko w jednym pliku (per-file, z nazwą katalogu w ścieżce):
cloc /tmp/requests/ /tmp/flask/ /tmp/httpx/ --by-file --include-lang=Python --csv --out=comparison.csv
```

Oddajecie jeden plik `comparison.csv` - wybierzcie wariant który wam pasuje. Ważne żeby dało się z niego odczytać wyniki per projekt.

**Krok 5:** Odpowiedz na pytania (zapiszcie w `answers.md`):

1. Który projekt jest "największy" (wg SLOC)?
2. Który ma najlepszy stosunek komentarzy do kodu?
3. Ile procent stanowią puste linie?
4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?

### Zadanie 2: Własny LOC counter (60 min)

`cloc` jest fajny, ale to czarna skrzynka. Czas napisać własny licznik, żeby zrozumieć co właściwie liczymy.

**Co skrypt ma robić:**

Napisz `loc_counter.py`, który:

1. Przyjmuje ścieżkę do katalogu jako argument
2. Znajduje wszystkie pliki `.py` (z pominięciem `.venv/`, `venv/`, `__pycache__/`, `.git/`)
3. Dla każdego pliku liczy:
   - **LOC** - wszystkie linie (łącznie z pustymi i komentarzami)
   - **SLOC** - source lines of code (niepuste, niekomentarzowe)
   - **Comments** - linie z komentarzami (`#` i docstringi)
   - **Blank** - puste linie
4. Generuje raport per-plik i podsumowanie
5. Porównuje swoje wyniki z `cloc`

**Ważna zasada:** Każda linia należy do dokładnie jednej kategorii. `LOC = SLOC + Comments + Blank`. Linia z kodem i inline commentem (np. `x = 1  # init`) liczymy jako **SLOC** (tak samo robi `cloc`).

**Punkt startowy:**

```python
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
    - Multi-line docstrings/strings (triple quotes: ''' lub """)
    - Blank lines
    - Inline comments (x = 1  # comment) -> liczone jako SLOC

    Uwaga: triple-quoted strings przypisane do zmiennych (np. x = \"""...\""")
    to technicznie kod, nie komentarze. Ale cloc traktuje je jako komentarze.
    Wy zdecydujcie jak chcecie je liczyć - i uzasadnijcie w answers.md.
    """
    stats = FileStats(path=str(filepath))

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
```

**Oczekiwany output (przykład):**

```
Znaleziono 35 plików .py

Plik                                                          LOC   SLOC   Comm  Blank
--------------------------------------------------------------------------------------
src/requests/__init__.py                                      183    103     47     33
src/requests/api.py                                           157     47     73     37
src/requests/models.py                                       1041    589    270    182
...
--------------------------------------------------------------------------------------
RAZEM                                                       11165   6810   2302   2053

Plików: 35
Komentarze/kod: 33.8%
Puste/całość:   18.4%
```

**Krok końcowy:** Porównaj wyniki z `cloc`:

```bash
cloc /tmp/requests/ --include-lang=Python
python loc_counter.py /tmp/requests/
```

Czy wyniki się zgadzają? Pewnie nie do końca. Opisz w `answers.md`:
- Jakie są różnice (konkretne liczby)?
- Dlaczego? (Podpowiedź: jak twój parser traktuje docstringi vs jak robi to cloc, stringi przypisane do zmiennych, inline comments.)

### Zadanie 3: Analiza trendów (45 min) - dla ambitnych

Jak zmieniał się rozmiar projektu w czasie? Sprawdźmy.

> **Uwaga:** Do tego zadania potrzebujesz pełnej kopii repozytorium (ze wszystkimi tagami). Jeśli klonowałeś z `--depth 1`, tagi nie będą dostępne. Sklonuj ponownie bez tego flaga.

**Do zrobienia:**
- Weź projekt ze stabilnymi tagami/wersjami (np. `requests` ma tagi `v2.20.0`, `v2.25.0`, `v2.28.0`, `v2.31.0`)
- Dla każdego tagu: checkout, uruchom `loc_counter.py`, zapisz wyniki
- Narysuj wykres: oś X = wersja, oś Y = SLOC

```python
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt

# Zaimportuj swój loc_counter jako moduł
# (loc_counter.py musi być w tym samym katalogu lub w PYTHONPATH)
from loc_counter import find_python_files, count_lines

tags = ["v2.20.0", "v2.25.0", "v2.28.0", "v2.31.0"]
repo_path = Path("/tmp/requests")
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
plt.title("Ewolucja rozmiaru projektu requests")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("loc_trend.png", dpi=150)
plt.show()
```

## Co oddajecie

W swoim branchu `lab04_nazwisko1_nazwisko2`:

1. **`loc_counter.py`** - działający licznik LOC z zadania 2
2. **`comparison.csv`** - wyniki cloc dla 3 projektów z zadania 1
3. **`answers.md`** - odpowiedzi na pytania z zadania 1 + porównanie loc_counter vs cloc (z konkretnymi liczbami i wyjaśnieniami różnic)
4. *(opcjonalnie)* **`loc_trend.png`** - wykres trendów z zadania 3

**Nie commitujcie** sklonowanych repozytoriów (requests/, flask/ itp.), wirtualnych środowisk, ani __pycache__/.

## Kryteria oceny

- `loc_counter.py` poprawnie liczy LOC, SLOC, komentarze i puste linie
- Zachowany invariant: LOC = SLOC + Comments + Blank
- Docstringi (triple quotes) są obsługiwane (przynajmniej te zaczynające się od `"""` / `'''`)
- Raport zawiera podsumowanie per-plik i ogólne
- `comparison.csv` z wynikami cloc dla 3 projektów
- `answers.md` zawiera odpowiedzi na pytania z zadania 1 ORAZ opis różnic loc_counter vs cloc z wyjaśnieniem przyczyn

## FAQ

**P: Mój loc_counter daje inne wyniki niż cloc. Kto ma rację?**
O: Prawdopodobnie oboje macie rację, ale liczycie co innego. `cloc` ma swoją heurystykę do rozpoznawania komentarzy - np. triple-quoted stringi przypisane do zmiennych też traktuje jako komentarze. Opisz różnice - to jest sedno tego zadania.

**P: Jak obsłużyć docstringi, które zaczynają się i kończą w jednej linii?**
O: `"""Krótki docstring."""` - to jedna linia komentarza. Sprawdź czy po usunięciu otwierającego `"""` reszta linii zawiera zamykający `"""`.

**P: A co z `x = """\nmulti-line\nstring"""`? To docstring czy kod?**
O: Technicznie to string przypisany do zmiennej - kod, nie komentarz. Ale cloc traktuje to jako komentarz. Twój prosty parser (sprawdzający `startswith('"""')`) tego nie złapie, bo linia zaczyna się od `x = `. To jest OK - opisz tę różnicę w answers.md. Jeśli chcesz być bliżej cloc, możesz szukać `"""` / `'''` w dowolnym miejscu linii, ale to komplikuje logikę.

**P: Mój parser zjada prawdziwy kod po zamknięciu stringa. Co robię źle?**
O: Klasyczny problem. Gdy `x = """` nie otwiera trybu docstringa w twoim parserze, to zamykający `"""` (osobna linia) zostaje zinterpretowany jako *otwarcie* nowego docstringa - i parser zaczyna liczyć kolejne linie kodu jako komentarze. To ograniczenie podejścia linia-po-linii bez pełnego parsowania. Opisz to. Jeśli chcesz to naprawić, rozważ moduł `tokenize`.

**P: Czy `# type: ignore` to komentarz?**
O: Technicznie tak - zaczyna się od `#`. Na potrzeby tego laba: komentarz.

**P: A co z shebangs (`#!/usr/bin/env python3`)?**
O: cloc liczy to jako kod. Ty zdecyduj - ale udokumentuj swoją decyzję.

**P: Mogę użyć modułu `ast` zamiast parsowania linia po linii?**
O: `ast` nie daje informacji o komentarzach i pustych liniach (bo je ignoruje przy parsowaniu). Do pełnego LOC countera musisz czytać plik jako tekst. Ale `tokenize` z biblioteki standardowej może pomóc - daje tokeny dla komentarzy, stringów i kodu.

**P: Mogę użyć ChatGPT / Claude do napisania parsera?**
O: Możesz, ale ostrzegam - LLM-y lubią generować parser docstringów który wygląda ładnie a potem zjada `return` statement bo nie śledzi poprawnie stanu. Zweryfikuj output na prawdziwym projekcie. Gdyby to było takie proste, nikt by nie napisał cloc.

**P: Mój skrypt skanuje tysiące plików z virtualenva. Pomocy.**
O: Używaj `find_python_files` z template'u - ma wykluczenia na `.venv/`, `venv/`, `__pycache__/` i inne. Jeśli piszesz własną wersję, pamiętaj o filtrach. Albo po prostu wskazuj na konkretny katalog projektu, nie na `.`.

**P: `UnicodeDecodeError` przy czytaniu pliku. Co jest?**
O: Niektóre pliki w projektach OSS mają nietypowe kodowanie. Otwieraj pliki z `encoding="utf-8", errors="replace"` - to zamieni nieczytelne bajty na `�` zamiast rzucać wyjątek.

## Przydatne linki

- [cloc - GitHub](https://github.com/AlDanial/cloc)
- [Python tokenize module](https://docs.python.org/3/library/tokenize.html)
- [Software Size Metrics (Wikipedia)](https://en.wikipedia.org/wiki/Source_lines_of_code)
- [Why Lines of Code is a Stupid Metric](https://blog.codinghorror.com/diseconomies-of-scale-and-lines-of-code/) - Jeff Atwood

---
*"Mierzenie postępu programowania liczbą linii kodu jest jak mierzenie postępu budowy samolotu jego wagą."* - Bill Gates (podobno)
