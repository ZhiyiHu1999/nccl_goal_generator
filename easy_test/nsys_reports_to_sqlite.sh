#!/bin/bash
# Converts all nsys reports in the repository 'results/nsys_reports' to sqlite
# The sqlite files will be saved in the same directory as the nsys reports
for file in results/nsys_reports/*.nsys-rep; do
    echo "Converting ${file} to ${file}.sqlite"
    # Extracts the filename without the extension
    nsys_report_file=$file
    file=$(basename -- "$file")
    file="${file%.*}"
    # Converts the report to sqlite
    nsys export --type=sqlite --output=results/nsys_reports/${file}.sqlite ${nsys_report_file}
done