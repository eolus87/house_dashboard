__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Union
# Third party libraries
import yaml
# Custom libraries


def load_conf(config_file: Union[str, dict]) -> dict:
    if isinstance(config_file, str):
        with open(config_file, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    elif isinstance(config_file, dict):
        config = config_file
    else:
        raise TypeError("Config file should be a path to a yaml config or a dictionary.")
    return config
