URUCHOMIENIE PROGRAMU

Symulator banku zacznie pracę po uruchomieniu modułu bank_simulator.py, na przykład poprzez wpisanie w wierszu poleceń komendy:

python3 bank_simulator.py

Można uruchomić symulator podając opcjonalny argument --load [path], gdzie path to ścieżka pliku zawierającego odpowiednie dane. W takim wypadku bank od początku symulacji będzie posiadał pewną ilość klientów obciążonych odpowiednimi kredytami. Poprawne dane do wykorzystania zawiera przykładowy plik example_csv_data.txt.

OPIS MODUŁÓW

1. bank_simulator

Główny moduł zawierający funkcję main() powodującą uruchomienie symulatora

2. bank_classes

Moduł zawiera implementację klas: Bank(), Loan() oraz Client(); wyjątków: InvalidValueError, InvalidRateError, InvalidInstallmentsError, InvalidNameError, NoBudgetError; oraz funkcji sprawdzających poprawność danych

3. test_bank_classes

Moduł zawiera testy jednostkowe sprawdzające poprawność metod i funkcji zawartych w module bank_classes

4. bank_io

Moduł zawierający funkcje służące komunikacji z użytkownikiem. Początkowe funkcje formatują dane i zwracają je w przyjaznym dla użytkownika, gotowym do wyświetlenia formacie. Funkcje 'take_correct...' służą pobieraniu poprawnych danych od użytkownika. Funkcje load_from_file() oraz read_from_csv umożliwiają czytanie danych z pliku .txt.

5. test_bank_io

Moduł zawiera testy jednostkowe sprawdzające poprawność funkcji czytającej dane z pliku .txt

6. bank_interface

Moduł zawiera implementacje klasy Interface() która odpowiada za interfejs użytkownika

7. example_csv_data.txt

Plik zawiera przykładowe dane, z którymi można uruchomić symulator (opcjonalnie). Format danych zawartych w pliku:

name,value,rate,installments\n

gdzie: name - nazwa klienta, value - całkowita wartość pożyczki, rate - oprocentowanie pożyczki, installments - liczba rat, w których pożyczka ma zostać spłacona.
Aby bank udzielił drugiej pożyczki klientowi, który już wziął jeden kredyt, parametr 'name' należy zastąpić słowem '[previous]' w nawiasach kwadratowych. W takim wypadku pożyczka o odopowiednich parametrach zostanie udzielona ostatniemu utworzonemu klientowi.

8. opis_zadania.txt

Opis zadania otrzymany na rozpoczęcie projektu

UWAGI:

Podczas pracy natrafiłem na możliwy błąd, wynikający z zaokrąglania. Przykładowo, klient ma do spłaty 100 zł w trzech ratach. Ponieważ może posługiwać się wartościami nie większymi niż jeden grosz, jedna rata wynosi 33.33 zł. Aby uniknąć straty w wysokości 1 grosza, przyjąłem założenie, że ostatnia rata jest obliczana na inny sposób tak, aby nadrobić wynikłą różnicę. W tym przypadku trzecia rata wyniesie nie 33.33 a 33.34 zł. W zależności od ilości rat, które zostały do zapłacenia, metoda klasy Loan self.payment() zwraca odpowiednią wartość.

Obliczanie wartości pojedynczej raty odbywa się z precyzją 28 miejsc po przecinku, jednak wartość jest zaokrąglana do dwóch miejsc po przecinku przed odjęciem jej od budżetu. W założeniu, klienci mogą posługiwać się wartościami nie mniejszymi niż jeden grosz.