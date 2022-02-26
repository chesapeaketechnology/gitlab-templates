import glob
import json

data = []

for f in glob.glob('**/code-climate-file.json', recursive=True):
    print(f)
    with open(f,) as infile:
        data.extend(json.load(infile))
    with open(".quality/merged_code-climate-file.json",'w') as outfile:
        json.dump(data, outfile)