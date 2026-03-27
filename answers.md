## Zad 1 

### 1. Który projekt jest "największy" (wg SLOC)?

Największy jest httpx (12187 linijek kodu).

### 2. Który ma najlepszy stosunek komentarzy do kodu?

Najlepszy stosunek komentarzy do kodu ma flask (35%)

### 3. Ile procent stanowią puste linie?

Requests: 18,4%

Flask: 23,2%

Httpx: 19%

### 4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?

Tak. Zaskakujące jest to, że HTTPX ma JSON'a, który ma prawie tyle samo linijek co Flask kodu w Pythonie.
Dodatkowo ciekawe jest to, że Flask ma niemal tyle samo plików dokumentacji, co plików Pythona.    

## Zad 2

Wyniki nie zgadzają się do końca.
Przy porównaniu `/requests`:

- loc_counter.py : 11165 LOC, 6957 SLOC, 2155 komentarzy i 2053 blanki.
- cloc: 11165 LOC, 7040 SLOC, 2072 komentarze i 2053 blanki.

Zatem nasz counter niektóre linijki, które cloc zalicza jako kod, traktuje jako komentarz.
Przykładowo plik `src/requests/api.py` według naszego countera ma 19 SLOC, a według cloc ma 26.
Używając najbardziej nieomylnego narzędzia liczenia na palcach też wyszło nam 19 SLOC.
Także uważamy, że musi to być związane z tym jak
wewnętrznie traktowane są multilinijkowe docstringi w clocu, tylko nie wiemy co może to powodować.
Naszym zdaniem inline comments obsłużone są w ten sam sposób co w clocu.
Hipoteza o tym, że stringi przypisane do zmiennych mogły by to psuć jest raczej zła ( :( ),
bo w `src/requests/api.py` nie ma stringów przypisanych do zmiennych.
