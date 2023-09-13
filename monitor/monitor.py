
from influxdb import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

import os
from ups import UPS, must_ep3000, must_pv1800, must_ph18_5248


SUPPORTED_INVERTERS = {
    "must-pv1800": must_pv1800.MustPV1800,
    "must-ep3000": must_ep3000.MustEP3000,
    "must-ph18-5248": must_ph18_5248.MustPH185248
}

USB_DEVICE = os.environ.get("USB_DEVICE", "/dev/ttyUSB0")

DB_HOST = os.environ.get("DB_HOST", "influxdb")
DB_PORT = int(os.environ.get("DB_PORT", "8086"))
DB_USERNAME = os.environ.get("DB_USERNAME", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "ups")
INVERTER_MODEL = os.environ.get("INVERTER_MODEL", "monitor-pv1800")

client = InfluxDBClient(DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME)

if INVERTER_MODEL not in SUPPORTED_INVERTERS:
    print("Unknown inverter model model: {0}".format(INVERTER_MODEL))
    exit(1)

inverter: UPS = SUPPORTED_INVERTERS[INVERTER_MODEL](USB_DEVICE)
sample = inverter.sample()

print("Measured: {0}".format(sample))

json_body = [
    {
        "measurement": "logs",
        "tags": {
            "host": INVERTER_MODEL,
            "state": sample.state
        },
        "fields": {
            "bat_volts": sample.bat_volts,
            "bat_amps": sample.bat_amps,
            "soc": sample.soc,
            "ac": sample.ac,
            "load_percent": sample.load_percent,
            "output_va": sample.output_va,
            "output_w": sample.output_w,
            "temp": sample.temp,
            "discharge": sample.discharge
        }
    }
]

print(json_body)

client.write_points(json_body)
