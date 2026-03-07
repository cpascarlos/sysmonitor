#!/bin/bash

total=$(top -bn1 | egrep "Cpu\(s\)" | awk '{print ($8=="id," ? 0 : 100 - $8)}')
echo "$total"