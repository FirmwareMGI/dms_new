import micomp122 as micomp122
import micomp123 as micomp123
import micomp443 as micomp443
import micomp442 as micomp442
import micomp141 as micomp141
import micomp143 as micomp143
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
import logging as _logging
import network_nmtcli

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
jmlRecord = 0
buff_jmlRecord = 0

servers_manager = _server_manager.ServersManager()

mydb = mysql.connector.connect(
    host="localhost",
    user="dms",
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
    print(dbDR[0][6])
  
    if(dbDR[0][6]=="1"):
        print(  "------------------Update Network-------------------")
        network_nmtcli.changeNet()



    #if str(buffer) != str(dbCfg5[0]):
        #print( dbCfg5[1])
    #    print("----------------------------------------------")
        #buffer = dbCfg5[0]
        #os.system('sudo ifconfig eth0 down')
        #os.system('sudo ifconfig eth0 '+str(dbCfg5[0]))
        #os.system('sudo ifconfig eth0 up')
        #time.sleep(10)

    response = os.system("ping -c 1 " + dbCfg5[1])
    if response == 0:
        GPIO.output(17, 1)
#         GPIO.output(27,1)
    else:
        GPIO.output(17, 0)
#         GPIO.output(27,1)


def popData(j,i):
    if relayfinal1[j][i] == 'MICOM P123' and typeRelayFinal1[j][i] == 'P123':
        micomp123.client[j].pop(i)
        micomp123.indexMaster[j].pop(i)                    
        micomp123.relayTeks[j].pop(i)
        micomp123.id_micom[j].pop(i)
        micomp123.type_relay[j].pop(i) 
        micomp123.port_address[j].pop(i) 
        micomp123.rak_lokasi[j].pop(i) 
        micomp123.baudrate[j].pop(i) 
        micomp123.stop_bit[j].pop(i) 
        micomp123.parity[j].pop(i) 
        micomp123.byte_size[j].pop(i)
        micomp123.mode[j].pop(i)
        
        micomp123.ctRegister[j].pop(i)
        micomp123.ctVariabel[j].pop(i)
        micomp123.period[j].pop(i)
        micomp123.id_pool[j].pop(i)
        micomp123.jmlData[j].pop(i)
        micomp123.dbDR1[j].pop(i)
        micomp123.hitungError[j].pop(i)
        micomp123.hitungLoop[j].pop(i)
        
        micomp123.fileDR[j].pop(i)
        micomp123.indexFileDR[j].pop(i)
        micomp123.statusFileDR[j].pop(i)
        micomp123.waktuFileDR[j].pop(i)
        micomp123.lokasiFileDR[j].pop(i)
            
    elif relayfinal1[j][i] == 'MICOM P122' and typeRelayFinal1[j][i] == 'P122':
        micomp122.client[j].pop(i)
        micomp122.indexMaster[j].pop(i)                    
        micomp122.relayTeks[j].pop(i)
        micomp122.id_micom[j].pop(i)
        micomp122.type_relay[j].pop(i) 
        micomp122.port_address[j].pop(i) 
        micomp122.rak_lokasi[j].pop(i) 
        micomp122.baudrate[j].pop(i) 
        micomp122.stop_bit[j].pop(i) 
        micomp122.parity[j].pop(i) 
        micomp122.byte_size[j].pop(i)
        micomp122.mode[j].pop(i)
        
        micomp122.ctRegister[j].pop(i)
        micomp122.ctVariabel[j].pop(i)
        micomp122.period[j].pop(i)
        micomp122.id_pool[j].pop(i)
        micomp122.jmlData[j].pop(i)
        micomp122.dbDR1[j].pop(i)
        micomp122.hitungError[j].pop(i)
        micomp122.hitungLoop[j].pop(i)
        
        micomp122.fileDR[j].pop(i)
        micomp122.indexFileDR[j].pop(i)
        micomp122.statusFileDR[j].pop(i)
        micomp122.waktuFileDR[j].pop(i)
        micomp122.lokasiFileDR[j].pop(i)
        
    elif relayfinal1[j][i] == 'MICOM P141' and typeRelayFinal1[j][i] == 'P141':
        micomp141.ser[j].pop(i)
        micomp141.relayTeks[j].pop(i)                        
        micomp141.indexMaster[j].pop(i)
        micomp141.id_Micom[j].pop(i) 
        micomp141.rak_lokasi[j].pop(i)
        micomp141.type_relay[j].pop(i)
        micomp141.baudrate[j].pop(i)
        micomp141.stop_bit[j].pop(i) 
        micomp141.parity[j].pop(i) 
        micomp141.byte_size[j].pop(i)
        micomp141.statusRelay[j].pop(i)
        micomp141.mode[j].pop(i)
        micomp141.port_address[j].pop(i)

        micomp141.DRdate[j].pop(i)
        micomp141.jmlDtDR[j].pop(i)
        micomp141.indexDR[j].pop(i)
        micomp141.hitungError[j].pop(i)
        micomp141.hitungLoop[j].pop(i)
        micomp141.id_pool[j].pop(i)
        micomp141.countCH[j].pop(i)
        micomp141.countCF[j].pop(i)
        
        micomp141.flagDtDR[j].pop(i)
        micomp141.flagDtDR1[j].pop(i)
        micomp141.count[j].pop(i)
        
        micomp141.fileDR[j].pop(i)
        micomp141.indexFileDR[j].pop(i)
        micomp141.waktuFileDR[j].pop(i)
        micomp141.statusFileDR[j].pop(i)
        micomp141.lokasiFileDR[j].pop(i)
        micomp141.flag[j].pop(i)
        
    elif relayfinal1[j][i] == 'MICOM P143' and typeRelayFinal1[j][i] == 'P143':
        micomp143.ser[j].pop(i)
        micomp143.relayTeks[j].pop(i)                        
        micomp143.indexMaster[j].pop(i)
        micomp143.id_Micom[j].pop(i) 
        micomp143.rak_lokasi[j].pop(i)
        micomp143.type_relay[j].pop(i)
        micomp143.baudrate[j].pop(i)
        micomp143.stop_bit[j].pop(i) 
        micomp143.parity[j].pop(i) 
        micomp143.byte_size[j].pop(i)
        micomp143.statusRelay[j].pop(i)
        micomp143.mode[j].pop(i)
        micomp143.port_address[j].pop(i)

        micomp143.DRdate[j].pop(i)
        micomp143.jmlDtDR[j].pop(i)
        micomp143.indexDR[j].pop(i)
        micomp143.hitungError[j].pop(i)
        micomp143.hitungLoop[j].pop(i)
        micomp143.id_pool[j].pop(i)
        micomp143.countCH[j].pop(i)
        micomp143.countCF[j].pop(i)
        
        micomp143.flagDtDR[j].pop(i)
        micomp143.flagDtDR1[j].pop(i)
        micomp143.count[j].pop(i)
        
        micomp143.fileDR[j].pop(i)
        micomp143.indexFileDR[j].pop(i)
        micomp143.waktuFileDR[j].pop(i)
        micomp143.statusFileDR[j].pop(i)
        micomp143.lokasiFileDR[j].pop(i)
        micomp143.flag[j].pop(i)
        
    elif relayfinal1[j][i] == 'MICOM P442' and typeRelayFinal1[j][i] == 'P442':
        micomp442.ser[j].pop(i)
        micomp442.relayTeks[j].pop(i)                        
        micomp442.indexMaster[j].pop(i)
        micomp442.id_Micom[j].pop(i) 
        micomp442.rak_lokasi[j].pop(i)
        micomp442.type_relay[j].pop(i)
        micomp442.baudrate[j].pop(i)
        micomp442.stop_bit[j].pop(i) 
        micomp442.parity[j].pop(i) 
        micomp442.byte_size[j].pop(i)
        micomp442.statusRelay[j].pop(i)
        micomp442.mode[j].pop(i)
        micomp442.port_address[j].pop(i)

        micomp442.DRdate[j].pop(i)
        micomp442.jmlDtDR[j].pop(i)
        micomp442.indexDR[j].pop(i)
        micomp442.hitungError[j].pop(i)
        micomp442.hitungLoop[j].pop(i)
        micomp442.id_pool[j].pop(i)
        micomp442.countCH[j].pop(i)
        micomp442.countCF[j].pop(i)
        
        micomp442.flagDtDR[j].pop(i)
        micomp442.flagDtDR1[j].pop(i)
        micomp442.count[j].pop(i)
        
        micomp442.fileDR[j].pop(i)
        micomp442.indexFileDR[j].pop(i)
        micomp442.waktuFileDR[j].pop(i)
        micomp442.statusFileDR[j].pop(i)
        micomp442.lokasiFileDR[j].pop(i)
        micomp442.flag[j].pop(i)
            
    elif relayfinal1[j][i] == 'MICOM P443' and typeRelayFinal1[j][i] == 'P443':
        micomp443.ser[j].pop(i)
        micomp443.relayTeks[j].pop(i)                        
        micomp443.indexMaster[j].pop(i)
        micomp443.id_Micom[j].pop(i) 
        micomp443.rak_lokasi[j].pop(i)
        micomp443.type_relay[j].pop(i)
        micomp443.baudrate[j].pop(i)
        micomp443.stop_bit[j].pop(i) 
        micomp443.parity[j].pop(i) 
        micomp443.byte_size[j].pop(i)
        micomp443.statusRelay[j].pop(i)
        micomp443.mode[j].pop(i)
        micomp443.port_address[j].pop(i)

        micomp443.DRdate[j].pop(i)
        micomp443.jmlDtDR[j].pop(i)
        micomp443.indexDR[j].pop(i)
        micomp443.hitungError[j].pop(i)
        micomp443.hitungLoop[j].pop(i)
        micomp443.id_pool[j].pop(i)
        micomp443.countCH[j].pop(i)
        micomp443.countCF[j].pop(i)
        
        micomp443.flagDtDR[j].pop(i)
        micomp443.flagDtDR1[j].pop(i)
        micomp443.count[j].pop(i)
        
        micomp443.fileDR[j].pop(i)
        micomp443.indexFileDR[j].pop(i)
        micomp443.waktuFileDR[j].pop(i)
        micomp443.statusFileDR[j].pop(i)
        micomp443.lokasiFileDR[j].pop(i)

        micomp443.flag[j].pop(i)

    

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
    global indexfinal3
    global data
    global config
    global servers_manager
    global modefinal1
    global jmlRecord

    relay_type = [0, 0]
    relay = [[], [], [], [], [], []]
    relayfinal = [[], []]
    relayfinal1 = [[], []]
    typeRelay = [[], [], [], [], [], []]
    typeRelayFinal = [[], []]
    typeRelayFinal1 = [[], []]
    index = [[], [], [], [], [], []]
    indexfinal = [[], []]
    indexfinal1 = [[], []]
    mode = [[], [], [], [], [], []]
    modefinal = [[], []]
    modefinal1 = [[], []]
    bd = [[], [], [], [], [], []]
    bdfinal = [[], []]
    bdfinal1 = [[], []]
    bytesize = [[], [], [], [], [], []]
    bytesizefinal = [[], []]
    bytesizefinal1 = [[], []]
    parity = [[], [], [], [], [], []]
    parityfinal = [[], []]
    parityfinal1 = [[], []]
    stopbit = [[], [], [], [], [], []]
    stopbitfinal = [[], []]
    stopbitfinal1 = [[], []]
    portaddress = [[], [], [], [], [], []]
    portaddressfinal = [[], []]
    portaddressfinal1 = [[], []]

    relayfinal2 = [[], []]
    typeRelayFinal2 = [[], []]
    indexfinal2 = [[], []]
    indexfinal3 = [[], []]
    counter = [0, 0, 0, 0, 0, 0]
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
        
        relay[5].append(micomp143.type_relay[i])
        typeRelay[5].append(micomp143.relayTeks[i])
        index[5].append(micomp143.indexMaster[i])
        mode[5].append(micomp143.mode[i])
        bd[5].append(micomp143.baudrate[i])
        bytesize[5].append(micomp143.byte_size[i])
        parity[5].append(micomp143.parity[i])
        stopbit[5].append(micomp143.stop_bit[i])
        portaddress[5].append(micomp143.port_address[i])

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
                
            elif relayfinal[i][j] == 'MICOM P143' and typeRelayFinal[i][j] == 'P143':
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

    cekServer()
    print(relayfinal1)

    counter[0] = 0
    counter[1] = 0
    counter[2] = 0
    counter[3] = 0
    counter[4] = 0
    counter[5] = 0

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
                             'servers': [{'address': '0.0.0.0', 'port': 2000+int(indexfinal1[0][i]), 'protocol': 'TCP'}]})

                indexfinal2[j].append(indexfinal1[j][i])
                try:
                    popData(j,i)
                            
                except IndexError:
                    print('sepurane error bro')
                    
                    
            else:

                relayfinal2[j].append(relayfinal1[j][i])
                typeRelayFinal2[j].append(typeRelayFinal1[j][i])
                indexfinal3[j].append(indexfinal1[j][i])

    mycursor = mydb.cursor()
    sql = "SELECT COUNT(port_number) FROM device_list WHERE port_type='" + str(0)+"'"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb.commit()
    mycursor.close()

    for l in dbDR:
        jmlRecord = l[0]

    if data_old != data:
        print('CONFIG REMOTE BARU')
        servers_manager.close()
        for config in data:
            servers_manager.add_server(_serial_proxy.SerialProxy(config, None))


#     print(indexfinal2)
#     print(data)
#     print(relayfinal2)
#     print(typeRelayFinal2)



micomp123.config()
micomp122.config()
micomp443.sistemconfig()
micomp442.sistemconfig()
micomp141.sistemconfig()
micomp143.sistemconfig()
relayType()


while True:
    dbdtList = [0]
    if len(data) != 0:
        # print('run remote')
        servers_manager.process()


    if not relayfinal2[0] and not relayfinal2[1] and not data:
        print("data kosong")
        micomp123.config()
        micomp122.config()
        micomp443.sistemconfig()
        micomp442.sistemconfig()
        micomp141.sistemconfig()
        micomp143.sistemconfig()
        relayType()
        time.sleep(1)

    else:
        dbdtList = [0]
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
                    counter[5] = 0
    #                     cekServer()

            
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
                    micomp122.dataReg(idPort, counter[4])
                    counter[4] += 1
                    
                elif relayfinal2[j][i] == 'MICOM P143' and typeRelayFinal2[j][i] == 'P143':
                    micomp143.micomP143(idPort, counter[5])
                    counter[5] += 1

                else:
                    micomp123.config()
                    micomp122.config()
                    micomp443.sistemconfig()
                    micomp442.sistemconfig()
                    micomp141.sistemconfig()
                    micomp143.sistemconfig()
                    relayType()

                if (micomp123.flag == True or micomp122.flag == True or micomp443.flag2 == True or micomp442.flag2 == True or micomp141.flag2 == True or micomp143.flag2 == True) and i == int(len(relayfinal2[j]) - 1):
                    micomp123.config()
                    micomp122.config()
                    micomp443.sistemconfig()
                    micomp442.sistemconfig()
                    micomp141.sistemconfig()
                    micomp143.sistemconfig()
                    relayType()
                    micomp123.flag = False
                    micomp122.flag = False
                    micomp443.flag2 = False
                    micomp442.flag2 = False
                    micomp141.flag2 = False
                    micomp143.flag2 = False

#                 if (micomp123.flag1 == True or micomp122.flag1 == True or micomp443.flag1 == True or micomp442.flag1 == True or micomp141.flag1 == True) and i == int(len(relayfinal2[j]) - 1):
#                     micomp123.config()
#                     micomp122.config()
#                     micomp443.sistemconfig()
#                     micomp442.sistemconfig()
#                     micomp141.sistemconfig()
#                     relayType()
#                     micomp123.flag1 = False
#                     micomp122.flag1 = False
#                     micomp443.flag1 = False
#                     micomp442.flag1 = False
#                     micomp141.flag1 = False


    mycursor = mydb.cursor()
    sql = "SELECT * FROM flag_config WHERE id='" + \
        str(1)+"'"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb.commit()
    mycursor.close()

    for l in dbDR:
        dbdtList[0] = l[0]

    if int(dbdtList[0]) == 1:
        micomp123.config()
        micomp122.config()
        micomp443.sistemconfig()
        micomp442.sistemconfig()
        micomp141.sistemconfig()
        micomp143.sistemconfig()
        relayType()
        
        mycursor = mydb.cursor()
        sql = "UPDATE flag_config SET flag = '"+str(0)+"' WHERE id='"+str(1)+"'"
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()


log.info("Exiting..")
servers_manager.close()
