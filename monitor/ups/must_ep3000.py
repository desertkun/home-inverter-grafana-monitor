
from . import Sample, UPS
import os


class MustEP3000(UPS):
    SELF_CHECK = 0
    BACKUP = 1
    LINE = 2
    STOP = 3
    DEBUG = 4
    SOFT_START = 5
    POWER_OFF = 6
    STANDBY = 7

    def __init__(self, device_path: str):
        super().__init__(device_path, 10, 9600)

    def sample(self) -> Sample:

        states = {
            MustEP3000.STANDBY: "PowerOn",
            MustEP3000.SELF_CHECK: "SelfTest",
            MustEP3000.BACKUP: "OffGrid",
            MustEP3000.STOP: "Stop",
            MustEP3000.DEBUG: "Debug",
            MustEP3000.SOFT_START: "SoftStart",
            MustEP3000.LINE: "GridCharging",
            MustEP3000.POWER_OFF: "PowerOff",
        }

        soc = self.scc.read_registers(30000, 25)

        batVolts = soc[14] / 10.0
        inputVolts = soc[5] // 10
        batAmps = soc[15]
        if batAmps > 32768:
            batAmps = batAmps - 65536
        batAmps //= 10
        batCharge = 0

        loadPercent = soc[12]
        outputVA = soc[7] / 10
        outputW = float(soc[10])
        tempInt = soc[18]
        state = states[soc[2]]

        if os.path.isfile("/var/run/discharge"):
            with open("/var/run/discharge", "r") as f:
                discharge = float(f.read())
        else:
            discharge = 0

        # accumulate wattage per minute
        discharge += outputW / 60.

        with open("/var/run/discharge", "w") as f:
            f.write(str(discharge))

        return Sample(
            batVolts,
            batAmps,
            batCharge,
            inputVolts,
            loadPercent,
            outputVA,
            outputW,
            tempInt,
            int(discharge // 100),
            state)
