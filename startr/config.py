import os
import yaml

__purpose__ = 'Read and store configuration information from config files.'


with open(os.path.join(os.path.expanduser('~'), '.startr', 'app_config.yml'), 'r') as f:
    config = yaml.load(f)

# with open(os.path.abspath(path_to_defaults_file)) as f:  # FIXME: establish a path to the defaults file.
#     defaults = yaml.load(f)  # TODO: Establish this as an enum.
# TODO: we still need to bring in the actual auth file if not from env vars
