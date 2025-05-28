from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.sync import ModbusTcpClient as ModbusClientTcp
import array as arr
import time
import mysql.connector
import datetime
from datetime import datetime, timedelta

import zipfile
from zipfile import ZipFile
import os
from os.path import basename
import monp122 as mon
import shutil
import requests
import struct
import socket


# timeCurrent = datetime.datetime.now()
# timeCurrent1 = datetime.datetime.now()
# timeCurrent2 = datetime.datetime.now()

flag = False
flag1 = False
dbList = [0, 0]
hitung = 0
hitungError = []
buff_hitungError = []

fileDR = []
buff_fileDR = []

waktuFileDR = []
buff_waktuFileDR = []

statusFileDR = []
buff_statusFileDR = []

lokasiFileDR = []
buff_lokasiFileDR = []

indexFileDR = []
buff_indexFileDR = []

hitungLoop = []
buff_hitungLoop = []

indexPort = []
statusRelay = []

client = []
indexMaster = []
buff_client = []
ctRegister = []
buff_ctRegister = []
ctVariabel = []
buff_ctVariabel = []
jmlData = []
buff_jmlData = []
jmlSisaData = []
buff_jmlSisaData = []
period = []
buff_period = []
id_pool = []
buff_id_pool = []
selisihJmlData = []
countData = 0

buffDR = []
ratio = []
ratio1 = []
totRatio = []
totRatio1 = []
prDevice = []
freq = []
statusReg = []
buff = []
tanggal = []
bulan = []
tahun = []
jam = []
menit = []
detik = []
dns = []
netmask = []
gateway = []
waktuAwalDR = []
waktuAkhirDR = []
buffcekKoneksi = []
buffcekKoneksi1 = []

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

relayTeks = []


mydb = mysql.connector.connect(
    host="localhost",
    user="dms",
    password="mgi",
    database="dms"
)

mycursor = mydb.cursor()


DR1 = ['it_ia', 'it_ib', 'it_ic', 'it_ie', 'it_f', 'it_relay']
DR = ['ia', 'ib', 'ic', 'ie', 'f', 'relay']
idHr = arr.array('i', [0, 1, 2, 3, 4, 5])
idDR = arr.array('i', [0, 14336, 14592, 14848, 15104, 15360])
dtRegister = arr.array('i', [15616, idDR[1], 0, 8704, 12, 2048, 2304, 2429, 2560, 2685, 2816, 2941, 3072, 3197, 3328, 3453, 3584, 3709, 3840, 3965,
                       4096, 4221, 4352, 4477, 4608, 4733, 4864, 4989, 5120, 5245, 5376, 5501, 5632, 5757, 5888, 6013, 6144, 6269, 6400, 6525, 6656, 6781, 6912, 7037, 7168, 7424, 7680, 7936, 8192, 8448])


def dataReg(idPort, index):
    global flagModbus
    global baca
    global countData

    connection = client[idPort][index].connect()
    if connection:
        if dtRegister[ctRegister[idPort][index]] == 15616:
            print(dtRegister[ctRegister[idPort][index]])
            baca = client[idPort][index].read_holding_registers(
                address=dtRegister[ctRegister[idPort][index]], count=36, unit=int(id_micom[idPort][index]))
            unit =int(id_micom[idPort][index])
            mon.readMeasurement(client[idPort][index],unit)
            flagModbus = 0

        elif dtRegister[ctRegister[idPort][index]] == dtRegister[1]:
            dtRegister[1] = idDR[dbDR1[idPort][index]] + \
                idHr[ctVariabel[idPort][index]]
            print(dtRegister[ctRegister[idPort][index]])
            baca = client[idPort][index].read_holding_registers(
                address=dtRegister[ctRegister[idPort][index]], count=11, unit=int(id_micom[idPort][index]))
            flagModbus = 1

        elif dtRegister[ctRegister[idPort][index]] == 0:
            print(dtRegister[ctRegister[idPort][index]])
            baca = client[idPort][index].read_holding_registers(
                address=dtRegister[ctRegister[idPort][index]], count=2, unit=int(id_micom[idPort][index]))
            flagModbus = 2

        elif dtRegister[ctRegister[idPort][index]] == 8704:
            print(dtRegister[ctRegister[idPort][index]])
            baca = client[idPort][index].read_holding_registers(
                address=dtRegister[ctRegister[idPort][index]], count=7, unit=int(id_micom[idPort][index]))
            flagModbus = 3

        elif dtRegister[ctRegister[idPort][index]] == 12:
            print(dtRegister[ctRegister[idPort][index]])
            baca = client[idPort][index].read_holding_registers(
                address=dtRegister[ctRegister[idPort][index]], count=1, unit=int(id_micom[idPort][index]))
            flagModbus = 4

        elif dtRegister[ctRegister[idPort][index]] == 2048:
            print(dtRegister[ctRegister[idPort][index]])
            baca = client[idPort][index].read_holding_registers(
                address=dtRegister[ctRegister[idPort][index]], count=4, unit=int(id_micom[idPort][index]))
            flagModbus = 5

        # elif dtRegister[ctRegister[idPort][index]] == 7168:

        #     print(dtRegister[ctRegister[idPort][index]])
        #     for i in range(0, 36):
        #         if jmlData[idPort][index] == 4785 + i:
        #             baca = client[idPort][index].read_holding_registers(
        #                 address=dtRegister[ctRegister[idPort][index]], count=35+i, unit=int(id_micom[idPort][index]))

        #     ctRegister[idPort][index] = 0
        #     ctVariabel[idPort][index] += 1
        #     flagModbus = 6

        else:
            jmlSisaData = jmlData[idPort][index] % 125
            selisihJmlData = jmlData[idPort][index]/125
            countData += 1
            if countData <= selisihJmlData:
                baca = client[idPort][index].read_holding_registers(
                    address=dtRegister[ctRegister[idPort][index]], count=125, unit=int(id_micom[idPort][index]))
                flagModbus = 7
            else:
                baca = client[idPort][index].read_holding_registers(
                    address=dtRegister[ctRegister[idPort][index]], count=jmlSisaData, unit=int(id_micom[idPort][index]))
                ctRegister[idPort][index] = 0
                ctVariabel[idPort][index] += 1
                flagModbus = 6
                countData = 0
            print(dtRegister[ctRegister[idPort][index]])

        ctRegister[idPort][index] += 1

        global ratio
        global ratio1
        global prDevice
        global freq
        global totRatio
        global totRatio1
        global statusReg
        global tanggal
        global bulan
        global tahun
        global jam
        global menit
        global detik
        global flag
        global flag1

        if flagModbus == 0:

            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")

                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()

                if hitungError[idPort][index] == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                buffDR[idPort][index] = baca.registers[29]
                
                read_milis_atas = client[idPort][index].read_holding_registers(address = 400, count = 1,unit= int(id_micom[idPort][index]))
                reg_milis_atas = read_milis_atas.registers[0]
                
                milis_atas = reg_milis_atas/10
                print(milis_atas)
                millis_bawah = baca.registers[33]
                print(millis_bawah)
                
                second_1 = hex(baca.registers[30])[2:]
                second_2 = hex(baca.registers[31])[2:]
                second_1f = second_1.rjust(4,'0')
                second_2f = second_2.rjust(4,'0')
                
                secTot = struct.unpack('>i', bytes.fromhex(second_1f + second_2f))
                base_date = datetime(1994,1,1)
                dateNow = base_date + timedelta(seconds=int(secTot[0]))
                print(dateNow)
                
                waktuAkhirDR[idPort][index] = dateNow+timedelta(milliseconds=millis_bawah)
                waktuAwalDR[idPort][index] = waktuAkhirDR[idPort][index] - timedelta(seconds=milis_atas) + timedelta(milliseconds= -1)

                mycursor = mydb.cursor()
                sql = "SELECT * FROM dataRegister WHERE port_device='" + \
                    str(idPort)+"' AND id_device='" + \
                    str(indexMaster[idPort][index])+"' "
                mycursor.execute(sql)
                dbDR = mycursor.fetchall()
                mydb.commit()

                if len(dbDR) == 0:
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO dataRegister(port_device, id_device, geser_register, geser_param, period, id_pool, jumlah_data, indexDR) VALUES('"+str(
                        idPort)+"', '"+str(indexMaster[idPort][index])+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"','"+str(0)+"', '"+str(4800)+"', '"+str(1)+"') "
                    mycursor.execute(sql)
                    mydb.commit()
                    dbDR1[idPort][index] = 1
                else:
                    for i in dbDR:
                        dbDR1[idPort][index] = int(i[7])
                        

                baca1 = client[idPort][index].read_holding_registers(
                    address=12, count=1, unit=int(id_micom[idPort][index]))
                if baca1.isError():
                    statusReg[idPort][index] = int(8)
                else:
                    statusReg[idPort][index] = int(baca1.registers[0])

                if int(buff[idPort][index]) != statusReg[idPort][index]:
                    x = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                    mycursor = mydb.cursor()
                    sql = "UPDATE device_list SET kondisi = '"+str(statusReg[idPort][index])+"', tanggal = '"+str(
                        x)+"' WHERE port_type='"+str(idPort)+"' AND port_number='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()

                    buff[idPort][index] = statusReg[idPort][index]

                if buffDR[idPort][index] != 0 and buffDR[idPort][index] != dbDR1[idPort][index]:
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexDR = '"+str(buffDR[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' "
                    mycursor.execute(sql)
                    mydb.commit()

                    dbDR1[idPort][index] = buffDR[idPort][index]

                    dtRegister[1] = idDR[buffDR[idPort][index]] + \
                        idHr[ctVariabel[idPort][index]]

                    buff[idPort][index] = 0

                else:
                    ctRegister[idPort][index] = 0

#                 if index == 0 and (idPort == 0 or idPort == 1):
#                     hitungLoop[idPort][index] += 1
#                     mycursor = mydb.cursor()
#                     sql = "UPDATE dataRegister SET indexLoop = '"+str(hitungLoop[idPort][index])+"' WHERE port_device='"+str(
#                         idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
#                     mycursor.execute(sql)
#                     mydb.commit()
# 
#                     if hitungLoop[idPort][index] == 500:
#                         hitungLoop[idPort][index] = 0
#                         mycursor = mydb.cursor()
#                         sql = "UPDATE dataRegister SET indexLoop = '"+str(hitungLoop[idPort][index])+"' WHERE port_device='"+str(
#                             idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
#                         mycursor.execute(sql)
#                         mydb.commit()
#                         flag1 = True

        elif flagModbus == 1:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                jmlData[idPort][index] = baca.registers[0]
                ratio[idPort][index] = baca.registers[7]
                ratio1[idPort][index] = baca.registers[8]

                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET jumlah_data = '" + \
                    str(jmlData[idPort][index])+"' WHERE port_device='"+str(idPort) + \
                    "' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()

        elif flagModbus == 2:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError[idPort][index] == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                prDevice[idPort][index] = chr(baca.registers[0] >> 8) + chr(
                    baca.registers[0] % 256) + chr(baca.registers[1] >> 8) + chr(baca.registers[1] % 256)

        elif flagModbus == 3:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                freq[idPort][index] = baca.registers[6]
                totRatio[idPort][index] = round((1/ratio[idPort][index])*1.4142, 6)
                print("TOTAL RATIO: ")
                print(totRatio[idPort][index])
                totRatio1[idPort][index] = round((1/ratio1[idPort][index])*1.4142, 6)
                print(totRatio1[idPort][index])
                if(idHr[ctVariabel[idPort][index]] == 0):
                    data = str(prDevice[idPort][index])+"*"+str(jmlData[idPort][index])+"*"+str(totRatio[idPort][index])+"*"+str(totRatio[idPort][index])+"*"+str(
                        totRatio[idPort][index])+"*"+str(totRatio1[idPort][index])+"*"+str(id_micom[idPort][index])+"*"+str(freq[idPort][index])
                    kirimServer(data, idPort, index)

        elif flagModbus == 4:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError[idPort][index] == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                statusReg[idPort][index] = baca.registers[0]

        elif flagModbus == 5:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                tahun[idPort][index] = baca.registers[0]
                bulan[idPort][index] = baca.registers[1] >> 8
                tanggal[idPort][index] = baca.registers[1] % 256
                jam[idPort][index] = baca.registers[2] >> 8
                menit[idPort][index] = baca.registers[2] % 256
                detik[idPort][index] = baca.registers[3]
                
                x = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                if buff[idPort][index] != statusReg[idPort][index] and ctVariabel[idPort][index] == 0:
                    #data = str(id_micom[idPort][index])+"*"+str(rak_lokasi[idPort][index])+"*"+str(statusReg[idPort][index])+"*"+str(tanggal[idPort][index])+"/"+str(
                    #    bulan[idPort][index])+"/"+str(tahun[idPort][index])+" "+str(jam[idPort][index])+":"+str(menit[idPort][index])+" WIB"
                    data = str(id_micom[idPort][index])+"*"+str(rak_lokasi[idPort][index])+"*"+str(statusReg[idPort][index])+"*"+str(x)+" WIB"
                    kirimServer(data, idPort, index)
                    buff[idPort][index] = statusReg[idPort][index]

        elif flagModbus == 6:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError[idPort][index] == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                data = baca.registers

                for i in range(0, len(data)):
                    if data[i] > 50000:
                        data[i] = data[i]-65536

                kirimServer(data, idPort, index)

        elif flagModbus == 7:
            if baca.isError():
                ctRegister[idPort][index] -= 1
                if int(idPort) == 0:
                    print(
                        "Port"+str(indexMaster[idPort][index])+" RS-485 tidak dapat menerima data")
                else:
                    print(
                        "IP "+str(ip_address[idPort][hitung])+" tidak dapat menerima data")

                hitungError[idPort][index] += 1
                mycursor = mydb.cursor()
                sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                    idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                mycursor.execute(sql)
                mydb.commit()
                if hitungError[idPort][index] == 10:
                    hitungError[idPort][index] = 0
                    mycursor = mydb.cursor()
                    sql = "UPDATE dataRegister SET indexError = '"+str(hitungError[idPort][index])+"' WHERE port_device='"+str(
                        idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    flag = True

            else:
                data = baca.registers

                for i in range(0, len(data)):
                    if data[i] > 50000:
                        data[i] = data[i]-65536

                kirimServer(data, idPort, index)

    else:
        if int(idPort) == 0:
            print('koneksi PORT' +
                  str(indexMaster[idPort][index])+' RS-485 Gagal')
            config()

        else:
            print('koneksi IP'+str(ip_address[idPort][hitung])+' Gagal')
            config()


def kirimServer(data, idPort, index):
    global statusRelay

    if flagModbus == 7 and ctVariabel[idPort][index] <= 5:
        listToString = '*'.join(str(elem) for elem in data)

        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(DR1[ctVariabel[idPort][index]])+" WHERE port_device='"+str(idPort)+"' AND id_device='"+str(
            indexMaster[idPort][index])+"' AND period='"+str(period[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO "+str(DR1[ctVariabel[idPort][index]])+"("+str(DR[ctVariabel[idPort][index]])+", flag, id_pool, period, port_device, id_device) VALUES('"+str(
                listToString)+"', '"+str(0)+"','"+str(id_pool[idPort][index])+"','"+str(period[idPort][index])+"','"+str(idPort)+"','"+str(indexMaster[idPort][index])+"') "
            mycursor.execute(sql)
            mydb.commit()
            print(listToString)
        else:
            mycursor = mydb.cursor()
            sql = "UPDATE "+str(DR1[ctVariabel[idPort][index]])+" SET "+str(DR[ctVariabel[idPort][index]])+" = '"+str(listToString)+"', flag = '"+(str(0))+"' WHERE port_device='"+str(
                idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"' AND period='"+str(period[idPort][index])+"' "
            mycursor.execute(sql)
            mydb.commit()
            print(listToString)

        period[idPort][index] += 1

        mycursor = mydb.cursor()
        sql1 = "UPDATE dataRegister SET geser_register = '"+str(ctRegister[idPort][index])+"', geser_param = '"+str(ctVariabel[idPort][index])+"', period = '"+str(
            period[idPort][index])+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' "
        mycursor.execute(sql1)
        mydb.commit()

    elif flagModbus == 6 and (ctVariabel[idPort][index] - 1) <= 5:
        listToString = '*'.join(str(elem) for elem in data)

        mycursor = mydb.cursor()
        sql = "SELECT * FROM "+str(DR1[ctVariabel[idPort][index] - 1])+" WHERE port_device='"+str(idPort)+"' AND id_device='"+str(
            indexMaster[idPort][index])+"' AND period = '"+str(period[idPort][index])+"' AND id_pool = '"+str(id_pool[idPort][index])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO "+str(DR1[ctVariabel[idPort][index] - 1])+"("+str(DR[ctVariabel[idPort][index] - 1])+", flag, id_pool, period, port_device, id_device) VALUES('"+str(
                listToString)+"', '"+str(0)+"','"+str(id_pool[idPort][index])+"','"+str(period[idPort][index])+"','"+str(idPort)+"','"+str(indexMaster[idPort][index])+"') "
            mycursor.execute(sql)
            mydb.commit()
            print(listToString)
        else:
            mycursor = mydb.cursor()
            sql = "UPDATE "+str(DR1[ctVariabel[idPort][index] - 1])+" SET "+str(DR[ctVariabel[idPort][index] - 1])+" = '"+str(listToString)+"', flag = '"+(str(0))+"' WHERE port_device='"+str(
                idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"' AND period='"+str(period[idPort][index])+"' "
            mycursor.execute(sql)
            mydb.commit()
            print(listToString)

        period[idPort][index] = 0

        mycursor = mydb.cursor()
        sql1 = "UPDATE dataRegister SET geser_register = '"+str(ctRegister[idPort][index])+"', geser_param = '"+str(ctVariabel[idPort][index] - 1)+"', period = '"+str(
            period[idPort][index])+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' "
        mycursor.execute(sql1)
        mydb.commit()

        if ctVariabel[idPort][index] > 5:
            ctVariabel[idPort][index] = 0
            ctRegister[idPort][index] = 0

            bentukFile(idPort, index, indexMaster[idPort][index])

            id_pool[idPort][index] += 1

            if id_pool[idPort][index] > 9:
                id_pool[idPort][index] = 0

            mycursor = mydb.cursor()
            sql = "UPDATE dataRegister SET geser_register = '"+str(ctRegister[idPort][index])+"', geser_param = '"+str(ctVariabel[idPort][index])+"', period = '"+str(
                period[idPort][index])+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
            mycursor.execute(sql)
            mydb.commit()

    elif flagModbus == 3:
        print(data)
        stringToList = data.split("*")

#        timeCurrent = datetime.now().strftime("%m/%d/%Y,%H:%M:%S")+'.' + \
#            str(waktuAwalDR[idPort][index]).rjust(3, '0').ljust(6, '0')
#        timeCurrent1 = datetime.now().strftime("%m/%d/%Y,%H:%M:%S")+'.' + \
#            str(waktuAkhirDR[idPort][index]).rjust(3, '0').ljust(6, '0')
#        timeCurrent2 = datetime.now().strftime("%m.%d.%Y %H.%M.%S")+'.' + \
#            str(waktuAkhirDR[idPort][index]).rjust(3, '0').ljust(6, '0')
        timeCurrent = waktuAwalDR[idPort][index].strftime("%Y/%m/%d %H:%M:%S.%f")
        timeCurrent1 = waktuAkhirDR[idPort][index].strftime("%Y/%m/%d %H:%M:%S.%f")
        timeCurrent2 = waktuAkhirDR[idPort][index].strftime("%m.%d.%Y %H.%M.%S")

        mycursor = mydb.cursor()
        sql = "SELECT * FROM it_cfg WHERE port_device='"+str(idPort)+"' AND id_device='"+str(
            indexMaster[idPort][index])+"' AND id_pool = '"+str(id_pool[idPort][index])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO it_cfg (micom_type, first_date, last_date, dr_count, ia_ratio, ib_ratio, ic_ratio, ie_ratio, id_micom, id_pool, flag, f_ratio, location, port_device, id_device, timeFile) VALUES('"+str(stringToList[0])+"','"+str(timeCurrent)+"', '"+str(timeCurrent1)+"','"+str(stringToList[1])+"','"+str(
                stringToList[2])+"','"+str(stringToList[3])+"','"+str(stringToList[4])+"','"+str(stringToList[5])+"','"+str(stringToList[6])+"','"+str(id_pool[idPort][index])+"','"+str(0)+"','"+str(stringToList[7])+"','"+str(rak_lokasi[idPort][index])+"','"+str(idPort)+"','"+str(indexMaster[idPort][index])+"','"+str(timeCurrent2)+"') "
            mycursor.execute(sql)
            mydb.commit()

        else:
            mycursor = mydb.cursor()
            sql = "UPDATE it_cfg SET micom_type = '"+str(stringToList[0])+"' , first_date = '"+str(timeCurrent)+"', last_date = '"+str(timeCurrent1)+"', dr_count = '"+str(stringToList[1])+"', ia_ratio = '"+str(stringToList[2])+"', ib_ratio = '"+str(stringToList[3])+"', ic_ratio = '"+str(stringToList[4])+"', ie_ratio = '"+str(
                stringToList[5])+"', id_micom = '"+str(stringToList[6])+"', flag = '"+str('0')+"', f_ratio = '"+str(stringToList[7])+"',location = '"+str(rak_lokasi[idPort][index])+"', timeFile = '"+str(timeCurrent2)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
            mycursor.execute(sql)
            mydb.commit()

    elif flagModbus == 5:
        dbCfg1 = ''
        dbCfg2 = ''
        dbCfg3 = ['', '']
        stringToList = data.split("*")

        x = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        mycursor = mydb.cursor()
        sql = "UPDATE device_list SET kondisi = '"+str(stringToList[2])+"', tanggal = '"+str(
            x)+"' WHERE port_type='"+str(idPort)+"' AND port_number='"+str(indexMaster[idPort][index])+"'"
        mycursor.execute(sql)
        mydb.commit()

#         statusRelay[idPort][index] = stringToList[2]

        mycursor = mydb.cursor()
        sql = "SELECT * FROM it_cfg WHERE port_device='"+str(idPort)+"' AND id_device='"+str(
            indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        for i in dbDR:
            dbCfg1 = i[15]

        mycursor = mydb.cursor()
        sql = "SELECT * FROM device_list WHERE port_type='" + \
            str(idPort)+"' AND port_number='" + \
            str(indexMaster[idPort][index])+"'"
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        for i in dbDR:
            dbCfg2 = i[2]

        if int(stringToList[2]) == 0:
            konversiStatus = 'healthy'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 8:
            konversiStatus = 'healthy'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 10:
            konversiStatus = 'alarm'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 11:
            konversiStatus = 'trip and alarm'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 12:
            konversiStatus = 'blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 26:
            konversiStatus = 'alarm tahap1 blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 27:
            konversiStatus = 'alarm tahap1 non blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 58:
            konversiStatus = 'alarm tahap2 blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 59:
            konversiStatus = 'alarm tahap2 non blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 122:
            konversiStatus = 'alarm tahap3 blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 123:
            konversiStatus = 'alarm tahap3 non blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 250:
            konversiStatus = 'alarm tahap4 blocking'
            statusRelay[idPort][index] = konversiStatus

        elif int(stringToList[2]) == 251:
            konversiStatus = 'alarm tahap4 non blocking'
            statusRelay[idPort][index] = konversiStatus

        mycursor = mydb.cursor()
        sql = "SELECT * FROM network"
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        for i in dbDR:
            dbCfg3[0] = i[5]
            dbCfg3[1] = i[7]
            
        bufwaktu= str(stringToList[3]).split(" ")
        dates =    bufwaktu[0].split("/")
        waktus = f"{dates[2]}/{dates[1]}/{dates[0]} {bufwaktu[1]}"

        if idPort == 0:
            d = {"machineCode": str(dbCfg3[1])
                 ,"relayId": str(stringToList[0])
                 , "lokasi": str(stringToList[1])
                 , "status": str(konversiStatus)
                 , "namaFile": str(dbCfg1) + ' Disturbance.000'
                 #, "waktu": str(stringToList[3])
                 , "waktu": waktus
                 , "flag": str(0)
                 , "type": str(dbCfg2)
                 , "portType": str(idPort)
                 , "portNumber": str(indexMaster[idPort][index])
                 }
        else:
            d = {"machineCode": str(dbCfg3[1])
               , "relayId": str(stringToList[0])
               , "lokasi": str(stringToList[1])
               , "status": str(konversiStatus)
               , "namaFile": str(dbCfg1) + ' Disturbance.000'
               #, "waktu": str(stringToList[3])
               , "waktu": waktus
               , "flag": str(0)
               , "type": str(dbCfg2)
               , "portType": str(idPort)
               , "portNumber": str(ip_address[idPort][index])
               }


#         response = requests.post("http://"+str(dbCfg3[0])+"/dms/fail/add", data=d)

        try:
            r = requests.post("http://"+str(dbCfg3[0])+"/mel/dms/fail/add", data=d)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)


def bentukFile(idPort, index, portNumber):

    dbCfg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    mycursor = mydb.cursor()
    sql = "SELECT * FROM it_cfg WHERE port_device='"+str(idPort)+"' AND id_device='"+str(
        indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb.commit()

    for i in dbDR:
        dbCfg[0] = i[0]
        dbCfg[1] = i[1]
        dbCfg[2] = i[2]
        dbCfg[3] = i[3]
        dbCfg[4] = i[4]
        dbCfg[5] = i[5]
        dbCfg[6] = i[6]
        dbCfg[7] = i[7]
        dbCfg[8] = i[8]
        dbCfg[11] = i[11]
        dbCfg[12] = i[12]
        dbCfg[15] = i[15]

    dirName = str(dbCfg[15])+" Disturbance.000"
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory ", dirName,  " Created ")
    else:
        print("Directory ", dirName,  " already exists")

    mycursor = mydb.cursor()

    sql = "SELECT DISTINCT it_ia.ia,it_ib.ib,it_ic.ic,it_ie.ie,it_f.f,it_relay.relay,it_ia.id_pool FROM it_ia \
        inner JOIN it_ib ON it_ib.period = it_ia.period\
        inner JOIN it_ic ON it_ic.period = it_ia.period\
        inner JOIN it_ie ON it_ie.period = it_ia.period\
        inner JOIN it_f ON it_f.period   = it_ia.period\
        inner JOIN it_relay ON it_relay.period = it_ia.period WHERE \
        it_ia.port_device = '"+str(idPort)+"' and\
        it_ib.port_device = '"+str(idPort)+"' and\
        it_ic.port_device = '"+str(idPort)+"' and\
        it_ie.port_device = '"+str(idPort)+"' and\
        it_f.port_device = '"+str(idPort)+"' and\
        it_relay.port_device = '"+str(idPort)+"' and\
        it_ia.id_device = '"+str(indexMaster[idPort][index])+"' and\
        it_ib.id_device = '"+str(indexMaster[idPort][index])+"' and\
        it_ic.id_device = '"+str(indexMaster[idPort][index])+"' and\
        it_ie.id_device = '"+str(indexMaster[idPort][index])+"' and\
        it_f.id_device = '"+str(indexMaster[idPort][index])+"' and\
        it_relay.id_device = '"+str(indexMaster[idPort][index])+"' and\
        it_ia.id_pool = '"+str(id_pool[idPort][index])+"'  and\
        it_ib.id_pool =  '"+str(id_pool[idPort][index])+"' and\
        it_ic.id_pool = '"+str(id_pool[idPort][index])+"' and\
        it_ie.id_pool =  '"+str(id_pool[idPort][index])+"' and\
        it_f.id_pool =  '"+str(id_pool[idPort][index])+"' and\
        it_relay.id_pool =  '"+str(id_pool[idPort][index])+"' and\
        it_ia.flag = 0  and\
        it_ib.flag = 0 and\
        it_ic.flag = 0 and\
        it_ie.flag = 0 and\
        it_f.flag = 0 and\
        it_relay.flag = 0\
        GROUP BY it_ia.period ORDER BY it_ia.period and\
        it_ib.period and\
        it_ic.period and\
        it_ie.period and\
        it_f.period and\
        it_relay.period asc"

    mycursor.execute(sql)
    dbDR = mycursor.fetchall()

    tes = [0, 0, 0, 0, 0, 0, 0]
    tes1 = ''
    tes2 = ''
    count = 0
    timefreq = 0
    for i in range(0, len(dbDR)):
        for j in range(0, (len(dbDR[i]))):
            tes[j] = dbDR[i][j].split('*')

        for k in range(0, len(tes[0])):
            count += 1
            tes[5][k] = ','.join(str(bin(int(tes[5][k]) % 256))[
                                 :1:-1].ljust(7, '0') + str(bin(int(tes[5][k]) >> 8))[2:].ljust(3, '0'))

            tes2 = tes[0][k]
            if tes2[0] == '-':
                tes[0][k] = '-'+str(tes[0][k])[1:].rjust(5, '0')
            else:
                tes[0][k] = str(tes[0][k]).rjust(6, '0')

            tes2 = tes[1][k]
            if tes2[0] == '-':
                tes[1][k] = '-'+str(tes[1][k])[1:].rjust(5, '0')
            else:
                tes[1][k] = str(tes[1][k]).rjust(6, '0')

            tes2 = tes[2][k]
            if tes2[0] == '-':
                tes[2][k] = '-'+str(tes[2][k])[1:].rjust(5, '0')
            else:
                tes[2][k] = str(tes[2][k]).rjust(6, '0')

            tes2 = tes[3][k]
            if tes2[0] == '-':
                tes[3][k] = '-'+str(tes[3][k])[1:].rjust(5, '0')
            else:
                tes[3][k] = str(tes[3][k]).rjust(6, '0')

            tes1 += str(count).rjust(10, '0') + ","+str(timefreq).rjust(10, '0')+","+str(tes[0][k]) + "," + str(tes[1][k]) + "," + str(
                tes[2][k]) + "," + str(tes[3][k]) + "," + str(int(10000 - (int(tes[4][k])/125*1000))).rjust(6, '0') + "," + str(tes[5][k])+""+"\n"
            timefreq += int(tes[4][k])
    print("BUILD FILE",dirName)
    #f = open("/home/pi/"+dirName+"/"+str(dirName)+".dat", "w")
    #f = open("/home/pi/Desktop/DMSv1.2/zipDR/"+dirName+"/"+str(dirName)+".dat", "w")
    f = open(""+dirName+"/"+str(dirName)+".dat","w")
    f.write(tes1)
    f.close()

    tes1 = ''
    count = 0

    tes1 += 'MiCOM '+str(dbCfg[0]) + ' BXXXXXX V11.C,' + str(dbCfg[8])+'\n'
    tes1 += '15,5A,10D\n'
    tes1 += '01,Ia,,, A,' + str(dbCfg[4]) + ','+'0.000000,0,-32768,32767\n'
    tes1 += '02,Ib,,, A,' + str(dbCfg[5]) + ','+'0.000000,0,-32768,32767\n'
    tes1 += '03,Ic,,, A,' + str(dbCfg[6]) + ','+'0.000000,0,-32768,32767\n'
    tes1 += '04,Ie,,, A,' + str(dbCfg[7]) + ','+'0.000000,0,-32768,32767\n'
    tes1 += '05,Frequency,,, Hz,' + \
        str('0.010000') + ','+'0.000000,0,-32768,32767\n'
    tes1 += '01,Relay 1 (Trip),0\n'
    tes1 += '02,Relay 2,0\n'
    tes1 += '03,Relay 3,0\n'
    tes1 += '04,Relay 4,0\n'
    tes1 += '05,Relay 0 (Watchdog),0\n'
    tes1 += '06,Relay 5,0\n'
    tes1 += '07,Relay 6,0\n'
    tes1 += '08,Digital Input 1,0\n'
    tes1 += '09,Digital Input 2,0\n'
    tes1 += '10,Digital Input 3,0\n'
    tes1 += str(dbCfg[11]) + '\n'
    tes1 += '0\n'
    tes1 += '0,'+str(dbCfg[3]) + '\n'
    tes1 += str(dbCfg[1]) + '\n'
    tes1 += str(dbCfg[2]) + '\n'
    tes1 += str('ASCII') + '\n'

    #f = open("/home/pi/"+dirName+"/"+str(dirName)+".cfg", "w")
    f = open(""+dirName+"/"+str(dirName)+".cfg","w")
    f.write(tes1)
    f.close()
    tes1 = ''

    #with ZipFile('/home/pi/Desktop/DMSv1.2/zipDR/' + dirName + '.zip', 'w') as zipObj: #perubahan 15-07-2024
    with ZipFile('/var/www/html/dms_setting/assets/api/file_dr/'+ dirName +'.zip', 'w') as zipObj: #perubahan 15-07-2024
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, compress_type=zipfile.ZIP_DEFLATED)

    if not os.path.exists('/home/pi/' + dirName):
        print("Folder ", dirName,  " tidak tersedia ")
    else:
        shutil.rmtree('/home/pi/'+dirName)
        print("Folder telah dihapus")

    buffFileDR = ''
    buffstatusFileDR = ''
    buffwaktuFileDR = ''
    bufflokasiFileDR = ''
    
    #dr_file = '/home/pi/Desktop/DMSv1.2/zipDR/' + dirName + '.zip' #sebelum perubahan 15-07-2024
    dr_file = '/var/www/html/dms_setting/assets/api/file_dr/' + dirName +'.zip' #perubahan 15-07-2024
    #hconn_send(dr_file)
    #hconn_send(0,dr_file,dirName,idPort ,str(statusRelay[idPort][index])) #sebelum perubahan 15-07-2024
    hconn_send(0,dr_file,dirName,portNumber ,str(statusRelay[idPort][index])) #perubahan 15-07-2024

    if int(indexFileDR[idPort][index]) < 10:
        indexFileDR[idPort][index] += 1
        buffFileDR = str(dirName+'.zip,')
        buffwaktuFileDR = str(dbCfg[2])+','
        bufflokasiFileDR = str(dbCfg[12])+','
        buffstatusFileDR = str(statusRelay[idPort][index])+','

        fileDR[idPort][index] += buffFileDR
        statusFileDR[idPort][index] += buffstatusFileDR
        waktuFileDR[idPort][index] += buffwaktuFileDR
        lokasiFileDR[idPort][index] += bufflokasiFileDR

        mycursor = mydb.cursor()
        sql = "UPDATE fileDR SET data = '"+str(fileDR[idPort][index])+"', jumlah_data = '"+str(indexFileDR[idPort][index])+"', status = '"+str(statusFileDR[idPort][index])+"', waktu = '"+str(
            waktuFileDR[idPort][index])+"', lokasi = '"+str(lokasiFileDR[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
        mycursor.execute(sql)
        mydb.commit()

    else:
        buffwaktuFileDR = str(dbCfg[2])+','
        bufflokasiFileDR = str(dbCfg[12])+','
        buffstatusFileDR = str(statusRelay[idPort][index])+','

        tes = fileDR[idPort][index].split(',')
        tes1 = statusFileDR[idPort][index].split(',')
        tes2 = waktuFileDR[idPort][index].split(',')
        tes3 = lokasiFileDR[idPort][index].split(',')
        print(tes[0])
        #if os.path.exists('/home/pi/Desktop/DMSv1.2/zipDR'): #sebelum perubahan 15-07-2024
        if os.path.exists('/var/www/html/dms_setting/assets/api/file_dr/'): #perubahan 15-07-2024
            print("removed Files")
            #os.remove('/home/pi/Desktop/DMSv1.2/zipDR/'+str(tes[0])) #sebelum perubahan 15-07-2024
        else:
            print("File tidak ditemukan")

        for i in range(1, 10):
            tes[i-1] = tes[i]
            tes1[i-1] = tes1[i]
            tes2[i-1] = tes2[i]
            tes3[i-1] = tes3[i]

            if i == 9:
                tes[i] = str(dirName+".zip")
                tes1[i] = str(buffstatusFileDR)
                tes2[i] = str(buffwaktuFileDR)
                tes3[i] = str(bufflokasiFileDR)
                fileDR[idPort][index] = ','.join(str(elem) for elem in tes)
                statusFileDR[idPort][index] = ','.join(
                    str(elem) for elem in tes1)
                waktuFileDR[idPort][index] = ','.join(
                    str(elem) for elem in tes2)
                lokasiFileDR[idPort][index] = ','.join(
                    str(elem) for elem in tes3)

        mycursor = mydb.cursor()
        sql = "UPDATE fileDR SET data = '"+str(fileDR[idPort][index])+"', jumlah_data = '"+str(indexFileDR[idPort][index])+"', status = '"+str(statusFileDR[idPort][index])+"', waktu = '"+str(
            waktuFileDR[idPort][index])+"', lokasi = '"+str(lokasiFileDR[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
        mycursor.execute(sql)
        mydb.commit()

#     files={'document':open('/home/pi/Desktop/DMSv1.2/zipDR/'+ dirName +'.zip','rb')}
#     resp = requests.post('https://api.telegram.org/bot1607521967:AAErjzP0St1Y2_p44ZsWwJgIzXEjQJNsHTQ/sendDocument?chat_id=712281930',files = files)
#     print(resp.status_code)

#def hconn_send(tipe_url,dr_file,dirName,idPort,status) :
#    dbCfg = ''
#    print(dr_file)
#    print("====")
#    print(status)
#    print("##########")
#    mycursor = mydb.cursor()
#    sql = "select network.*,device_list.* from device_list cross join network where device_list.port_number = 0"
#    mycursor.execute(sql)
#    dbDR = mycursor.fetchall()
#    mydb.commit()
#    buffName = dirName.split(" ")
#    bufftanggal = buffName[0].split(".")
#    tanggal=bufftanggal[2]+"-"+bufftanggal[0]+"-"+bufftanggal[1]
#    buffwaktu =buffName[1].split(".")
#    waktu =buffwaktu[0]+":"+buffwaktu[1]
#    print(dbDR)
#    for i in dbDR:
#        dbCfg = i[5]
#        machineCode =i[7]
#        lokasi =i[21]
#        type =i[17]
#        relay_id=i[16]
#    url=""
#    if(tipe_url==0):
#        url = 'http://'+str(dbCfg)+'/mel/dms/notif'
#    else:
#        url = 'http://'+str(dbCfg)+'/mel/dms/notif'
#    file = {'myfile': open(dr_file,'rb')}
#    dataReq={'status':status,'file_name':dirName,'machine_code':machineCode,'lokasi':lokasi,'type':type,'tanggal':tanggal,'waktu':waktu,'relay_id':relay_id,'port':idPort}
#    print(dataReq)
#    try:
#        r = requests.post(url,  data=dataReq,files=file,verify=False)
#        if r.status_code != 200:
#            print('sendErr: '+r.url)
#        else :
#            print(r.text)
#        
#    except:
#        print("request file Event ")

def hconn_send(tipe_url,dr_file,dirName,portNumber,status) :
    dbCfg = ''
    print("idPort: ",portNumber)
    print(dr_file)
    print("====")
    print(status)
    print("##########")
    mycursor = mydb.cursor()
    sql = "SELECT  network.* ,device_list.*from device_list cross join network where device_list.port_type = 0 and port_number = "+str(portNumber)
    print(sql)
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb.commit()
    buffName = dirName.split(" ")
    bufftanggal = buffName[0].split(".")
    tanggal=bufftanggal[2]+"-"+bufftanggal[0]+"-"+bufftanggal[1]
    buffwaktu =buffName[1].split(".")
    waktu =buffwaktu[0]+":"+buffwaktu[1]
    print(dbDR)
    for i in dbDR:
        dbCfg = i[5]
        machineCode =i[7]
        lokasi =i[21]
        type =i[17]
        relay_id=i[16]
    url=""
    if(tipe_url==0):
        url = 'http://'+str(dbCfg)+'/mel/dms/notif'
    else:
        url = 'http://'+str(dbCfg)+'/mel/dms/notif'
    file = {'myfile': open(dr_file,'rb')}
    dataReq={'status':status,'file_name':dirName,'machine_code':machineCode,'lokasi':lokasi,'type':type,'tanggal':tanggal,'waktu':waktu,'relay_id':relay_id,'port':portNumber}
    print(dataReq)
    status=str(dataReq).replace("'", "\"")
    try:
        r = requests.post(url,  data=dataReq,files=file,verify=False)
        if r.status_code != 200:
            #print('sendErr: '+r.url)
            print("ERROR")
            #perubahan 15-07-2024
            #query= f"insert into it_file_iec (domain_id,item_id,id_device,ip_address) values('{domainId}','{itemId}','{relayId}','{ip}')"
            sql = f"INSERT INTO fileDR_temp (port_device,id_device,status,flag,nama) values('{portNumber}','{relay_id}','{status}','{0}','{dirName}')"
            mycursor.execute(sql)
            mydb.commit()
            #perubahan 15-07-2024
        else :
            print("SUCCESS")
            #print(r.text)
            #perubahan 15-07-2024
            #query= f"insert into it_file_iec (domain_id,item_id,id_device,ip_address) values('{domainId}','{itemId}','{relayId}','{ip}')"
            sql = f"INSERT INTO fileDR_temp (port_device,id_device,status,flag,nama) values('{portNumber}','{relay_id}','{status}','{1}','{dirName}')"
            mycursor.execute(sql)
            mydb.commit()
            #perubahan 15-07-2024
            
        
    except:
        print("request file Event ")


def config():
    print("------------------Micom P122---------------------------")
    DR1 = ['it_ia', 'it_ib', 'it_ic', 'it_ie', 'it_f', 'it_relay']
    DR = ['ia', 'ib', 'ic', 'ie', 'f', 'relay']
    idHr = arr.array('i', [0, 1, 2, 3, 4, 5])
    idDR = arr.array('i', [0, 14336, 14592, 14848, 15104, 15360])
    dtRegister = arr.array('i', [15616, idDR[1], 0, 8704, 12, 2048, 2304, 2429, 2560, 2685, 2816, 2941, 3072, 3197, 3328, 3453, 3584, 3709, 3840, 3965,
                           4096, 4221, 4352, 4477, 4608, 4733, 4864, 4989, 5120, 5245, 5376, 5501, 5632, 5757, 5888, 6013, 6144, 6269, 6400, 6525, 6656, 6781, 6912, 7037, 7168])

    resetData()

    global buffcekKoneksi
    global buffcekKoneksi1

    for i in range(0, 10):
        idPort = 0
        mycursor = mydb.cursor()
        sql = "SELECT * FROM scan_port WHERE port_device='" + \
            str(idPort)+"' and id_device='"+str(i)+"'"
        mycursor.execute(sql)
        dbStatus = mycursor.fetchall()
        mydb.commit()

        if len(dbStatus) <= 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO scan_port(port_device, id_device, status) VALUES('"+str(
                idPort)+"', '"+str(i)+"', '"+str(0)+"') "
            mycursor.execute(sql)
            mydb.commit()

            cekStatus = ModbusClient(method='rtu', port='/dev/ttyUSB'+str(
                i),  stopbits=1, bytesize=8, parity='N', baudrate=19200, timeout=.500)
            connection = cekStatus.connect()
            if connection:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '" + \
                    str(1)+"' WHERE port_device='"+str(idPort) + \
                    "' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()
            else:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '" + \
                    str(0)+"' WHERE port_device='"+str(idPort) + \
                    "' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()

        else:
            cekStatus = ModbusClient(method='rtu', port='/dev/ttyUSB'+str(
                i),  stopbits=1, bytesize=8, parity='N', baudrate=19200, timeout=.500)
            connection = cekStatus.connect()
            if connection:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '" + \
                    str(1)+"' WHERE port_device='"+str(idPort) + \
                    "' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()
            else:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '" + \
                    str(0)+"' WHERE port_device='"+str(idPort) + \
                    "' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()

    for i in range(0, len(dbList)):
        mycursor = mydb.cursor()
        sql = "SELECT * FROM device_list WHERE port_type='"+str(i)+"'"
        mycursor.execute(sql)
        dbList[i] = mycursor.fetchall()
        mydb.commit()

        buff_client.append([0 for x in range(0, len(dbList[i]))])
        buff_ctRegister.append([0 for x in range(0, len(dbList[i]))])
        buff_ctVariabel.append([0 for x in range(0, len(dbList[i]))])
        buffDR.append([0 for x in range(0, len(dbList[i]))])
        buff_jmlData.append([0 for x in range(0, len(dbList[i]))])
        ratio.append([1 for x in range(0, len(dbList[i]))])
        ratio1.append([1 for x in range(0, len(dbList[i]))])
        totRatio.append([1 for x in range(0, len(dbList[i]))])
        totRatio1.append([1 for x in range(0, len(dbList[i]))])
        prDevice.append([0 for x in range(0, len(dbList[i]))])
        freq.append([0 for x in range(0, len(dbList[i]))])
        statusReg.append([0 for x in range(0, len(dbList[i]))])
        buff.append([0 for x in range(0, len(dbList[i]))])
        buff_period.append([0 for x in range(0, len(dbList[i]))])
        buff_id_pool.append([0 for x in range(0, len(dbList[i]))])
        tanggal.append([0 for x in range(0, len(dbList[i]))])
        bulan.append([0 for x in range(0, len(dbList[i]))])
        tahun.append([0 for x in range(0, len(dbList[i]))])
        jam.append([0 for x in range(0, len(dbList[i]))])
        menit.append([0 for x in range(0, len(dbList[i]))])
        detik.append([0 for x in range(0, len(dbList[i]))])
        buff_id_micom.append([0 for x in range(0, len(dbList[i]))])
        buff_type_relay.append([0 for x in range(0, len(dbList[i]))])
        buff_port_address.append([0 for x in range(0, len(dbList[i]))])
        buff_rak_lokasi.append([0 for x in range(0, len(dbList[i]))])
        buff_baudrate.append([0 for x in range(0, len(dbList[i]))])
        ip_address.append([0 for x in range(0, len(dbList[i]))])
        dns.append([0 for x in range(0, len(dbList[i]))])
        netmask.append([0 for x in range(0, len(dbList[i]))])
        gateway.append([0 for x in range(0, len(dbList[i]))])
        buff_ip_address.append([0 for x in range(0, len(dbList[i]))])
        buff_stop_bit.append([0 for x in range(0, len(dbList[i]))])
        buff_parity.append([0 for x in range(0, len(dbList[i]))])
        buff_byte_size.append([0 for x in range(0, len(dbList[i]))])
        buff_dbDR1.append([0 for x in range(0, len(dbList[i]))])
        waktuAwalDR.append([0 for x in range(0, len(dbList[i]))])
        waktuAkhirDR.append([0 for x in range(0, len(dbList[i]))])
        id_micom.append([0 for x in range(0, len(dbList[i]))])
        type_relay.append([0 for x in range(0, len(dbList[i]))])
        port_address.append([0 for x in range(0, len(dbList[i]))])
        rak_lokasi.append([0 for x in range(0, len(dbList[i]))])
        baudrate.append([0 for x in range(0, len(dbList[i]))])
        stop_bit.append([0 for x in range(0, len(dbList[i]))])
        parity.append([0 for x in range(0, len(dbList[i]))])
        byte_size.append([0 for x in range(0, len(dbList[i]))])
        ctRegister.append([0 for x in range(0, len(dbList[i]))])
        ctVariabel.append([0 for x in range(0, len(dbList[i]))])
        period.append([0 for x in range(0, len(dbList[i]))])
        id_pool.append([0 for x in range(0, len(dbList[i]))])
        jmlData.append([0 for x in range(0, len(dbList[i]))])
        dbDR1.append([0 for x in range(0, len(dbList[i]))])
        indexMaster.append([0 for x in range(0, len(dbList[i]))])
        hitungError.append([0 for x in range(0, len(dbList[i]))])
        buff_hitungError.append([0 for x in range(0, len(dbList[i]))])
        indexPort.append([0 for x in range(0, len(dbList[i]))])
        hitungLoop.append([0 for x in range(0, len(dbList[i]))])
        buff_hitungLoop.append([0 for x in range(0, len(dbList[i]))])
        statusRelay.append([0 for x in range(0, len(dbList[i]))])
        fileDR.append([0 for x in range(0, len(dbList[i]))])
        buff_fileDR.append([0 for x in range(0, len(dbList[i]))])
        indexFileDR.append([0 for x in range(0, len(dbList[i]))])
        buff_indexFileDR.append([0 for x in range(0, len(dbList[i]))])
        statusFileDR.append([0 for x in range(0, len(dbList[i]))])
        buff_statusFileDR.append([0 for x in range(0, len(dbList[i]))])
        waktuFileDR.append([0 for x in range(0, len(dbList[i]))])
        buff_waktuFileDR.append([0 for x in range(0, len(dbList[i]))])
        lokasiFileDR.append([0 for x in range(0, len(dbList[i]))])
        buff_lokasiFileDR.append([0 for x in range(0, len(dbList[i]))])
        relayTeks.append([0 for x in range(0, len(dbList[i]))])
        buff_mode.append([0 for x in range(0, len(dbList[i]))])
        mode.append([0 for x in range(0, len(dbList[i]))])

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

        mycursor = mydb.cursor()
        sql = "SELECT * FROM dataRegister WHERE port_device='" + \
            str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO dataRegister(port_device, id_device, geser_register, geser_param, period, id_pool, jumlah_data, indexDR, indexError, indexLoop,flagDtDR,flagDtDR1,flag,dateDR) VALUES('"+str(idPort)+"', '"+str(
                indexPort[idPort][i])+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"','"+str(0)+"', '"+str(4800)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"') "
            mycursor.execute(sql)
            mydb.commit()
            buff_ctRegister[idPort][i] = 0
            buff_ctVariabel[idPort][i] = 0
            buff_period[idPort][i] = 0
            buff_id_pool[idPort][i] = 0
            buff_jmlData[idPort][i] = 4800
            buff_dbDR1[idPort][i] = 0
            buff_hitungError[idPort][i] = 0
            buff_hitungLoop[idPort][i] = 0
        else:
            for j in dbDR:
                buff_ctRegister[idPort][i] = int(j[2])
                buff_ctVariabel[idPort][i] = int(j[3])
                buff_period[idPort][i] = int(j[4])
                buff_id_pool[idPort][i] = int(j[5])
                buff_jmlData[idPort][i] = int(j[6])
                buff_dbDR1[idPort][i] = int(j[7])
                buff_hitungError[idPort][i] = int(j[8])
                buff_hitungLoop[idPort][i] = int(j[9])

        mycursor = mydb.cursor()
        sql = "SELECT * FROM fileDR WHERE port_device='" + \
            str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            sql = "INSERT INTO fileDR(port_device, id_device, data, jumlah_data, status, waktu, lokasi) VALUES('"+str(
                idPort)+"', '"+str(indexPort[idPort][i])+"', '""','"+str(0)+"', '""', '""', '""') "
            mycursor.execute(sql)
            mydb.commit()

            buff_fileDR[idPort][i] = ''
            buff_waktuFileDR[idPort][i] = ''
            buff_statusFileDR[idPort][i] = ''
            buff_lokasiFileDR[idPort][i] = ''
            buff_indexFileDR[idPort][i] = int(0)

        else:
            buff_fileDR[idPort][i] = str(dbDR[0][2])
            buff_indexFileDR[idPort][i] = int(dbDR[0][3])
            buff_waktuFileDR[idPort][i] = str(dbDR[0][5])
            buff_statusFileDR[idPort][i] = str(dbDR[0][4])
            buff_lokasiFileDR[idPort][i] = str(dbDR[0][6])

        connection = buff_client[idPort][i].connect()
        if connection:
            baca = buff_client[idPort][i].read_holding_registers(
                address=15616, count=36, unit=int(buff_id_micom[idPort][i]))

            if baca.isError():
                print('Port'+str(indexPort[idPort][i]) +
                      ' RS-485 tidak dapat menerima data')

            elif buff_type_relay[idPort][i] == 'MICOM P122':
                baca = buff_client[idPort][i].read_holding_registers(
                    address=0, count=2, unit=int(buff_id_micom[idPort][i]))
                relayTeks[idPort][hitung] = chr(baca.registers[0] >> 8) + chr(
                    baca.registers[0] % 256) + chr(baca.registers[1] >> 8) + chr(baca.registers[1] % 256)

                buffcekKoneksi.append(buff_client[idPort][i])

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

                ctRegister[idPort][hitung] = buff_ctRegister[idPort][i]
                ctVariabel[idPort][hitung] = buff_ctVariabel[idPort][i]
                period[idPort][hitung] = buff_period[idPort][i]
                id_pool[idPort][hitung] = buff_id_pool[idPort][i]
                jmlData[idPort][hitung] = buff_jmlData[idPort][i]
                dbDR1[idPort][hitung] = buff_dbDR1[idPort][i]
                hitungError[idPort][hitung] = buff_hitungError[idPort][i]
                hitungLoop[idPort][hitung] = buff_hitungLoop[idPort][i]

                fileDR[idPort][hitung] = buff_fileDR[idPort][i]
                indexFileDR[idPort][hitung] = buff_indexFileDR[idPort][i]
                statusFileDR[idPort][hitung] = buff_statusFileDR[idPort][i]
                waktuFileDR[idPort][hitung] = buff_waktuFileDR[idPort][i]
                lokasiFileDR[idPort][hitung] = buff_lokasiFileDR[idPort][i]

                hitung += 1

        else:
            print('Port'+str(indexPort[idPort][i])+' RS-485 tidak terhubung')

    client.append(buffcekKoneksi)

    hitung = 0
    for i in range(0, len(dbList[1])):
        idPort = 1

        buff_id_micom[idPort][i] = dbList[idPort][i][1]
        buff_type_relay[idPort][i] = dbList[idPort][i][2]
        indexPort[idPort][i] = dbList[idPort][i][4]
        buff_port_address[idPort][i] = dbList[idPort][i][5]
        buff_rak_lokasi[idPort][i] = dbList[idPort][i][6]
        buff_ip_address[idPort][i] = dbList[idPort][i][8]

        buff_client[idPort][i] = ModbusClientTcp(host=str(
            buff_ip_address[idPort][i]), port=int(buff_port_address[idPort][i]), timeout=.500)

        mycursor = mydb.cursor()
        sql = "SELECT * FROM dataRegister WHERE port_device='" + \
            str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO dataRegister(port_device, id_device, geser_register, geser_param, period, id_pool, jumlah_data, indexDR, indexError, indexLoop,flagDtDR,flagDtDR1,flag,dateDR) VALUES('"+str(idPort)+"', '"+str(
                indexPort[idPort][i])+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"','"+str(0)+"', '"+str(4800)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"') "
            mycursor.execute(sql)
            mydb.commit()

            buff_ctRegister[idPort][i] = 0
            buff_ctVariabel[idPort][i] = 0
            buff_period[idPort][i] = 0
            buff_id_pool[idPort][i] = 0
            buff_jmlData[idPort][i] = 4800
            buff_dbDR1[idPort][i] = 0
            buff_hitungError[idPort][i] = 0
            buff_hitungLoop[idPort][i] = 0

        else:
            for j in dbDR:
                buff_ctRegister[idPort][i] = int(j[2])
                buff_ctVariabel[idPort][i] = int(j[3])
                buff_period[idPort][i] = int(j[4])
                buff_id_pool[idPort][i] = int(j[5])
                buff_jmlData[idPort][i] = int(j[6])
                buff_dbDR1[idPort][i] = int(j[7])
                buff_hitungError[idPort][i] = int(j[8])
                buff_hitungLoop[idPort][i] = int(j[9])

        mycursor = mydb.cursor()
        sql = "SELECT * FROM fileDR WHERE port_device='" + \
            str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()

        if len(dbDR) == 0:
            sql = "INSERT INTO fileDR(port_device, id_device, data, jumlah_data, status, waktu, lokasi) VALUES('"+str(
                idPort)+"', '"+str(indexPort[idPort][i])+"', '""','"+str(0)+"', '""', '""', '""') "
            mycursor.execute(sql)
            mydb.commit()

            buff_fileDR[idPort][i] = ''
            buff_waktuFileDR[idPort][i] = ''
            buff_statusFileDR[idPort][i] = ''
            buff_lokasiFileDR[idPort][i] = ''
            buff_indexFileDR[idPort][i] = int(0)

        else:
            buff_fileDR[idPort][i] = str(dbDR[0][2])
            buff_indexFileDR[idPort][i] = int(dbDR[0][3])
            buff_waktuFileDR[idPort][i] = str(dbDR[0][5])
            buff_statusFileDR[idPort][i] = str(dbDR[0][4])
            buff_lokasiFileDR[idPort][i] = str(dbDR[0][6])

        connection = buff_client[idPort][i].connect()
        if connection:
            if baca.isError():
                print(
                    'IP '+str(buff_ip_address[idPort][i])+' Tcp/Ip tidak dapat menerima data')

            else:
                baca = buff_client[idPort][i].read_holding_registers(
                    address=0, count=2, unit=int(buff_id_micom[idPort][i]))
                relayTeks[idPort][hitung] = chr(baca.registers[0] >> 8) + chr(
                    baca.registers[0] % 256) + chr(baca.registers[1] >> 8) + chr(baca.registers[1] % 256)

                buffcekKoneksi1.append(buff_client[idPort][i])

                indexMaster[idPort][hitung] = str(indexPort[idPort][i])
                id_micom[idPort][hitung] = buff_id_micom[idPort][i]
                type_relay[idPort][hitung] = buff_type_relay[idPort][i]
                port_address[idPort][hitung] = buff_port_address[idPort][i]
                rak_lokasi[idPort][hitung] = buff_rak_lokasi[idPort][i]
                ip_address[idPort][hitung] = buff_ip_address[idPort][i]

                ctRegister[idPort][hitung] = buff_ctRegister[idPort][i]
                ctVariabel[idPort][hitung] = buff_ctVariabel[idPort][i]
                period[idPort][hitung] = buff_period[idPort][i]
                id_pool[idPort][hitung] = buff_id_pool[idPort][i]
                jmlData[idPort][hitung] = buff_jmlData[idPort][i]
                dbDR1[idPort][hitung] = buff_dbDR1[idPort][i]
                hitungError[idPort][hitung] = buff_hitungError[idPort][i]
                hitungLoop[idPort][hitung] = buff_hitungLoop[idPort][i]

                fileDR[idPort][hitung] = buff_fileDR[idPort][i]
                indexFileDR[idPort][hitung] = buff_indexFileDR[idPort][i]
                statusFileDR[idPort][hitung] = buff_statusFileDR[idPort][i]
                waktuFileDR[idPort][hitung] = buff_waktuFileDR[idPort][i]
                lokasiFileDR[idPort][hitung] = buff_lokasiFileDR[idPort][i]

                hitung += 1

        else:
            print('IP '+str(buff_ip_address[idPort]
                  [i])+' Tcp/Ip tidak terhubung')

    client.append(buffcekKoneksi1)
    print(client)


def resetData():
    buff_fileDR.clear()
    fileDR.clear()

    waktuFileDR.clear()
    buff_waktuFileDR.clear()

    statusFileDR.clear()
    buff_statusFileDR.clear()

    lokasiFileDR.clear()
    buff_lokasiFileDR.clear()

    buff_indexFileDR.clear()
    indexFileDR.clear()

    statusRelay.clear()
    hitungError.clear()
    buff_hitungError.clear()

    hitungLoop.clear()
    buff_hitungLoop.clear()

    indexPort.clear()

    client.clear()
    indexMaster.clear()
    buff_client.clear()
    ctRegister.clear()
    buff_ctRegister.clear()
    ctVariabel.clear()
    buff_ctVariabel.clear()
    jmlData.clear()
    buff_jmlData.clear()
    period.clear()
    buff_period.clear()
    id_pool.clear()
    buff_id_pool.clear()

    buffDR.clear()
    ratio.clear()
    ratio1.clear()
    totRatio.clear()
    totRatio1.clear()
    prDevice.clear()
    freq.clear()
    statusReg.clear()
    buff.clear()
    tanggal.clear()
    bulan.clear()
    tahun.clear()
    jam.clear()
    menit.clear()
    detik.clear()
    dns.clear()
    netmask.clear()
    gateway.clear()
    waktuAwalDR.clear()
    waktuAkhirDR.clear()
    buffcekKoneksi.clear()
    buffcekKoneksi1.clear()

    id_micom.clear()
    buff_id_micom.clear()
    type_relay.clear()
    buff_type_relay.clear()
    port_address.clear()
    buff_port_address.clear()
    rak_lokasi.clear()
    buff_rak_lokasi.clear()
    baudrate.clear()
    buff_baudrate.clear()
    ip_address.clear()
    buff_ip_address.clear()
    stop_bit.clear()
    buff_stop_bit.clear()
    parity.clear()
    buff_parity.clear()
    byte_size.clear()
    buff_byte_size.clear()
    dbDR1.clear()
    buff_dbDR1.clear()
    mode.clear()
    buff_mode.clear()
    relayTeks.clear()


# config()
#
# while True :
#     if not client[0] and not client[1]:
#         print("data RS-485 kosong")
#         config()
#         time.sleep(5)
#
#     else:
#         for i in range(0, len(client[0])):
#             idPort = 0
#             dataReg(idPort, i)
#
#             if flag == True and i == int(len(client[0])-1):
#                 config()
#                 flag = False
#
#             if flag1 == True and i == int(len(client[0])-1):
#                 config()
#                 flag1 = False
#
#
#     if not client[1] and not client[0]:
#         print("data Tcp/Ip kosong")
#         config()
#         time.sleep(5)
#
#     else:
#         for i in range(0, len(client[1])):
#             idPort = 1
#             dataReg(idPort, i)
#
#             if flag == True and i == int(len(client[1])-1):
#                 config()
#                 flag = False
#
#             if flag1 == True and i == int(len(client[1])-1):
#                 config()
#                 flag1 = False
