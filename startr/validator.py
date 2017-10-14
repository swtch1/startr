from requests.exceptions import HTTPError
import os

from startr.scalr.api import Api
from startr.logger import log

__purpose__ = 'Provide validation functions in a centralized location.'


class ValidateArgs:
    @staticmethod
    def start_def(start_def_path):
        """
        Verify that the start_definition_file_string is of the correct type and exists on the filesystem.
        :param start_def_path: path to config file
        :return: start_definition_file_string
        """
        if not isinstance(start_def_path, str):
            print('Invalid input for config file: argument must be a string')
            exit(1)
        if not os.path.isfile(start_def_path):
            print('Invalid input for config file: could not find a file at {}'.format(start_def_path))
            exit(1)
        return start_def_path

    @staticmethod
    def block_seconds(seconds):
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
                 env_id,
                 farm_id_or_name,
                 farm_roles,
                 depends,
                 running_counts):
        self.env_id = env_id
        self.farm_id_or_name = farm_id_or_name
        self.farm_roles = farm_roles
        self.depends = depends
        self.running_counts = running_counts

        self.scalr_api = Api(environment_id=self.env_id,
                             farm_id_or_name=self.farm_id_or_name)
        self.verified_farm_roles = self.scalr_api.farm_roles()

    def validate_definition(self):
        self._validate_farm_id()
        self._validate_farm_roles()
        self._validate_dependency_roles()
        self._validate_running_counts()
        self._validate_block_not_greater_than_running_count()

    def _validate_environment_id(self):
        """
        Verify that the environment ID is valid.
        """
        try:
            self.scalr_api.farm_details()
        except HTTPError:
            log.critical('start definition validation failed: invalid environment id')

    def _validate_farm_id(self):
        """
        Verify that the farm ID is valid.
        """
        try:
            self.scalr_api.farm_details()
        except HTTPError:  # FIXME
            log.critical('start definition validation failed: invalid farm id')
            exit(1)

    def _validate_farm_roles(self):
        """
        Verify that all of the farm roles are valid.
        """
        if not all(map(lambda role: role in self.verified_farm_roles, self.farm_roles)):
            invalid_farm_roles = filter(lambda role: role not in self.verified_farm_roles, self.farm_roles)
            log.critical('start definition validation failed: invalid farm roles: {}'.format(invalid_farm_roles))
            exit(1)

    def _validate_dependency_roles(self):
        """
        Verify that all of the dependencies listed are valid.
        """
        if not all(map(lambda role: role in self.verified_farm_roles, self.depends)):
            invalid_dependencies = filter(lambda dependency: dependency not in self.verified_farm_roles, self.depends)
            log.critical('start definition validation failed: invalid dependencies: {}'.format(invalid_dependencies))
            exit(1)

    def _validate_running_counts(self):
        """
        Verift that the farm role running counts are all numbers.
        """
        running_counts = filter(lambda x: x != 'role_maximum', self.running_counts)
        try:
            [int(count) for count in running_counts]
        except ValueError:
           log.critical('start definition validation failed: running count must be an integer')
           exit(1)
        if not all(map(lambda x: x > 0, running_counts)):
            log.critical('start definition validation failed: running count must be greater than 0')
            exit(1)

    def _validate_block_not_greater_than_running_count(self):
        """
        Verift that the block until running count is not greater than the running count for any role.
        :return:
        """
        pass  # FIXME
