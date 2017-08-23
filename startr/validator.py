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


class ValidateLaunchDefinition:
    def __init__(self, farm_id, farm_roles, dependencies):
        self.farm_id = farm_id
        self.farm_roles = farm_roles
        self.dependencies = dependencies

    def validate_definition(self):
        self._validate_farm_id()
        self._validate_farm_roles()
        self._validate_dependency_roles()

    def _validate_farm_id(self):
        """
        Verify that the farm ID is valid.
        :param farm_id: farm ID of the farm to verify.
        """
        try:
            api.get_farm_details(self.farm_id)
        except HTTPError:  # FIXME
            log.critical('invalid farm id: quitting')
            exit(1)


    def _validate_farm_roles(self):
        """
        Verify that all of the farm roles are valid.
        :param farm_roles: list of farm roles to validate.
        """
        pass

    def _validate_dependency_roles(self):
        """
        Verify that all of the dependencies listed are valid.
        :param depends: list of dependencies to validate.
        """
        pass
