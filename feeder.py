import tinytuya
import asyncio

d = tinytuya.Device('x', '10.0.0.0',
                    'x', version=3.3)


def turn_on_light():
    asyncio.get_running_loop().run_in_executor(None, d.set_value, 19, True, True)


def turn_off_light():
    asyncio.get_running_loop().run_in_executor(None, d.set_value, 19, False, True)


def feed_portion(potions):
    asyncio.get_running_loop().run_in_executor(None, d.set_value, 3, potions, True)
