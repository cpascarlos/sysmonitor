#!/bin/bash

rrd=""
output_dir=""
mkdir -p "$output_dir"

echo "-+-+-+-+-+-+-+-+-+carlos+-+-+-+-+-+-+-+-+-+-"
echo "     GENERATEUR DE GRAPHIQUES AUTOMATIQUE    "
echo "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"

for rrd_file in "$rrd"/*.rrd; do
    
    [ -e "$rrd_file" ] || continue

    nom_machine=$(basename "$rrd_file" .rrd)
    
    echo "Traitement de la machine : $nom_machine"

    for sonde in "cpu" "ram" "disque"; do
        
        file="graph_${nom_machine}_${sonde}.png"
        
        rrdtool graph "$output_dir/$file" \
        --start "-24h" \
        --title "Stats $sonde - $nom_machine" \
        --vertical-label "%" \
        --width 800 --height 250 \
        --lower-limit 0 --upper-limit 100 --rigid \
        --color CANVAS#000000 \
        --color BACK#101010 \
        --color FONT#FFFFDF \
        DEF:valeur="$rrd_file":"$sonde":AVERAGE \
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
        GPRINT:valeur:AVERAGE:"Moyenne\: %6.2lf %%" > /dev/null

        echo "  [OK] -> $file"
    done
done

echo "------------------------------------------"
echo "TERMINÉ : Tous les graphiques sont dans $output_dir"