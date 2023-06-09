__author__ = "Nicolas Gutierrez"

# Standard libraries
import time
import asyncio
from typing import Tuple
# Third party libraries
import kasa
# Custom libraries

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def switch_on(target: str) -> bool:
    plug = kasa.SmartPlug(target)
    await plug.turn_on()

    time.sleep(0.1)

    await plug.update()
    is_successful = plug.is_on
    del plug
    return is_successful


def switch_on_function(target: str) -> bool:
    is_successful = asyncio.run(switch_on(target))
    return is_successful


async def switch_off(target: str) -> bool:
    plug = kasa.SmartPlug(target)
    await plug.turn_off()

    time.sleep(0.1)

    await plug.update()
    is_successful = plug.is_off
    del plug
    return is_successful


def switch_off_function(target: str) -> bool:
    is_successful = asyncio.run(switch_off(target))
    return is_successful
