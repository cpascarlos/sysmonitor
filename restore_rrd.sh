#!/bin/bash

rrd=""
backup_dir=""

echo "Fichiers de sauvegarde disponibles :"
PS3="Choisissez le fichier à restaurer (entrez le numéro) : "
select xml in $(ls $backup_dir/monitor_backup_*.xml); do
    if [ -n "$xml" ]; then
        echo "Vous avez choisi : $xml"
        break
    else
        echo "Choix invalide."
    fi
done
/usr/bin/rrdtool restore "$xml" "$rrd"