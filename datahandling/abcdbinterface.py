__author__ = "Nicolas Gutierrez"

# Standard libraries
from abc import ABC, abstractmethod
# Third party libraries
# Custom libraries


class ABCDBInterface(ABC):
    @abstractmethod
    def query_sensor_data_latest_hours(self, group_name, list_of_targets, hours_to_query):
        pass

    @abstractmethod
    def _connect(self):
        pass

    @staticmethod
    @abstractmethod
    def _disconnect(conn) -> None:
        pass

    @abstractmethod
    def _query(self, query):
        pass
