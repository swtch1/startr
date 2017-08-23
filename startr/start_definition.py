from startr.scalr import api

__purpose__ = 'Operations related to parsing the start definition file.'


class StartDefinitionHandler:
    def __init__(self, start_definition):
        self.start_definition = start_definition

    def get_farm_id(self):
        try:
            return int(self.start_definition['farm_id_or_name'])
        except ValueError:
            return api.get_farm_id_by_name(self.start_definition['farm_id_or_name'])  # TODO: Make this enumeration.

    def get_farm_roles(self):
        return [farm_role for farm_role in self.start_definition['farm_roles']]

    def get_dependencies(self):
        """
        Get all of the dependencies in a start definition.
        :param start_definition: full start definition from file
        :return: dependencies list
        """
        dependencies = []
        for farm_role, role_details in self.start_definition['farm_roles'].items():
            try:
                depends = role_details.get('depends')
                if depends is None:
                    continue
                dependencies.extend(depends) if isinstance(depends, list) else dependencies.append(depends)
            except AttributeError:
                pass
        return dependencies
