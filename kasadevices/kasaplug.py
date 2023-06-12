__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
import platform
import asyncio
from threading import Lock
# Third party libraries
import kasa
# Custom libraries


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class KasaPlug:
    def __init__(self, ip_address: str) -> None:
        self.device_lock = Lock()

        self.ip_address = ip_address
        self.plug_object = kasa.SmartPlug(ip_address)
        asyncio.run(self.__device_update())

    async def __device_update(self):
        await self.plug_object.update()

    async def __power_function(self):
        self.device_lock.acquire()
        try:
            power = self.plug_object.emeter_realtime
        except Exception as inst:
            print(f"\tError while requesting power from device {inst}")
            power = -1
        self.device_lock.release()
        return power, "W"

    def power_request(self):
        power, unit = asyncio.run(self.__power_function())
        return power, unit
