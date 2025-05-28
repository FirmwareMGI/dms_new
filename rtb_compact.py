from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.sync import ModbusTcpClient as ModbusClientTcp
import monrecti as monrtb

import time
import mysql.connector

buff_client = []
type_relay = []
relayTeks = []
indexMaster = []
mode = []
baudrate = []
byte_size = []
parity = []
stop_bit = []
port_address = []
indexMaster = []

id_micom = []
buff_id_micom = []
type_relay = []
buff_type_relay = []
port_address = []
buff_port_address = []
rak_lokasi = []
buff_rak_lokasi = []
baudrate = []
buff_baudrate = []
ip_address = []
buff_ip_address = []
stop_bit = []
buff_stop_bit = []
parity = []
buff_parity = []
byte_size = []
buff_byte_size = []
dbDR1 = []
buff_dbDR1 = []
mode = []
buff_mode = []
indexPort = []

buffcekKoneksi = []
buffcekKoneksi1 = []

client = []
dbList = [0, 0]

mydb = mysql.connector.connect(
    host="localhost",
    user="dms",
    password="mgi",
    database="dms"
)

mycursor = mydb.cursor()


def dataReg(idPort, index):
    global flagModbus
    global baca
    global countData

    # print(idPort, index)
    connection = client[idPort][index].connect()
    if connection:
        print("READ MEASUREMENT")
        unit = int(id_micom[idPort][index])
        print(unit)
        monrtb.readMeasurement(client[idPort][index], unit)


def config():
    print("------------------RTB COMPACT---------------------------")
    global buffcekKoneksi
    global buffcekKoneksi1

    for i in range(0, len(dbList)):
        mycursor = mydb.cursor()
        sql = "SELECT * FROM device_list WHERE port_type='"+str(i)+"'"
        mycursor.execute(sql)
        dbList[i] = mycursor.fetchall()

        # id_micom.append([0 for x in range(0, len(dbList[i]))])
        type_relay.append([0 for x in range(0, len(dbList[i]))])
        port_address.append([0 for x in range(0, len(dbList[i]))])

        baudrate.append([0 for x in range(0, len(dbList[i]))])
        stop_bit.append([0 for x in range(0, len(dbList[i]))])
        parity.append([0 for x in range(0, len(dbList[i]))])
        byte_size.append([0 for x in range(0, len(dbList[i]))])
        relayTeks.append([0 for x in range(0, len(dbList[i]))])
        indexMaster.append([0 for x in range(0, len(dbList[i]))])
        mode.append([0 for x in range(0, len(dbList[i]))])
        rak_lokasi.append([0 for x in range(0, len(dbList[i]))])

        buff_id_micom.append([0 for x in range(0, len(dbList[i]))])
        buff_type_relay.append([0 for x in range(0, len(dbList[i]))])
        buff_port_address.append([0 for x in range(0, len(dbList[i]))])
        buff_rak_lokasi.append([0 for x in range(0, len(dbList[i]))])
        buff_baudrate.append([0 for x in range(0, len(dbList[i]))])
        indexPort.append([0 for x in range(0, len(dbList[i]))])
        buff_parity.append([0 for x in range(0, len(dbList[i]))])
        buff_byte_size.append([0 for x in range(0, len(dbList[i]))])
        buff_mode.append([0 for x in range(0, len(dbList[i]))])
        buff_stop_bit.append([0 for x in range(0, len(dbList[i]))])
        buff_client.append([0 for x in range(0, len(dbList[i]))])

        id_micom.append([0 for x in range(0, len(dbList[i]))])
        buff_ip_address.append([0 for x in range(0, len(dbList[i]))])
        ip_address.append([0 for x in range(0, len(dbList[i]))])

    hitung = 0
    for i in range(0, len(dbList[0])):
        idPort = 0

        buff_id_micom[idPort][i] = dbList[idPort][i][1]
        buff_type_relay[idPort][i] = dbList[idPort][i][2]
        indexPort[idPort][i] = dbList[idPort][i][4]
        buff_port_address[idPort][i] = dbList[idPort][i][5]
        buff_rak_lokasi[idPort][i] = dbList[idPort][i][6]
        buff_baudrate[idPort][i] = dbList[idPort][i][7]
        buff_stop_bit[idPort][i] = dbList[idPort][i][12]
        buff_parity[idPort][i] = dbList[idPort][i][13]
        buff_byte_size[idPort][i] = dbList[idPort][i][14]
        buff_mode[idPort][i] = dbList[idPort][i][17]

        buff_client[idPort][i] = ModbusClient(method='rtu', port='/dev/ttyUSB'+str(indexPort[idPort][i]),  stopbits=int(buff_stop_bit[idPort][i]), bytesize=int(
            buff_byte_size[idPort][i]), parity=str(buff_parity[idPort][i]), baudrate=int(buff_baudrate[idPort][i]), timeout=.500)

        # print('/dev/ttyUSB'+str(indexPort[idPort][i]))
        connection = buff_client[idPort][i].connect()
        if connection:
            baca = buff_client[idPort][i].read_holding_registers(
                address=53, count=1, unit=int(buff_id_micom[idPort][i]))

            if baca.isError():
                print('Port'+str(indexPort[idPort][i]) +
                      ' RS-485 tidak dapat menerima data')
            elif baca.registers[0] == 3:
                print(baca.registers)
                buffcekKoneksi.append(buff_client[idPort][i])

                relayTeks[idPort][hitung] = "RTBCOMPACT"
                indexMaster[idPort][hitung] = str(indexPort[idPort][i])
                id_micom[idPort][hitung] = buff_id_micom[idPort][i]
                type_relay[idPort][hitung] = buff_type_relay[idPort][i]
                port_address[idPort][hitung] = buff_port_address[idPort][i]
                rak_lokasi[idPort][hitung] = buff_rak_lokasi[idPort][i]
                baudrate[idPort][hitung] = buff_baudrate[idPort][i]
                stop_bit[idPort][hitung] = buff_stop_bit[idPort][i]
                parity[idPort][hitung] = buff_parity[idPort][i]
                byte_size[idPort][hitung] = buff_byte_size[idPort][i]
                port_address[idPort][hitung] = buff_port_address[idPort][i]
                mode[idPort][hitung] = buff_mode[idPort][i]

            hitung += 1
        else:
            print('Port'+str(indexPort[idPort][i])+' RS-485 tidak terhubung')

    client.append(buffcekKoneksi)

    hitung = 0
    for i in range(0, len(dbList[1])):
        idPort = 1
        print(dbList[1])
        buff_id_micom[idPort][i] = dbList[idPort][i][1]
        buff_type_relay[idPort][i] = dbList[idPort][i][2]
        indexPort[idPort][i] = dbList[idPort][i][4]
        buff_port_address[idPort][i] = dbList[idPort][i][5]
        buff_rak_lokasi[idPort][i] = dbList[idPort][i][6]
        buff_ip_address[idPort][i] = dbList[idPort][i][8]

        buff_client[idPort][i] = ModbusClientTcp(host=str(
            buff_ip_address[idPort][i]), port=int(buff_port_address[idPort][i]), timeout=.500)

        connection = buff_client[idPort][i].connect()
        if connection:
            baca = buff_client[idPort][i].read_holding_registers(
                address=53, count=1, unit=int(buff_id_micom[idPort][i]))

            if baca.isError():
                print(
                    'IP '+str(buff_ip_address[idPort][i])+' Tcp/Ip tidak dapat menerima data')

            elif baca.registers[0] == 3:
                print(baca.registers)
                relayTeks[idPort][hitung] = "RTBCOMPACT"
                print(relayTeks[idPort][hitung])
                buffcekKoneksi1.append(buff_client[idPort][i])

                indexMaster[idPort][hitung] = str(indexPort[idPort][i])
                id_micom[idPort][hitung] = buff_id_micom[idPort][i]
                type_relay[idPort][hitung] = buff_type_relay[idPort][i]
                port_address[idPort][hitung] = buff_port_address[idPort][i]
                rak_lokasi[idPort][hitung] = buff_rak_lokasi[idPort][i]
                ip_address[idPort][hitung] = buff_ip_address[idPort][i]


                hitung += 1

        else:
            print('IP '+str(buff_ip_address[idPort]
                  [i])+' Tcp/Ip tidak terhubung')

    client.append(buffcekKoneksi1)
    print(client)
#
#            elif buff_type_relay[idPort][i] == 'MICOM P122':
#                baca = buff_client[idPort][i].read_holding_registers(
#                    address=0, count=2, unit=int(buff_id_micom[idPort][i]))
#                relayTeks[idPort][hitung] = chr(baca.registers[0] >> 8) + chr(
#                    baca.registers[0] % 256) + chr(baca.registers[1] >> 8) + chr(baca.registers[1] % 256)


#        mycursor = mydb.cursor()
#        sql = "SELECT * FROM dataRegister WHERE port_device='" + \
#            str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
#        mycursor.execute(sql)
#        dbDR = mycursor.fetchall()
#        mydb.commit()

    # print(dbDR)
    # connection = buff_client[idPort][i].connect()
    # if connection:
    #     baca = buff_client[idPort][i].read_holding_registers(
    #         address=15616, count=36, unit=int(buff_id_micom[idPort][i]))

    #     if baca.isError():
    #         print('Port'+str(indexPort[idPort][i]) +
    #               ' RS-485 tidak dapat menerima data')
