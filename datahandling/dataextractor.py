__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Dict, List, Tuple
# Third party libraries
import pandas as pd
# Custom libraries
from datahandling.postgresqlinterface import PostGreSqlInterface


class DataExtractor:
    def __init__(self, sensor_type: str, devices_dict: Dict, querier: PostGreSqlInterface) -> None:
        self.__sensor_type = sensor_type
        self.__type_sensors = devices_dict["devices"]
        self.__querier = querier

    def retrieve_type_data(
            self,
            device_type: List[int],
            past_time_hours: float,
            downsample_value: int = 1
    ) -> Dict:
        # Obtaining the required targets for the Query
        devices_ip, devices_name = self.__devices_type_details(device_type)
        # Querying
        dict_of_dfs = self.__retrieve_data(
            devices_ip,
            devices_name,
            past_time_hours,
            downsample_value
        )
        return dict_of_dfs

    def retrieve_sensors_data(self, devices_name: List[str], past_time_hours: float) -> Dict:
        # Obtaining the required details of the devices name
        devices_ip = self.__devices_name_details(devices_name)
        # Querying
        dict_of_dfs = self.__retrieve_data(devices_ip, devices_name, past_time_hours)
        return dict_of_dfs

    def __devices_name_details(self, devices_name: List[str]) -> List[str]:
        devices_ip = []
        for device_name in devices_name:
            devices_ip.append(self.__type_sensors[device_name]["address"])
        return devices_ip

    def __devices_type_details(self, device_type: List[int]) -> Tuple[List[str], List[str]]:
        devices_ip = []
        devices_name = []
        for device in self.__type_sensors:
            if int(self.__type_sensors[device]["type"]) in device_type:
                devices_ip.append(self.__type_sensors[device]['address'])
                devices_name.append(device)
        return devices_ip, devices_name

    def __retrieve_data(
            self,
            devices_ip: List[str],
            devices_name: List[str],
            past_time_hours: float,
            downsamle_value: int = 1,
    ) -> Dict:
        # Querying
        try:
            records = self.__querier.query_sensor_data_latest_hours(
                self.__sensor_type,
                devices_ip,
                past_time_hours,
                downsamle_value
            )
        except Exception as inst:
            print(f"Error while querying querier: {inst}")
            records = pd.DataFrame()
        # Dividing results per sensor
        dict_of_dfs = dict()
        for i in range(len(devices_ip)):
            df_per_device = records[records["target"] == devices_ip[i]].copy(deep=True)
            df_per_device.dropna(inplace=True)
            df_per_device.drop(columns=["target"], inplace=True)
            dict_of_dfs[devices_name[i]] = df_per_device
        return dict_of_dfs
