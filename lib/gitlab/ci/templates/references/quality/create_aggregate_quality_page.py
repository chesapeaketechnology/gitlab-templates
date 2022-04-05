import os
import shutil

module_to_index_directory = {}

for root, dirs, files in os.walk("./"):
    for file in files:
        index_path = os.path.join(root, file)
        if "/build/reports/pmd/main.html" in index_path:
             module = index_path.replace("./", "").replace("/build/reports/pmd/main.html", "")
             index_directory = index_path.replace("main.html", "")
             module_to_index_directory[module] = index_directory

index_html_output = open("public/quality/index.html","w")
index_html_output.write("<html>\n")
index_html_output.write("<head>\n")
index_html_output.write("<title>Quality Resources</title>\n")
index_html_output.write("</head>\n")
index_html_output.write("<body>\n")

for module, index_directory in module_to_index_directory.items():
    print(module, index_directory)
    destination_directory = "public/quality/"+module
    shutil.copytree(index_directory, destination_directory)
    value_index = '<h1><a href="./' + module + '/main.html">' + module + '</a></h1>\n'
    index_html_output.write(value_index)

index_html_output.write("</body>\n")
index_html_output.write("</html>\n")
index_html_output.close()