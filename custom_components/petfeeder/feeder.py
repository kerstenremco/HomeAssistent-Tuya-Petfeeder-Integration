import tinytuya
import asyncio
import base64


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

    def _decode_plan(self):
        # TODO: implement fetching, https://community.home-assistant.io/t/pet-feeder-entities/454077/60
        raw = base64.b64decode()

        # Feeding plan = 6 groups × 5 bytes = 30 bytes
        plans = []
        for i in range(0, len(raw), 5):
            group = raw[i:i+5]
            if len(group) < 5:
                continue

            day, hour, minute, servings, switch = group

            # Skip empty (zero-filled) groups
            if all(v == 0 for v in group):
                continue

            days_bin = f"{day:07b}"
            days = []
            week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for j, w in enumerate(week):
                if days_bin[j] == "1":
                    days.append(w)

            plans.append({
                "days": days,
                "time": f"{hour:02d}:{minute:02d}",
                "servings": servings,
                "enabled": (switch == 1)
            })

        return plans
