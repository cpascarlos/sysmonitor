import requests
import xml.etree.ElementTree as ET
import json

url = "https://www.cert.ssi.gouv.fr/feed/"
json_file = "derniere_alerte.json"

response = requests.get(url, timeout=10)
response.raise_for_status()

root = ET.fromstring(response.content)

item = root.find('.//item')

if item is not None:
    titre = item.find('title').text
    date_pub = item.find('pubDate').text
    link = item.find('link').text
    
    etat = "Clôturé" if "clôture" in titre.lower() else "Actif"
    
    alerte = {
        "titre": titre,
        "date": date_pub,
        "url": link,
        "etat": etat,
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(alerte, f, indent=4, ensure_ascii=False)
    
    print(f"Succès : Alerte '{titre[:30]}...' enregistrée.")
    
