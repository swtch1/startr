import argparse
import os

from startr.validator import ValidateArgs

parser = argparse.ArgumentParser(description="Dependency aware farm role starter for Scalr.")
parser.add_argument('-c',
                    '--config-file',
                    dest="config_file",
                    type=ValidateArgs.config_file,
                    help="Config file containing farm roles and dependnecies.",
                    default="./startr_config.yml",
                    )
parser.add_argument('-b',
                    '--block-time-seconds',
                    dest="block_time_seconds",
                    type=ValidateArgs.block_time_seconds,
                    help="Deploy faster by sleeping after dependency deployment has started instead of waiting \
                         for the dependency to be verified online.  WARNING... this option trades safety for speed. \
                         Dependant roles are not guaranteed to be online before role deployment is started.")


args = parser.parse_args()
