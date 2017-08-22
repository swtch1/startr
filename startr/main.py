from startr.parser import args
from startr.scalr import api
from startr.validator import ValidateLaunchDefinition
from startr.launch_definition import LaunchDefinitionHandler


__purpose__ = 'Application entry point.'


def main():
    if not args.dry_run:
        definition_validator = ValidateLaunchDefinition(farm_id=ldh.get_farm_id(),
                                                        farm_roles=ldh.get_farm_roles(),
                                                        dependencies=ldh.get_dependencies())
        definition_validator.validate_definition()




if __name__ == '__main__':
    ldh = LaunchDefinitionHandler()
    main()
