import os
import re

# SCRIPT_PATH = r'M:\pT1_selected - Copy\scripts'
# os.chdir(r'M:\pT1_selected - skzbnaket')
SCRIPT_PATH = os.path.join(os.getcwd(), 'scripts')

version_name = os.path.normpath(SCRIPT_PATH).split('\\')[-2]

script_file = os.path.join(SCRIPT_PATH, [script for script in os.listdir(SCRIPT_PATH)][0])

with open(script_file, 'r+') as f:
    f.seek(0, 0)
    content = f.read()
    to_be_replaced = re.search("def version_name = '(.*)'", content).group(1)
    content = content.replace(to_be_replaced, version_name)
os.remove(script_file)

with open(script_file, 'w') as file_to_write:
    file_to_write.write(content)
    file_to_write.close()