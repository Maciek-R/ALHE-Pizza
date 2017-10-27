Zespół:
1. Maciej Ruszczyk
2. Jan Antoniak

Treść zadania:
Dla grafu opisującego sieć ulic w danym mieście opracować metodę wyznaczania trasy dla dostawcy pizzy. Metoda powinna uwzględniać występowanie korków w godzinach szczytu oraz poziom niezadowolenia klientów (nieliniowo proporcjonalny do czasu dostawy).

Język programowania: Python

Przyjęte założenia:

- węzeł grafu reprezentuje możliwe miejsce dostarczenia pizzy
- krawędzie grafu reprezentują możliwość przejazdu z jednego węzła do drugiego
- krawędzie grafu nie są skierowane(jest możliwość przejazdu w tę i z powrotem)
- aplikacja ma wbudowany fikcyjny czas dnia, od którego będzie zależał czas przejazdu między węzłami(symulacja korków)
- koszt przejazdu(waga krawędzi) jest ustalony w pewnym przedziale i zmienia się w zależności od godziny.
- koszt przejazdu wyrażany jest w jednostkach czasu symulującego upływ czasu
- Niezadowolenie klientów jest zależne kwadratowo od upływu czasu

Aplikacja implementować będzie algorytm A* optymalizujący:
1. Czas dostawy
2. Poziom niezadowolenia
3. Zysk

Dodatkowe założenia:
- za dowiezienie pizzy klient płaci przy odbiorze
- klient odmawia zapłaty za pizzę, gdy jego poziom zadowolenia przekroczy dany poziom

Aplikacja napisana będzie w formie skryptu i będzie wykonywać następujące operacje:

1. Odczyt danych z pliku tekstowego(pliki .csv)
2. Przetworzenie danych przy pomocy zaimplementowanego algorytmu
3. Pokazanie wyników(graf ukazujący najlepszą ścieżkę)
