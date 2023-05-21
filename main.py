__author__ = "Nicolas Gutierrez"

# Standard libraries
import asyncio
import time
# Third party libraries
from pythonping import ping
import kasa

# Custom libraries

# User variables
plug_ip = "X.X.X.X"

response = ping('8.8.8.8', count=1, verbose=True)

# The general command does not seem to work
found_devices = asyncio.run(kasa.Discover.discover())
print("Devices found")
print(found_devices)

# Specifying an IP does work
found_devices = asyncio.run(kasa.Discover.discover(target=plug_ip))
print("Devices found specifying target:")
print(found_devices)


#

async def turn_on_off():
    plug = kasa.SmartPlug(plug_ip)
    await plug.update()
    print(plug.alias)
    print("Turning Off")
    await plug.turn_off()
    time.sleep(10)
    print("Turning On")
    await plug.turn_on()
    time.sleep(10)
    print("Turning Off")
    await plug.turn_off()


asyncio.run(turn_on_off())
