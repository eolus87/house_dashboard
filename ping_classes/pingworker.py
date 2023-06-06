__author__ = "Nicolas Gutierrez"

# Standard libraries
import time
from collections import deque
from threading import Thread
# Third party libraries
from pythonping import ping
import numpy as np
# Custom libraries


class PingWorker(Thread):
    def __init__(self, target_info: dict, target_deque: deque) -> None:
        self.__target_info = target_info
        self.__target_deque = target_deque
        self.__keep_pinging = False
        super().__init__()

    def run(self) -> None:
        self.__keep_pinging = True
        while self.__keep_pinging:
            initial_time = time.time()

            response = ping(self.__target_info["ip"], count=1, verbose=False)
            self.__target_deque.popleft()
            self.__target_deque.append(response.rtt_avg_ms)

            final_time = time.time()
            sleeping_time = self.__target_info["rate"] - (final_time-initial_time)
            sleeping_time = float(np.clip(sleeping_time, a_min=0, a_max=None))

            time.sleep(sleeping_time)

    def join(self, timeout=None) -> None:
        self.__stop()
        super().join(timeout)

    def __stop(self) -> None:
        self.__keep_pinging = False
        time.sleep(1)

    @property
    def target_deque(self) -> deque:
        return self.__target_deque
