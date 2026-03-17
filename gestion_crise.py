import json
import os
import smtplib
from email.message import EmailMessage

config_dir = "config"
dossier_donnees = "json_parc"
fichier_config = os.path.join(config_dir, "config_crise.json")
fichier_template = os.path.join(config_dir, "modele_mail.html")

config_par_defaut = {
    "seuil_cpu": 80.0,
    "seuil_ram": 85.0,
    "seuil_disque": 90.0,
    "email_admin": "email",
    "serveur_smtp": "smtp",
    "port_smtp": 465,
    "utilisateur_smtp": "email",
    "mdp_smtp": "mdp"
}

modele_par_defaut = """
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: red;">SITUATION DE CRISE : {machine}</h2>
    <p>Le module de crise a détecté un dépassement de seuil sur cette machine :</p>
    <ul>
        <li><strong>CPU :</strong> {cpu}%</li>
        <li><strong>RAM :</strong> {ram}%</li>
        <li><strong>Disque :</strong> {disque}%</li>
    </ul>
</body>
</html>
"""

def initialiser_fichiers():
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(fichier_config):
        with open(fichier_config, 'w', encoding='utf-8') as f:
            json.dump(config_par_defaut, f, indent=4)
    if not os.path.exists(fichier_template):
        with open(fichier_template, 'w', encoding='utf-8') as f:
            f.write(modele_par_defaut)

def extraire_donnees_json(chemin_fichier):
    if not os.path.exists(chemin_fichier):
        return None
    try:
        with open(chemin_fichier, 'r') as f:
            donnees = json.load(f)
        
        entrees = donnees['data']
        derniere_entree = entrees[-2] 

        if derniere_entree[0] is not None:
            return {
                "cpu": round(derniere_entree[0], 2),
                "ram": round(derniere_entree[1], 2),
                "disque": round(derniere_entree[2], 2),
            }
    except Exception as e:
        print(f"Erreur de lecture sur {chemin_fichier}: {e}")
    return None

def envoyer_alerte(stats, nom_machine):
    with open(fichier_config, 'r') as f:
        config = json.load(f)
    with open(fichier_template, 'r') as f:
        contenu = f.read().format(machine=nom_machine, **stats)

    message = EmailMessage()
    message.set_content(contenu, subtype='html')
    message['Subject'] = f"[AUTOMATIQUE] Dépassement détecté sur {nom_machine}"
    message['From'] = config["utilisateur_smtp"]
    message['To'] = config["email_admin"]

    try:
        with smtplib.SMTP_SSL(config["serveur_smtp"], config["port_smtp"]) as serveur:
            serveur.login(config["utilisateur_smtp"], config["mdp_smtp"])
            serveur.send_message(message)
        print(f"Mail d'alerte envoyé pour {nom_machine}.")
    except Exception as e:
        print(f"Erreur d'envoi SMTP pour {nom_machine} : {e}")

initialiser_fichiers()

with open(fichier_config, 'r') as f:
    config = json.load(f)

if os.path.exists(dossier_donnees):
    for nom_fichier in os.listdir(dossier_donnees):
        if nom_fichier.endswith(".json"):
            chemin_complet = os.path.join(dossier_donnees, nom_fichier)
            nom_machine = os.path.splitext(nom_fichier)[0]
            nom_machine = nom_machine.replace("export_", "")
            
            stats_actuelles = extraire_donnees_json(chemin_complet)

            if stats_actuelles:
                en_crise = (stats_actuelles["cpu"] >= config["seuil_cpu"] or 
                            stats_actuelles["ram"] >= config["seuil_ram"] or 
                            stats_actuelles["disque"] >= config["seuil_disque"])

                if en_crise:
                    print(f"CRISE {nom_machine} !!!")
                    envoyer_alerte(stats_actuelles, nom_machine)
                else:
                    print(f"Machine {nom_machine} : État normal.")
            else:
                print(f"Données manquantes pour {nom_machine}.")
else:
    print(f"Le dossier {dossier_donnees} est introuvable.")