# English
A bot for Discord that helps with calculations and automates processes in the Grepolis game.
## Functions
### INVITATIONS VIA DISCORD
Requires Olympus Essentials setup (https://github.com/pmpm2000/olympus_essentials).
Calling the bot using the "zap" command. The first argument is the alliance number, and the second is the nickname of the player to be invited.
Examples:
  - zap 1 gracz123
  - zap 3 pmpm2000

### GREPOLYMPIA
1. Command starts with "lvl"
2. After the space, enter your athlete's level.
3. You will get the best stat distributions for each Grepolympia discipline. At high levels, you have to wait a few seconds for the result, because of high computational complexity.
4. Examples:
   - lvl 122
   - lvl 8

### CITY PROTECTION TIME AT 5X WORLDS
1. The bot is invoked with the "ochr" command and time the protection was cast. It gives the times of next three spells to be cast.
2. Times can be entered with or without seconds - in the latter case, the bot will assume that a second is 00.
3. Midnight can be entered either as 24, 0 or 00.
4. The time is entered using colons, just like in the game, so copying the time from the report will work.
5. Examples:
     - ochr 23:16:22
     - ochr 00:45
     - ochr 24:01:19

### TRANSPORT SHIPS CALCULATOR
1. The bot is invoked with the "tra" command and appropriate arguments. Calculations are for speed transport ships with Bunks research.
2. There are 2 ways to specify arguments:
    - number of free citizens only - a good way if we have a balance in land units and transport ships, e.g. when the city is empty.
    - number of free citizens, number of transport ships, number of land units - more advanced way, good when we already have some troops recruited.
3. The bot will return number of fast transport ships that is needed.
4. Examples:
    - tra 3883 => we have 3883 free citizens and the city is empty or there is already a balance between units
    - tra 1214 30 269 => we have 1214 free citizens, but also 30 transport ships and 269 land units recruited

## Configuration
1. In the code, change the value of the 'token' variable to your bot's token.
2. Change the value of the 'webhook_url' variable to the url to your webhook.
3. If you want to use the invitations, permissions and alerts features, configure and run Olympus Essentials (https://github.com/pmpm2000/olympus_essentials). The standard server port is 8002.
4. Enjoy.

# Polski
Bot do Discorda pomagajacy w obliczeniach i automatyzujący procesy w grze Grepolis.
## Funkcje
### ZAPROSZENIA PRZEZ DISCORDA
Wymaga skonfigurowania Olympus Essentials (https://github.com/pmpm2000/olympus_essentials).
Wywołanie bota za pomocą polecenia "zap". Pierwszym argumentem jest numer sojuszu, a drugim jest nick gracza, który ma być zaproszony.
Przykład:
  - zap 1 gracz123
  - zap 3 pmpm2000

### GREPOLYMPIA
1. Polecenie rozpoczyna się od "lvl"
2. Po spacji wpisz poziom swojego atlety.
3. Otrzymasz najlepsze rozkłady statystyk dla każdej konkurencji Grepolympii. Przy wysokich poziomach na wynik trzeba chwilę poczekać (~kilkanaście sekund), bo obliczenia są spore.
4. Przykłady:
  - lvl 122
  - lvl 8

### CZAS OCHRONY NA SWIECIE Z PREDKOSCIA 5
1. Bota wywoluje sie komenda "ochr" i czasem rzucenia ochrony. Podaje on czasy trzech kolejnych ochronek do rzucenia.
2. Czasy mozna wpisywac z sekundami lub bez - w drugim przypadku bot zalozy, ze sekunda to 00.
3. Polnoc mozna wpisac zarowno jako 24, 0 jak i 00.
4. Czas wpisuje sie z uzyciem dwukropkow, dokladnie tak jak w grze, wiec kopiowanie czasu z raportu zadziala.
5. Przyklady:
    - ochr 23:16:22
    - ochr 00:45
    - ochr 24:01:19

### LICZBA TRANSOW W MIESCIE
1. Bota wywoluje sie komenda "tra" i odpowiednimi argumentami. Obliczenia dotyczą szybkich transów z kojami.
2. Sa dwa sposoby wpisywania argumentow:
    - tylko liczba wolnych mieszkancow - sposob dobry kiedy mamy aktualnie rownowage pomiedzy transami a ladem, czyli np. kiedy miasto jest puste.
    - liczba wolnych mieszkancow, aktualna liczba transow, aktualna liczba ladu - dobre kiedy mamy juz zbudowane po troche wszystkiego i nie chce nam sie nic przeliczac.
3. Bot zwroci potrzebna liczbe transow zaokraglona w gore do jednosci.
4. Wyliczenia dotycza tylko szybkich transow ze zbadanymi kojami.
5. Przyklady:
    - tra 3883 => liczba wolnych mieszkancow wynosi 3883, a miasto jest puste lub aktualnie posiadane transy i wojsko maja rownowage
    - tra 1214 30 269 => w miescie jest zbudowanych 30 transow i 269 wojska ladowego (uwzgledniajac te w kolejce), a oprocz tego jest jeszcze wolnych 1214 ludzi
Wskazowka: przez "rownowage" rozumiemy tu sytuacje, kiedy transow jest odpowiednio duzo do posiadanego wojska, czyli np. jest w miescie 1 trans i 16 wojska ladowego. Drugi sposob jest bardziej uniwersalny, ale wymaga wiecej informacji.

### EVENT DIONIZJE GRUDZIEN 2022
Pierwsze co trzeba wpisac to "ev" - znak dla bota\
Po spacji wpisuje sie numer jednostki z tego paska jednostek na ktorym mozna je kupowac. Dla jasnosci:\
1 - Panes\
2 - Sileny\
3 - Phallophoroi / Fallofor\
4 - Kanephoroi\
5 - Driady\
6 - Arcykaplani\
po kolejnej spacji wpisujecie pierwsza liczbe ktora pojawila sie w zadaniu, czyli jesli macie eskortowac 3 Thespianow to wpisujecie 3, a jak macie ulepic 20 koszykow to wpisujecie 20\
po kolejnej spacji wpisujecie czego potrzeba do przyspieszenia. wazne zeby to bylo w liczbie mnogiej w mianowniku, czyli: wozki, noze, osly, kozy, leopardy, pedzle. Polskie znaki dopuszczalne.\
Przyklady:\
ev 1 15 osly\
ev 5 21 kozy\
ev 4 5 pędzle

## Konfiguracja
1. W kodzie zmien wartosc zmiennej 'token' na token swojego bota.
2. Zmien wartosc zmiennej 'webhook_url' na url do swojego webhooka.
3. Jesli chcesz korzystac z funkcji zaproszen, uprawnien i alarmow, skonfiguruj i uruchom Olympus Essentials (https://github.com/pmpm2000/olympus_essentials). Standardowy port serwera to 8002.
4. Korzystaj
