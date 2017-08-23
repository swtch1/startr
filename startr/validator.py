from requests.exceptions import HTTPError
import os

from startr.scalr import api
from startr.logger import log

__purpose__ = 'Provide validation functions in a centralized location.'


class ValidateArgs:
    @staticmethod
    def start_definition_file(start_definition_file_string):
        """
        Verify that the start_definition_file_string is of the correct type and exists on the filesystem.
        :param start_definition_file_string: path to config file
        :return: start_definition_file_string
        """
        if not isinstance(start_definition_file_string, str):
            print('Invalid input for config file: argument must be a string')
            exit(1)
        abs_file_path = os.path.abspath(start_definition_file_string)
        if not os.path.isfile(abs_file_path):
            print('Invalid input for config file: could not find a file at {}'.format(abs_file_path))
            exit(1)
        return start_definition_file_string

    @staticmethod
    def block_time_seconds(seconds):
        """
        Verify that seconds is of the correct type and range.
        :param seconds: positive integer to validate
        :return: seconds
        """
        try:
            seconds = int(seconds)
        except ValueError:
            print('Invalid input for block time seconds: argument must be an integer greater than 0')
            exit(1)
        if seconds < 1:
            print('Invalid input for block time seconds: argument must be an integer greater than 0')
            exit(1)
        return seconds


class ValidateStartDefinition:
    def __init__(self,
                 environment_id_from_start_definition,
                 farm_id_from_start_definition,
                 farm_roles_from_start_definition,
                 dependencies_from_start_definition,
                 running_counts_from_start_definition):
        self.environment_id_from_start_definition = environment_id_from_start_definition
        self.farm_id_from_start_definition = farm_id_from_start_definition
        self.farm_roles_from_start_definition = farm_roles_from_start_definition
        self.dependencies_from_start_definition = dependencies_from_start_definition
        self.running_counts_from_start_definition = running_counts_from_start_definition

        self.verified_farm_roles = api.get_farm_roles(environment_id=self.environment_id_from_start_definition,
                                                      farm_id=self.farm_id_from_start_definition)

    def validate_definition(self):
        self._validate_farm_id()
        self._validate_farm_roles()
        self._validate_dependency_roles()
        self._validate_running_counts()

    def _validate_environment_id(self):
        """
        Verify that the environment ID is valid.
        """
        try:
            api.get_farm_details(environment_id=self.environment_id_from_start_definition,
                                 farm_id=self.farm_id_from_start_definition)
        except HTTPError:
            log.critical('start definition validation failed: invalid environment id')

    def _validate_farm_id(self):
        """
        Verify that the farm ID is valid.
        """
        try:
            api.get_farm_details(environment_id=self.environment_id_from_start_definition,
                                 farm_id=self.farm_id_from_start_definition)
        except HTTPError:  # FIXME
            log.critical('start definition validation failed: invalid farm id')
            exit(1)

    def _validate_farm_roles(self):
        """
        Verify that all of the farm roles are valid.
        """
        if not all(map(lambda role: role in self.verified_farm_roles, self.farm_roles_from_start_definition)):
            invalid_farm_roles = filter(lambda role: role not in self.verified_farm_roles, self.farm_roles_from_start_definition)
            log.critical('start definition validation failed: invalid farm roles: {}'.format(invalid_farm_roles))
            exit(1)

    def _validate_dependency_roles(self):
        """
        Verify that all of the dependencies listed are valid.
        """
        if not all(map(lambda role: role in self.verified_farm_roles, self.dependencies_from_start_definition)):
            invalid_dependencies = filter(lambda dependency: dependency not in self.verified_farm_roles, self.dependencies_from_start_definition)
            log.critical('start definition validation failed: invalid dependencies: {}'.format(invalid_dependencies))
            exit(1)

    def _validate_running_counts(self):
        """
        Verift that the farm role running counts are all numbers.
        """
        running_counts = filter(lambda x: x != 'role_maximum', self.running_counts_from_start_definition)
        try:
            [int(count) for count in running_counts]
        except ValueError:
           log.critical('start definition validation failed: running count must be an integer')
           exit(1)
        if not all(map(lambda x: x > 0, running_counts)):
            log.critical('start definition validation failed: running count must be greater than 0')
            exit(1)
