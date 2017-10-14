from startr.scalr.api import Api

__purpose__ = 'Operations related to parsing the start definition file.'


class StartDefHandler:
    def __init__(self, start_def):
        self.start_def = start_def

    def env_id(self):
        """
        Get the ID of the environment in the start definition.
        :return: environment ID
        """
        return int(self.start_def['environment_id'])

    def farm_id_or_name(self):
        """
        Get the ID or name of the farm defined in the start definition.
        :return: farm ID or name
        """
        return self.start_def['farm_id_or_name']

    def farm_roles(self):
        """
        Get all farm roles defined in start definition.
        :return: list of farm roles
        """
        return [farm_role for farm_role in self.start_def['farm_roles']]

    def dependencies(self):
        """
        Get all of the dependencies in a start definition.
        :return: dependencies list
        """
        dependencies = []
        for farm_role, role_details in self.start_def['farm_roles'].items():
            try:
                depends = role_details.get('depends')
                if depends is None:
                    continue
                dependencies.extend(depends) if isinstance(depends, list) else dependencies.append(depends)
            except AttributeError:
                pass
        return dependencies

    def running_counts(self):
        """
        Get all of the running counts in a start definition.
        """
        running_counts = []
        for farm_role, role_details in self.start_def['farm_roles'].items():
            try:
                running_count = role_details.get('running_count')
                if running_count is None:
                    continue
                running_counts.extend(running_count) if isinstance(running_count, list) else running_counts.append(running_count)
            except AttributeError:
                pass
        return running_counts

    def dependencies_by_farm_role(self, farm_role):
        """
        Get all of the dependencies for a farm role.
        :param farm_role: name of farm role to queery
        :return: farm role dependencies list
        """
        try:
            return self.start_def['farm_roles'][farm_role]['depends']
        except KeyError:
            return None

    def delay_between_start_seconds_by_farm_role(self, farm_role):
        """
        Get the delay between start seconds for a farm role.
        :param farm_role: name of farm role to query
        :return: farm role delay between start seconds
        """
        try:
            return self.start_def['farm_roles'][farm_role]['delay_between_start_seconds']
        except KeyError:
            return None

    def block_until_running_count_by_farm_role(self, farm_role):
        """
        Get the block until running count for a farm role.
        :param farm_role: name of the farm role to query
        :return: farm role block until running count
        """
        try:
            return self.start_def['farm_roles'][farm_role]['block_until_running_count']
        except KeyError:
            return None

    def running_count_by_farm_role(self, farm_role):
        """
        Get the running count for a farm role.
        :param farm_role: name of the farm role to query
        :return: farm role running count
        """
        try:
            return self.start_def['farm_roles'][farm_role]['running_count']
        except KeyError:
            return None
