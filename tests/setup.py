import sys
from os import path

project_root = path.dirname(path.dirname(__file__))
src = path.join(project_root, 'src')

sys.path.extend((project_root, src))
