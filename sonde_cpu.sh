#!/bin/bash

while true; do
    date=$(date '+%Y-%m-%d %H:%M:%S')
    total=$(top -bn1 | egrep "Cpu\(s\)" | awk '{print ($8=="id," ? 0 : 100 - $8)}')
    echo "[$date] [CPU] Global : $total%"
    sleep 1
done