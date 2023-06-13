__author__ = "Nicolas Gutierrez"

# Standard libraries
import platform
import asyncio
# Third party libraries
import kasa
# Custom libraries

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def switch_on(target: str) -> bool:
    plug = kasa.SmartPlug(target)
    try:
        await plug.update()
        await asyncio.sleep(0.1)
        await plug.turn_on()
        is_successful = plug.is_on
    except Exception as inst:
        print(f"Switch on function failed with error: {inst}")
        is_successful = False
    del plug
    return is_successful


def switch_on_function(target: str) -> bool:
    is_successful = asyncio.run(switch_on(target))
    return is_successful


async def switch_off(target: str) -> bool:
    plug = kasa.SmartPlug(target)
    try:
        await plug.update()
        await asyncio.sleep(0.1)
        await plug.turn_off()
        is_successful = plug.is_off
    except Exception as inst:
        print(f"Switch off function failed with error: {inst}")
        is_successful = False
    del plug
    return is_successful


def switch_off_function(target: str) -> bool:
    is_successful = asyncio.run(switch_off(target))
    return is_successful
