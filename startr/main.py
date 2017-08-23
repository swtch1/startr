from time import sleep
import os
import argparse

import yaml

from startr.scalr.api import Api
from startr.validator import ValidateArgs, ValidateStartDefinition
from startr.start_definition import StartDefinitionHandler
from startr.config import defaults
from startr.logger import log

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
            start_definition = StartDefinitionHandler(start_definition=yaml.load(f))
    else:
        with open(os.path.join(os.path.expanduser('~'), '.startr', 'start_definition.yml'), 'r') as f:
            start_definition = StartDefinitionHandler(start_definition=yaml.load(f))

    if args.dry_run:
        print('validating start definition');sleep(defaults['application']['dry_run_sleep_timer_seconds'])
    definition_validator = ValidateStartDefinition(environment_id_from_start_definition=start_definition.get_environment_id(),
                                                   farm_id_from_start_definition=start_definition.get_farm_id(),
                                                   farm_roles_from_start_definition=start_definition.get_farm_roles(),
                                                   dependencies_from_start_definition=start_definition.get_all_dependencies(),
                                                   running_counts_from_start_definition=start_definition.get_running_counts())
    definition_validator.validate_definition()

    scalr_api = Api(start_definition.get_environment_id())

    farm_roles = start_definition.get_farm_roles()
    while farm_roles:
        for farm_role in farm_roles:
            farm_id = start_definition.get_farm_id()
            farm_role_id = scalr_api.get_farm_role_id_by_name(start_definition.get_farm_id(), farm_role)
            farm_role_deps = start_definition.get_dependencies_by_farm_role(farm_role)
            running_count = start_definition.get_running_count_by_farm_role(farm_role) \
                            or defaults['start_definition']['farm_role']['running_count']
            delay_between_start = start_definition.get_delay_between_start_seconds_by_farm_role(farm_role) \
                                  or defaults['start_definition']['farm_role']['delay_between_start_seconds']

            if scalr_api.get_running_server_count_by_role(farm_role_id) >= start_definition.get_running_count_by_farm_role(farm_role):
                log.debug('actual running count is greater than start definition running count for farm role {}: removing it from the pool'.format(farm_role))
                farm_roles.remove(farm_role)
                continue

            for dep_farm_role in farm_role_deps:
                dep_farm_role_id = scalr_api.get_farm_role_id_by_name(farm_id, dep_farm_role)
                dep_running_server_count = scalr_api.get_running_server_count_by_role(dep_farm_role_id)
                dep_blcok_until_running_count = start_definition.get_block_until_running_count_by_farm_role(dep_farm_role)
                if dep_running_server_count >= dep_blcok_until_running_count:
                    for count in range(running_count):
                        # TODO: thread this whole thing
                        if args.dry_run:
                            print('starting instance of farm role {}'.format(farm_role));sleep(defaults['application']['dry_run_sleep_timer_seconds'])
                        else:
                            scalr_api.launch_server(farm_role_id=farm_role_id)
                            # print('go for it')
                            if count != running_count - 1:
                                sleep(delay_between_start)


                            # farm_role_id = scalr_api.get_farm_role_id_by_name(start_definition.get_farm_id(), 'base-role')
                            # print scalr_api.get_running_server_count_by_role(farm_role_id)

if __name__ == '__main__':
    args = parser.parse_args()
    main()
