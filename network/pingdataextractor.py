__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Dict, List
# Third party libraries
import pandas as pd
import numpy as np
from psycopg2.extensions import connection
# Custom libraries
from network.devicetype import DeviceType

db_query = (
    """
    SELECT time_stamp, value FROM {table_name}
    WHERE type = 'ping' 
    and target = '{target}' 
    and time_stamp::timestamp >= 'now'::timestamp - '{hours_to_display} hour'::interval
    order by time_stamp::timestamp ASC
    """
)


class PingDataExtractor:
    def __init__(self, config: Dict, conn: connection) -> None:
        self.__db_config_name = "postgresql"
        self.__db_ip = config[self.__db_config_name]["ip"]
        self.__db_port = config[self.__db_config_name]["port"]
        self.__db_user = config[self.__db_config_name]["user"]
        self.__db_password = config[self.__db_config_name]["user"]
        self.__db_table_name = config[self.__db_config_name]["table_name"]

        self.__group_name = "network"
        self.__network_sensors = config[self.__group_name]["devices"]
        self.__display_past_hours = config[self.__group_name]["display_past_hours"]

        self.__db_connection = conn

        self.__ping_availability_threshold = 1000

    def retrieve_ping_data(self, device_type: DeviceType) -> pd.DataFrame:
        results = pd.DataFrame()
        cur = self.__db_connection.cursor()
        for device in self.__network_sensors:
            if int(self.__network_sensors[device]["type"]) == device_type:
                query = db_query.format(
                    table_name=self.__db_table_name,
                    target=self.__network_sensors[device]['address'],
                    hours_to_display=self.__display_past_hours
                )
                cur.execute(query)
                records = cur.fetchall()
                records_df = pd.DataFrame(records, columns=["Time", device])
                records_df.set_index("Time", inplace=True)
                results = results.join(records_df, how="outer")
        return results

    def retrieve_ping_stats(self, device_type: DeviceType, length: int) -> pd.DataFrame:
        network_df = self.retrieve_ping_data(device_type)
        devices_list = network_df.columns.to_list()
        mean_list = network_df.astype("float").tail(length).mean().round(0).to_numpy()
        std_list = network_df.astype("float").tail(length).std().round(0).to_numpy()
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
