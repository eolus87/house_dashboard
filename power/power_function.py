__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
import asyncio
from typing import Tuple
# Third party libraries
import kasa
# Custom libraries

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def power_request(target: str) -> Tuple[float, str]:
    plug = kasa.SmartPlug(target)
    try:
        await plug.update()
        power = await plug.current_consumption()
    except Exception as inst:
        print(f"Power request function failed with error: {inst}")
        power = -1
    del plug
    return power, "W"


def power_function(target: str) -> Tuple[float, str]:
    power, unit = asyncio.run(power_request(target))
    return power, unit