import json
import sys

vulnerability_report = open('/Users/cjohnson/Downloads/gl-dependency-scanning-report-test.json')

data = json.load(vulnerability_report)

# Iterating through the json
for vulnerability in data['vulnerabilities']:
    if vulnerability['severity'] == 'Critical':
        location = vulnerability['location']
        packageName = location['dependency']['package']['name']

        excludedPackages = sys.argv[1].replace(' ', '')
        for excludedPackage in excludedPackages.split(","):
            print("Vulnerability found in " + packageName + "\n")
            exit(1)

# Closing file
vulnerability_report.close()