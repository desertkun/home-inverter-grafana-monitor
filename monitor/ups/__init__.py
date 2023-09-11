import minimalmodbus
from dataclasses import dataclass


@dataclass
class Sample(object):
    bat_volts: int
    bat_amps: int
    soc: int
    ac: int
    load_percent: int
    output_va: int
    output_w: int
    temp: int
    discharge: int
    state: str


class UPS(object):
    def __init__(self, device_path: str, device_id: int, baud_rate: int):
        self.device_path = device_path
        self.device_id = device_id
        self.baud_rate = baud_rate

        self.scc = minimalmodbus.Instrument(device_path, device_id)
        self.scc.serial.baudrate = baud_rate
        self.scc.serial.timeout = 0.5

    def sample(self) -> Sample:
        pass
