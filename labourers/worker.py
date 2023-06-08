__author__ = "Nicolas Gutierrez"

# Standard libraries
from typing import Callable
import time
from collections import deque
from threading import Thread
# Third party libraries
import numpy as np
# Custom libraries


class Worker(Thread):
    def __init__(self, target_address: str, rate: float, work_function: Callable, target_deque: deque) -> None:
        self.__target_address = target_address
        self.__period = 1/rate
        self.__work_function = work_function
        self.__target_deque = target_deque

        self.__keep_working = False
        super().__init__()

    def run(self) -> None:
        self.__keep_working = True
        while self.__keep_working:
            initial_time = time.time()

            result, _ = self.__work_function(self.__target_address)
            self.__target_deque.popleft()
            self.__target_deque.append(result)

            final_time = time.time()
            sleeping_time = self.__period - (final_time-initial_time)
            sleeping_time = float(np.clip(sleeping_time, a_min=0, a_max=None))

            time.sleep(sleeping_time)

    def join(self, timeout=None) -> None:
        self.__stop()
        super().join(timeout)

    def __stop(self) -> None:
        self.__keep_working = False
        time.sleep(1)

    @property
    def target_deque(self) -> deque:
        return self.__target_deque
