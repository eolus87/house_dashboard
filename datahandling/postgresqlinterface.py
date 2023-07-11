__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import List, Union
# Third Party libraries
import psycopg2
import psycopg2.extensions
import pandas as pd
# Custom libraries
from datahandling.abcdbinterface import ABCDBInterface

db_query_time = (
    """
    SELECT time_stamp, target, value FROM (
        SELECT time_stamp, target, value, ROW_NUMBER() OVER (ORDER BY time_stamp::timestamp ASC)
        FROM {table_name}
        WHERE type = '{group_name}'
        AND target IN {target} 
        AND time_stamp::timestamp >= (LOCALTIMESTAMP - interval '{hours_to_query} hour')
    ) x WHERE mod(ROW_NUMBER, {downsample_value}) = 0
    """
)


class PostGreSqlInterface(ABCDBInterface):
    def __init__(self, db_config: dict) -> None:
        self.__db_ip = db_config["ip"]
        self.__db_port = db_config["port"]
        self.__db_user = db_config["user"]
        self.__db_password = db_config["password"]
        self.__db_table_name = db_config["table_name"]

    def query_sensor_data_latest_hours(
            self,
            group_name: str,
            list_of_targets: List[str],
            hours_to_query: float,
            downsample_value: int = 1
    ) -> pd.DataFrame:
        # Query filling
        query = db_query_time.format(
            table_name=self.__db_table_name,
            group_name=group_name,
            target=tuple(list_of_targets).__str__().replace(",)", ")"),
            hours_to_query=hours_to_query,
            downsample_value=downsample_value
        )

        records = self._query(query)

        records_df = pd.DataFrame(records, columns=["time", "target", "value"])
        records_df.set_index("time", inplace=True)

        return records_df

    def _connect(self) -> psycopg2.extensions.connection:
        conn = psycopg2.connect(
            host=self.__db_ip,
            port=self.__db_port,
            user=self.__db_user,
            password=self.__db_password)
        return conn

    @staticmethod
    def _disconnect(conn: psycopg2.extensions.connection) -> None:
        conn.close()

    @staticmethod
    def __cursor_instantiation(conn: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
        cur = conn.cursor()
        return cur

    @staticmethod
    def __cursor_close(cur: psycopg2.extensions.cursor) -> None:
        cur.close()

    def _query(self, query: str) -> Union[List, None]:
        # Connection and cursor
        conn = self._connect()
        cur = self.__cursor_instantiation(conn)

        # Query execution
        try:
            cur.execute(query)
            records = cur.fetchall()
        except Exception as inst:
            print(f"Query to PostGreSQL db {self.__db_ip}:{self.__db_port} failed with error: {inst}")
            records = None

        # Closing cursor and connection
        self.__cursor_close(cur)
        self._disconnect(conn)

        return records
