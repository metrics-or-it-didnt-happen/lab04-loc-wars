1. Największy projekt (wg SLOC)
    - Największy projekt to tensorflow — ma 761 408 linii kodu.
2. Najlepszy stosunek komentarzy do kodu
    - Najlepszy stosunek ma tensorflow - `279936/761408 = 0.36`
3. Procent pustych linii
    - Najwięcej pustych linii ma tensorflow - `182709/(182709 + 279936 + 761408) = 0.149`
4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?
    -  Nie zaskakują, tensorflow jest największy, bo to bardzo rozbudowana biblioteka ML z dużą ilością kodu i dokumentacji

Analiza wyników dla `Django`:
```
--------------------------------------------------------------------------------------
RAZEM                                                        511128 351935 100347  61468

Plików: 2287
Komentarze/kod: 28.5%
Puste/całość:   12.0%

Porównanie z cloc (jeśli dostępny):
--------------------------------------------------------------------------------------
                                                                LOC   SLOC   Comm  Blank
RAZEM                                                        510718 384382  58215  68121

Plików: 2287
Komentarze/kod: 15.1%
Puste/całość:   13.3%

```

Różnica polega na tym, że w skrypcie liczymy komentarze heurystycznie, a powinniśmy liczyć przez zbudowanie AST (albo użycie ast-comments) dla Pythona i rozpoznawanie komentarzy w ten sposób.