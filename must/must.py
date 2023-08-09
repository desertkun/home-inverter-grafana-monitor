import minimalmodbus
from influxdb import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import time

scc = minimalmodbus.Instrument('/dev/ttyUSB0', 4)
scc.serial.baudrate = 19200
scc.serial.timeout = 0.5


client = InfluxDBClient("influxdb", 8086, "root", "root", "ups")
probed = 0

soc = scc.read_registers(25200, 75)

batVolts = soc[5] / 10.0
inputVolts = soc[7] // 10
batAmps = soc[74]
if batAmps > 32768:
    batAmps = batAmps - 65536
batCharge = 0
discharge = soc[54]
loadPercent = soc[16]
outputVA = soc[19]
outputW = soc[15]
tempInt = soc[33]
state = soc[1]

states = {
    0: "PowerOn",
    1: "SelfTest",
    2: "OffGrid",
    3: "GridTie",
    4: "ByPass",
    5: "Stop",
    6: "GridCharging"
}

json_body = [
    {
        "measurement": "logs",
        "tags": {
            "host": "monitor",
            "state": states[state]
        },
        "fields": {
            "bat_volts": batVolts,
            "bat_amps": batAmps,
            "soc": batCharge,
            "ac": inputVolts,
            "load_percent": loadPercent,
            "output_va": outputVA,
            "output_w": outputW,
            "temp": tempInt,
            "discharge": discharge
        }
    }
]

print(json_body)

client.write_points(json_body)
