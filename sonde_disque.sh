#!/bin/bash

total=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
echo "$total"