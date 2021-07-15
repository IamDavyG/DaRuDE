#!/bin/bash
for filename in *.orcainp; do
  /project/RDS-FMH-PCOLxQM0-RW/orca_4.2.0/orca "$filename" | tee "$filename".log
  echo "$filename"
  cp *.log ./Results
  cp *.xyz ./Results
done
