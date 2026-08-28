#!/bin/bash

# Controlla che ci sia un argomento
if [ -z "$1" ]; then
  echo "Usage: $0 <segment_length>"
  exit 1
fi

SEGMENT=$1

echo "Running QPO_allDUs_freq_analysis.py for frequency analysis with segment length: $SEGMENT"
python3 QPO_allDUs_freq_analysis.py -seg "$SEGMENT" -method hybrid -s

if [ $? -ne 0 ]; then
  echo "First script failed. Aborting."
  exit 1
fi

# Esegui il secondo script
echo "Running QPO_allDUs_polar_analysis.py for polarization analysis with segment length: $SEGMENT"
python3 QPO_allDUs_polar_analysis.py -seg "$SEGMENT" -st -s -m hybrid
