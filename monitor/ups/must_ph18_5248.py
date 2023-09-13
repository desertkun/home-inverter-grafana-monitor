
from . import Sample, UPS


class MustPH185248(UPS):
    def __init__(self, device_path: str):
        super().__init__(device_path, 4, 19200)

    def sample(self) -> Sample:
        states = {
            0: "PowerOn",
            1: "SelfTest",
            2: "OffGrid",
            3: "GridTie",
            4: "ByPass",
            5: "Stop",
            6: "GridCharging"
        }

        # 15205: ["PV voltage", 0.1, "V"],
        # 15206: ["Battery voltage", 0.1, "V"],
        # 15207: ["Charger current", 0.1, "A"],
        # 15208: ["Charger power", 0.1, "W"],
        # 15209 : ["Radiator temperature", 1, "°C"],
        # 15210 : ["External temperature", 1, "°C"],
        # 15211: ["Battery Relay", 1, ""],
        # 15212: ["PV Relay", 1, ""],

        # 25205: ["Battery voltage", 0.1, "V"],
        # 25206: ["Inverter voltage", 0.1, "V"],
        # 25207: ["Grid voltage", 0.1, "V"],
        # 25208: ["BUS voltage", 0.1, "V"],
        # 25209: ["Control current", 0.1, "A"],
        # 25210: ["Inverter current", 0.1, "A"],
        # 25211: ["Grid current", 0.1, "A"],
        # 25212: ["Load current", 0.1, "A"],
        # 25213: ["Inverter power(P)", 1, "W"],
        # 25214: ["Grid power(P)", 1, "W"],
        # 25215: ["Load power(P)", 1, "W"],
        # 25216: ["Load percent", 1, "%"],
        # 25217: ["Inverter complex power(S)", 1, "VA"],
        # 25218: ["Grid complex power(S)", 1, "VA"],
        # 25219: ["Load complex power(S)", 1, "VA"],
        # 25221: ["Inverter reactive power(Q)", 1, "var"],
        # 25222: ["Grid reactive power(Q)", 1, "var"],
        # 25223: ["Load reactive power(Q)", 1, "var"],
        # 25225: ["Inverter frequency", 0.01, "Hz"],
        # 25226: ["Grid frequency", 0.01, "Hz"],
        # 25233: ["AC radiator temperature", 1, "°C"],
        # 25234: ["Transformer temperature", 1, "°C"],
        # 25235: ["DC radiator temperature", 1, "°C"],
        # 25237: ["Inverter relay state", 1, ""],
        # 25238: ["Grid relay state", 1, ""],
        # 25239: ["Load relay state", 1, ""],
        # 25240: ["N_Line relay state", 1, ""],
        # 25241: ["DC relay state", 1, ""],
        # 25242: ["Earth relay state", 1, ""],
        # 25245: ["Accumulated charger power high", 1, "kWh"],
        # 25246: ["Accumulated charger power low", 0.1, "kWh"],
        # 25247: ["Accumulated discharger power high", 1, "kWh"],
        # 25248: ["Accumulated discharger power low", 0.1, "kWh"],
        # 25249: ["Accumulated buy power high", 1, "kWh"],
        # 25250: ["Accumulated buy power low", 0.1, "kWh"],
        # 25251: ["Accumulated sell power high", 1, "kWh"],
        # 25252: ["Accumulated sell power low", 0.1, "kWh"],
        # 25253: ["Accumulated load power high", 1, "kWh"],
        # 25254: ["Accumulated load power low", 0.1, "kWh"],
        # 25255: ["Accumulated self_use power high", 1, "kWh"],
        # 25256: ["Accumulated self_use power low", 0.1, "kWh"],
        # 25257: ["Accumulated PV_sell power high", 1, "kWh"],
        # 25258: ["Accumulated PV_sell power low", 0.1, "kWh"],
        # 25259: ["Accumulated grid_charger power high", 1, "kWh"],
        # 25260: ["Accumulated grid_charger power low", 0.1, "kWh"],
        # 25271: ["Hardware version", 1, ""],
        # 25272: ["Software version", 1, ""],
        # 25273: ["Battery power", 1, "W"],
        # 25274: ["Battery current", 1, "A"],

        soc = self.scc.read_registers(25200, 75)
        # time.sleep(1)
        # soc2 = self.scc.read_registers(15200, 12)

        batVolts = soc[5] / 10.0
        batAmps = soc[74]
        if batAmps > 32768:
            batAmps = batAmps - 65536
            batAmps = abs(batAmps)
        else:
            batAmps = -batAmps
        batCharge = 0
        gridVoltage = soc[7] / 10
        discharge = soc[54]
        loadPercent = soc[16]
        loadPower = soc[15]
        inverterVoltage = soc[6] / 10
        transformerTemp = soc[34]
        state = states[soc[1]]

        return Sample(
                batVolts,
                batAmps,
                batCharge,
                gridVoltage,
                loadPercent,
                inverterVoltage,
                loadPower,
                transformerTemp,
                discharge,
                state)
