import tinytuya
import asyncio
import json


class Feeder:
    def __init__(self, name: str, host: str, device_id: str, local_key: str):
        self.name = name
        self.device = tinytuya.Device(device_id, host, local_key, version=3.3)
        self.device.set_socketRetryDelay(0.5)
        self.device.set_socketRetryLimit(3)
        self.device.set_socketTimeout(1)

    async def turn_on_light(self) -> bool:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.device.set_value, 19, True)
        return 'dps' in result

    async def turn_off_light(self) -> bool:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, self.device.set_value, 19, False)
        return 'dps' in result

    async def feed_portion(self, portions) -> bool:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.device.set_value, 3, portions)
        return 'dps' in result

    async def check_connection(self) -> bool:
        loop = asyncio.get_running_loop()
        status = await loop.run_in_executor(None, self.device.status)
        return 'dps' in status
