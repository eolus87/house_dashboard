__author__ = "Nicolas Gutierrez"

# Standard libraries
import unittest
from collections import deque
import time
import copy
# Third party libraries
# Custom libraries
from labourers.worker import Worker


class TestPingWorker(unittest.TestCase):
    def setUp(self) -> None:
        self.target_info = {"ip": "127.0.0.1", "rate": 0.1}
        self.buffer_size = 100
        self.zero_deque = deque([0]*self.buffer_size)
        self.target_deque = copy.deepcopy(self.zero_deque)
        self.pinger_worker = Worker(self.target_info, self.target_deque)

    def test_initialization(self) -> None:
        # ARRANGE
        # ACT
        # ASSERT
        self.assertEqual(self.pinger_worker._PingWorker__target_info, self.target_info)
        self.assertEqual(self.pinger_worker._PingWorker__target_deque, self.target_deque)
        self.assertEqual(self.pinger_worker._PingWorker__keep_pinging, False)

    def test_start_modifies_the_values_of_the_deque(self) -> None:
        # ARRANGE
        # ACT
        self.pinger_worker.start()
        time.sleep(3*self.target_info["rate"])
        self.pinger_worker.join()
        # ASSERT
        self.assertGreater(sum(self.pinger_worker.target_deque), sum(self.zero_deque))


if __name__ == '__main__':
    unittest.main()
