#!/bin/bash

# time segments lenght
segments=("70" "80" "90" "100" "110")

# path to the folder where the csv tables files will be created
CSV_BASE_PATH="/Users/stefanotugliani/Desktop/dati_ixpe/swift/event_files/02250901"

for SEGMENT in "${segments[@]}"
do
  echo "---------------------------------------"
  echo "Running scripts for segment length: $SEGMENT"

  LOG_FILE="log_${SEGMENT}.txt"
  echo "📄 Logging output to: $LOG_FILE"

  {
    echo "▶️ QPO_allDUs_freq_analysis.py for frequency analysis"
    python3 QPO_allDUs_freq_analysis.py -seg "$SEGMENT" -method hybrid -s
    if [ $? -ne 0 ]; then
      echo "❌ QPO_allDUs_freq_analysis.py failed for segment $SEGMENT. Skipping to next."
      exit 1
    fi

    echo "▶️ QPO_allDUs_polar_analysis.py for polarization analysis"
    python3 QPO_allDUs_polar_analysis.py -seg "$SEGMENT" -st -s -m hybrid
    if [ $? -ne 0 ]; then
      echo "❌ QPO_allDUs_polar_analysis.py failed for segment $SEGMENT. Skipping to next."
      exit 1
    fi

    # path to the csv file just created
    CSV_FILE="$CSV_BASE_PATH/ALL_DU_merged_hybrid_${SEGMENT}s_v.csv"

    echo "▶️ QPO_allDUs_stat_analysis.py for the statistical analysis"
    python3 QPO_allDUs_stat_analysis.py -f "$CSV_FILE" -seg "$SEGMENT" -du 0 -stt
    if [ $? -ne 0 ]; then
      echo "❌ QPO_allDUs_stat_analysis.py failed for segment $SEGMENT."
      exit 1
    fi

    echo "✅ Finished all steps for segment: $SEGMENT"
  } > "$LOG_FILE" 2>&1

  echo "✅ Logs for segment $SEGMENT saved to $LOG_FILE"
  echo "---------------------------------------"

done

echo "🎉 ALL PROCESSES HAVE FINISHED."
