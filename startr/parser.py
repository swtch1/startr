import argparse
import os

parser = argparse.ArgumentParser(description="Dependency aware farm role starter for Scalr.")
parser.add_argument('-c',
                    '--config-file',
                    type=str,
                    help="config file containing farm roles and dependnecies",
                    default="./startr_config.yml",
                    )

args = parser.parse_args()
