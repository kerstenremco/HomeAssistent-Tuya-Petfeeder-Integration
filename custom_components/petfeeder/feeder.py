import tinytuya
import asyncio
import base64


class Feeder:
    def __init__(self, name: str, device_id: str, local_key: str, host: str | None, api_key: str | None, api_secret: str | None, region: str | None):
        self.name: str = name
        self.device_id: str = device_id
        self.local_key: str = local_key
        self.host: str | None = host
        self.api_key: str | None = api_key
        self.api_secret: str | None = api_secret
        self.region: str | None = region
        self.device = tinytuya.Device(device_id, host, local_key, version=3.3,
                                      connection_timeout=1, connection_retry_delay=0.5, connection_retry_limit=3)

    def get_light_status(self) -> bool:
        status = self.device.status()
        return status['dps'].get('19', False)

    async def async_get_led_status(self) -> bool:
        result = await asyncio.get_running_loop().run_in_executor(None, self.get_light_status)
        return result

    def toggle_light(self, turn_on: bool) -> bool:
        result = self.device.set_value(19, turn_on)
        return 'dps' in result

    async def async_toggle_light(self, turn_on: bool) -> bool:
        result = await asyncio.get_running_loop().run_in_executor(None, self.toggle_light, turn_on)
        return result

    def feed_portion(self, portions) -> bool:
        result = self.device.set_value(3, portions)
        return 'dps' in result

    async def async_feed_portion(self, portions) -> bool:
        result = await asyncio.get_running_loop().run_in_executor(None, self.feed_portion, portions)
        return result

    def check_local_connection(self):
        self.device = tinytuya.Device(self.device_id, self.host, self.local_key, connection_timeout=1, version=3.3,
                                      connection_retry_delay=0.5, connection_retry_limit=3)
        status = self.device.status()
        return status

    async def async_check_local_connection(self):
        result = await asyncio.get_running_loop().run_in_executor(None, self.check_local_connection)
        if 'Error' in result:
            raise Exception(result['Error'])

    def check_cloud_connection(self):
        c = tinytuya.Cloud(self.region, self.api_key,
                           self.api_secret, self.device_id)
        result = c.getdevices()
        return result

    async def async_check_cloud_connection(self):
        result = await asyncio.get_running_loop().run_in_executor(None, self.check_cloud_connection)
        if 'Error' in result:
            raise Exception(result['Error'])

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
