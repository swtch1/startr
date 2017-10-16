import os
import yaml

__purpose__ = 'Read and store configuration information from config files.'
CUR_DIR = os.path.dirname(__file__)


with open(os.path.join(os.path.expanduser('~'), '.startr', 'app_config.yml'), 'r') as f:
    config = yaml.load(f)
with open(os.path.join(CUR_DIR, 'defaults.yml')) as f:  # FIXME: establish a path to the defaults file.
    defaults = yaml.load(f)  # TODO: Establish this as an enum.
with open(os.path.join(CUR_DIR, 'auth.yml')) as f:  # FIXME: establish a path to the auth file.
    auth = yaml.load(f)  # TODO: Establish this as an enum.
