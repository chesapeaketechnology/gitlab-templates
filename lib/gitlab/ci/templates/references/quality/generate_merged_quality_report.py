import glob
import json
import os
import re

data = []
directory = ".quality/"

if not os.path.exists(directory):
    os.makedirs(directory)

regex = re.compile(r"\/builds\/(.*src?)\/", re.IGNORECASE)

for f in glob.glob('**/code-climate-file.json', recursive=True):
    print(f)
    with open(f,) as infile:
        data.extend(json.load(infile))
    for item in data:
        location = item.get("location")
        pathReplacement = location.get("path")
        pathReplacement = re.sub(regex, "src", pathReplacement)
        location["path"] = pathReplacement
    with open(directory + "/merged-code-climate-file.json",'w') as outfile:
        json.dump(data, outfile)