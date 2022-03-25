import json
import sys

vulnerability_report = open(sys.argv[1])

data = json.load(vulnerability_report)

if len(sys.argv) > 2:
    print ("Excluded packages: " + sys.argv[2])

# Iterating through the json
for vulnerability in data['vulnerabilities']:
    if vulnerability['severity'] == 'Critical':
        location = vulnerability['location']
        filePath = location['file']

        excludedFilePaths = []
        if len(sys.argv) > 2:
            excludedFilePaths = sys.argv[2].replace(' ', '')
            excludedFilePaths = excludedFilePaths.split(",")
            # Verify that the the critical vulnerability isn't part of any excluded packages
            if not any(filePath in string for string in excludedFilePaths):
                print(str("Non excluded vulnerability detected: " + filePath))
                exit(1)
        else:
            print(str("Vulnerability detected: " + filePath))
            exit(1)


# Closing file
vulnerability_report.close()
