#!/bin/bash

/usr/bin/rrdtool create monitor.rrd --step 60 \
  DS:cpu:GAUGE:600:0:100 \
  DS:ram:GAUGE:600:0:100 \
  DS:disk:GAUGE:600:0:100 \
  RRA:AVERAGE:0.5:1:43200