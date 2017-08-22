import argparse

from startr.validator import ValidateArgs

__purpose__ = 'Parse command line arguments.'

parser = argparse.ArgumentParser(description='Dependency aware farm role starter for Scalr.')
parser.add_argument('-c',
                    '--config-file',
                    dest='launch_definition_file',
                    type=ValidateArgs.launch_definition_file,
                    help='Config file containing farm roles and dependnecies.',
                    default='./launch_definition.yml',
                    )
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
parser.add_argument('-d',
                    '--dry-run',
                    dest='dry_run',
                    type=bool,  # FIXME: not the type I want
                    help='Perform a dry run.  Display what would happen without actually making any changes.')

args = parser.parse_args()
