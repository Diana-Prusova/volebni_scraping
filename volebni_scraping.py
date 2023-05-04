"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Diana Průšová
email: di.prusova@gmail.com
discord: Diana P. / Wild Diana#5386
"""
from bs4 import BeautifulSoup
from random import randint
import requests
import json
import csv
import sys
import os
import time
import random


def kontrola_url(url: str) -> bool:
    """
    Funkce přijme argument obsahující URL adresu a zkontroluje,
    jestli byla zadána ve správném formátu.

    Return: True - byla zadána v pořádku
            False - URL má špatný formát
    """
    status = True

    if not url.startswith("https://"):
        print("CHYBA: URL adresa musí být zadána ve formátu 'https://...'")
        status = False
    elif not url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("CHYBA: program pracuje pouze s výsledky roku 2017 "
            "zveřejněnými na stránkách volby.cz")
        status = False
    elif " " in url:
        print("CHYBA: URL adresa nesmí obsahovat mezeru")
        status = False
    
    return status
    
     
def kontrola_jmena_souboru(jmeno_souboru: str) -> bool:
    """
    Funkce přijme argument obsahující jméno souboru a zkontroluje,
    jestlo byla zadána ve správném formátu a bez zakázaných znaků.

    Return: True - zadáno v pořádku
            False - jméno obsahuje chybu
    """
    nepovolene_znaky = ["<", ">", "*", ":", "\\", "/", "?", "."]
    status = True

    # KONTROLA KONCOVKY
    if not jmeno_souboru.endswith(".csv"):
        print("CHYBA: název souboru mít koncovku '.csv' ")
        status = False

    # KONTROLA NEPOVOLENÝCH ZNAKŮ
    ocistene_jm_souboru = jmeno_souboru.rstrip('.csv')
    for znak in ocistene_jm_souboru:
        if znak == " ":
            print("CHYBA: název souboru nesmí obsahovat mezeru")
            status = False
        elif znak in nepovolene_znaky:
            print(f"CHYBA: název souboru nesmí obsahovat '{znak}'")
            status = False
    
    return status


def kontrola_agumentu(url: str, jmeno_souboru: str):
    """
    Funkce přijme argumenty URL a jména souboru ve formátu str. 
    Pomocí pomocných funkcí zkontroluje jestli jsou ve správném formátu
    a na základě výsledku rozhodne jestli bude program pokračovat
    nebo se ukončí.
    """
    oddelovac = "=" * 67
    print(f"\nPROBÍHÁ KONTROLA ZADANÝCH ARGUMETŮ:")
    time.sleep(1.0)

    url_kontr = kontrola_url(url)
    jmeno_souboru_kontr = kontrola_jmena_souboru(jmeno_souboru)

    if (url_kontr and jmeno_souboru_kontr):
        print("Požadované argumenty byly zadány v pořádku. Pokračuji...")
        return
    else:
        print(
            "\nProsím, spusťte program se správnými argumenty. "
            f"Ukončuji program...\n{oddelovac}"
        )
        sys.exit()


def kontrola_pripojeni(url: str):
    """
    Funkce přijme argument URL ve formátu str a zkontroluje kvalitu 
    připojení. Pokud je připojení v pořádku, program pokračuje. Pokud
    je v připojení chyba, informuje uživatele o kódu chyby a program 
    ukončí.
    """
    oddelovac = "=" * 91
    chybova_hlaska = (
        "\n\nProsím zkontrolujte správnost URL, či případnězkuste připojení "
        f"později. Ukončuji program...\n{oddelovac}"
    )
    print(f"\nPROBÍHÁ KONTROLA PŘIPOJENÍ:")
    time.sleep(1.0)

    # NAČTENÍ SEZNAMU STAVOVÝCH CHYB
    with open(
        os.path.join("pomocne_soubory", "statove_kody_http.json"),
        mode="r", encoding="utf-8"
        ) as file:
        seznam_chyb = json.load(file)
   
    # PŘIPOJENÍ NA SERVER A NAČTENÍ HTML
    response = requests.get(url)

    # KONTROLA PŘIPOJENÍ
    num_response = response.status_code
    if num_response == 200:
        print("Připojení k serveru proběhlo v pořadku. Pokračuji...\n")
        return response

    elif str(num_response) in seznam_chyb.keys():
        print(f"CHYBA {seznam_chyb[str(num_response)]}{chybova_hlaska}")
        sys.exit()

    else:
        print(f"CHYBA: došlo k nespecifikované chybě.{chybova_hlaska}")
        sys.exit()

def stazeni_html(url: str):
    """
    Funkce přijme argument URL ve formátu str, odešle požadavek
    na daný server a následně vrátí html kód ve formátu bs4.BeautifulSoup.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def num_cleaning(not_clean_num: str) -> str:
    """
    Funkce přijme argument čísla ve formátu str a očistí jej od
    jakýchkoliv nenumerických znaků a vrátí číslo ve formátu str.
    """
    num = ""
    for znak in not_clean_num:
        if znak.isdigit():
            num += znak
    return num

def stazeni_volebnich_dat(url: str) -> dict:
    """
    Funkce přijme argument URL, pomocí funkce "stazeni_html" přečte kód,
    a následně z nej vytáhne požadovaný data. Ta vrátí ve fomátu dict.
    """
    soup = stazeni_html(url)
    tabulky = soup.find_all("table")

    volebni_data = {}

    # POČET VOLIČŮ
    pocet_volicu_notcls = (tabulky[0].find("td", headers="sa2")).getText()
    volebni_data["Počet voličů"] = (int(num_cleaning(pocet_volicu_notcls)))

    # VYDANÉ OBÁLKY
    vydane_obalky_notcls = (tabulky[0].find("td", headers="sa3")).getText()
    volebni_data["Vydané obálky"] = (int(num_cleaning(vydane_obalky_notcls)))

    # POČET PLATNÝCH HLASŮ
    platne_hlasy_notcls = (tabulky[0].find("td", headers="sa6")).getText()
    volebni_data["Platné hlasy"] = (int(num_cleaning(platne_hlasy_notcls)))


    # POČET HLASŮ PRO KAŽDOU STRANU
    for index in range(1, 3):
        radky = tabulky[index].find_all("tr")
        for radek in radky[2:(len(radky))]:
            try:
                klic = (radek.find("td", class_="overflow_name")).getText()
                hodnota_notcls = (radek.find("td", headers=f"t{index}sa2 t{index}sb3")).getText()
            except AttributeError:
                continue
            else:
                hodnota = int(num_cleaning(hodnota_notcls))
                volebni_data[klic] = hodnota

    return volebni_data

def vytvoreni_hlavicky_CSV() -> list:
    """
    Funkce, pomocí funkce "stazeni_html", načte seznam stran, které v daném
    roce kandidovali a vytvoří list, který bude představovat hlavičku CSV.

    Return: list s názvy klíčů, podle kterých se budou řadit údaje v CSV.
    """
    hlavicka_CSV = [
        "Kód obce", "Název obce", "Počet voličů",
        "Vydané obálky", "Platné hlasy"
        ]
    soup = stazeni_html("https://www.volby.cz/pls/ps2017nss/ps2?xjazyk=CZ")
    nazvy_stran = soup.find_all("td", class_="overflow_name")

    for strana in nazvy_stran:
        hlavicka_CSV.append(strana.getText())

    return hlavicka_CSV


def data_obce_finalni_verze(hlavicka_CSV: list, data_obce: dict) -> dict:
    """
    Funkce spojí list hlavicka_CSV (který mimo jiné obsahuje také všechny 
    pol. strany, které v daném roce kandidovali) a dict vyscrapovaných dat
    z dané lokality a vytvoří dict, který bude obsahovat i informacce o 
    straných, které v dané lokalitě nekandidovali.
    """
    data_obce_aktual = {}

    for polozka in hlavicka_CSV:
        if polozka in data_obce.keys():
            data_obce_aktual[polozka] = data_obce[polozka]
        else:
            data_obce_aktual[polozka] = "zde nekandidoval"
        
    return data_obce_aktual
        

def vytvoreni_souboru_CSV(jmeno_souboru: str, hlavicka_CSV: list):
    """
    Funkce přijme argument jména souboru a seznam klíčů (hlavičku CSV)
    a na základě toho vytvoří soubor, do kterého se můžou ukládat
    scrapovaná data.
    """
    with open(
        os.path.join("volebni_data", jmeno_souboru),
        mode="w", newline="", encoding="utf-8"
        ) as file:
        zapisovac = csv.writer(file)
        zapisovac.writerow(hlavicka_CSV)
    

def zapsani_dat_obce(jmeno_souboru: str, data_obce_aktual: dict):
    """
    Funkce přijme argument jméno souboru a finální verzi vyscrapovaných
    dat (dict) a do daného souboru zapíše řádek s danými daty.
    """
    with open(
        os.path.join("volebni_data", jmeno_souboru),
        mode="a", newline="", encoding="utf-8"
        ) as file:
        zapisovac = csv.DictWriter(file, data_obce_aktual.keys())
        zapisovac.writerow(data_obce_aktual)

def precteni_txt() -> list:
    """
    Funkce načte soubor se zajímavostmi z daných voleb a vytvoří z něj list.

    Return: list se zajímavostmi a informací, která zajímavost byla načtena 
            naposledy.
    """
    with open(
    os.path.join("pomocne_soubory", "zajimavosti.txt"),
    mode="r", encoding="utf-8") as file:
        zajimavosti = eval(file.read())

    return zajimavosti


def vypsani_zajimavosti():
    """
    Funkce, pomocí funkce "precteni_txt", zobrazí uživateli náhodnou zajímavost
    z daných voleb. Zaroveň také hlídá, aby se dvakrát za sebou nezobrazila 
    stejná zajímavost.
    """
    # PŘEČTENÍ ZAJÍMAVOSTI
    zajimavosti = precteni_txt()
    oddelovac = "-" * 48

    while True:
        posledni_index = zajimavosti[5]
        novy_index = random.randint(0, 4)

        if posledni_index != novy_index:
            print("\nZajímavost o těchto volbách pro zkrácení čekání:\n"
            f"{oddelovac}\nVěděli jste, že {zajimavosti[novy_index]}")
            zajimavosti[5] = novy_index
            break

    # AKTUALIZACE INDEXU POSLEDNÍ ZOBRAZENÉ ZAJÍMAVOSTI
    with open(
    os.path.join("pomocne_soubory", "zajimavosti.txt"),
    mode="w", encoding="utf-8") as file:
        file.write(str(zajimavosti))
    

def main():
    url = sys.argv[1]
    jmeno_souboru = sys.argv[2]
    
    oddelovac = "=" * 62
    oddelovac_end = "=" * (62 + len(jmeno_souboru))
    chybova_hlaska = (
    "\n\nProsím, spusťte program se správnými argumenty. "
    f"Ukončuji program...\n{oddelovac}"
    )

    # KONTROLA VSTUPNÍCH DAT
    os.system("cls")
    try:
        url = sys.argv[1]
        jmeno_souboru = sys.argv[2]
    except IndexError:
        print(
            "\nCHYBA: při spuštění programu je třeba zadat dva argumenty "
            "(URL a jméno souboru)"
            f"{chybova_hlaska}"
            )
        sys.exit()
    else:
        if len(sys.argv) > 3:
            print(
            "\nCHYBA: zadali jste více než dva argumenty"
            f"{chybova_hlaska}"
            )
            sys.exit()

    kontrola_agumentu(url, jmeno_souboru)
    kontrola_pripojeni(url)

    # VYTVOŘENÍ CSV PRO DATA
    print("Vytvářím soubor pro uložení dat...")
    hlavicka_CSV = vytvoreni_hlavicky_CSV()
    vytvoreni_souboru_CSV(jmeno_souboru, hlavicka_CSV)

    # EXTRAHOVÁNÍ DAT Z WEBU A JEJICH ZÁPIS
    print("Získávám a zapisuju data jednotlivých obcí...")
    vypsani_zajimavosti()

    soup = stazeni_html(url)
    radky = soup.find_all("tr")
    for radek in radky:
        if "overflow_name" not in str(radek):
            continue
        else:
            data_obce = {}
            data_obce["Kód obce"] = (radek.find("td", class_="cislo")).getText()
            data_obce["Název obce"] = (radek.find("td", class_="overflow_name")).getText()
            pod_url = "https://www.volby.cz/pls/ps2017nss/" + (radek.find_all("a")[0]).get("href")

            data_obce.update(stazeni_volebnich_dat(pod_url))
            data_obce_aktual = data_obce_finalni_verze(hlavicka_CSV, data_obce)
            zapsani_dat_obce(jmeno_souboru, data_obce_aktual)
    
    # POTVRZENÍ ÚSPĚŠNÉHO ZÁPISU
    print("\nZápis proběhl v pořádku.\n\nPožadovaná data najdete ve složce "
        f"'volebni_data' v souboru '{jmeno_souboru}'.\n{oddelovac_end}")


if __name__ == "__main__":
    main()