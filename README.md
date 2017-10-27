Zesp�:
1. Maciej Ruszczyk
2. Jan Antoniak

Tre�� zadania:
Dla grafu opisuj�cego sie� ulic w danym mie�cie opracowa� metod� wyznaczania trasy dla dostawcy pizzy. Metoda powinna uwzgl�dnia� wyst�powanie kork�w w godzinach szczytu oraz poziom niezadowolenia klient�w (nieliniowo proporcjonalny do czasu dostawy).

J�zyk programowania: Python
Przyj�te za�o�enia:

- w�ze� grafu reprezentuje mo�liwe miejsce dostarczenia pizzy
- kraw�dzie grafu reprezentuj� mo�liwo�� przejazdu z jednego w�z�a do drugiego
- kraw�dzie grafu nie s� skierowane(jest mo�liwo�� przejazdu w t� i z powrotem)
- aplikacja ma wbudowany fikcyjny czas dnia, od kt�rego b�dzie zale�a� czas przejazdu mi�dzy w�z�ami(symulacja kork�w)
- koszt przejazdu(waga kraw�dzi) jest ustalony w pewnym przedziale i zmienia si� w zale�no�ci od godziny.
- koszt przejazdu wyra�any jest w jednostkach czasu symuluj�cego up�yw czasu
- Niezadowolenie klient�w jest zale�ne kwadratowo od up�ywu czasu

Aplikacja implementowa� b�dzie algorytm A* optymalizuj�cy:
1. Czas dostawy
2. Poziom niezadowolenia
3. Zysk

Dodatkowe za�o�enia:
- za dowiezienie pizzy klient p�aci przy odbiorze
- klient odmawia zap�aty za pizz�, gdy jego poziom zadowolenia przekroczy dany poziom

Aplikacja napisana b�dzie w formie skryptu i b�dzie wykonywa� nast�puj�ce operacje:

1. Odczyt danych z pliku tekstowego(pliki .csv)
2. Przetworzenie danych przy pomocy zaimplementowanego algorytmu
3. Pokazanie wynik�w(graf ukazuj�cy najlepsz� �cie�k�)