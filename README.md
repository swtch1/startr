# startr
Dependency aware farm role starter for Scalr.

## Requirements
* Python2 (the goal is to port compatibility to Python3 in the future)
* scalrapi library
```
pip install git+git://github.build.ge.com/CoreTechAutomation/scalrapi.git
```

## Generating Scalr API Key and Secret
Access to the Scalr API requires a key and secret generated from
your account.  If you do not have one already navigate to
the[GE Scalr API keys page](https://scalr.corporate.ge.com/#/core/api2)
and generate one.  These will be required for configuration.

## configuration
Scalr configuration details are managed through the following environment variables:
* SCALR_API_KEY: Key ID generated from the API keys page.
* SCALR_SECRET_KEY: Secret key generated from the API keys page.
* SCALR_URL: URL of the Scalr instance to query.
* SCALR_ENV_ID: ID of the Scalr environment to manage. This can
be found in the Scalr interface by hovering over the environment
(sometimes refered to as VPC) dropdown in the top right corner without
clicking it.  Alternatively if this application is running on a
Scalr managed server the environment variable is likely already set.

## Start Definition
The start definition is a configuration file used to specify ...  

## Contributing
I will merge pull requests if you:
* Follow the general stype of the library
* Comply with PEP8 style standards

\# TODO: talk about role_maximum as special variable. Also, warn that
if using the farm role maximum you had better know that it's higher
than your block_until_running_count.
