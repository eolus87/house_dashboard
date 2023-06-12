__author__ = "Nicolas Gutierrez"

# Standard libraries
import asyncio
import time
# Third party libraries
from pythonping import ping
import kasa

# Custom libraries
from control.control_functions import switch_on_function, switch_off_function

# User variables
plug_ip = "192.168.0.49"

# The general command does not seem to work
found_devices = asyncio.run(kasa.Discover.discover())
print("Devices found")
print(found_devices)

# Specifying an IP does work
found_devices = asyncio.run(kasa.Discover.discover(target=plug_ip))
print("Devices found specifying target:")
print(found_devices)


#

# async def turn_on_off():
#     plug = kasa.SmartPlug(plug_ip)
#     await plug.update()
#     print(plug.alias)
#     print(f"Current consumption: {await plug.current_consumption()} W")
#     print("Turning Off")
#     await plug.turn_off()
#     time.sleep(10)
#     print("Turning On")
#     await plug.turn_on()
#     time.sleep(5)
#     await plug.update()
#     print(f"Current consumption: {await plug.current_consumption()} W")
#     time.sleep(10)
#     print("Turning Off")
#     await plug.turn_off()
#
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(turn_on_off())

print(switch_on_function(plug_ip))
time.sleep(10)
print(switch_off_function(plug_ip))