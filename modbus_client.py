import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
# initialize a serial RTU client instance
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
import time
import os

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


client = ModbusClient(method="rtu", port="/dev/ttyUSB0",
                      stopbits=1, bytesize=8, parity='N', baudrate=19200)
# connect to the serial modbus server
connection = client.connect()
message = 'hello'
print(message)
print(connection)
# Starting add, num of reg to read, slave unit.
# def hello():
while True:
    address = 40065
    value = 5
    result = client.write_register(0x0000, 0x01, unit=0x01)

    print(result)
    time.sleep(2)

client.close()
