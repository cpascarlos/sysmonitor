#!/bin/bash

rrd=""
backup_dir=""
$date=$(date +%Y-%m-%d_%Hh%M)

mkdir -p $backup_dir
/usr/bin/rrdtool dump $rrd > $backup_dir/monitor_backup_$date.xml
find $backup_dir -name "monitor_backup_*.xml" -mtime +7 -delete