import glob
import json
import os

data = []
directory = ".quality/"

if not os.path.exists(directory):
    os.makedirs(directory)

for f in glob.glob('**/code-climate-file.json', recursive=True):
    print(f)
    with open(f,) as infile:
        data.extend(json.load(infile))
    with open(directory + "/merged-code-climate-file.json",'w') as outfile:
        json.dump(data, outfile)