__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Dict, List
# Third party libraries
import pandas as pd
import numpy as np
# Custom libraries
from labourers.leader import Leader
from network_classes.devicetype import DeviceType


class PingDataExtractor:
    def __init__(self, config: Dict, ping_manager: Leader) -> None:
        self.__config = config
        self.__ping_manager = ping_manager

        self.__ping_availability_threshold = 1000

    def retrieve_ping_data(self, device_type: DeviceType) -> pd.DataFrame:
        devices_of_device_type = self.__list_device_type(device_type)
        ping_data_df = self.__ping_manager.target_deque[devices_of_device_type]
        return ping_data_df

    def retrieve_ping_stats(self, device_type: DeviceType, length: int) -> pd.DataFrame:
        df = self.retrieve_ping_data(device_type)
        devices_list = df.columns.to_list()
        mean_list = np.round(df.tail(length).mean()).to_list()
        std_list = np.round(df.tail(length).std()).to_list()
        available = []
        for x in mean_list:
            if x > self.__ping_availability_threshold:
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
        list_of_devices = self.__config["devices"].keys()
        for device in list_of_devices:
            if self.__config["devices"][device]["type"] == device_type:
                list_of_device_type.append(device)
        return list_of_device_type
