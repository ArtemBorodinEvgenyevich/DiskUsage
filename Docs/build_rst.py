import os

os.system("rm -r source/rst")

os.system('sphinx-apidoc -e -T -f -o source/rst ../DiscUsage_Console')
