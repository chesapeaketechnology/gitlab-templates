from json2html import *

fileName = sys.argv[1]
htmlFileName = fileName.replace("json", "html")
with open (fileName, "r") as report:
    input=report.read()


htmlReport = open(htmlFileName, 'w')
htmlReport.write(json2html.convert(json = input))