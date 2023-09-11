import minimalmodbus
from dataclasses import dataclass


@dataclass
class Sample(object):
    # battery voltage
    bat_volts: int
    # battery amperage used
    bat_amps: int
    # battery state of charge
    soc: int
    # input ac voltage
    ac: int
    # systa load in percents
    load_percent: int
    # load voltage
    output_va: int
    # load power
    output_w: float
    # inverter temperature
    temp: int
    # accumulated used power, 100W per
    discharge: int
    # inverter state
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
