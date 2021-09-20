from configuration.common import ConfigurationBuilder, Configuration
from configuration.env import EnvironmentVariables
from configuration.yaml import YAMLFile


def load_configuration() -> Configuration:
    builder = ConfigurationBuilder()

    # NB: loads settings from a yaml file, then environment variables
    # refer to https://github.com/RobertoPrevato/roconfiguration documentation
    # for more details.
    builder.add_source(YAMLFile("settings.yaml"))
    builder.add_source(EnvironmentVariables())

    config = builder.build()

    return config
