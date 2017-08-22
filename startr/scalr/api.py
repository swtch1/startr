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
SCALR_ENV_ID = os.getenv('SCALR_ENV_ID') or auth[3]  # FIXME: Remove - testing

client = ScalrApiClient(api_url=SCALR_URL, key_id=SCALR_API_KEY, key_secret=SCALR_SECRET_KEY)


def get_farm_id_by_name(farm_name):
    farms = client.get('/api/v1beta0/user/{envId}/farms/'.format(envId=SCALR_ENV_ID))
    # TODO: handle errors
    try:
        matching_farm = filter(lambda x: x['name'] == farm_name, farms)[0]
        return matching_farm['id']
    except IndexError:
        return None


def get_farm_servers(farm_id):
    return client.get('/api/v1beta0/user/{envId}/farms/{farmId}/servers/'.format(envId=SCALR_ENV_ID,
                                                                                 farmId=farm_id))
    # TODO: Handle errors


def get_farm_role_id_by_name(farm_id, farm_role_name):
    farm_roles = client.get('/api/v1beta0/user/{envId}/farms/{farmId}/farm-roles/'.format(envId=SCALR_ENV_ID,
                                                                                          farmId=farm_id))
    # TODO: handle errors
    try:
        matching_role = filter(lambda x: x['alias'] == farm_role_name, farm_roles)[0]
        return matching_role['id']
    except IndexError:
        return None


def get_all_server_count_by_role(farm_role_id):
    return len(client.get('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/servers/'.format(envId=SCALR_ENV_ID,
                                                                                              farmRoleId=farm_role_id)))
    # TODO: handle errors

def get_running_server_count_by_role(farm_role_id):
    servers = client.get('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/servers/'.format(envId=SCALR_ENV_ID,
                                                                                             farmRoleId=farm_role_id))
    return len(filter(lambda x: x['status'] == 'running', servers))
    # TODO: handle errors


def launch_server(farm_role_id):
    ret = client.post('/api/v1beta0/user/{envId}/farm-roles/{farmRoleId}/servers/'.format(envId=SCALR_ENV_ID,
                                                                                        farmRoleId=farm_role_id))
    # TODO: handle errors
    # Successful response, Status 201
    # TODO: ensure launch was successful
    # TODO: Return the id of the server so we can verify it's up.
    # TODO: Test that launching will automatically increase min/max server counts.



# print get_farm_id_by_name('rundeck-sandbox')
# farms =  client.get('/api/v1beta0/user/{envId}/farms/'.format(envId=SCALR_ENV_ID))
# id = get_farm_role_id_by_name(farm_id, 'base-role')
id = get_farm_role_id_by_name(6000, 'base-role')
launch_server(id)
print get_all_server_count_by_role(id)
print get_running_server_count_by_role(id)

# pprint(client.get('/api/v1beta0/user/269/farm-roles/376c2e5f-2fde-4fb0-bab1-11d0e9f59676/servers/'))
# pprint(get_farm_servers(6000)[0])
# client.get('/api/v1beta0/user/{envId}/servers/{serverId}/'.format(envId=SCALR_ENV_ID,
#                                                                   serverId=''))

print('done')

