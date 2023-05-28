__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
import threading
from collections import deque
import pandas as pd
from typing import Dict, List, Union
# Third party libraries
import yaml
# Custom libraries
from ping_classes.pingworker import PingWorker


class PingManager:
    def __init__(self, config_file: Union[str, dict]) -> None:
        config = self.__load_conf(config_file)
        self.__target_deque = self.__ping_deque_instantiation(config)
        self.__ping_workers = self.__ping_workers_instantiation(config, self.__target_deque)
        self.started_event = threading.Event()

    @staticmethod
    def __load_conf(config_file: Union[str, dict]) -> dict:
        if isinstance(config_file, str):
            with open(os.path.join("config", config_file), "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        elif isinstance(config_file, dict):
            config = config_file
        else:
            raise TypeError("Config file should be a path to a yaml config or a dictionary.")
        return config

    @staticmethod
    def __ping_deque_instantiation(config: dict) -> dict:
        target_deque = dict()
        for target_key in config["pinger"]["devices_to_ping"].keys():
            target_deque[target_key] = deque([0]*config["pinger"]["buffer_size"])
        return target_deque

    @staticmethod
    def __ping_workers_instantiation(config: dict, target_deque: Dict) -> List[PingWorker]:
        list_of_threads = []
        for target_key in config["pinger"]["devices_to_ping"].keys():
            list_of_threads.append(
                PingWorker(config["pinger"]["devices_to_ping"][target_key], target_deque[target_key])
            )
        return list_of_threads

    def start(self) -> None:
        for pingworker in self.__ping_workers:
            pingworker.start()
        self.started_event.set()

    def stop(self) -> None:
        if self.started_event.is_set():
            for pingworker in self.__ping_workers:
                pingworker.join()
        else:
            raise Exception("Threads have not been started yet")

    @property
    def target_deque(self) -> pd.DataFrame:
        return pd.DataFrame(self.__target_deque)
