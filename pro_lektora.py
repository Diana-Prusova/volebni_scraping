
# INFORMACE: Tento soubor obsahuje kód, kterým jsem pro třetí projekt   
# scrapovala z wiki data o statových kódech a následně je uložila do 
# JSON souboru.

from bs4 import BeautifulSoup
import requests
import json
import os

# NAČTENÍ POTŘEBNÝCH DAT
response = requests.get("https://cs.wikipedia.org/wiki/Stavov%C3%A9_k%C3%B3dy_HTTP")
soup = BeautifulSoup(response.text, "html.parser")
chyby = soup.find_all("dl")

# VYTVOŘENÍ SLOVNÍKU
seznam_chyb = {}
for chyba in chyby:
    klic = int(chyba.getText()[:3])
    obsah = (chyba.getText()).replace("\n", ": ")
    seznam_chyb[klic] = obsah

# ULOŽENÍ DAT DO JSONu
with open(
    os.path.join("pomocne_soubory", "statove_kody_http.json"),
    mode="w", encoding="utf-8") as file:
    json.dump(seznam_chyb, file)


