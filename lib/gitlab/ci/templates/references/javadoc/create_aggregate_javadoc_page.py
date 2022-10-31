import os
import shutil
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

module_to_index_directory = {}

for root, dirs, files in os.walk("./"):
    for file in files:
        index_path = os.path.join(root, file)
        if "/build/docs/javadoc/index.html" in index_path:
             logging.info('Found index.html at %s', index_path)
             module = index_path.replace("./", "").replace("/build/docs/javadoc/index.html", "")
             module = module.rsplit('/',1)[-1]
             logging.info('Module rename is %s', module)
             index_directory = index_path.replace("index.html", "")
             logging.info('Index directory is %s', index_directory)
             module_to_index_directory[module] = index_directory

logging.info('Writing base JavaDoc index html')
index_html_output = open("public/javadocs/index.html","w")
index_html_output.write("<html>\n")
index_html_output.write("<head>\n")
index_html_output.write("<title>JavaDoc Resources</title>\n")
index_html_output.write("</head>\n")
index_html_output.write("<body>\n")

for module, index_directory in module_to_index_directory.items():
    logging.info('Module is %s', module)
    logging.info('Index directory is %s', index_directory)
    destination_directory = "public/javadocs/"+module
    logging.info('Destination directory is %s', destination_directory)
    shutil.copytree(index_directory, destination_directory)
    logging.info('Copied from index to destination directory')
    value_index = '<h1><a href="./' + module + '/index.html">' + module + '</a></h1>\n'
    logging.info('Value index is %s', value_index)
    index_html_output.write(value_index)
    logging.info('Work index html out')

logging.info('Writing finishing index html')
index_html_output.write("</body>\n")
index_html_output.write("</html>\n")
index_html_output.close()
logging.info('Closing html out')
