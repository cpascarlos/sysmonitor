import json
import os
import subprocess

config = "config"
parc_config = os.path.join(config, "parc_config.json")
json_dir = "json_parc"
rrd_dir = "rrd_parc"

config_defaut = {
    "machines": [
        {
            "nom": "carl1",
            "ip": "192.168.1.55",
            "user": "ben",
            "remote_path_json": "/home/ben/sysmonitor/export.json",
            "remote_path_rrd": "/home/ben/sysmonitor/monitor.rrd"
        },
        {
            "nom": "carl2",
            "ip": "192.168.1.56",
            "user": "carlos",
            "remote_path_json": "/home/carlos/sysmonitor/export.json",
            "remote_path_rrd": "/home/carlos/sysmonitor/monitor.rrd"
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
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    if not os.path.exists(rrd_dir):
        os.makedirs(rrd_dir)

    with open(parc_config, 'r') as f:
        config = json.load(f)

    for i in config['machines']:
        print(f"Tentative sur {i['nom']} ({i['ip']})")
        
        json_dest = os.path.join(json_dir, f"export_{i['nom']}.json")
        remote_json = f"{i['user']}@{i['ip']}:{i['remote_path_json']}"
        commande1 = ["scp", "-o", "ConnectTimeout=5", remote_json, json_dest]

        rrd_dest = os.path.join(rrd_dir, f"monitor_{i['nom']}.rrd")
        remote_rrd = f"{i['user']}@{i['ip']}:{i['remote_path_rrd']}"
        commande2 = ["scp", "-o", "ConnectTimeout=5", remote_rrd, rrd_dest]

        try:
            subprocess.run(commande1, check=True)
            print(f"OK -> {json_dest}")
            subprocess.run(commande2, check=True)
            print(f"OK -> {rrd_dest}")
        except subprocess.CalledProcessError:
            print(f"ERREUR : Impossible de connecter {i['nom']}.")

if init_config():
    collecter_donnees()
else:
    print("Modifiez la config json avant de continuer..")