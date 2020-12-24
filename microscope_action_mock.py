import os
import sys
from definitions import ROOT_DIR

if os.path.exists(fr'{ROOT_DIR}\translated_actions\\actions.txt'):
    f = open(sys.argv[1], 'r')
    print(f.read())
    print('\n')
    f.close()
    os.remove(sys.argv[1])
