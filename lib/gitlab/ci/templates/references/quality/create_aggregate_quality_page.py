import os
import shutil
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

module_to_index_directory = {}

for root, dirs, files in os.walk("./"):
    for file in files:
        index_path = os.path.join(root, file)
        if "/build/reports/pmd/main.html" in index_path:
             logging.info('Found main.html at %s', index_path)
             index_path_trimmed = index_path.replace("/build/reports/pmd/main.html", "")
             module = index_path_trimmed.rsplit('/',1)[-1]
             index_directory = index_path.replace("main.html", "")
             if module == ".":
                 module = "root"
                 logging.info("Replacing top-level module with the name %s", module)
             logging.info('Module name found is %s for index directory %s', module, index_directory)
             module_to_index_directory[module] = index_directory

logging.info('Writing base quality index html')
index_html_output = open("public/quality/index.html","w")
index_html_output.write("<html>\n")
index_html_output.write("<head>\n")
index_html_output.write("<title>Quality Resources</title>\n")
index_html_output.write("</head>\n")
index_html_output.write("<body>\n")

for module, index_directory in module_to_index_directory.items():
    destination_directory = "public/quality/"+module
    logging.info('For module %s the index directory is %s and the destination directory is %s', module, index_directory, destination_directory)
    shutil.copytree(index_directory, destination_directory)
    value_index = '<h1><a href="./' + module + '/main.html">' + module + '</a></h1>\n'
    index_html_output.write(value_index)

index_html_output.write("</body>\n")
index_html_output.write("</html>\n")
index_html_output.close()
logging.info('Closing html out')
