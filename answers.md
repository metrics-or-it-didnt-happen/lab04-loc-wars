# Odpowiedzi — Lab 04

## Zadanie 1: cloc

Wyniki cloc (tylko Python):

- **requests** — 35 plików, 7040 SLOC, 2072 komentarzy, 2053 puste
- **flask** — 80 plików, 10451 SLOC, 3666 komentarzy, 4273 puste
- **httpx** — 57 plików, 12187 SLOC, 2189 komentarzy, 3377 puste

### 1. Który projekt jest największy wg SLOC?

httpx — 12187 linii kodu.

### 2. Stosunek komentarzy do kodu

Flask wygrywa — 3666 komentarzy na 10451 SLOC, czyli ~35%. requests ma ok. 29%, a httpx tylko 18%. Flask jest znany z dobrej dokumentacji i to widać w kodzie, prawie co trzecia niepusta linia to komentarz albo docstring.

### 3. Puste linie

- requests: 18.4%
- flask: 23.2%
- httpx: 19.0%

### 4. Zaskoczenia?

Najbardziej to, że requests jest taki mały (7040 SLOC). 

## Porównanie loc_counter vs cloc

Wyniki mojego countera:
- **requests** — 6627 SLOC, 2485 komentarzy, 2053 puste (LOC = 11165)
- **flask** — 10444 SLOC, 3673 komentarzy, 4273 puste (LOC = 18390)
- **httpx** — 12215 SLOC, 2161 komentarzy, 3377 puste (LOC = 17753)

Puste linie i łączny LOC zgadzają się idealnie. Różnice są w podziale comment vs SLOC.

Największa rozbieżność jest w requests - mój counter znalazł 413 komentarzy więcej niż cloc (2485 vs 2072). W httpx odwrotnie, 28 mniej (2161 vs 2189). Flask prawie się zgadza (różnica 7 linii)

### Skąd te różnice?

Główna przyczyna to triple-quoted stringi przypisane do zmiennych, np.:

```python
_codes = """
100: Continue
200: OK
"""
```

Mój parser sprawdza czy linia zaczyna się od `"""`. Linia `_codes = """` zaczyna się od `_codes`, więc parser widzi ją jako SLOC i nie wchodzi w tryb docstringa. Ale potem zamykający `"""` jest osobną linią zaczynającą się od `"""` — i parser myśli, że to otwarcie nowego docstringa. Od tego momentu zjada kolejne linie kodu jako komentarze, aż trafi na następny `"""`. Dokładnie ten problem jest opisany w FAQ.

W requests jest sporo takich konstrukcji (np. `status_codes.py` z długim multi-line stringiem), stąd duża różnica. W httpx jest ich mniej i tam dominuje odwrotny efekt — cloc łapie triple-quoted stringi zmiennych jako komentarze, a mój parser je pomija.

### Ograniczenia

- Parser linia-po-linii nie widzi kontekstu — nie wie, czy `"""` otwiera docstring czy zamyka string przypisany do zmiennej
- Żeby to naprawić porządnie, trzeba by użyć modułu `tokenize` albo parsować plik jako drzewo AST
- Shebangi (`#!/usr/bin/env python3`) traktuję jako komentarze (bo zaczynają się od `#`)
- Inline comments (`x = 1  # komentarz`) idą jako SLOC (tak samo jak w cloc)
