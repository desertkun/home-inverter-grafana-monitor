import minimalmodbus
import sys

registers_from = int(sys.argv[1])
registers_to = int(sys.argv[2])

SERPORT = '/dev/ttyUSB0'
SERTIMEOUT = 0.5
SERBAUD = 19200

i = minimalmodbus.Instrument(SERPORT, 4)
i.serial.timeout= SERTIMEOUT
i.serial.baudrate = SERBAUD

results = i.read_registers(registers_from, registers_to - registers_from)
for i, v in enumerate(results):
    print("{0} = {1}".format(i + registers_from, v))
