1. Który projekt jest "największy" (wg SLOC)?
    Flask: 10451
    Requests: 3277
    Httpx: 12187

    Zdecydowanym zwycięzcą jest Httpx.

2. Który ma najlepszy stosunek komentarzy do kodu?
    Flask: 3666/10451 ~= 35%, na każdą linie kodu przypada 0,35 linii komentarzy
    Requests: 1775/3277 ~= 54% na każdą linie kodu przypada 0,54 linii komentarzy
    Httpx: 2189/12187 ~= 18% na każdą linie kodu przypada 0,18 linii komentarzy

    Requests wygrywa tę kategorię, najmniej linii kodu, ale najlepiej pokryte komentarzem, może jakość nad ilość?


3. Ile procent stanowią puste linie?
    Flask: 4273/18390 ~= 23% wszystkich linii jest pusta
    Requests: 1225/6277 ~= 19% wszystkich linii jest pusta
    Httpx: 3377/17753 ~= 19% wszystkich linii jest pusta

    Flask "wygrywa" największą ilość pustych linii, może ktoś lubi clean albo ma dużo małych sekcji, które są często oddzielane

4. Czy wyniki Cię zaskakują? Dlaczego / dlaczego nie?
    Bardzo zbliżone procenty pustych linii kodu mnie zdziwiły, po poprzednich statystykach spodziewałem sie większego rozrzutu przez różną kulturę pisania i duże różnice w procencie komentarzy.

######################################################################################

cloc /tmp/requests/ --include-lang=Python
python3 loc_counter.py /tmp/requests/
      89 text files.
      67 unique files.
      80 files ignored.

github.com/AlDanial/cloc v 1.98  T=0.07 s (311.5 files/s, 93100.3 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          21           1225           1775           3277
-------------------------------------------------------------------------------
SUM:                            21           1225           1775           3277
-------------------------------------------------------------------------------
Znaleziono 22 plików .py

Plik                                                            LOC   SLOC   Comm  Blank
--------------------------------------------------------------------------------------
/tmp/requests/docs/_themes/flask_theme_support.py                86     68      6     12
/tmp/requests/docs/conf.py                                      386     77    215     94
/tmp/requests/src/requests/__init__.py                          183    103     47     33
/tmp/requests/src/requests/__version__.py                        14     10      3      1
/tmp/requests/src/requests/_internal_utils.py                    51     25     15     11
/tmp/requests/src/requests/adapters.py                          697    379    210    108
/tmp/requests/src/requests/api.py                               157     47     73     37
/tmp/requests/src/requests/auth.py                              314    205     45     64
/tmp/requests/src/requests/certs.py                              18      3     10      5
/tmp/requests/src/requests/compat.py                            106     60     27     19
/tmp/requests/src/requests/cookies.py                           561    292    159    110
/tmp/requests/src/requests/exceptions.py                        152     39     53     60
/tmp/requests/src/requests/help.py                              131     98     11     22
/tmp/requests/src/requests/hooks.py                              34     14     10     10
/tmp/requests/src/requests/models.py                           1041    589    270    182
/tmp/requests/src/requests/packages.py                           23     15      4      4
/tmp/requests/src/requests/sessions.py                          834    361    323    150
/tmp/requests/src/requests/status_codes.py                      128     15    101     12
/tmp/requests/src/requests/structures.py                         99     40     32     27
/tmp/requests/src/requests/utils.py                            1086    537    317    232
/tmp/requests/tests/testserver/server.py                        176    137      7     32
--------------------------------------------------------------------------------------
RAZEM                                                          6277   3114   1938   1225

Plików: 21
Komentarze/kod: 62.2%
Puste/całość:   19.5%
            blank   comment     code
cloc        1225    1775        3277
our code    1225    1938        3114

Cloc więcej linii zaliczył do kodu, a nasz więcej do komentarzy.
Różnice mogą pochodzić z innego podejścia do wykrywania Docstringów.