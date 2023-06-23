__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Dict, List, Tuple
# Third party libraries
import pandas as pd
from psycopg2.extensions import connection
# Custom libraries

db_query_time = (
    """
    SELECT time_stamp, target, value FROM {table_name}
    WHERE type = '{group_name}'
    AND target IN {target} 
    AND time_stamp::timestamp >= 'now'::timestamp - '{hours_to_display} hour'::interval
    ORDER BY time_stamp::timestamp ASC
    """
)


class DataExtractor:
    def __init__(self, config: Dict, group_name: str, conn: connection) -> None:
        self.__db_config_name = "postgresql"
        self.__db_ip = config[self.__db_config_name]["ip"]
        self.__db_port = config[self.__db_config_name]["port"]
        self.__db_user = config[self.__db_config_name]["user"]
        self.__db_password = config[self.__db_config_name]["user"]
        self.__db_table_name = config[self.__db_config_name]["table_name"]

        self.__group_name = group_name
        self.__network_sensors = config[self.__group_name]["devices"]

        self.__db_connection = conn

        self.__ping_availability_threshold = 1000

    def retrieve_data(self, device_type: int, past_time_hours: float) -> Dict:
        # Obtaining the required targets for the Query
        devices_ip, devices_name = self.__devices_details(device_type)

        # Querying
        records = self.__query_execution(self.__db_table_name, devices_ip, past_time_hours)

        # Query operations
        dict_of_dfs = dict()
        for i in range(len(devices_ip)):
            df_per_device = records[records["target"] == devices_ip[i]].copy(deep=True)
            df_per_device.dropna(inplace=True)
            df_per_device.drop(columns=["target"], inplace=True)
            dict_of_dfs[devices_name[i]] = df_per_device
        return dict_of_dfs

    def retrieve_stats(self, device_type: int, past_time_hours: float) -> pd.DataFrame:
        # Obtaining the required targets for the Query
        dict_of_dfs = self.retrieve_data(device_type, past_time_hours)

        devices_list = list(dict_of_dfs.keys())
        mean_list = [df["value"].astype("float").mean().round(0) for df in dict_of_dfs.values()]
        std_list = [df["value"].astype("float").std().round(0) for df in dict_of_dfs.values()]
        available = []
        for x in mean_list:
            if x > self.__ping_availability_threshold:
                available.append(False)
            else:
                available.append(True)

        data_as_dict = {"Device": devices_list,
                        "Mean": mean_list,
                        "Std": std_list,
                        "Available": available}
        data_as_pd = pd.DataFrame(data_as_dict)

        return data_as_pd

    def __query_execution(self, table_name: str, devices_ip: List[str], hours_to_retrieve: float) -> pd.DataFrame:
        cur = self.__db_connection.cursor()

        query = db_query_time.format(
            table_name=table_name,
            group_name=self.__group_name,
            target=tuple(devices_ip).__str__().replace(",)", ")"),
            hours_to_display=hours_to_retrieve
        )
        cur.execute(query)
        records = cur.fetchall()

        records_df = pd.DataFrame(records, columns=["time", "target", "value"])
        records_df.set_index("time", inplace=True)

        return records_df

    def __devices_details(self, device_type: int) -> Tuple[List[str], List[str]]:
        devices_ip = []
        devices_name = []
        for device in self.__network_sensors:
            if int(self.__network_sensors[device]["type"]) == device_type:
                devices_ip.append(self.__network_sensors[device]['address'])
                devices_name.append(device)
        return devices_ip, devices_name
