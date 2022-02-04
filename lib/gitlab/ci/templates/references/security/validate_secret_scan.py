import json
import sys

# See https://gitlab.com/gitlab-org/security-products/security-report-schemas/-/blob/master/dist/secret-detection-report-format.json for details on report format

secret_report = open(sys.argv[1])

data = json.load(secret_report)

if len(sys.argv) > 2:
    print ("Excluded ids: " + sys.argv[2])

# Iterating through the json
for vulnerability in data['vulnerabilities']:
    confidence = vulnerability['confidence']
    if vulnerability['severity'] == 'Critical' and (confidence == 'Medium' or confidence == 'High' or confidence == 'Confirmed'):
        secretId = vulnerability['id']
        description = vulnerability['description']
        excludedIds = []
        if len(sys.argv) > 2:
            excludedIds = sys.argv[2].replace(' ', '')
            excludedIds = excludedIds.split(",")
            # Verify that the the critical secret isn't part of any excluded ids
            if not any(secretId in string for string in excludedIds):
                print(str("Non excluded secret detected: " + description))
                exit(1)
        else:
            print(str("Secret detected: " + description))
            exit(1)


# Closing file
secret_report.close()
