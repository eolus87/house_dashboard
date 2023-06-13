__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Union
# Third party libraries
import yaml
# Custom libraries


def load_yaml(file_path_or_dict: Union[str, dict]) -> dict:
    if isinstance(file_path_or_dict, str):
        with open(file_path_or_dict, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    elif isinstance(file_path_or_dict, dict):
        config = file_path_or_dict
    else:
        raise TypeError("File should be a path to a yaml config or a dictionary.")
    return config
