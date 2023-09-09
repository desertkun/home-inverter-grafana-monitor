import minimalmodbus
from influxdb import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import time
import os

USB_DEVICE = os.environ.get("USB_DEVICE", "/dev/ttyUSB0")

DB_HOST = os.environ.get("DB_HOST", "influxdb")
DB_PORT = int(os.environ.get("DB_PORT", "8086"))
DB_USERNAME = os.environ.get("DB_USERNAME", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "ups")
INVERTER_MODEL = os.environ.get("INVERTER_MODEL", "monitor-pv1800")

client = InfluxDBClient(DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME)

if INVERTER_MODEL == "must-pv1800":
    states = {
        0: "PowerOn",
        1: "SelfTest",
        2: "OffGrid",
        3: "GridTie",
        4: "ByPass",
        5: "Stop",
        6: "GridCharging"
    }

    scc = minimalmodbus.Instrument(USB_DEVICE, 4)
    scc.serial.baudrate = 19200
    scc.serial.timeout = 0.5

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
    state = states[soc[1]]
elif INVERTER_MODEL == "must-ep3000":

    SELF_CHECK = 0
    BACKUP = 1
    LINE = 2
    STOP = 3
    DEBUG = 4
    SOFT_START = 5
    POWER_OFF = 6
    STANDBY = 7

    states = {
        STANDBY: "PowerOn",
        SELF_CHECK: "SelfTest",
        BACKUP: "OffGrid",
        STOP: "Stop",
        DEBUG: "Debug",
        SOFT_START: "SoftStart",
        LINE: "GridCharging",
        POWER_OFF: "PowerOff",
    }

    scc = minimalmodbus.Instrument(USB_DEVICE, 10)
    scc.serial.baudrate = 9600
    scc.serial.timeout = 0.5

    soc = scc.read_registers(30000, 25)

    batVolts = soc[14] / 10.0
    inputVolts = soc[5] // 10
    batAmps = soc[15]
    if batAmps > 32768:
        batAmps = batAmps - 65536
    batAmps //= 10
    batCharge = 0
    discharge = 0
    loadPercent = soc[12]
    outputVA = soc[7] / 10
    outputW = float(soc[10])
    tempInt = soc[18]
    state = states[soc[2]]
else:
    print("Unknown model")
    exit(1)

json_body = [
    {
        "measurement": "logs",
        "tags": {
            "host": INVERTER_MODEL,
            "state": state
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
