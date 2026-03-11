import json
import os
import subprocess

config_dir = "config"
config_file = os.path.join(config_dir, "crisis_config.json")
template_file = os.path.join(config_dir, "template_mail.html")
data_file = "FICHIER JSON GENERE PAR RRDTOOL"

config_defaut = {
    "cpu_threshold": 80.0,
    "ram_threshold": 85.0,
    "disk_threshold": 90.0,
    "admin_email": "ton-adresse@email.com"
}

template_defaut = """
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: red;">SITUATION DE CRISE : seuil atteint</h2>
    <p>La module de crise a détecté un dépassement :</p>
    <ul>
        <li><strong>CPU :</strong> {cpu}%</li>
        <li><strong>RAM :</strong> {ram}%</li>
        <li><strong>Disque :</strong> {disk}%</li>
    </ul>
    <p>Date du relevé : {date}</p>
</body>
</html>
"""

def init_files():
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_defaut, f, indent=4)
            
    if not os.path.exists(template_file):
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_defaut)

def get_data_from_json():
    if not os.path.exists(data_file):
        return None

    with open(data_file, 'r') as f:
        data = json.load(f)
    
    row_data = data['data']
    
    for last_entry in reversed(row_data):
        if last_entry[1] is not None:
            return {
                "cpu": round(last_entry[0], 2),
                "ram": round(last_entry[1], 2),
                "disk": round(last_entry[2], 2),
            }
    return None

def send_mail(stats):
    with open(config_file, 'r') as f:
        config = json.load(f)
    with open(template_file, 'r') as f:
        content = f.read().format(**stats)
    
    dest = config["admin_email"]
    subject = "Subject: [CRISE] Alerte Ressources Serveur\n"
    header = f"To: {dest}\n"
    header += "Content-Type: text/html; charset=UTF-8\n\n"
    full_msg = subject + header + content
    
    try:
        p = subprocess.Popen(['/usr/sbin/sendmail', '-t'], stdin=subprocess.PIPE)
        p.communicate(input=full_msg.encode('utf-8'))
    except Exception as e:
        print(f"Erreur envoi mail : {e}")


init_files()

stats = get_data_from_json()
if not stats:
    print("Erreur : Impossible de lire les données JSON (fichier vide ou absent).")
with open(config_file, 'r') as f:
    config = json.load(f)

is_crisis = (
    stats["cpu"] >= config["cpu_threshold"] or 
    stats["ram"] >= config["ram_threshold"] or 
    stats["disk"] >= config["disk_threshold"]
)

if is_crisis:
    print(f"ALERTE CRISE ! CPU:{stats['cpu']} RAM:{stats['ram']} DISK:{stats['disk']}")
    send_mail(stats)
else:
    print(f"OK. CPU:{stats['cpu']} RAM:{stats['ram']} DISK:{stats['disk']}")