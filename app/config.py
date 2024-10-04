import struct
from datetime import datetime

from pydantic import BaseModel


class SensorConfig(BaseModel):
    mac: str
    name: str
    graph_colour: str


class SensorReading(BaseModel):
    temperature: float
    humidity: int
    battery: int
    date_recorded: datetime
    mac: str

    def __str__(self) -> str:
        return f"Sensor Reading {self.mac} at {self.temperature}C with {self.humidity}% humdity and {self.battery}% battery"

    @staticmethod
    def from_adv_payload(payload: bytes) -> "SensorReading":
        # We expect an advertising message payload of
        # <48 bits of Mac address><16 bit unsigned int - current temperature x 10><8 bit unsigned int - humidity %><8 bit unsigned int - battery of %>
        mac = ":".join("%02x" % struct.unpack("B", bytes([x]))[0] for x in payload[0:6]).upper()

        return SensorReading(
            temperature=int.from_bytes(payload[6:8]) / 10,
            humidity=payload[8],
            battery=payload[9],
            date_recorded=datetime.now(),
            mac=mac,
        )
