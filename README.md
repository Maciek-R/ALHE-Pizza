Zespó³:
1. Maciej Ruszczyk
2. Jan Antoniak

Treœæ zadania:
Dla grafu opisuj¹cego sieæ ulic w danym mieœcie opracowaæ metodê wyznaczania trasy dla dostawcy pizzy. Metoda powinna uwzglêdniaæ wystêpowanie korków w godzinach szczytu oraz poziom niezadowolenia klientów (nieliniowo proporcjonalny do czasu dostawy).

Jêzyk programowania: Python
Przyjête za³o¿enia:

- wêze³ grafu reprezentuje mo¿liwe miejsce dostarczenia pizzy
- krawêdzie grafu reprezentuj¹ mo¿liwoœæ przejazdu z jednego wêz³a do drugiego
- krawêdzie grafu nie s¹ skierowane(jest mo¿liwoœæ przejazdu w tê i z powrotem)
- aplikacja ma wbudowany fikcyjny czas dnia, od którego bêdzie zale¿a³ czas przejazdu miêdzy wêz³ami(symulacja korków)
- koszt przejazdu(waga krawêdzi) jest ustalony w pewnym przedziale i zmienia siê w zale¿noœci od godziny.
- koszt przejazdu wyra¿any jest w jednostkach czasu symuluj¹cego up³yw czasu
- Niezadowolenie klientów jest zale¿ne kwadratowo od up³ywu czasu

Aplikacja implementowaæ bêdzie algorytm A* optymalizuj¹cy:
1. Czas dostawy
2. Poziom niezadowolenia
3. Zysk

Dodatkowe za³o¿enia:
- za dowiezienie pizzy klient p³aci przy odbiorze
- klient odmawia zap³aty za pizzê, gdy jego poziom zadowolenia przekroczy dany poziom

Aplikacja napisana bêdzie w formie skryptu i bêdzie wykonywaæ nastêpuj¹ce operacje:

1. Odczyt danych z pliku tekstowego(pliki .csv)
2. Przetworzenie danych przy pomocy zaimplementowanego algorytmu
3. Pokazanie wyników(graf ukazuj¹cy najlepsz¹ œcie¿kê)