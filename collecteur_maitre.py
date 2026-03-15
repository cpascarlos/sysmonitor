import json
import os
import subprocess

config = "config"
parc_config = os.path.join(config, "parc_config.json")
data_dir = "data_parc"

config_defaut = {
    "machines": [
        {
            "nom": "carl1",
            "ip": "192.168.1.55",
            "user": "ben",
            "remote_path": "/home/ben/sysmonitor/export.json"
        },
        {
            "nom": "carl2",
            "ip": "192.168.1.56",
            "user": "carlos",
            "remote_path": "/home/carlos/sysmonitor/export.json"
        }
    ]
}

def init_config():
    if not os.path.exists(config):
        os.makedirs(config)
        print(f"Dossier '{config}' créé.")

    if not os.path.exists(parc_config):
        with open(parc_config, 'w', encoding='utf-8') as f:
            json.dump(config_defaut, f, indent=4)
        print(f"Fichier '{parc_config}' créé avec un exemple. Modifiez le avant de continuer.")
        return False
    return True

def collecter_donnees():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(parc_config, 'r') as f:
        config = json.load(f)

    for i in config['machines']:
        print(f"Tentative sur {i['nom']} ({i['ip']})")
        
        local_dest = os.path.join(data_dir, f"export_{i['nom']}.json")
        
        remote_source = f"{i['user']}@{i['ip']}:{i['remote_path']}"
        commande = ["scp", "-o", "ConnectTimeout=5", remote_source, local_dest]

        try:
            subprocess.run(commande, check=True)
            print(f"OK -> {local_dest}")
        except subprocess.CalledProcessError:
            print(f"ERREUR : Impossible de connecter {i['nom']}.")

if init_config():
    collecter_donnees()
else:
    print("Modifiez la config json avant de continuer..")