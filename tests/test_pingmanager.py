__author__ = "Nicolas Gutierrez"

# Standard libraries
import unittest
import time

import pandas as pd

# Third party libraries
# Custom libraries
from ping_classes.pingmanager import PingManager


class TestPingManager(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {"pinger":
            {"devices_to_ping": {
                "localhost": {"ip": "127.0.0.1", "rate": 0.1},
                "local_host": {"ip": "127.0.0.1", "rate": 0.1}},
                "buffer_size": 10}}
        self.ping_manager = PingManager(self.config)

    def test_load_conf(self) -> None:
        # ARRANGE
        # ACT
        config_loaded = self.ping_manager._PingManager__load_conf(self.config)
        # ASSERT
        self.assertEqual(self.config, config_loaded)  # add assertion here

    def test_deque_instantiation(self) -> None:
        # ARRANGE
        # ACT
        target_deques = self.ping_manager._PingManager__ping_deque_instantiation(self.config)
        # ASSERT
        self.assertEqual(len(target_deques), len(self.config["pinger"]["devices_to_ping"]))

    def test_ping_manager_returns_a_data_frame_with_pings(self) -> None:
        # ARRANGE
        # ACT
        self.ping_manager.start()
        time.sleep(0.5)
        self.ping_manager.stop()
        # ASSERT
        self.assertIsInstance(self.ping_manager.target_deque, pd.DataFrame)

    def test_ping_manager_returns_a_data_frame_with_the_correct_size(self) -> None:
        # ARRANGE
        # ACT
        self.ping_manager.start()
        time.sleep(0.5)
        self.ping_manager.stop()
        # ASSERT
        self.assertEqual(self.ping_manager.target_deque.shape[0], self.config["pinger"]["buffer_size"])
        self.assertEqual(self.ping_manager.target_deque.shape[1], len(self.config["pinger"]["devices_to_ping"]))


if __name__ == '__main__':
    unittest.main()
