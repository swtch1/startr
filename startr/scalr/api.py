from pprint import pprint
import os

from startr.scalr.client import ScalrApiClient

__purpose__ = 'Scalr API communication functions.'

with open('c:/important_files/code_projects/coretechautomation/startr/startr/auth.conf', 'r') as f:
    auth = f.read().split(',')  # FIXME: Remove - testing

# TODO: Make this enumeration.
SCALR_API_KEY = os.getenv('SCALR_API_KEY') or auth[0]  # FIXME: Remove - testing
SCALR_SECRET_KEY = os.getenv('SCALR_SECRET_KEY') or auth[1]  # FIXME: Remove - testing
SCALR_URL = (os.getenv('SCALR_URL') or auth[2]).rstrip('/')  # FIXME: Remove - testing
# SCALR_ENV_ID = os.getenv('SCALR_ENV_ID') or auth[3]  # FIXME: Remove - testing

client = ScalrApiClient(api_url=SCALR_URL, key_id=SCALR_API_KEY, key_secret=SCALR_SECRET_KEY)


class Api:
    def __init__(self, environment_id, farm_id_or_name):
        """
        :param environment_id: ID of the environment to query
        :param farm_id_or_name: the ID or name of the farm
        """
        self.environment_id = environment_id
        try:
            self.farm_id = int(farm_id_or_name)
        except ValueError:
            self.farm_id = self.farm_id_by_name(farm_id_or_name)

    def farm_id_by_name(self, farm_name):
        """
        Get the ID of a farm from the farm name.
        :param farm_name: name of farm to query
        :return: farm ID
        """
        farms = client.get('/api/v1beta0/user/{envId}/farms/'.format(envId=self.environment_id))
        # TODO: handle errors
        try:
            matching_farm = filter(lambda x: x['name'] == farm_name, farms)[0]
            return matching_farm['id']
        except IndexError:
            return None

    def farm_details(self):
        """
        Get general details on a farm.
        :return: farm details JSON
        """
        return client.get('/api/v1beta0/user/{envId}/farms/{farmId}/'.format(envId=self.environment_id,
                                                                             farmId=self.farm_id))

    def farm_role_details(self, farm_role_id):
        """
        Get general details on a farm role.
        :param farm_role_id: IDof the farm role to query
        :return: farm role details JSON
        """
        return client.get('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/'.format(envId=self.environment_id,
                                                                                      farmRoleId=farm_role_id))

    def farm_role_max_instances(self, farm_role_id):
        """
        Get the number of max instances set for a scalr farm role.
        :param farm_role_id: ID of the farm role to query
        :return: farm role max instances count
        """
        return self.farm_role_details(farm_role_id=farm_role_id)['scaling']['maxInstances']

    def farm_roles(self):
        """
        Return list of farm roles in a farm.
        :return: list of farm roles
        """
        roles_object = client.get('/api/v1beta0/user/{envId}/farms/{farmId}/farm-roles/'.format(envId=self.environment_id,
                                                                                                farmId=self.farm_id))
        return [farm_role['alias'] for farm_role in roles_object]

    def farm_role_id_by_name(self, farm_role_name):
        """
        Get a farm role ID from the farm role name
        :param farm_role_name: name of farm role to query
        :return: farm role ID
        """
        farm_roles = client.get('/api/v1beta0/user/{envId}/farms/{farmId}/farm-roles/'.format(envId=self.environment_id,
                                                                                              farmId=self.farm_id))
        try:
            matching_role = filter(lambda x: x['alias'] == farm_role_name, farm_roles)[0]
            return matching_role['id']
        except IndexError:
            return None

    def farm_servers(self):
        """
        Get all servers in a farm.
        :return: farm servers list
        """
        return client.get('/api/v1beta0/user/{envId}/farms/{farmId}/servers/'.format(envId=self.environment_id,
                                                                                     farmId=self.farm_id))

    def all_server_count_by_role(self, farm_role_id):
        """
        Get a count of all servers in a farm role, regardless of status.
        :param farm_role_id: ID of farm role to query
        :return: server count
        """
        return len(client.get('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/servers/'.format(envId=self.environment_id,
                                                                                                  farmRoleId=farm_role_id)))

    def running_server_count_by_role(self, farm_role_id):
        """
        Get a count of all servers in a farm role with a status of 'running'
        :param farm_role_id: ID of farm role to query
        :return: running server count
        """
        servers = client.get('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/servers/'.format(envId=self.environment_id,
                                                                                                 farmRoleId=farm_role_id))
        return len(filter(lambda x: x['status'] == 'running', servers))

    def launch_server(self, farm_role_id):
        """
        Launch a server of a particular farm role type.
        :param farm_role_id: ID of farm role to launch server in
        :return: None
        """
        return client.post('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/servers/'.format(envId=self.environment_id,
                                                                                               farmRoleId=farm_role_id))
        # TODO: handle errors
        # Successful response, Status 201
        # TODO: ensure launch was successful
        # TODO: Return the id of the server so we can verify it's up.
        # TODO: Test that launching will automatically increase min/max server counts.
