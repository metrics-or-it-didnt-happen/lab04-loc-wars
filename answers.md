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
Wyniki się róznią, ale są dość zbliżone.Może to wynikać z zastosowania różnych metod liczenia — cloc potrafi analizować wiele języków, podczas gdy własny skrypt obsługuje tylko Pythona. Również dane z cloc mogły zostać niepoprawnie przeliczone (np. stosunek linii komentarzy do kodu czy procent pustych linii) podczas ręcznego przenoszenia ich do kalkulatora.
```c
_ /\
<(o )___~  ~  ~  ~  ~
 ( ._> /  ~  ~  ~  ~
  `---'~  ~  ~  ~  ~
```