import os
import yaml

from startr.parser import args

__purpose__ = 'Read and store configuration information from config files.'

with open(os.path.abspath(args.launch_definition_file)) as f:
    launch_definition = yaml.load(f)  # TODO: support path to file or default location
with open(os.path.abspath(path_to_defaults_file)) as f:  # FIXME: establish a path to the defaults file.
    defaults = yaml.load(f)  # TODO: Establish this as an enum.
# TODO: we still need to bring in the actual auth file if not from env vars
