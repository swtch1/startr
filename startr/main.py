#!/usr/bin/python
from time import sleep
import os
import argparse

import yaml
# TODO: Test that launching will automatically increase min/max server counts.
from scalrapi import Api
# from startr.scalr.api import Api
from startr.validator import ValidateArgs, ValidateStartDefinition
from startr.start_definition import StartDefHandler
from startr.config import config, defaults, auth

__purpose__ = 'Application entry point.'

parser = argparse.ArgumentParser(description='Dependency aware farm role starter for Scalr.')
parser.add_argument('-d',
                    '--start-definition',
                    dest='start_def',
                    type=ValidateArgs.start_def,
                    help='Config file containing farm roles and dependnecies.')
# TODO: Future feature
# parser.add_argument('-b',
#                     '--block-time-seconds',
#                     dest='block_seconds',
#                     type=ValidateArgs.block_seconds,
#                     help='Deploy faster by sleeping after dependency deployment has started instead of waiting \
#                          for the dependency to be verified online.  WARNING... this option trades safety for speed. \
#                          Dependant roles are not guaranteed to be online before role deployment is started.',
#                     default=None)
parser.add_argument('--dry-run',
                    dest='dry_run',
                    action='store_true',
                    help='Perform a dry run.  Display what would happen without actually making any changes.')

# TODO: Do something with this
# client = ScalrApiClient((os.getenv('SCALR_URL') or config['scalr_url']).rstrip('/'),
#                         os.getenv('SCALR_API_KEY') or auth['scalr_api_key'],
#                         os.getenv('SCALR_SECRET_KEY') or auth['scalr_secret_key'])

def main():
    if args.dry_run:
        print('##### DRY RUN #####')
        print("any output is just a sanity check, don't worry about timing")
    if args.start_def:
        with open(os.path.abspath(args.start_def), 'r') as f:
            start_def = StartDefHandler(start_def=yaml.load(f))
    else:
        with open(os.path.join(os.path.expanduser('~'), '.startr', 'start_definition.yml'), 'r') as f:
            start_def = StartDefHandler(start_def=yaml.load(f))

    print('validating start definition')
    definition_validator = ValidateStartDefinition(start_def.env_id(),
                                                   start_def.farm_id_or_name(),
                                                   start_def.farm_roles(),
                                                   start_def.dependencies(),
                                                   start_def.running_counts())  # TODO: refactor to just take start definition.
    definition_validator.validate_definition()

    scalr = Api(start_def.env_id(),
                start_def.farm_id_or_name(),
                config['scalr_url'],
                auth['scalr_key_id'],
                auth['scalr_secret_key'])

    def dependency_satisfied(farm_role, dry_run):  # TODO: move somwehere else.
        """
        Verify whether a farm role's dependencies are satisfied.
        :param farm_role: name of farm role to verify
        :param dry_run: is this a dry run?
        :return: True if farm role's running count is satisfied
        """
        if dry_run:
            return True

        dep_farm_role_id = scalr.farm_role_id_by_name(farm_role)
        dep_running_server_count = scalr.running_server_count_by_role(dep_farm_role_id)
        dep_block_until_running_count = start_def.block_until_running_count_by_farm_role(farm_role)
        if dep_running_server_count >= dep_block_until_running_count:
            return True
        return False

    farm_roles = start_def.farm_roles()

    launched_roles = set()
    while farm_roles:
        for role in farm_roles:
            farm_role_id = scalr.farm_role_id_by_name(role)
            sd_farm_role_deps = start_def.dependencies_by_farm_role(role) or []
            sd_running_count = start_def.running_count_by_farm_role(role) \
                or defaults['start_definition']['farm_role']['running_count']
            sd_delay_between_start = start_def.delay_between_start_seconds_by_farm_role(role) \
                or defaults['start_definition']['farm_role']['delay_between_start_seconds']

            rc = scalr.running_server_count_by_role(farm_role_id)
            sdrc = start_def.running_count_by_farm_role(role)
            if rc >= sdrc or role in launched_roles:
                print('{} {} servers running or launched'.format(sdrc, role))
                farm_roles.remove(role)
                continue

            if all(map(lambda r: dependency_satisfied(r, args.dry_run), sd_farm_role_deps)):
                for count in range(sd_running_count):
                    print('launching 1 instance of {}'.format(role))
                    if args.dry_run:
                        sleep(defaults['application']['dry_run_sleep_timer_seconds'])
                        launched_roles.add(role)
                    else:
                        scalr.launch_server(farm_role_id)
                        if count != sd_running_count - 1:  # -1 because loops start at 0
                            sleep(sd_delay_between_start)
                launched_roles.add(role)
            else:
                print('dependencies not yet met for {}'.format(role))
                sleep(defaults['application']['dep_not_satisfied_sleep_timer_seconds'])


if __name__ == '__main__':
    args = parser.parse_args()
    main()
