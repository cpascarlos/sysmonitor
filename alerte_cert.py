import requests
import xml.etree.ElementTree as ET
import json
import os
import smtplib
import ssl
from email.message import EmailMessage

url = "https://www.cert.ssi.gouv.fr/feed/"
json_file = "derniere_alerte.json"
config_file = ""

def send_alert_mail(alerte):
    if not os.path.exists(config_file):
        print("Erreur : Fichier de config SMTP introuvable.")
        return

    with open(config_file, 'r') as f:
        config = json.load(f)

    msg = EmailMessage()
    content = f"""
    <html>
    <body>
        <h2 style="color: red;">ALERTE CERT</h2>
        <p><strong>Titre :</strong> {alerte['titre']}</p>
        <p><strong>Date :</strong> {alerte['date']}</p>
        <p><strong>État :</strong> {alerte['etat']}</p>
        <p><a href="{alerte['url']}">Consulter l'alerte complète ici</a></p>
    </body>
    </html>
    """
    msg.set_content(content, subtype='html')
    msg['Subject'] = f"[VEILLE] {alerte['titre']}"
    msg['From'] = config["smtp_user"]
    msg['To'] = config["admin_email"]

    try:
        with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"]) as server:
            server.login(config["smtp_user"], config["smtp_pass"])
            server.send_message(msg)
    except Exception as e:
        print(f"Erreur envoi mail veille : {e}")

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    item = root.find('.//item')
except Exception as e:
    print(f"Erreur lors de la récupération du flux : {e}")
    item = None

if item is not None:
    titre = item.find('title').text
    date_pub = item.find('pubDate').text
    link = item.find('link').text
    etat = "Clôturé" if "clôture" in titre.lower() else "Actif"

    nouvelle_alerte = {
        "titre": titre,
        "date": date_pub,
        "url": link,
        "etat": etat,
    }

    ancienne_alerte = {}
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            ancienne_alerte = json.load(f)

    if nouvelle_alerte["titre"] != ancienne_alerte.get("titre") or \
       nouvelle_alerte["date"] != ancienne_alerte.get("date"):
        
        print("Nouvelle alerte détectée ! Mise à jour et envoi du mail...")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(nouvelle_alerte, f, indent=4, ensure_ascii=False)
        
        send_alert_mail(nouvelle_alerte)
    else:
        print("Aucun changement détecté depuis la dernière vérification.")