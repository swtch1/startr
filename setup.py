from setuptools import setup

setup(
    name='startr',
    version='0.1',
    description='Dependency aware farm role starter for Scalr.',
    url='https://github.build.ge.com/CoreTechAutomation/startr',
    author='Joshua Thornton',
    author_email='joshua.thornton@ge.com',
    packages='startr',
    install_requires=[
        'pyyaml'
    ]
)

# TODO: Add all the config files to the right place.
# TODO: Setup an alias for the tool so it can be used from the command line.
