import asyncio

from bleak import BleakScanner
from config import SensorReading

from data import get_configured_sensors, write_sensor_data


async def main():
    sensors = get_configured_sensors()
    devices = await BleakScanner.discover(timeout=60, return_adv=True)

    for mac in devices:
        (_, ble_advert_data) = devices[mac]
        if mac in sensors:
            r = SensorReading.from_adv_payload(next(iter(ble_advert_data.service_data.values())))
            print(r)
            write_sensor_data(r)


asyncio.run(main())
