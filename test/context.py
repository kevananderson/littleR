import os
import sys
import inspect

path_to_littleR = __file__
for i in range(2):
    path_to_littleR = os.path.dirname(path_to_littleR)
path_to_littleR = os.path.join(path_to_littleR, "src")
path_to_littleR = os.path.abspath(path_to_littleR)

frame = inspect.stack()[1]
filename = frame.filename
#print(f"Called from: {os.path.abspath(filename)}")
#print(f"Path to littleR (Test): {path_to_littleR}")
sys.path.insert(0, path_to_littleR)

import littleR
