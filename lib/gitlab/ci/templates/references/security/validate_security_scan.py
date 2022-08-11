import json
import sys

vulnerability_report = open(sys.argv[1])

data = json.load(vulnerability_report)

excluded_packages = []
if len(sys.argv) > 2:
    excluded_packages_arg = sys.argv[2]
    trimmed_string = excluded_packages_arg.replace(' ', '')
    excluded_packages = trimmed_string.split(",")
    print("Excluded packages:")
    print(excluded_packages)

vulnerabilities_found = set()
# Iterating through the json
for vulnerability in data['vulnerabilities']:
    if vulnerability['severity'] == 'Critical':
        location = vulnerability['location']
        package_name = location['dependency']['package']['name']
        # Verify that the critical vulnerability isn't part of any excluded packages
        if package_name not in excluded_packages:
            vulnerabilities_found.add(package_name)

# Closing file
vulnerability_report.close()

if len(vulnerabilities_found) > 0:
    print("Found " + str(len(vulnerabilities_found)) + " vulnerabilities.")
    for vulnerability in vulnerabilities_found:
        print(vulnerability)
    exit(1)
else:
    print("No vulnerabilities found.")
