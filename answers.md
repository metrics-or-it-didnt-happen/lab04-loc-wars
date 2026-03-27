1. Który projekt jest "największy" (wg SLOC)?

Największy projekt to httpx .

2. Który ma najlepszy stosunek komentarzy do kodu?

httpx: 0,084 (8%)
flask: 0,357  (36%)
requests: 0,200 (20%)

flask ma najwiekszy stosunek komentarzy do kodu (36%), ale najlepszy stosunek ma requests (20%) co jest bardziej wyważone

3. Ile procent stanowią puste linie?
httpx: 0,15
flask: 0,24
requests: 0,21

Najwięcej pustych linii: flask (\~24%)
Najmniej: httpx (\~15%)

4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?
* httpx to największy projekt, ale najmniej opisany (tylko \~8% komentarzy) Powód: dużo kodu + duży plik JSON (9746 linii), który zawyża SLOC co trochę „oszukuje” wynik wielkości
* flask ma najlepszą dokumentację (36% komentarzy) ale dużo reStructuredText czyli dokumentacji w repo co jest typowe dla dojrzałego frameworka
* requests jest mniejszy i bardziej „zbalansowany” (\~20% komentarzy, co jest typowe dla wyważonych projektów)







##### cloc result:

   119 text files.
    91 unique files.
    95 files ignored.

\---

Language                     files          blank        comment           code

Python                          35           2053           2072           7040

SUM:                            35           2053           2072           7040



Comment/code: 2072 / 7040 =  0,294 = 29.4%
Blank/all: 2053 /  ( 2053   +   2072   +   7040 ) = 0,184 = 18.4%

##### loc\_counter result:


Znaleziono 36 plików .py
Plik                                                            LOC   SLOC   Comm  Blank

...

RAZEM                                                         11165   6810   2302   2053

Plików: 35
Komentarze/kod: 33.8%
Puste/całość:   18.4%

