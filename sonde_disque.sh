#!/bin/bash

total=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
rrdtool update monitor.rrd N:U:U:$total
