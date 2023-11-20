import json
import sys

vulnerability_report = open(sys.argv[1])

data = json.load(vulnerability_report)

excluded_files = []
if len(sys.argv) > 2:
    excluded_files_arg = sys.argv[2]
    trimmed_string = excluded_files_arg.replace(' ', '')
    excluded_files = trimmed_string.split(",")
    print("Excluded files:")
    print(excluded_files)

vulnerabilities_found = set()
# Iterating through the json
for vulnerability in data['vulnerabilities']:
    if vulnerability['severity'] == 'Critical':
        location = vulnerability['location']
        file_name = location['file']
        # Verify that the critical vulnerability isn't part of any excluded file
        if file_name not in excluded_files:
            vulnerabilities_found.add(file_name)

# Closing file
vulnerability_report.close()

if len(vulnerabilities_found) > 0:
    print("Found " + str(len(vulnerabilities_found)) + " files with vulnerabilities.")
    for vulnerability in vulnerabilities_found:
        print(vulnerability)
    exit(1)
else:
    print("No vulnerabilities found.")
