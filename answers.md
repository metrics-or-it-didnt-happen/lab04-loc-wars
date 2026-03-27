# Odpowiedzi

## Zadanie 1.

Według *SLOC* największym projektem jest **httpx** (*12187 linii kodu*)

## Zadanie 2.

| Projekt  | Liczba linii komentarzy | Liczba linii kodu | Stosunek komentarzy do kodu |
|----------|-----------------|-----------------|----------------------------|
| requests | 2073            | 7039            | 0.2945                     |
| **flask**    | **3666**            | **10451**           | **0.3507**                    |
| httpx    | 2189            | 12187           | 0.1796                     |

Zatem najlepszy stosunek liczby komentarzy do liczby linii kodu ma projekt **flask**.

## Zadanie 3.

| Projekt  | Liczba pustych linii | Liczba wszystkich linii  | % pustych linii |
|----------|-----------------|-----------------|----------------------------|
| requests | 2052            | 11164           | 18,3%                      |
| flask    | 4273            | 18390           | 23,2%                    |
| httpx    | 3377            | 17753           | 19%                     |

## Zadanie 4.

Wyniki nie są zaskakujące - dla przejrzystości między funkcjami i klasami zostawiamy linie odstępu, więc ich liczba jest w pełni uzasadniona. Podobnie wysokie wartości komentarzy również nie dziwią - dobrze jest dokumentować kod i opisywać jego działanie, dlatego większa liczba linii komentarza jest w tym przypadku naturalna.


## *loc_counter* vs *cloc*

### **Requests**

| Kategoria | LOC Counter | cloc | Różnica |
|-----------|------------|------|---------|
| SLOC      | 6324       | 7040 | -10.2%  |
| Comments  | 2788       | 2072 | +34.6%  |
| Blank     | 2053       | 2053 | 0%      |

**Uwagi:**  
- `Blank` się zgadza.
- Różnice w SLOC i Comments wynikają z traktowania docstringów i stringów przypisanych do zmiennych: mój parser liczy wszystkie docstringi jako komentarze, `cloc` czasem jako kod.  
- Inline comments mogą też powodować różnice.  
- Całkowita liczba linii jest zgodna, więc parser nie pomija żadnych linii.  

- Różnice są normalne przy prostym liczeniu linii w Pythonie.  


### **Flask**


| Kategoria | LOC Counter | cloc  | Różnica |
|-----------|------------|-------|---------|
| SLOC      | 10430      | 10451 | -0.2%   |
| Comments  | 3687       | 3666  | +0.6%   |
| Blank     | 4273       | 4273  | 0%      |

**Uwagi:**  
- Wyniki są prawie identyczne.  
- Minimalne różnice w SLOC i Comments wynikają z innego traktowania docstringów i inline comments.  
- Puste linie (`Blank`) się zgadzają w 100%.  
- Całkowita liczba linii pokrywa się, więc parser nie pomija żadnych linii.  


### **Httpx**

| Kategoria | LOC Counter | cloc  | Różnica |
|-----------|------------|-------|---------|
| SLOC      | 12215      | 12187 | +0.2%   |
| Comments  | 2161       | 2189  | -1.3%   |
| Blank     | 3377       | 3377  | 0%      |

**Uwagi:**  
- Wyniki praktycznie się zgadzają.  
- Minimalne różnice w SLOC i Comments wynikają z innego traktowania docstringów i inline comments.  
- Puste linie (`Blank`) są identyczne.  
- Całkowita liczba linii pokrywa się, więc parser nie pomija żadnych linii. 