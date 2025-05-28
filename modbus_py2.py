#!/usr/bin/env python
import sys
import time
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from modbus_tk import modbus_rtu
import serial
logger = modbus_tk.utils.create_logger("console")
if __name__ == "__main__":
    serverSlave = ''
    portSlave = 0
    param = []
    reg = []
    startAdr = []
    rangeAdr = []
    setFrom = []
    setRange = []
    rtuAddress = []
    units = 0
    try:
        count = 0
        param = []
        i = 0
        for _ in range(256):
            param.append(i)
            reg.append(i)
            startAdr.append(i)
            rangeAdr.append(i)
            setFrom.append(i)
            setRange.append(i)
            rtuAddress.append(i)
            i = i + 1
        with open('/home/pi/Desktop/DMSv1.2/setting.cfg') as f:
            for line in f:
                param[count] = line.split(';')
                if(param[count][0] == 'server'):
                    serverSlave = param[count][1]
                    portSlave = param[count][2]
                if(param[count][0] == 'cport'):
                    serialPort = param[count][1]
                if(param[count][0] == 'rtu'):
                    rtuAddress[count] = param[count][1]
                    reg[count] = param[count][2]
                    startAdr[count] = param[count][3]
                    rangeAdr[count] = param[count][4]
                    setFrom[count] = param[count][5]
                    setRange[count] = param[count][6]
                    count = count + 1
                    units = count
            server = modbus_tcp.TcpServer(
                address=serverSlave, port=int(portSlave))
            server.start()
            slave = server.add_slave(1)
            slave.add_block('0', cst.COILS, 0, 1000)
            slave.add_block('1', cst.DISCRETE_INPUTS, 0, 1000)
            slave.add_block('2', cst.ANALOG_INPUTS, 0, 1000)
            slave.add_block('3', cst.HOLDING_REGISTERS, 0, 1000)
            f.close()
            serialPort = serial.Serial(
                port=serialPort, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
            master = modbus_rtu.RtuMaster(serialPort)
            master.set_timeout(1.0)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    try:
        print 'Starting server...'
        while True:
            i = 0
            for i in range(units):
                if(reg[i] == 'READ_INPUT_REGISTERS'):
                    dataRIR = []
                    for c in range(0, int(rangeAdr[i])):
                        dataRIR.append(c)
                        c += 1
                    try:
                        dataRIR = master.execute(int(rtuAddress[i]), cst.READ_INPUT_REGISTERS, int(
                            startAdr[i]), int(rangeAdr[i]))
                        slave.set_values('2', int(setFrom[i]), dataRIR)
                        serialPort.flushInput()
                        serialPort.flushOutput()
                        serialPort.flush()
                        print 'rtu', rtuAddress[i], 'READ_INPUT_REGISTERS', dataRIR
                    except:
                        for c in range(0, int(rangeAdr[i])):
                            dataRIR[c] = 0
                            c += 1
                        print 'rtu', rtuAddress[i], 'READ_INPUT_REGISTERS', 'Fail to connect', dataRIR
                        slave.set_values('2', int(setFrom[i]), dataRIR)
                if(reg[i] == 'READ_DISCRETE_INPUTS'):
                    dataRDI = []
                    for c in range(0, int(rangeAdr[i])):
                        dataRDI.append(c)
                        c += 1
                    try:
                        dataRDI = master.execute(int(rtuAddress[i]), cst.READ_DISCRETE_INPUTS, int(
                            startAdr[i]), int(rangeAdr[i]))
                        slave.set_values('1', int(setFrom[i]), dataRDI)
                        serialPort.flushInput()
                        serialPort.flushOutput()
                        serialPort.flush()
                        print 'rtu', rtuAddress[i], 'READ_DISCRETE_INPUTS', dataRDI
                    except:
                        for c in range(0, int(rangeAdr[i])):
                            dataRDI[c] = 0
                            c += 1
                        print 'rtu', rtuAddress[i], 'READ_DISCRETE_INPUTS', 'Fail to connect', dataRDI, len(
                            dataRDI)
                        slave.set_values('1', int(setFrom[i]), dataRDI)
                if(reg[i] == 'READ_COILS'):
                    dataRC = []
                    for c in range(0, int(rangeAdr[i])):
                        dataRC.append(c)
                        c += 1
                    try:
                        dataRC = master.execute(int(rtuAddress[i]), cst.READ_COILS, int(
                            startAdr[i]), int(rangeAdr[i]))
                        slave.set_values('0', int(setFrom[i]), dataRC)
                        serialPort.flushInput()
                        serialPort.flushOutput()
                        serialPort.flush()
                        print 'rtu', rtuAddress[i], 'READ_COILS', dataRC
                    except:
                        for c in range(0, int(rangeAdr[i])):
                            dataRC[c] = 0
                            c += 1
                        slave.set_values('0', int(setFrom[i]), dataRC)
                        print 'rtu', rtuAddress[i], 'READ_COILS', 'Fail to connect', dataRC
                if(reg[i] == 'READ_HOLDING_REGISTERS'):
                    dataRHR = []
                    for c in range(0, int(rangeAdr[i])):
                        dataRHR.append(c)
                        c += 1
                    try:
                        dataRHR = master.execute(int(rtuAddress[i]), cst.READ_HOLDING_REGISTERS, int(
                            startAdr[i]), int(rangeAdr[i]))
                        slave.set_values('3', int(setFrom[i]), dataRHR)
                        serialPort.flushInput()
                        serialPort.flushOutput()
                        serialPort.flush()
                        print 'rtu', rtuAddress[i], 'READ_HOLDING_REGISTERS', dataRHR
                    except:
                        for c in range(0, int(rangeAdr[i])):
                            dataRHR[c] = 0
                            c += 1
                        slave.set_values('3', int(setFrom[i]), dataRHR)
                        print 'rtu ', rtuAddress[i], 'READ_HOLDING_REGISTERS', 'Fail to connect', dataRHR
            time.sleep(0.1)
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
