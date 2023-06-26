__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Dict, List, Tuple, Union, Any, Iterable

# Third party libraries
import pandas as pd
import numpy as np
from numpy import ndarray

# Custom libraries

PING_AVAILABILITY_THRESHOLD = 1000
MAX_PING = 2000


def calculate_stats(dict_of_dfs: Dict) -> pd.DataFrame:
    devices_list = list(dict_of_dfs.keys())
    mean_list = [df["value"].astype("float").mean().round(0) for df in dict_of_dfs.values()]
    std_list = [df["value"].astype("float").std().round(0) for df in dict_of_dfs.values()]
    available = []
    for x in mean_list:
        if x > PING_AVAILABILITY_THRESHOLD:
            available.append(False)
        else:
            available.append(True)

    data_as_dict = {"Device": devices_list,
                    "Mean": mean_list,
                    "Std": std_list,
                    "Available": available}
    data_as_pd = pd.DataFrame(data_as_dict)

    return data_as_pd


def calculate_histogram(dict_of_dfs: Dict) -> List[Tuple[Union[ndarray, Iterable, int, float], Any]]:
    devices_list = list(dict_of_dfs.keys())

    list_of_output_pds = []
    for device_name in devices_list:
        ping_values = dict_of_dfs[device_name]["value"][dict_of_dfs[device_name]["value"] < MAX_PING].astype("float")
        list_of_output_pds.append(np.histogram(ping_values, bins=50, range=[0, 100]))

    return list_of_output_pds


def calculate_downtime(dict_of_dfs: Dict) -> List[ndarray]:
    devices_list = list(dict_of_dfs.keys())

    list_of_downtime = []
    for device_name in devices_list:
        ping_values = dict_of_dfs[device_name]["value"].astype("float").to_numpy()
        time_diff = np.diff(dict_of_dfs[device_name].index).astype(float) / 1e9
        indexes_of_downtime = np.where(ping_values[:-1] >= MAX_PING)
        list_of_downtime.append(np.sum(time_diff[indexes_of_downtime[0]-1]))
    return list_of_downtime
