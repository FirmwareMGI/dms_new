import micomp122 as micomp122
import micomp123 as micomp123
import micomp443 as micomp443
import micomp442 as micomp442
import micomp141 as micomp141
from micomp141 import serial
import time
import mysql.connector
import os
import RPi.GPIO as GPIO


# import for remote
import ser2tcp.server_manager as _server_manager
import ser2tcp.serial_proxy as _serial_proxy
import sys as _sys
import signal as _signal
import ser2tcp.serial_proxy as _serial_proxy
import ser2tcp.server_manager as _server_manager


def sigterm_handler(_signo, _stack_frame):
    """Raises SystemExit(0)"""
    _sys.exit(0)


_signal.signal(_signal.SIGTERM, sigterm_handler)
_signal.signal(_signal.SIGINT, sigterm_handler)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


GPIO.output(17, 0)
GPIO.output(27, 0)

data_old = []
data = []
buffer = ''
dbCfg5 = ['', '']

servers_manager = _server_manager.ServersManager()

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="mgi",
    database="dms"
)


def cekServer():
    global buffer

    mycursor = mydb.cursor()
    sql = "SELECT * FROM network"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb.commit()
    mycursor.close()

    for i in dbDR:
        dbCfg5[0] = i[0]
        dbCfg5[1] = i[5]

    if str(buffer) != str(dbCfg5[0]):

        print('masuk config IP')
        buffer = dbCfg5[0]
        os.system('sudo ifconfig eth0 down')
        os.system('sudo ifconfig eth0 '+str(dbCfg5[0]))
        os.system('sudo ifconfig eth0 up')
        time.sleep(10)

    response = os.system("ping -c 1 " + dbCfg5[1])
    if response == 0:
        GPIO.output(17, 1)
#         GPIO.output(27,1)
    else:
        GPIO.output(17, 0)
#         GPIO.output(27,1)


def relayType():
    global relay
    global relayfinal
    global typeRelay
    global typeRelayFinal
    global counter
    global relayfinal1
    global typeRelayFinal1
    global relayfinal2
    global typeRelayFinal2
    global indexfinal2
    global data
    global config
    global servers_manager
    global modefinal1

    relay_type = [0, 0]
    relay = [[], [], [], [], []]
    relayfinal = [[], []]
    relayfinal1 = [[], []]
    typeRelay = [[], [], [], [], []]
    typeRelayFinal = [[], []]
    typeRelayFinal1 = [[], []]
    index = [[], [], [], [], []]
    indexfinal = [[], []]
    indexfinal1 = [[], []]
    mode = [[], [], [], [], []]
    modefinal = [[], []]
    modefinal1 = [[], []]
    bd = [[], [], [], [], []]
    bdfinal = [[], []]
    bdfinal1 = [[], []]
    bytesize = [[], [], [], [], []]
    bytesizefinal = [[], []]
    bytesizefinal1 = [[], []]
    parity = [[], [], [], [], []]
    parityfinal = [[], []]
    parityfinal1 = [[], []]
    stopbit = [[], [], [], [], []]
    stopbitfinal = [[], []]
    stopbitfinal1 = [[], []]
    portaddress = [[], [], [], [], []]
    portaddressfinal = [[], []]
    portaddressfinal1 = [[], []]

    relayfinal2 = [[], []]
    typeRelayFinal2 = [[], []]
    indexfinal2 = [[], []]
    counter = [0, 0, 0, 0, 0]
    flag = True

    for i in range(0, len(relay_type)):
        relay[0].append(micomp123.type_relay[i])
        typeRelay[0].append(micomp123.relayTeks[i])
        index[0].append(micomp123.indexMaster[i])
        mode[0].append(micomp123.mode[i])
        bd[0].append(micomp123.baudrate[i])
        bytesize[0].append(micomp123.byte_size[i])
        parity[0].append(micomp123.parity[i])
        stopbit[0].append(micomp123.stop_bit[i])
        portaddress[0].append(micomp123.port_address[i])

        relay[1].append(micomp443.type_relay[i])
        typeRelay[1].append(micomp443.relayTeks[i])
        index[1].append(micomp443.indexMaster[i])
        mode[1].append(micomp443.mode[i])
        bd[1].append(micomp443.baudrate[i])
        bytesize[1].append(micomp443.byte_size[i])
        parity[1].append(micomp443.parity[i])
        stopbit[1].append(micomp443.stop_bit[i])
        portaddress[1].append(micomp443.port_address[i])

        relay[2].append(micomp442.type_relay[i])
        typeRelay[2].append(micomp442.relayTeks[i])
        index[2].append(micomp442.indexMaster[i])
        mode[2].append(micomp442.mode[i])
        bd[2].append(micomp442.baudrate[i])
        bytesize[2].append(micomp442.byte_size[i])
        parity[2].append(micomp442.parity[i])
        stopbit[2].append(micomp442.stop_bit[i])
        portaddress[2].append(micomp442.port_address[i])

        relay[3].append(micomp141.type_relay[i])
        typeRelay[3].append(micomp141.relayTeks[i])
        index[3].append(micomp141.indexMaster[i])
        mode[3].append(micomp141.mode[i])
        bd[3].append(micomp141.baudrate[i])
        bytesize[3].append(micomp141.byte_size[i])
        parity[3].append(micomp141.parity[i])
        stopbit[3].append(micomp141.stop_bit[i])
        portaddress[3].append(micomp141.port_address[i])

        relay[4].append(micomp122.type_relay[i])
        typeRelay[4].append(micomp122.relayTeks[i])
        index[4].append(micomp122.indexMaster[i])
        mode[4].append(micomp122.mode[i])
        bd[4].append(micomp122.baudrate[i])
        bytesize[4].append(micomp122.byte_size[i])
        parity[4].append(micomp122.parity[i])
        stopbit[4].append(micomp122.stop_bit[i])
        portaddress[4].append(micomp122.port_address[i])

    for i in range(0, len(relay)):
        for j in range(0, 2):
            for k in range(0, len(relay[i][j])):
                if relay[i][j][k] != 0:
                    relayfinal[j].append(str(relay[i][j][k]))
                    typeRelayFinal[j].append(str(typeRelay[i][j][k]))
                    indexfinal[j].append(str(index[i][j][k]))
                    modefinal[j].append(str(mode[i][j][k]))
                    bdfinal[j].append(str(bd[i][j][k]))
                    bytesizefinal[j].append(str(bytesize[i][j][k]))
                    parityfinal[j].append(str(parity[i][j][k]))
                    stopbitfinal[j].append(str(stopbit[i][j][k]))
                    portaddressfinal[j].append(str(portaddress[i][j][k]))

    for i in range(0, 2):
        for j in range(0, len(relayfinal[i])):
            if relayfinal[i][j] == 'MICOM P123' and typeRelayFinal[i][j] == 'P123':
                for k in range(0, len(indexfinal1[i])):
                    if str(indexfinal1[i][k]) == indexfinal[i][j]:
                        flag = False

                if flag == True:
                    relayfinal1[i].append(relayfinal[i][j])
                    typeRelayFinal1[i].append(typeRelayFinal[i][j])
                    indexfinal1[i].append(indexfinal[i][j])
                    modefinal1[i].append(modefinal[i][j])
                    bdfinal1[i].append(bdfinal[i][j])
                    bytesizefinal1[i].append(bytesizefinal[i][j])
                    parityfinal1[i].append(parityfinal[i][j])
                    stopbitfinal1[i].append(stopbitfinal[i][j])
                    portaddressfinal1[i].append(portaddressfinal[i][j])
                    flag = True

                flag = True

            elif relayfinal[i][j] == 'MICOM P122' and typeRelayFinal[i][j] == 'P122':
                for k in range(0, len(indexfinal1[i])):
                    if str(indexfinal1[i][k]) == indexfinal[i][j]:
                        flag = False

                if flag == True:
                    relayfinal1[i].append(relayfinal[i][j])
                    typeRelayFinal1[i].append(typeRelayFinal[i][j])
                    indexfinal1[i].append(indexfinal[i][j])
                    modefinal1[i].append(modefinal[i][j])
                    bdfinal1[i].append(bdfinal[i][j])
                    bytesizefinal1[i].append(bytesizefinal[i][j])
                    parityfinal1[i].append(parityfinal[i][j])
                    stopbitfinal1[i].append(stopbitfinal[i][j])
                    portaddressfinal1[i].append(portaddressfinal[i][j])
                    flag = True

                flag = True

            elif relayfinal[i][j] == 'MICOM P443' and typeRelayFinal[i][j] == 'P443':
                for k in range(0, len(indexfinal1[i])):
                    if str(indexfinal1[i][k]) == indexfinal[i][j]:
                        flag = False

                if flag == True:
                    relayfinal1[i].append(relayfinal[i][j])
                    typeRelayFinal1[i].append(typeRelayFinal[i][j])
                    indexfinal1[i].append(indexfinal[i][j])
                    modefinal1[i].append(modefinal[i][j])
                    bdfinal1[i].append(bdfinal[i][j])
                    bytesizefinal1[i].append(bytesizefinal[i][j])
                    parityfinal1[i].append(parityfinal[i][j])
                    stopbitfinal1[i].append(stopbitfinal[i][j])
                    portaddressfinal1[i].append(portaddressfinal[i][j])
                    flag = True

                flag = True

            elif relayfinal[i][j] == 'MICOM P442' and typeRelayFinal[i][j] == 'P442':
                for k in range(0, len(indexfinal1[i])):
                    if str(indexfinal1[i][k]) == indexfinal[i][j]:
                        flag = False

                if flag == True:
                    relayfinal1[i].append(relayfinal[i][j])
                    typeRelayFinal1[i].append(typeRelayFinal[i][j])
                    indexfinal1[i].append(indexfinal[i][j])
                    modefinal1[i].append(modefinal[i][j])
                    bdfinal1[i].append(bdfinal[i][j])
                    bytesizefinal1[i].append(bytesizefinal[i][j])
                    parityfinal1[i].append(parityfinal[i][j])
                    stopbitfinal1[i].append(stopbitfinal[i][j])
                    portaddressfinal1[i].append(portaddressfinal[i][j])
                    flag = True

                flag = True

            elif relayfinal[i][j] == 'MICOM P141' and typeRelayFinal[i][j] == 'P141':
                for k in range(0, len(indexfinal1[i])):
                    if str(indexfinal1[i][k]) == indexfinal[i][j]:
                        flag = False

                if flag == True:
                    relayfinal1[i].append(relayfinal[i][j])
                    typeRelayFinal1[i].append(typeRelayFinal[i][j])
                    indexfinal1[i].append(indexfinal[i][j])
                    modefinal1[i].append(modefinal[i][j])
                    bdfinal1[i].append(bdfinal[i][j])
                    bytesizefinal1[i].append(bytesizefinal[i][j])
                    parityfinal1[i].append(parityfinal[i][j])
                    stopbitfinal1[i].append(stopbitfinal[i][j])
                    portaddressfinal1[i].append(portaddressfinal[i][j])
                    flag = True

                flag = True

#     cekServer()

    counter[0] = 0
    counter[1] = 0
    counter[2] = 0
    counter[3] = 0
    counter[4] = 0

    data_old = data
    data = []
    ser = serial
    for j in range(0, 2):
        for i in range(0, len(relayfinal1[j])):
            if int(modefinal1[j][i]) == 1:
                ser = serial.Serial(port='/dev/ttyUSB'+str(
                    indexfinal1[0][i]), baudrate=19200, parity='N', stopbits=1, bytesize=8, timeout=.500)
                ser.close()
                data.append({'serial': {'port': '/dev/ttyUSB'+str(indexfinal1[0][i]), 'baudrate': int(bdfinal1[0][i]), 'parity': parityfinal1[0][i], 'stopbits': int(stopbitfinal1[0][i])},
                             'servers': [{'address': '0.0.0.0', 'port': int(portaddressfinal1[0][i]), 'protocol': 'TCP'}]})

                indexfinal2[j].append(indexfinal1[j][i])

            else:

                relayfinal2[j].append(relayfinal1[j][i])
                typeRelayFinal2[j].append(typeRelayFinal1[j][i])

    if data_old != data:
        print('CONFIG REMOTE BARU')
        servers_manager.close()
        for config in data:
            servers_manager.add_server(_serial_proxy.SerialProxy(config, None))

    print(data)
    print(relayfinal2)
    print(typeRelayFinal2)


micomp123.config()
micomp122.config()
micomp443.sistemconfig()
micomp442.sistemconfig()
micomp141.sistemconfig()
relayType()


while True:
    if len(data) != 0:
        print('run remote')
        ser =
        servers_manager.process()
    if not relayfinal2[0] and not relayfinal2[1]:
        print(relayfinal2)
        print("data kosong")
        micomp123.config()
        micomp122.config()
        micomp443.sistemconfig()
        micomp442.sistemconfig()
        micomp141.sistemconfig()
        relayType()
        time.sleep(1)

    else:
        for j in range(0, 2):
            for i in range(0, len(relayfinal2[j])):
                idPort = j

                # servers_manager.close()
                if i == 0:
                    counter[0] = 0
                    counter[1] = 0
                    counter[2] = 0
                    counter[3] = 0
                    counter[4] = 0
#                     cekServer()

                    dbdtList = [0]

                    for k in range(0, len(indexfinal2[j])):
                        mycursor = mydb.cursor()
                        sql = "SELECT * FROM device_list WHERE port_type='" + \
                            str(idPort)+"' AND port_number='" + \
                            str(indexfinal2[idPort][k])+"'"
                        mycursor.execute(sql)
                        dbDR = mycursor.fetchall()
                        mydb.commit()
                        mycursor.close()

                        for l in dbDR:
                            dbdtList[0] = l[17]

                        if int(dbdtList[0]) == 0:
                            micomp123.config()
                            micomp122.config()
                            micomp443.sistemconfig()
                            micomp442.sistemconfig()
                            micomp141.sistemconfig()
                            relayType()

                if relayfinal2[j][i] == 'MICOM P123' and typeRelayFinal2[j][i] == 'P123':
                    micomp123.dataReg(idPort, counter[0])
                    counter[0] += 1

                elif relayfinal2[j][i] == 'MICOM P443' and typeRelayFinal2[j][i] == 'P443':
                    micomp443.micomP443(idPort, counter[1])
                    counter[1] += 1

                elif relayfinal2[j][i] == 'MICOM P442' and typeRelayFinal2[j][i] == 'P442':
                    micomp442.micomP442(idPort, counter[2])
                    counter[2] += 1

                elif relayfinal2[j][i] == 'MICOM P141' and typeRelayFinal2[j][i] == 'P141':
                    micomp141.micomP141(idPort, counter[3])
                    counter[3] += 1

                elif relayfinal2[j][i] == 'MICOM P122' and typeRelayFinal2[j][i] == 'P122':
                    micomp122.dataReg(idPort, counter[0])
                    counter[4] += 1

                else:
                    micomp123.config()
                    micomp122.config()
                    micomp443.sistemconfig()
                    micomp442.sistemconfig()
                    micomp141.sistemconfig()
                    relayType()

                if (micomp123.flag == True or micomp122.flag == True or micomp443.flag2 == True or micomp442.flag2 == True or micomp141.flag2 == True) and i == int(len(relayfinal1[j]) - 1):
                    micomp123.config()
                    micomp122.config()
                    micomp443.sistemconfig()
                    micomp442.sistemconfig()
                    micomp141.sistemconfig()
                    relayType()
                    micomp123.flag = False
                    micomp122.flag = False
                    micomp443.flag2 = False
                    micomp442.flag2 = False
                    micomp141.flag2 = False

                if (micomp123.flag1 == True or micomp122.flag1 == True or micomp443.flag1 == True or micomp442.flag1 == True or micomp141.flag1 == True) and i == int(len(relayfinal1[j]) - 1):
                    micomp123.config()
                    micomp122.config()
                    micomp443.sistemconfig()
                    micomp442.sistemconfig()
                    micomp141.sistemconfig()
                    relayType()
                    micomp123.flag1 = False
                    micomp122.flag1 = False
                    micomp443.flag1 = False
                    micomp442.flag1 = False
                    micomp141.flag1 = False
                # if len(data) != 0:
                #     print('run remote')
                #     servers_manager.process()


servers_manager.close()
