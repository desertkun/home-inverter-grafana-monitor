import minimalmodbus
import sys

device_id = int(sys.argv[1])
baud_rate = int(sys.argv[2])
registers_from = int(sys.argv[3])
registers_to = int(sys.argv[4])

SERPORT = '/dev/ttyUSB0'
SERTIMEOUT = 0.5
SERBAUD = baud_rate

i = minimalmodbus.Instrument(SERPORT, device_id)
i.serial.timeout= SERTIMEOUT
i.serial.baudrate = SERBAUD

results = i.read_registers(registers_from, registers_to - registers_from)
for i, v in enumerate(results):
    print("{0} = {1}".format(i + registers_from, v))
