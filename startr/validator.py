import os


class ValidateArgs:
    def __init__(self):
        pass

    @staticmethod
    def config_file(config_file_string):
        if not isinstance(config_file_string, str):
            print('Invalid input for config file: argument must be a string')
            exit(1)
        abs_file_path = os.path.abspath(config_file_string)
        if not os.path.isfile(abs_file_path):
            print('Invalid input for config file: could not find a file at {}'.format(abs_file_path))
            exit(1)
        return config_file_string

    @staticmethod
    def block_time_seconds(seconds):
        try:
            seconds = int(seconds)
        except ValueError:
            print('Invalid input for block time seconds: argument must be an integer greater than 0')
            exit(1)
        if seconds < 1:
            print('Invalid input for block time seconds: argument must be an integer greater than 0')
            exit(1)
        return seconds
