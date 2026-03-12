#!/bin/bash

rrd=""
output_dir=""
mkdir -p "$output_dir"

echo "-+-+-+-+-+-+-+-+-+carlos+-+-+-+-+-+-+-+-+-+-"
echo "         GENERATEUR DE GRAPHIQUES          "
echo "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"

PS3="Entrez le numéro (1, 2 ou 3) : "
select choix in "Processeur (CPU)" "Mémoire (RAM)" "Disque (Disk)"
do
    if [ "$choix" = "Processeur (CPU)" ]; then
        sonde="cpu"
        break
    elif [ "$choix" = "Mémoire (RAM)" ]; then
        sonde="ram"
        break
    elif [ "$choix" = "Disque (Disk)" ]; then
        sonde="disk"
        break
    else
        echo "Choix invalide, merci de taper 1, 2 ou 3."
    fi
done

echo ""
echo "Sur combien d'heures voulez-vous l'historique ?"
read -p "Nombre d'heures (ex: 24) : " HEURES

if [ -z "$hr" ]; then hr=24; fi

file="flame_${sonde}.png"

echo "Génération en cours..."

rrdtool graph "$output_dir/$file" \
--start "-${hr}h" \
--title "$sonde" \
--vertical-label "%" \
--width 800 --height 250 \
--lower-limit 0 --upper-limit 100 --rigid \
--color CANVAS#000000 \
--color BACK#101010 \
--color FONT#FFFFDF \
DEF:valeur="$rrd":"$sonde":AVERAGE \
CDEF:base=valeur,40,*,100,/ \
CDEF:etage=valeur,5,*,100,/ \
AREA:base#FFFF5F:"$sonde" \
STACK:etage#FFFC51 \
STACK:etage#FFF046 \
STACK:etage#FFE95F \
STACK:etage#FFD237 \
STACK:etage#FFC832 \
STACK:etage#FFBE2D \
STACK:etage#FFAA23 \
STACK:etage#FF9619 \
STACK:etage#FF841E \
STACK:etage#FF6600 \
STACK:etage#FF4500 \
GPRINT:valeur:LAST:"Actuel\: %6.2lf %%" \
GPRINT:valeur:MAX:"Max\: %6.2lf %%" \
GPRINT:valeur:AVERAGE:"Moyenne\: %6.2lf %%"

echo "------------------------------------------"
echo "TERMINÉ : $output_dir/$file"