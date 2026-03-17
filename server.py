from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__, template_folder='template', static_folder='graphes')

dossier_donnees = "data_parc"
dossier_graphes = "graphes"

def lister_machines():
    machines = []
    if os.path.exists(dossier_donnees):
        for f in os.listdir(dossier_donnees):
            if f.endswith(".json"):
                nom = f.replace("export_", "").replace(".json", "")
                machines.append(nom)
    return sorted(machines)

@app.route('/')
def accueil():
    liste_machines = lister_machines()
    return render_template('accueil.html', machines=liste_machines)

@app.route('/machine/<nom>')
def detail_machine(nom):
    chemin_json = os.path.join(dossier_donnees, f"export_{nom}.json")
    
    if not os.path.exists(chemin_json):
        chemin_json = os.path.join(dossier_donnees, f"{nom}.json")

    try:
        with open(chemin_json, 'r') as f:
            donnees = json.load(f)
        
        entrees = donnees['data']
        derniere_entree = entrees[-2]
        stats_actuelles = {
            "cpu": round(derniere_entree[0], 2),
            "ram": round(derniere_entree[1], 2),
            "disque": round(derniere_entree[2], 2)
        }
    except:
        abort(404)

    return render_template('machine.html', nom=nom, stats=stats_actuelles)

app.run(debug=True, port=6767, host='0.0.0.0')