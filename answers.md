**Krok 5:** Odpowiedz na pytania (zapiszcie w `answers.md`):

1. Który projekt jest "największy" (wg SLOC)?

Największym projektem jest **Django** 801639 linii kodu

2. Który ma najlepszy stosunek komentarzy do kodu?

Django 0.1514
Flask 0.3508
requests 0.2943

Flask ma najlepszy stosunek komentarzy do kodu.

3. Ile procent stanowią puste linie?
Requests = 18.38%
Flask = 23.24%
Django = 13.34%
4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?
Wyniki mnie zaskakują ponieważ Django ma bardzo mało komentarzy (najmniejszay stosunek linii komentarzy do linii kodu). Flask ma bardzo dużo linii pustych, ale to nie jest dziwne dla Python ponieważ puste linii służą do rozdielania funkcji, klasy etc.

**Krok końcowy:** Porównaj wyniki z `cloc`:

```bash
cloc /tmp/requests/ --include-lang=Python
python loc_counter.py /tmp/requests/
```

Czy wyniki się zgadzają? Pewnie nie do końca. Opisz w `answers.md`:
- Jakie są różnice (konkretne liczby)?
- Dlaczego? (Podpowiedź: jak twój parser traktuje docstringi vs jak robi to cloc, stringi przypisane do zmiennych, inline comments.)

Wyniki skryptu są w plikack **owncloc_`nazwa repozytria`.txt**
Wyniki się róznią, ale są dość zbliżone. To wynika z różnej ilości przeanalizowanych plików:
| Repozytorium  | CLoc | Owncloc |
|---------------|------|---------|
| Django        | 2257 | 2894    |
| Flask         | 80   | 83      |
| Requests      | 35   | 36      |

Również w inny sposób traktukje dockstrings. W pryzpadku 
```py
x = """
tekst
"""
``` 
Ostatnie cudzysłowy są liczone jako kometarz, jak i kod po nich do aż dopóki parser nie znajdzie zakonczenia tego pseudo komentarza. Co może zancznie zanurzyć danych. Cloc pracuje barziej kontekstowo i będzie widział że to jest definicja stringu, a nie kometarz.
Nasz parser:

traktujemy wszystkie triple-quoted stringi jako komentarze, jeśli zaczynają się od """ lub ''' po strip()
liczy każdą linię docstringa jako comments

cloc:

rozpoznaje docstringi bardziej kontekstowo (np. tylko jako pierwszy element w funkcji/klasie/modułu)

Efekt: możemy nadliczać komentarze względem cloc
Główne źródła różnic:

* Docstringi – uproszczone wykrywanie vs heurystyki cloc
* Triple-quoted stringi w kodzie – brak rozróżnienia kontekstu
* Parser liniowy – brak pełnej analizy składni

Porównanie liczby linii kometarzy:
| Repozytorium  | CLoc | Owncloc |
|---------------|------|---------|
| Django        | 58217| 66646   |
| Flask         | 3666 | 3687    |
| Requests      | 2072 | 2302    |

Porównanie liczby linii pustych:
| Repozytorium  | CLoc | Owncloc |
|---------------|------|---------|
| Django        |68152 | 68217   |
| Flask         | 4273 | 4273    |
| Requests      | 2053 | 2053    |

Porównanie liczby linii kodu:
| Repozytorium  | CLoc | Owncloc |
|---------------|------|---------|
| Django        |384503|376419   |
| Flask         | 10451| 10430   |
| Requests      | 7040 | 6810    |

Jak widać z tablei owncloc często liczy więcej komentarzy niż cloc, ale lubi nie doszacować liczby linii kodu. TO właśnie pokazuje że liczymy czasami linii jako kometarzy chociaż bardziej zaawansowany cloc liczy to jako kod.

Wniosek:
Nasz parser jest prostszy i deterministyczny, ale mniej dokładny niż cloc, szczególnie w przypadkach granicznych związanych z """.

```c
_ /\
<(o )___~  ~  ~  ~  ~
 ( ._> /  ~  ~  ~  ~
  `---'~  ~  ~  ~  ~
```