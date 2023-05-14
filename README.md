
# VOLEBNÍ SCRAPING - Engeto

Třetí projekt pro Python akademii




## Popis projektu
Kód slouží k získání volebních výsledků jednotlivých obcí Parlamentních volem z roku 2017. Konkrétně pracuje s webem volby.cz a odkaz na základní rozcestník daných volem najdete zde: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ .

Kód projektu jsem se snažila psát přehledně a uspořádaně, ale zároveň jsem na některých místech záměrvně volila rozvětvenější možnosti, abych si více protrénovala znalosti, které jsem v akademii získala.
## Instalace knihoven
Dokument requirements.txt obsahuje seznam použitých knihoven. Aby kód fungoval správně, doporučuji vytvořit si nové virtuální prostředí a do něj knihovny instalovat. 

To můžete provést například pomocí příkazu:

    pip install -r requirements.txt
## Spuštění projektu

Spuštění kódu je třeba provést pomocí příkazového řádku a je nutné rovnou zadat také dva vstupní argumenty (oba zadané v uvozovkách):
    
1. ODKAZ ÚZEMNÍHO CELKU
- správný odkaz získate když si ve výše uvedeném odkazu vyberete obec a kliknete na 'X' ve sloupci 'výběr obce'
 2. NÁZEV VÝSLEDNÉHO SOUBORU
- název můžete zvolit libovolný, je však nutné, aby měl koncovku '.csv'

Příklad formátu:

    python volebni_scraping.py "https://..." "nazev_souboru.csv"

Zbytkem procesu Vás již program provede sám.
## Ukázka projektu (volební výsledky obce Tachov)

1. argument: "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3207"
2. argument: "vysledky_tachov.csv"


PŘÍKAZ PRO SPUŠTĚNÍ:

    python volebni_scraping.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3207" "vysledky_tachov.csv"

UKÁZKA PRŮBEHU:

    PROBÍHÁ KONTROLA ZADANÝCH ARGUMETŮ:
    Požadované argumenty byly zadány v pořádku. Pokračuji...

    PROBÍHÁ KONTROLA PŘIPOJENÍ:
    Připojení k serveru proběhlo v pořadku. Pokračuji...

    Vytvářím soubor pro uložení dat...
    ...

UKÁZKA VÝSTUPU:

    Kód obce,Název obce,Počet voličů... Občanská demokratická strana,Řád národa - Vlastenecká unie...
    560723,Benešovice,177,86,85,1,0,0,10...nekandidoval,0,3,8,0,1... 
    560740,Bezdružice,752,395,393,31,1,0,31,zde nekandidoval,1,23,61,1,7... 
    560758,Bor,3256,1445,1436,81,2,0,110,zde nekandidoval,4,100,179,22,14... 
    541605,Brod nad Tichou,202,112,112,1,1,0,3,zde nekandidoval,0,2,21,0,0... 

## Seznam souborů v balíčku
    1. README.md
        - soubor se základními informacemi o projektu, jeho spuštění a použití
    2. requirements.txt
        - soubor se seznamem knihoven, které je třeba instalovat pro správný chod kódu.
    3. volebni_scraping.py
        - soubor s hlavním kódem projektu + informacemi o autorce
    4. SLOŽKA volebni_data
        - složka určená k ukládání scrapovaných dat
    5. SLOŽKA pomocné soubory:
        -   statove_kody_http.json - soubor obsahuje stavové kódy response HTML včetně popisu (použito v hlavním kódu)
        -   zajimavosti.txt - soubor obsahuje zajímavosti z daných voleb (použito v hlavním kódu)
