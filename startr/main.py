import os

from startr.parser import args

f = args.config_file
print(os.path.abspath(f))
print(os.path.isfile(f))

