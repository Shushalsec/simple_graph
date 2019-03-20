import os

# SCRIPT_PATH = r'M:\pT1_selected - Copy\scripts'
SCRIPT_PATH = os.getcwd()

version_name = os.path.normpath(SCRIPT_PATH).split('\\')[-2]

script_file = os.path.join(SCRIPT_PATH, [script for script in os.listdir(SCRIPT_PATH)][0])
line = "def version_name = '{}'".format(version_name)
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content) #TODO: Modify the version_name line instead of just prepending a line

line_prepender(script_file, line)

