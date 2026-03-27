## Odpowiedzi na pytania z zadania 1

### 1) Który projekt jest "największy" (wg SLOC)?
**SLOC** - Source LOC, linie z kodem (bez pustych i komentarzy)

Wielkość projektów (wg SLOC):
* `reqests`:    11,770
* `flask`:      19,378
* `httpx`:      26,107

**Największy jest projekt `httpx/`.**

### 2) Który ma najlepszy stosunek komentarzy do kodu?

Stosunek komentarzy do kodu:
* `reqests`:    20.14%
* `flask`:      35.79%
* `httpx`:      8.43%

(Obliczenia wykonane w pomocniczym `.ipynb`)

Najlepszy stosunek komentarzy do kodu ma projekt **requests**, bo znajduje się on w optymalnym zakresie (ok. 10–30%). Wskazuje to na dobrze zbalansowaną dokumentację – **kod jest opisany, ale nie przeładowany komentarzami**.

Projekt **flask** ma z kolei stosunkowo wysoki udział komentarzy, co może sugerować nadmierne komentowanie. Z kolei **httpx** ma niski poziom komentarzy, zwłaszcza jak na tak duży projekt, co może utrudniać jego czytelność i utrzymanie.

### 3) Ile porcent stanowią puste linie?
Liczymy to w stosunku do całego projektu czyli: `code+comment+blank`.

Odsetek pustych linii w całym projekcie:
* `reqests`:    20.83%
* `flask`:      23.91%
* `httpx`:      22.61%

(Obliczenia wykonane w pomocniczym `.ipynb`)

**W każdym z projektów udział pustych linii jest na podobnym poziomie.**

### 4) Czy wyniki są dla nas zaskakujące?
Raczej nie, choć trochę dziwi nas jak **duża jest rozbieżność stosunku komentarzy do kodu** w poszczególnych projektach. Może ona jednak wynikać z różnic w charakterze projektów, poziomie skomplikowania kodu lub ustaleń panujących w poszczególnych zespołach programistów.

Dodatkowo, **podobny odsetek pustych linii** we wszystkich projektach sugeruje, że niezależnie od wielkości i stylu projektu, programiści stosują podobne praktyki formatowania kodu. To jak nieduże były tu różnice taż lekko nas zaskoczyło, zwłaszcza, że odsetek `comment/code` wahał się znacznie bardziej między analizowanymi repozytoriami.


## Porównanie wyników `loc_counter` vs `cloc`

W naszej implementacji narzędzie do zliczania linii kodu (`loc_counter`), wykorzystujemy moduł `tokenize`. Analizę zaczynamy od tokenizacji całego pliku źródłowego i przypisaniu każdej linii informacji o tym, czy zawiera kod, komentarz lub oba te elementy. Pozwala to, w szczególności na rozróżnianie komentarzy od znaków `#` występujących wewnątrz stringów oraz na obsługę wielolinijkowych konstrukcji.

Całkowita liczba linii (`LOC`) odpowiada liczbie wszystkich linii w pliku.
Linie puste (`blank`) identyfikowane są poprzez brak treści po usunięciu białych znaków.

Pozostałe wiersze są klasyfikowana jest na podstawie typów występujących w nich tokenów:
* linie komentarzy (`comment`) to linie zawierające tokeny typu `COMMENT` lub wielolinijkowe stringi (`'''`, `"""`) traktowane jako docstringi
 **ALE: są doliczane do `comment` tylko jeżeli nie są jednocześni klasyfikowane jako `SLOC`, aby zapewnić spełnienie warunku: `LOC=SLOC+comment+blank`.**
* linie kodu (`SLOC`) to linie zawierające inne tokeny (np. identyfikatory, operatory, literały).

Podsumowanie wyników:
| Projekt | Narzędzie  | LOC | SLOC | Comm | Blank |
|---------|------|----------:|----------:|----------:|----------:|
| requests | OWN |     11164 |      7420 |      1692 |      2052 |
| requests | CLOC|     11164 |      7039 |      2073 |      2052 |
| flask    | OWN |     18390 |     10756 |      3361 |      4273 |
| flask    | CLOC|     18390 |     10451 |      3666 |      4273 |
| httpx    | OWN |     17753 |     12507 |      1869 |      3377 |
| httpx    | CLOC|     17753 |     12187 |      2189 |      3377 |

Otrzymane wyniki wykazują bardzo dużą zgodność z tymi pochodzącymi z `cloc` (raportowanymi w najniższej linii raportu). Wartości LOC oraz liczby pustych linii są identyczne dla wszystkich analizowanych projektów, dla SLOC i komentarzy odchylenia są niewielkie (rzędu kilku procent).

Różnice te wynikają głównie z odmiennych definicji komentarzy stosowanych przez oba narzędzia. W naszej implementacji wielolinijkowe stringi rozpoczynające się od `'''` lub `"""` są zawsze traktowane jako komentarze (docstringi), natomiast pozostałe stringi jako kod. Heurystyki stosowane w `cloc` mogą w niektórych przypadkach klasyfikować takie konstrukcje inaczej.
Dodatkowo specjalne przypadki, takie jak shebang (`#!/usr/bin/env python3`), są przez moduł tokenize traktowane jako komentarze, a przez `cloc` jako kod, co również wpływa na niewielkie różnice w wynikach.
