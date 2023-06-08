__author__ = "Nicolas Gutierrez"

# Standard libraries
import threading
from collections import deque
import pandas as pd
from typing import Dict, List, Callable
# Third party libraries
# Custom libraries
from labourers.worker import Worker


class Leader:
    def __init__(self, leader_config: Dict, work_function: Callable) -> None:
        self.__target_deque = self.__deque_instantiation(leader_config)
        self.__workers = self.__workers_instantiation(leader_config, self.__target_deque, work_function)
        self.started_event = threading.Event()

    @staticmethod
    def __deque_instantiation(config: Dict) -> Dict:
        target_deque = dict()
        for target_key in config["devices"].keys():
            target_deque[target_key] = deque([0] * config["buffer_size"])
        return target_deque

    @staticmethod
    def __workers_instantiation(config: Dict, target_deque: Dict, work_function: Callable) -> List[Worker]:
        list_of_threads = []
        for target_key in config["devices"].keys():
            list_of_threads.append(
                Worker(
                    config["devices"][target_key]["address"],
                    config["devices"][target_key]["rate"],
                    work_function,
                    target_deque[target_key]
                )
            )
        return list_of_threads

    def start(self) -> None:
        for worker in self.__workers:
            worker.start()
        self.started_event.set()

    def stop(self) -> None:
        if self.started_event.is_set():
            for worker in self.__workers:
                worker.join()
        else:
            raise Exception("Threads have not been started yet")

    @property
    def target_deque(self) -> pd.DataFrame:
        return pd.DataFrame(self.__target_deque)
