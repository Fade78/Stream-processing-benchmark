#!/bin/bash

REPORT=benchmark_report.txt

echo "Logging to $REPORT"

bash common/runbenchmark.sh 2>&1 | tee "$REPORT"
