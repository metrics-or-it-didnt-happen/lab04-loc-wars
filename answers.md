**Zadanie 1**

* **Największy projekt pod kątem SLOC:** `httpx` (12 187 linii).
* **Najlepsza proporcja komentarzy do kodu:** `flask` (35%).
* **Udział pustych linii:** `flask` (23,2%), `httpx` (19%), `requests` (18,4%).
* **Zaskoczenia:** Tak. Po pierwsze, w httpx znajduje się plik JSON, który jest prawie tak duży jak cały pythonowy kod Flaska. Po drugie, we Flasku liczba plików dokumentacji jest niemal równa liczbie skryptów Pythona.

**Zadanie 2**

**Porównanie narzędzi dla `/requests`:**

* **Zgodność:** Puste linie są identyczne (2054).
* **Rozbieżność:** Nasz `loc_counter.py` raportuje mniej SLOC i więcej komentarzy niż `cloc` (SLOC: 6825 vs 7052 | Komentarze: 2298 vs 2071).
* **Różnica w liczbie plików:** Nasz skrypt znalazł 36 plików `.py`, a `cloc` raportuje 35.
* **Przyczyna:** Różnice wynikają z interpretacji docstringów i potrójnych cudzysłowów (nasz parser częściej traktuje je jako komentarze), a także z parsowania linia po linii.