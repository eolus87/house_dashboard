__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Union, List
# Third party libraries
import pandas as pd
import numpy as np
# Custom libraries
from utilities.utilities import load_conf
from ping_classes.pingmanager import PingManager
from ping_classes.devicetype import DeviceType


class PingDataExtractor:
    def __init__(self, config_file: Union[str, dict], ping_manager: PingManager) -> None:
        self.config = load_conf(config_file)
        self.ping_manager = ping_manager

    def retrieve_ping_data(self, device_type: DeviceType) -> pd.DataFrame:
        devices_of_device_type = self.__list_device_type(device_type)
        ping_data_df = self.ping_manager.target_deque[devices_of_device_type]
        return ping_data_df

    def retrieve_ping_stats(self, device_type: DeviceType, length: int) -> pd.DataFrame:
        df = self.retrieve_ping_data(device_type)
        devices_list = df.columns.to_list()
        mean_list = np.round(df.tail(length).mean()).to_list()
        std_list = np.round(df.tail(length).std()).to_list()
        available = []
        for x in mean_list:
            if x > 1000:
                available.append(False)
            else:
                available.append(True)

        data_as_dict = {"Device": devices_list,
                        "Mean [ms]": mean_list,
                        "Std [ms]": std_list,
                        "Available": available}
        data_as_pd = pd.DataFrame(data_as_dict)

        return data_as_pd

    def __list_device_type(self, device_type: DeviceType) -> List[str]:
        list_of_device_type = []
        list_of_devices = self.config["pinger"]["devices_to_ping"].keys()
        for device in list_of_devices:
            if self.config["pinger"]["devices_to_ping"][device]["type"] == device_type:
                list_of_device_type.append(device)
        return list_of_device_type
