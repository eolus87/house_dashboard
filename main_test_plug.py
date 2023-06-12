
import asyncio
import time
from kasadevices.kasaplug import KasaPlug
from power.power_function import power_function
import kasa

plug = KasaPlug("192.168.0.49")

while True:
    time.sleep(2)
    power, unit = power_function("192.168.0.49")
    print(f"{time.time()} the Power in the plug is {power} {unit}")


# async def get_plug():
#     plug = kasa.SmartPlug("192.168.0.49")
#     return plug
#
#
# async def set_plug():
#     res = get_plug()
#     bulb = await res
#     await bulb.update()
#     assert bulb.is_bulb
#
#
# if __name__ == '__main__':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(set_plug())
