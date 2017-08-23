import os
import argparse

import yaml

from startr.scalr import api
from startr.validator import ValidateArgs, ValidateStartDefinition
from startr.start_definition import StartDefinitionHandler

__purpose__ = 'Application entry point.'

parser = argparse.ArgumentParser(description='Dependency aware farm role starter for Scalr.')
parser.add_argument('-d',
                    '--start-definition',
                    dest='start_definition_file',
                    type=ValidateArgs.start_definition_file,
                    help='Config file containing farm roles and dependnecies.')
parser.add_argument('-b',
                    '--block-time-seconds',
                    dest='block_time_seconds',
                    type=ValidateArgs.block_time_seconds,
                    help='Deploy faster by sleeping after dependency deployment has started instead of waiting \
                         for the dependency to be verified online.  WARNING... this option trades safety for speed. \
                         Dependant roles are not guaranteed to be online before role deployment is started.',
                    default=None)
parser.add_argument('-q',
                    '--quiet',
                    dest='quiet',
                    type=bool,  # FIXME: not the type I want.
                    help='Do not display any output while running the application.')
parser.add_argument('--dry-run',
                    dest='dry_run',
                    type=bool,  # FIXME: not the type I want
                    help='Perform a dry run.  Display what would happen without actually making any changes.')


def main():
    if args.start_definition_file:
        with open(os.path.abspath(args.start_definition_file), 'r') as f:
            sdh = StartDefinitionHandler(start_definition=yaml.load(f))
    else:
        with open(os.path.join(os.path.expanduser('~'), '.startr', 'start_definition.yml'), 'r') as f:
            sdh = StartDefinitionHandler(start_definition=yaml.load(f))

    if not args.dry_run:
        definition_validator = ValidateStartDefinition(farm_id=sdh.get_farm_id(),
                                                       farm_roles=sdh.get_farm_roles(),
                                                       dependencies=sdh.get_dependencies())
        definition_validator.validate_definition()




if __name__ == '__main__':
    args = parser.parse_args()
    main()
