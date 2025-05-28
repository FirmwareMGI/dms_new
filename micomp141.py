from ctypes import pythonapi
import serial
import mysql.connector
import time

import zipfile
from zipfile import ZipFile
import os
from os.path import basename

import shutil
import requests



flag2 = False
flag1 = False


buffer = []
register =[]
dbList = [0, 0]

countflagbuff = 0

buffcekKoneksi = []
buffcekKoneksi1 = []

relayTeks = []

pollDtDR = []
buffPollDtDR = []

buff_id_pool = []
id_pool = []
flag  = [] 
buff_flagDtDR = []
flagDtDR = []
buff_flagDtDR1 = []
flagDtDR1 = []
buff_flagCF = []
flagCF = []
tanggal = []
bulan = []
tahun = []
jam = []
menit = []
detik = []
buff_DRdate = []
DRdate = []
buff_id_Micom = []
id_Micom = []
buff_count = []
count = []
buff_count3 = []
count3 = []
buff_countCH = []
countCH = []
countCF = []
buffBanyakData = []
buffPanjangDataASDU = []
buffAddrASDU = []
buffCF = []
buffAddrASDUIn = []
buffIOA = []
buffindexDR = []
buff_indexDR = []
indexDR = []
indexNewDRLSB = []
indexNewDRMSB = []
buff_jmlDtDR = []
jmlDtDR = []
freq = []
nameRelay = []
buff_ser = []
ser = []
indexPort = []
buff_baudrate = []
baudrate = []
buff_parity = []
parity = []
buff_stop_bit = []
stop_bit = []
buff_byte_size = []
byte_size = []
buff_hitungError = []
hitungError = []
buff_hitungLoop = []
hitungLoop = []
buff_fileDR = []
buff_indexFileDR = []
buff_waktuFileDR = []
buff_statusFileDR = [] 
buff_lokasiFileDR = []
fileDR = []
indexFileDR = []
waktuFileDR = []
statusFileDR = []
lokasiFileDR = []
indexMaster = []
buff_type_relay = []
type_relay = []
buff_rak_lokasi = []
rak_lokasi = []
buff_statusRelay = []
statusRelay = []
statusRelay1 = []
buff_mode = []
mode = []
buff_port_address = []
port_address = []

lbdigitalCFG = []
strdigitalCFG = ''








# ser = serial.Serial(port = 'COM32', baudrate = 19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize= serial.EIGHTBITS,timeout = 0 )

VA = [32,180]
VB = [33,180]
VC = [34,180]
IA = [35,180]
IB = [36,180]
IC = [37,180]
IN = [38,180]
INSensitive = [39,180]
Frequency = [40,180]

regChangevalueAddr = [[20 ,180],VA,VB,VC,IA,IB,IC,IN,INSensitive,Frequency,[62 ,180],[63 ,180]]
labelChangevalueAddr = ['it_waktup141','it_vap141','it_vbp141','it_vcp141','it_iap141','it_ibp141','it_icp141','it_inp141','it_insensitivep141','it_fp141','it_orp141','it_inlp141']

regLengthASDU = [7,7,11,7,10,5,47,7,6,6,6,7,7,7,7,7,7,6,6,6,7,6,6,6]
regCF = [123,91]
# regAddRTU = [id_Micom[idPort][index],id_Micom[idPort][index],id_Micom[idPort][index],id_Micom[idPort][index],id_Micom[idPort][index],1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
regTypeID = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
regVSQ = [7,7,7,7,7,5,7,7,6,6,6,7,7,7,7,7,7,6,6,6,7,6,6,6]
regCOT = [20,20,20,21,64,78,20,25,33,33,33,20,20,20,20,20,25,33,33,33,25,33,33,33]
regAddRTU1 = [[2,191],[1,180],[1,191,7,20,2,191],[1,180],[1,180,42,0,0],[0],[5,0,7,20,9,0,7,20,2,179,7,20,1,180,7,20,2,180,7,20,3,180,7,20,4,180,7,20,16,180,7,20,17,180,7,20,18,180,7,20,19,180],[3,180],[0],[1],[2],[5,180],[6,180],[7,180],[8,180],[9,180],[62,180],[0],[1],[2],[63,180],[0],[1],[2]]


flagIndex = []
flagIndex1 = []

analogCFG = ['','','','','','','','','']
digitalCFG = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
scalAnalogCFG = [0,0,0,0,0,0,0,0,0]
skewValCFG = [0,0,0,0,0,0,0,0,0]
minValueCFG = [0,0,0,0,0,0,0,0,0]
maxValueCFG = [0,0,0,0,0,0,0,0,0]
ratioscalAnalogCFG = [0,0,0,0,0,0,0,0,0]


mydb = mysql.connector.connect(
    host = "localhost",
    user = "dms",
    password = "mgi",
    database = "dms"
    )


mydb1 = mysql.connector.connect(
    host = "localhost",
    user = "dms",
    password = "mgi",
    database = "dms1"
    )        


def Writeregister(idPort,index, panjangData, CF, addRTU, TypeID, VSQ, COT, addRTU1 ):
#     buffaddRTU1 = ''
#     buffaddRTU1 =
#     print(addRTU1)
    register = [0]*(panjangData + 6)

    # ---------------header and CF-------------------
    register[0] = register[3] = 104
    register[1] = register[2] = int(panjangData)
    register[4] = int(CF)
    register[5] = int(addRTU)
    
    # ----------------ASDU----------------------
    
    if  panjangData >= 5:
        register[6] = int(TypeID)
        register[7] = int(VSQ)
        register[8] = int(COT)

        panjangASDU = int(panjangData) - 5

        register[9 + panjangASDU] =  int(register[4])+int(register[5])+int(register[6])+int(register[7])+int(register[8])
        register[10 + panjangASDU] = 22

        for i in range(0,panjangASDU):
            register[9+i] = int(addRTU1[i])
            register[9 + panjangASDU] += int(register[9+i])

        register[9 + panjangASDU] = int(register[9 + panjangASDU]) % 256

    elif panjangData == 3:
        register[6] = int(TypeID)
        register[7] = int(register[4]+ register[5]+ register[6]) % 256
        register[8] = 22

    ser[idPort][index].write(bytearray(register))
    print(register)



def Writeregister1(idPort,index, panjangData, CF, addRTU, TypeID, VSQ, COT, addRTU1 ):
    register = [0]*(panjangData + 6)

    # ---------------header and CF-------------------
    register[0] = register[3] = 104
    register[1] = register[2] = panjangData
    register[4] = CF
    register[5] = addRTU
    
    # ----------------ASDU----------------------
    
    if  panjangData >= 5:
        register[6] = TypeID
        register[7] = VSQ
        register[8] = COT

        panjangASDU = panjangData - 5

        register[9 + panjangASDU] =  int(register[4])+int(register[5])+int(register[6])+int(register[7])+int(register[8])
        register[10 + panjangASDU] = 22

        for i in range(0,panjangASDU):
            register[9+i] = addRTU1[i]
            register[9 + panjangASDU] += register[9+i]

        register[9 + panjangASDU] = register[9 + panjangASDU] % 256

    elif panjangData == 3:
        register[6] = TypeID
        register[7] = (register[4]+ register[5]+ register[6]) % 256
        register[8] = 22


    buff_ser[idPort][index].write(bytearray(register))
    print(register)




def pollDR(idPort,index):
    global pollDtDR
    global buffPollDtDR
    
    for i in range(15,len(buffer) - 2):
        if i % 2 != 0:
            buffPollDtDR[idPort][index] = buffer[i]
            
        else:
            buffPollDtDR[idPort][index] += buffer[i] * 256

            if buffPollDtDR[idPort][index] > 50000:
                buffPollDtDR[idPort][index] = buffPollDtDR[idPort][index] - 65536

            pollDtDR.append(str(buffPollDtDR[idPort][index]))
            
    dtString = ''
    dtString = "*".join(pollDtDR)
#     print(dtString)

    mycursor = mydb1.cursor()
    sql = "SELECT * FROM "+str(labelChangevalueAddr[countCH[idPort][index]])+" WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND period='"+str(count[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb1.commit()
    mycursor.close()
    
    if len(dbDR) == 0:
        mycursor = mydb1.cursor()
        sql = "INSERT INTO "+str(labelChangevalueAddr[countCH[idPort][index]])+"(data, flag, id_pool, period, port_device, id_device) VALUES('"+str(dtString)+"', '"+str(0)+"','"+str(id_pool[idPort][index])+"','"+str(count[idPort][index])+"','"+str(idPort)+"','"+str(indexMaster[idPort][index])+"')"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        
    else:
        mycursor = mydb1.cursor()
        sql = "UPDATE "+str(labelChangevalueAddr[countCH[idPort][index]])+" SET data = '"+str(dtString)+"', flag = '"+(str(0))+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"' AND period='"+str(count[idPort][index])+"' "
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()

    pollDtDR.clear()



def bentukFile(idPort,index):
    dbCfg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    lbanalog = [0]
    scalanalog = [0]
    skewval = [0]
    minvalue = [0]
    maxvalue = [0]
    lbdigital = [0]
    ratioscalanalog = [0]
    ratio = 0
    
    mycursor = mydb1.cursor()
    sql = "SELECT * FROM it_cfgp141 WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb1.commit()
    mycursor.close()
    
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
        dbCfg[9] = i[9]
        dbCfg[10] = i[10]
        dbCfg[11] = i[11]
        dbCfg[12] = i[12]
        dbCfg[13] = i[13]
        dbCfg[14] = i[14]
        dbCfg[15] = i[15]
        dbCfg[16] = i[16]
        dbCfg[17] = i[17]
        dbCfg[18] = i[18]

    lbanalog[0] = str(dbCfg[17]).split("*")
    lbdigital[0] = str(dbCfg[16]).split("*")
    scalanalog[0] = str(dbCfg[12]).split("*")
    skewval[0] = str(dbCfg[13]).split("*")
    minvalue[0] = str(dbCfg[14]).split("*")
    maxvalue[0] = str(dbCfg[15]).split("*")
    ratioscalanalog[0] = str(dbCfg[18]).split("*")

    dirName = str(dbCfg[10]) + " Disturbance.000"
    if not os.path.exists( dirName ):
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")




#------------------------------File .dat-------------------------------------
    labelChangevalueAddr1 = []
    counttes = []
    countflag = []
    hitungflag = 0
    flag = True
    
    for i in range(0,len(labelChangevalueAddr)):
        if len(labelChangevalueAddr1) == 0:
            labelChangevalueAddr1.append(labelChangevalueAddr[i])
            counttes.append(-1)
            countflag.append(hitungflag)
        else:
            for j in range(0,len(labelChangevalueAddr1)):
                if labelChangevalueAddr[i] == labelChangevalueAddr1[j]:
                    counttes.append(j)
                    countflag.append(j)
                    flag = False

            if flag == True:
                hitungflag += 1
                labelChangevalueAddr1.append(labelChangevalueAddr[i])
                counttes.append(-1)
                countflag.append(hitungflag)

            flag = True
    
    
    mycursor = mydb1.cursor()
    sql = "SELECT DISTINCT "    
    for i in range(0,len(labelChangevalueAddr1)):
        sql += labelChangevalueAddr1[i]+".data,"
        
    sql += labelChangevalueAddr1[0]+".id_pool FROM "+ labelChangevalueAddr1[0]
    for i in range(1, len(labelChangevalueAddr1)):
        sql += " inner JOIN "+labelChangevalueAddr1[i]+" ON "+labelChangevalueAddr1[i]+".period = "+ labelChangevalueAddr1[0]+".period "

    sql += "WHERE "
    for i in range(0, len(labelChangevalueAddr1)):
        sql += labelChangevalueAddr1[i]+".port_device = " + str(idPort) + " and "
        
    for i in range(0, len(labelChangevalueAddr1)):
        sql += labelChangevalueAddr1[i]+".id_device = " + str(indexMaster[idPort][index]) + " and "
        
    for i in range(0, len(labelChangevalueAddr1)):
        sql += labelChangevalueAddr1[i]+".id_pool = " + str(id_pool[idPort][index]) + " and "
        
    for i in range(0, len(labelChangevalueAddr1)):
        if len(labelChangevalueAddr1) - 1 == i:
            sql += labelChangevalueAddr1[i]+".flag = 0 "
        else:
            sql += labelChangevalueAddr1[i]+".flag = 0 and "
            
    sql += "GROUP BY "+labelChangevalueAddr1[0]+".period ORDER BY "+ labelChangevalueAddr1[0]+".period and "

    for i in range(1, len(labelChangevalueAddr1)):
        if len(labelChangevalueAddr1) - 1 == i:
            sql += labelChangevalueAddr1[i]+".period asc "
        else:
            sql += labelChangevalueAddr1[i]+".period and "



    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb1.commit()
    mycursor.close()

    tes = []
    for i in range(0,len(labelChangevalueAddr1)+1):
        tes.append(0)  

    # tes=[0,0,0,0,0,0,0,0,0,0,0,0]
    tes1=''
    tes2=''
    count = 0
    timefreq = 0 
    for i in range(0,len(dbDR)) :
        # print(dbDR[i][0])
        for j in range(0,(len(dbDR[i]))) :
            tes[j] = dbDR[i][j].split('*')
        for k in range(0,len(tes[0])):
            count += 1
            tes[len(tes)-3][k] = ','.join(str(bin(int(tes[len(tes)-3][k])))[:1:-1].ljust(16,'0')+str(bin(int(tes[len(tes)-2][k])))[:1:-1].ljust(16,'0'))
            
            for l in range(1,len(tes)-3):
                tes2 = tes[l][k]
                if tes2[0] == '-':
                    tes[l][k] = '-'+str(tes[l][k])[1:].rjust(5,'0')
                else :
                    tes[l][k] = str(tes[l][k]).rjust(6,'0')

            tes1 = str(count).rjust(6,'0')+ ","+str(timefreq).rjust(10,'0')
            for i in range(1,len(counttes)):
                if int(counttes[i]) == -1:
                    tes1+= ","+str(tes[int(countflag[i])][k])
                
                else:
                    tes1+= ","+str(tes[int(countflag[i])][k])

            tes1 += "\n"
            timefreq +=int(tes[0][k])
#             print(tes1)

            f = open("/home/pi/"+dirName+"/"+str(dirName)+".dat","a")
            f.write(tes1)
            f.close()


#---------------------------------File .cfg----------------------------------------------
    tes1 = ''
    tes1 += str(dbCfg[0])+','+str(dbCfg[4])+',2001\n'
    tes1 += '41,9A,32D\n'

    for i in range(0, len(lbanalog[0])):
        ratio = int(str(ratioscalanalog[0][i])[:3]) - 126
        
        if str(ratioscalanalog[0][i])[3:] == '1':
            if ratio <= 0:
                if abs(ratio)>= int(len(scalanalog[0][i])):
                    tes1+=str(i+1)+','+str(lbanalog[0][i])+',,,V,'+'0.'+str(scalanalog[0][i]).rjust(abs(ratio),'0')[:abs(ratio)]+','+str(skewval[0][i])+','+str(skewval[0][i])+',-'+str(minvalue[0][i])+','+str(maxvalue[0][i])+',1,1,S\n'
                
                else:
                    tes1+=str(i+1)+','+str(lbanalog[0][i])+',,,V,'+str(scalanalog[0][i])[:int(len(scalanalog[0][i])) - abs(ratio)]+'.'+str(scalanalog[0][i])[int(len(scalanalog[0][i])) - abs(ratio):]+','+str(skewval[0][i])+','+str(skewval[0][i])+',-'+str(minvalue[0][i])+','+str(maxvalue[0][i])+',1,1,S\n'
                
        elif str(ratioscalanalog[0][i])[3:] == '0':
            if ratio <= 0:
                if abs(ratio)>= int(len(scalanalog[0][i])):
                    tes1+=str(i+1)+','+str(lbanalog[0][i])+',,,A,'+'0.'+str(scalanalog[0][i]).rjust(abs(ratio),'0')[:abs(ratio)]+','+str(skewval[0][i])+','+str(skewval[0][i])+',-'+str(minvalue[0][i])+','+str(maxvalue[0][i])+',1,1,S\n'
                
                else:
                    tes1+=str(i+1)+','+str(lbanalog[0][i])+',,,A,'+str(scalanalog[0][i])[:int(len(scalanalog[0][i])) - abs(ratio)]+'.'+str(scalanalog[0][i])[int(len(scalanalog[0][i])) - abs(ratio):]+','+str(skewval[0][i])+','+str(skewval[0][i])+',-'+str(minvalue[0][i])+','+str(maxvalue[0][i])+',1,1,S\n'
            
        elif str(ratioscalanalog[0][i])[3:] == '11':
            if ratio <= 0:
                if abs(ratio)>= int(len(scalanalog[0][i])):
                    tes1+=str(i+1)+','+str(lbanalog[0][i])+',,,Hz,'+'0.'+str(scalanalog[0][i]).rjust(abs(ratio),'0')[:abs(ratio)]+','+str(skewval[0][i])+','+str(skewval[0][i])+',-'+str(minvalue[0][i])+','+str(maxvalue[0][i])+',1,1,S\n'
                
                else:
                    tes1+=str(i+1)+','+str(lbanalog[0][i])+',,,Hz,'+str(scalanalog[0][i])[:int(len(scalanalog[0][i])) - abs(ratio)]+'.'+str(scalanalog[0][i])[int(len(scalanalog[0][i])) - abs(ratio):]+','+str(skewval[0][i])+','+str(skewval[0][i])+',-'+str(minvalue[0][i])+','+str(maxvalue[0][i])+',1,1,S\n'

            
    for i in range(0, len(lbdigital[0])):
        tes1+=str(i+1)+','+str(lbdigital[0][i])+',,,0\n'

    tes1 += str(dbCfg[11]) + '\n'
    tes1 += '0\n'
    tes1 += '0,'+str(dbCfg[3]) + '\n'
    tes1 += str(dbCfg[1]) + '\n'
    tes1 += str(dbCfg[2]) + '\n'
    tes1 += str('ASCII') + '\n1\n'

    # print(tes1)
    f = open("/home/pi/"+dirName+"/"+str(dirName)+".cfg","w")
    f.write(tes1)
    f.close()
    tes1 = ''

    with ZipFile('/home/pi/dms/DMSv1.2/zipDR/'+ dirName +'.zip', 'w') as zipObj:
       for folderName, subfolders, filenames in os.walk(dirName):
           for filename in filenames:
               filePath = os.path.join(folderName, filename)
               zipObj.write(filePath, compress_type=zipfile.ZIP_DEFLATED)


    if not os.path.exists('/home/pi/' + dirName):
        print("Folder " , dirName ,  " tidak tersedia ")
    else:
        shutil.rmtree('/home/pi/'+dirName)
        print("Folder telah dihapus")

    dr_file = '/home/pi/dms/DMSv1.2/zipDR/'+ dirName +'.zip'
    hconn_send(dr_file )


    if int(statusRelay[idPort][index]) == 8:
        konversiStatus = 'healthy'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 10:
        konversiStatus = 'alarm'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 11:
        konversiStatus = 'trip and alarm'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 12:
        konversiStatus = 'blocking'
        # statusRelay1[idPort][index] = konversiStatus
    
    elif int(statusRelay[idPort][index]) == 26:
        konversiStatus = 'alarm tahap1 blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 27:
        konversiStatus = 'alarm tahap1 non blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 58:
        konversiStatus = 'alarm tahap2 blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 59:
        konversiStatus = 'alarm tahap2 non blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 122:
        konversiStatus = 'alarm tahap3 blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 123:
        konversiStatus = 'alarm tahap3 non blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 250:
        konversiStatus = 'alarm tahap4 blocking'
        # statusRelay1[idPort][index] = konversiStatus
        
    elif int(statusRelay[idPort][index]) == 251:
        konversiStatus = 'alarm tahap4 non blocking'
        # statusRelay1[idPort][index] = konversiStatus


    buffFileDR = ''
    buffstatusFileDR = ''
    buffwaktuFileDR = ''
    bufflokasiFileDR = ''

    if int(indexFileDR[idPort][index]) < 10:
        indexFileDR[idPort][index] += 1
        buffFileDR = str(dirName+'.zip,')
        buffwaktuFileDR = str(dbCfg[2])+','
        bufflokasiFileDR = str(dbCfg[7])+','
        buffstatusFileDR = str(konversiStatus)+','
        
        fileDR[idPort][index] += buffFileDR
        statusFileDR[idPort][index] += buffstatusFileDR
        waktuFileDR[idPort][index] += buffwaktuFileDR
        lokasiFileDR[idPort][index] += bufflokasiFileDR
        
        mycursor = mydb.cursor()
        sql = "UPDATE fileDR SET data = '"+str(fileDR[idPort][index])+"', jumlah_data = '"+str(indexFileDR[idPort][index])+"', status = '"+str(statusFileDR[idPort][index])+"', waktu = '"+str(waktuFileDR[idPort][index])+"', lokasi = '"+str(lokasiFileDR[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        
    else:
        buffwaktuFileDR = str(dbCfg[2])+','
        bufflokasiFileDR = str(dbCfg[7])+','
        buffstatusFileDR = str(konversiStatus)+','
        
        tes = fileDR[idPort][index].split(',')
        tes1 = statusFileDR[idPort][index].split(',')
        tes2 = waktuFileDR[idPort][index].split(',')
        tes3 = lokasiFileDR[idPort][index].split(',')
#         print(tes)
        if os.path.exists('/home/pi/dms/DMSv1.2/zipDR'):
          os.remove('/home/pi/dms/DMSv1.2/zipDR/'+str(tes[0]))
        else:
          print("File tidak ditemukan")
        
        for i in range(1,10):
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
                statusFileDR[idPort][index] = ','.join(str(elem) for elem in tes1)
                waktuFileDR[idPort][index] = ','.join(str(elem) for elem in tes2)
                lokasiFileDR[idPort][index] = ','.join(str(elem) for elem in tes3)
        
        mycursor = mydb.cursor()
        sql = "UPDATE fileDR SET data = '"+str(fileDR[idPort][index])+"', jumlah_data = '"+str(indexFileDR[idPort][index])+"', status = '"+str(statusFileDR[idPort][index])+"', waktu = '"+str(waktuFileDR[idPort][index])+"', lokasi = '"+str(lokasiFileDR[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()



def hconn_send(dr_file) :
    dbCfg = ''
    
    mycursor = mydb.cursor()
    sql = "SELECT * FROM network"
    mycursor.execute(sql)
    dbDR = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    
    for i in dbDR:
        dbCfg = i[5]
    
    url = 'http://'+str(dbCfg)+'/dms/notif'
    file = {'myfile': open(dr_file,'rb')}
    r = requests.post(url, files=file, verify=False)
    if r.status_code != 200:
        print('sendErr: '+r.url)
    else :
        print(r.text)



def configDR(idPort,index,buf,hitung):
    global count
    global count3
    global buffindexDR
    global indexDR
    global jmlDtDR
    global indexNewDRLSB
    global indexNewDRMSB
    global nameRelay
    global freq
    global analogCFG
    global scalAnalogCFG
    global ratioscalAnalogCFG
    global skewValCFG
    global minValueCFG
    global maxValueCFG
    global digitalCFG
    global lbdigitalCFG 
    global strdigitalCFG 
    global DRdate
    global flag1
    global regChangevalueAddr
    global labelChangevalueAddr
    
    count1 = [[0],[0]]
    count1[idPort][index] = 0
    count2 = [[0],[0]]
    count2[idPort][index] = 0


    if  hitung == 4:
        for i in range(0,len(buf)):
            if i == 16:
                buffindexDR[idPort][index] = buf[16] 
                indexNewDRLSB[idPort][index] = buf[16]

            elif i == 17:
                buffindexDR[idPort][index] += buf[17] * 256
                indexNewDRMSB[idPort][index] = buf[17]
                regAddRTU1[4][3] = indexNewDRLSB[idPort][index]
                regAddRTU1[4][4] = indexNewDRMSB[idPort][index]

        
        if buffindexDR[idPort][index] > 50000:
            buffindexDR[idPort][index] = buffindexDR[idPort][index] - 65536

    
    elif hitung == 7:
        for i in range(0,len(buf)):
            if i > 10 and i <= 26:
                nameRelay[idPort][index] += str(chr(buf[i]))

            elif i == 28:
                freq[idPort][index] = buf[28]

            elif i == 29:
                freq[idPort][index] += buf[29] *256
            
            elif i == 53:
                detik[idPort][index] = buf[53]

            elif i == 54:
                detik[idPort][index] += buf[54]*256

            elif i == 55:
                menit[idPort][index] = buf[55]
            
            elif i == 56:
                jam[idPort][index] = buf[56]
            
            elif i == 57:
                tanggal[idPort][index] = buf[57] & 31
            
            elif i == 58:
                bulan[idPort][index] = buf[58]

            elif i == 59:
                tahun[idPort][index] = buf[59]
                
            elif i == 73: 
                jmlDtDR[idPort][index] = buf[73]

            elif i == 74:
                jmlDtDR[idPort][index] += buf[74] * 256 

                first_date = ''
                last_date = ''
                timeFile = ''
                firstFinalSec = ''
                lastFinalSec = ''
                
                firstFinalSec = str(detik[idPort][index] - 484)
                lastFinalSec = str(detik[idPort][index])

                if len(lastFinalSec) < 5:
                    lastFinalSec = lastFinalSec.rjust(5,'0')
                    firstFinalSec = firstFinalSec.rjust(5,'0')

                first_date = str(tanggal[idPort][index])+ "/"+ str(bulan[idPort][index])+ "/20"+ str(tahun[idPort][index])+ ","+str(jam[idPort][index])+":"+str(menit[idPort][index])+":"+str(firstFinalSec[:2])+"."+str(firstFinalSec[2:]).ljust(6,'0')
                last_date = str(tanggal[idPort][index])+ "/"+ str(bulan[idPort][index])+ "/20"+ str(tahun[idPort][index])+ ","+str(jam[idPort][index])+":"+str(menit[idPort][index])+":"+str(lastFinalSec[:2])+"."+str(lastFinalSec[2:]).ljust(6,'0')
                timeFile = str(tanggal[idPort][index])+ "."+ str(bulan[idPort][index])+ ".20"+ str(tahun[idPort][index])+ " "+str(jam[idPort][index])+"."+str(menit[idPort][index])+"."+str(detik[idPort][index]).ljust(6,'0')
                waktuTelegram = str(tanggal[idPort][index])+"/"+str(bulan[idPort][index])+"/20"+str(tahun[idPort][index])+" "+str(jam[idPort][index])+":"+str(menit[idPort][index])+" WIB"

#                 print(buffindexDR[idPort][index])
#                 print(indexDR[idPort][index])
#                 print(last_date)
#                 print(DRdate[idPort][index])

                if int(buffindexDR[idPort][index]) > 200 or int(buffindexDR[idPort][index]) < -200:
                    count[idPort][index] = 0
                    flagIndex[idPort][index] = 1
                    
                elif int(buffindexDR[idPort][index]) >= int(indexDR[idPort][index]) or DRdate[idPort][index] == last_date :
                    count[idPort][index] = 0
                    flagIndex1[idPort][index] = 1

                elif flagIndex[idPort][index] == 1 or flagIndex1[idPort][index] == 1:
                    dbCfg2 = ''
                    dbCfg3 = ['','']
                    
                    indexDR[idPort][index] = buffindexDR[idPort][index]
                    DRdate[idPort][index] = last_date
                    flagIndex[idPort][index] = 0
                    flagIndex1[idPort][index] = 0
                    
                    
                    mycursor = mydb1.cursor()
                    sql = "UPDATE dataRegisterp141 SET jumlah_data = '"+str(jmlDtDR[idPort][index])+"', dateDR = '"+str(DRdate[idPort][index])+"', indexDR = '"+str(indexDR[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb1.commit()
                    mycursor.close()
                    
                    
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM device_list WHERE port_type='"+str(idPort)+"' AND port_number='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    dbDR = mycursor.fetchall()
                    mydb.commit()
                    mycursor.close()
                    
                    for i in dbDR:
                        dbCfg2 = i[2]
                        
                    
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM network"
                    mycursor.execute(sql)
                    dbDR = mycursor.fetchall()
                    mydb.commit()
                    mycursor.close()
                    
                    for i in dbDR:
                        dbCfg3[0] = i[5]
                        dbCfg3[1] = i[7]
                        
                        
                    last_date1 = ''
                    lastFinalSec1 = ''
                    lastFinalSec1 = str(detik[idPort][index])
                    last_date1 = "20"+str(tahun[idPort][index])+ "/"+ str(bulan[idPort][index]).ljust(2,'0')+ "/"+ str(tanggal[idPort][index]).ljust(2,'0')+ " "+str(jam[idPort][index]).ljust(2,'0')+":"+str(menit[idPort][index]).ljust(2,'0')+":"+str(lastFinalSec1[:2]).ljust(2,'0')
                        
                    statusRelay[idPort][index] = 11
                        
                    
                    mycursor = mydb.cursor()
                    sql = "UPDATE device_list SET kondisi = '"+str(statusRelay[idPort][index])+"', tanggal = '"+str(last_date1)+"' WHERE port_type='"+str(idPort)+"' AND port_number='"+str(indexMaster[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb.commit()
                    
                    
                    d= {"machineCode":str(dbCfg3[1])
                        ,"relayId": str(id_Micom[idPort][index])
                        ,"lokasi": str(rak_lokasi[idPort][index])
                        ,"status": str('Trip and Alarm')
                        ,"namaFile": str(timeFile)+str(" Disturbance.000")
                        ,"waktu": str(waktuTelegram)
                        ,"flag": str(0)
                        ,"type": str(dbCfg2)
                        ,"portType": str(idPort)
                        ,"portNumber": str(indexMaster[idPort][index])
                        }
                    
                    
#                     response = requests.post("http://"+str(dbCfg3[0])+"/dms/fail/add", data=d)
                    
#                     try:
#                         r = requests.post("http://"+str(dbCfg3[0])+"/dms/fail/add", data=d)
#                         r.raise_for_status()
#                     except requests.exceptions.HTTPError as errh:
#                         print ("Http Error:",errh)
#                     except requests.exceptions.ConnectionError as errc:
#                         print ("Error Connecting:",errc)
#                     except requests.exceptions.Timeout as errt:
#                         print ("Timeout Error:",errt)
#                     except requests.exceptions.RequestException as err:
#                         print ("OOps: Something Else",err)
                    
                    

#                 if index == 0 and (idPort == 0 or idPort == 1) :
#                     hitungLoop[idPort][index] += 1
#                     mycursor = mydb1.cursor()
#                     sql = "UPDATE dataregisterp141 SET indexLoop = '"+str(hitungLoop[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
#                     mycursor.execute(sql)
#                     mydb1.commit()
#                     mycursor.close()
#                     
#                     if hitungLoop[idPort][index] == 300:
#                         hitungLoop[idPort][index] = 0
#                         mycursor = mydb1.cursor()
#                         sql = "UPDATE dataregisterp141 SET indexLoop = '"+str(hitungLoop[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
#                         mycursor.execute(sql)
#                         mydb1.commit()
#                         mycursor.close()
#                         flag1 = True


                mycursor = mydb1.cursor()
                sql = "SELECT * FROM it_cfgp141 WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool = '"+str(id_pool[idPort][index])+"' "
                mycursor.execute(sql)
                dbDR = mycursor.fetchall()
                mydb1.commit()
                mycursor.close()
                
                if len(dbDR) == 0:
                    mycursor = mydb1.cursor()
                    sql = "INSERT INTO it_cfgp141 (micom_type, first_date, last_date, dr_count,id_micom, id_pool, flag, location, port_device, id_device, timeFile, f_ratio) VALUES('"+str(nameRelay[idPort][index])+"','"+str(first_date)+"', '"+str(last_date)+"','"+str(jmlDtDR[idPort][index])+"','"+str(id_Micom[idPort][index])+"','"+str(id_pool[idPort][index])+"','"+str(0)+"','"+str(rak_lokasi[idPort][index])+"','"+str(idPort)+"','"+str(indexMaster[idPort][index])+"','"+str(timeFile)+"','"+str(freq[idPort][index])+"') "
                    mycursor.execute(sql)
                    mydb1.commit()
                    mycursor.close()
                    
                else :
                    mycursor = mydb1.cursor()
                    sql = "UPDATE it_cfgp141 SET micom_type = '"+str(nameRelay[idPort][index])+"' , first_date = '"+str(first_date)+"', last_date = '"+str(last_date)+"', dr_count = '"+str(jmlDtDR[idPort][index])+"', id_micom = '"+str(id_Micom[idPort][index])+"', flag = '"+str(0)+"', location = '"+str(rak_lokasi[idPort][index])+"', timeFile = '"+str(timeFile)+"', f_ratio = '"+str(freq[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
                    mycursor.execute(sql)
                    mydb1.commit()
                    mycursor.close()

                nameRelay[idPort][index] = ''

    
    elif hitung == 9:
        lbAnalogCFG = []
        strLbAnalogCFG = ''

        for i in range(0,len(buf)):
            if i > (15+(18*count1[idPort][index])) and i <= (31+(18*count1[idPort][index])) and count1[idPort][index] < 9:
                analogCFG[count1[idPort][index]] += chr(buf[i])
                if i == (31+(18*count1[idPort][index])):
                    lbAnalogCFG.append(str(analogCFG[count1[idPort][index]]))
                    count1[idPort][index] += 1
                    
        for i in range(0,len(analogCFG)):
            if analogCFG[i] == 'VA              ':
                regChangevalueAddr[i+1] = VA
                labelChangevalueAddr[i+1] ='it_vap141'
            elif analogCFG[i] == 'VB              ':
                regChangevalueAddr[i+1] = VB
                labelChangevalueAddr[i+1] ='it_vbp141'
            elif analogCFG[i] == 'VC              ':
                regChangevalueAddr[i+1] = VC
                labelChangevalueAddr[i+1] ='it_vcp141'
            elif analogCFG[i] == 'IA              ':
                regChangevalueAddr[i+1] = IA
                labelChangevalueAddr[i+1] ='it_iap141'
            elif analogCFG[i] == 'IB              ':
                regChangevalueAddr[i+1] = IB
                labelChangevalueAddr[i+1] ='it_ibp141'
            elif analogCFG[i] == 'IC              ':
                regChangevalueAddr[i+1] = IC
                labelChangevalueAddr[i+1] ='it_icp141'
            elif analogCFG[i] == 'IN              ':
                regChangevalueAddr[i+1] = IN
                labelChangevalueAddr[i+1] ='it_inp141'
            elif analogCFG[i] == 'IN Sensitive    ':
                regChangevalueAddr[i+1] = INSensitive
                labelChangevalueAddr[i+1] ='it_insensitivep141'
            elif analogCFG[i] == 'Frequency       ':
                regChangevalueAddr[i+1] = Frequency
                labelChangevalueAddr[i+1] ='it_fp141'

                
        strLbAnalogCFG = '*'.join(lbAnalogCFG)

        mycursor = mydb1.cursor()
        sql = "UPDATE it_cfgp141 SET analogCFG = '"+str(strLbAnalogCFG)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        # print(strLbAnalogCFG)

    elif hitung == 13:
        lbScalAnalogCFG = []
        strscalAnalogCFG = ''
        ratiolbScalAnalogCFG = []
        ratiostrscalAnalogCFG = ''
        

        for i in range(0,len(buf)):
            if i > 13 and i <= 49:
                count2[idPort][index] += 1
                if count2[idPort][index] == 1:
                    scalAnalogCFG[count1[idPort][index]] = buf[i]

                elif count2[idPort][index] == 2:
                    scalAnalogCFG[count1[idPort][index]] += buf[i]*256
                    lbScalAnalogCFG.append(str(scalAnalogCFG[count1[idPort][index]]))
                    
                elif count2[idPort][index] == 3:
                    ratioscalAnalogCFG[count1[idPort][index]] = str(buf[i])
                    
                elif count2[idPort][index] == 4:
                    ratioscalAnalogCFG[count1[idPort][index]] += str(buf[i])
                    ratiolbScalAnalogCFG.append(str(ratioscalAnalogCFG[count1[idPort][index]]))
                    count2[idPort][index] = 0
                    count1[idPort][index] += 1

        strscalAnalogCFG = '*'.join(lbScalAnalogCFG)
        ratiostrscalAnalogCFG = '*'.join(ratiolbScalAnalogCFG)
        

        mycursor = mydb1.cursor()
        sql = "UPDATE it_cfgp141 SET scalAnalogCFG = '"+str(strscalAnalogCFG)+"',ratioscalAnalogCFG = '"+str(ratiostrscalAnalogCFG)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        # print(strscalAnalogCFG)
                    
    elif hitung == 14:
        lbSkewValCFG = []
        strSkewValCFG = ''
        for i in range(0,len(buf)):
            if i > 12 and i <= 30:
                if i % 2 == 0:
                    skewValCFG[count1[idPort][index]] += buf[i]*256
                    lbSkewValCFG.append(str(skewValCFG[count1[idPort][index]]))
                    count1[idPort][index] += 1
                else:
                    skewValCFG[count1[idPort][index]] = buf[i]

        strSkewValCFG = '*'.join(lbSkewValCFG)
    
        mycursor = mydb1.cursor()
        sql = "UPDATE it_cfgp141 SET skewValCFG = '"+str(strSkewValCFG)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        # print(strSkewValCFG)

    elif hitung == 15:
        lbMinValueCFG = []
        strMinValueCFG = ''
        for i in range(0,len(buf)):
            if i > 12 and i <= 30:
                count2[idPort][index] += 1
                if count2[idPort][index] == 1:
                    minValueCFG[count1[idPort][index]] = buf[i]
                elif count2[idPort][index] == 2:
                    minValueCFG[count1[idPort][index]] += buf[i]*256
                    lbMinValueCFG.append(str(minValueCFG[count1[idPort][index]]))
                    count1[idPort][index] += 1
                    count2[idPort][index] = 0

        strMinValueCFG = '*'.join(lbMinValueCFG)

        mycursor = mydb1.cursor()
        sql = "UPDATE it_cfgp141 SET minValueCFG= '"+str(strMinValueCFG)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        # print(strMinValueCFG)
    
    elif hitung == 16:
        lbMaxValueCFG = []
        strMaxValueCFG = ''
        for i in range(0,len(buf)):
            if i > 12 and i <= 30:
                count2[idPort][index] += 1
                if count2[idPort][index] == 1:
                    maxValueCFG[count1[idPort][index]] = buf[i]
                elif count2[idPort][index] == 2:
                    maxValueCFG[count1[idPort][index]] += buf[i]*256
                    lbMaxValueCFG.append(str(maxValueCFG[count1[idPort][index]]))
                    count1[idPort][index] += 1
                    count2[idPort][index] = 0
        
        strMaxValueCFG = '*'.join(lbMaxValueCFG)

        mycursor = mydb1.cursor()
        sql = "UPDATE it_cfgp141 SET maxValueCFG= '"+str(strMaxValueCFG)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        # print(strMaxValueCFG)
    

    elif hitung == 18:
        for i in range(0,len(buf)):
            if i > (15 + (count3[idPort][index]*18)) and i <= (31 + (count3[idPort][index]*18)):
                 digitalCFG[count3[idPort][index]] += chr(buf[i])
                 if i == (31 + (count3[idPort][index]*18)):
                    lbdigitalCFG.append(str(digitalCFG[count3[idPort][index]]))
                    count3[idPort][index] += 1
        # print(digitalCFG)
    
    elif hitung == 19:
        for i in range(0,len(buf)):
            if i > (15 + (count1[idPort][index]*18)) and i <= (31 + (count1[idPort][index]*18)):
                 digitalCFG[count3[idPort][index]] += chr(buf[i])
                 if i == (31 + (count1[idPort][index]*18)):
                    lbdigitalCFG.append(str(digitalCFG[count3[idPort][index]]))
                    count3[idPort][index] += 1
                    count1[idPort][index] += 1
    
    elif hitung == 22:
        for i in range(0,len(buf)):
            if i > (15 + (count1[idPort][index]*18)) and i <= (31 + (count1[idPort][index]*18)):
                 digitalCFG[count3[idPort][index]] += chr(buf[i])
                 if i == (31 + (count1[idPort][index]*18)):
                    lbdigitalCFG.append(str(digitalCFG[count3[idPort][index]]))
                    count3[idPort][index] += 1
                    count1[idPort][index] += 1

    elif hitung == 23:
        for i in range(0,len(buf)):
            if i > (15 + (count1[idPort][index]*18)) and i <= (31 + (count1[idPort][index]*18)):
                 digitalCFG[count3[idPort][index]] += chr(buf[i])
                 if i == (31 + (count1[idPort][index]*18)):
                    lbdigitalCFG.append(str(digitalCFG[count3[idPort][index]]))
                    count3[idPort][index] += 1
                    count1[idPort][index] += 1
        
        strdigitalCFG = '*'.join(lbdigitalCFG)

        mycursor = mydb1.cursor()
        sql = "UPDATE it_cfgp141 SET digitalCFG = '"+str(strdigitalCFG)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"' AND id_pool='"+str(id_pool[idPort][index])+"'"
        mycursor.execute(sql)
        mydb1.commit()
        mycursor.close()
        # print(strdigitalCFG)





def sistemconfig():
    print("------------------Micom P141---------------------------")
    regChangevalueAddr = [[20 ,180],VA,VB,VC,IA,IB,IC,IN,INSensitive,Frequency,[62 ,180],[63 ,180]]
    labelChangevalueAddr = ['it_waktup141','it_vap141','it_vbp141','it_vcp141','it_iap141','it_ibp141','it_icp141','it_inp141','it_insensitivep141','it_fp141','it_orp141','it_inlp141']

    regLengthASDU = [7,7,11,7,10,5,47,7,6,6,6,7,7,7,7,7,7,6,6,6,7,6,6,6]
    regCF = [123,91]
    regTypeID = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    regVSQ = [7,7,7,7,7,5,7,7,6,6,6,7,7,7,7,7,7,6,6,6,7,6,6,6]
    regCOT = [20,20,20,21,64,78,20,25,33,33,33,20,20,20,20,20,25,33,33,33,25,33,33,33]
    regAddRTU1 = [[2,191],[1,180],[1,191,7,20,2,191],[1,180],[1,180,42,0,0],[0],[5,0,7,20,9,0,7,20,2,179,7,20,1,180,7,20,2,180,7,20,3,180,7,20,4,180,7,20,16,180,7,20,17,180,7,20,18,180,7,20,19,180],[3,180],[0],[1],[2],[5,180],[6,180],[7,180],[8,180],[9,180],[62,180],[0],[1],[2],[63,180],[0],[1],[2]]



    global buffcekKoneksi
    global buffcekKoneksi1
    global flag
    global count
    global countCH
    global flagDtDR
    global flagDtDR1


    resetData()


    for i in range(0, 10):
        cekStatus = [0]
        idPort = 0
        mycursor = mydb.cursor()
        sql = "SELECT * FROM scan_port WHERE port_device='"+str(idPort)+"' and id_device='"+str(i)+"'"
        mycursor.execute(sql)
        dbStatus = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        
        if len(dbStatus) <= 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO scan_port(port_device, id_device, status) VALUES('"+str(idPort)+"', '"+str(i)+"', '"+str(0)+"') "
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()

            try:
                cekStatus = serial.Serial(port = '/dev/ttyUSB'+str(i), baudrate = 19200, parity = 'N', stopbits = 1, bytesize = 8,timeout = .500 )
            except serial.SerialException as e:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '"+str(0)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()
                mycursor.close()

            else:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '"+str(1)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()
                mycursor.close()
                
        else:
            try:
                cekStatus = serial.Serial(port = '/dev/ttyUSB'+str(i), baudrate = 19200, parity = 'N', stopbits = 1, bytesize = 8,timeout = .500)
            except serial.SerialException as e:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '"+str(0)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()
                mycursor.close()

            else:
                mycursor = mydb.cursor()
                sql = "UPDATE scan_port SET status = '"+str(1)+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(i)+"'"
                mycursor.execute(sql)
                mydb.commit()
                mycursor.close()


    for i in range(0,len(dbList)):        
        mycursor = mydb.cursor()
        sql = "SELECT * FROM device_list WHERE port_type='"+str(i)+"'"
        mycursor.execute(sql)
        dbList[i] = mycursor.fetchall()
        mydb.commit()
        mycursor.close()

        buff_id_pool.append([0 for x in range(0, len(dbList[i]))])
        id_pool.append([0 for x in range(0, len(dbList[i]))])
        flag.append([0 for x in range(0,len(dbList[i]))])
        buff_flagDtDR.append([0 for x in range(0,len(dbList[i]))])
        flagDtDR.append([0 for x in range(0,len(dbList[i]))])
        buff_flagDtDR1.append([0 for x in range(0,len(dbList[i]))])
        flagDtDR1.append([0 for x in range(0,len(dbList[i]))])
        buff_flagCF.append([0 for x in range(0,len(dbList[i]))])
        flagCF.append([0 for x in range(0,len(dbList[i]))])
        tanggal.append([0 for x in range(0,len(dbList[i]))])
        bulan.append([0 for x in range(0,len(dbList[i]))])
        tahun.append([0 for x in range(0,len(dbList[i]))])
        jam.append([0 for x in range(0,len(dbList[i]))])
        menit.append([0 for x in range(0,len(dbList[i]))])
        detik.append([0 for x in range(0,len(dbList[i]))])
        buff_DRdate.append([0 for x in range(0,len(dbList[i]))])
        DRdate.append([0 for x in range(0,len(dbList[i]))])
        buff_id_Micom.append([0 for x in range(0,len(dbList[i]))])
        id_Micom.append([0 for x in range(0,len(dbList[i]))])
        buff_count.append([0 for x in range(0,len(dbList[i]))])
        count.append([0 for x in range(0,len(dbList[i]))])
        buff_count3.append([0 for x in range(0,len(dbList[i]))])
        count3.append([0 for x in range(0,len(dbList[i]))])
        buff_countCH.append([0 for x in range(0,len(dbList[i]))])
        countCH.append([0 for x in range(0,len(dbList[i]))])
        countCF.append([0 for x in range(0,len(dbList[i]))])
        buffBanyakData.append([0 for x in range(0,len(dbList[i]))])
        buffPanjangDataASDU.append([0 for x in range(0,len(dbList[i]))])
        buffAddrASDU.append([0 for x in range(0,len(dbList[i]))])
        buffCF.append([0 for x in range(0,len(dbList[i]))])
        buffAddrASDUIn.append([0 for x in range(0,len(dbList[i]))])
        buffIOA.append([0 for x in range(0,len(dbList[i]))])
        buffindexDR.append([0 for x in range(0,len(dbList[i]))])
        buff_indexDR.append([0 for x in range(0,len(dbList[i]))])
        indexDR.append([0 for x in range(0,len(dbList[i]))])
        indexNewDRLSB.append([0 for x in range(0,len(dbList[i]))])
        indexNewDRMSB.append([0 for x in range(0,len(dbList[i]))])
        buff_jmlDtDR.append([0 for x in range(0,len(dbList[i]))])
        jmlDtDR.append([0 for x in range(0,len(dbList[i]))])
        freq.append([0 for x in range(0,len(dbList[i]))])
        buffPollDtDR.append([0 for x in range(0,len(dbList[i]))])
        nameRelay.append(['' for x in range(0,len(dbList[i]))])
        buff_ser.append([0 for x in range(0,len(dbList[i]))])
        indexPort.append([0 for x in range(0,len(dbList[i]))])
        buff_baudrate.append([0 for x in range(0,len(dbList[i]))])
        baudrate.append([0 for x in range(0,len(dbList[i]))])
        buff_parity.append([0 for x in range(0,len(dbList[i]))])
        parity.append([0 for x in range(0,len(dbList[i]))])
        buff_stop_bit.append([0 for x in range(0,len(dbList[i]))])
        stop_bit.append([0 for x in range(0,len(dbList[i]))])
        buff_byte_size.append([0 for x in range(0,len(dbList[i]))])
        byte_size.append([0 for x in range(0,len(dbList[i]))])
        buff_hitungError.append([0 for x in range(0,len(dbList[i]))])
        hitungError.append([0 for x in range(0,len(dbList[i]))])
        buff_hitungLoop.append([0 for x in range(0,len(dbList[i]))])
        hitungLoop.append([0 for x in range(0,len(dbList[i]))])
        buff_fileDR.append([0 for x in range(0,len(dbList[i]))])
        buff_indexFileDR.append([0 for x in range(0,len(dbList[i]))])
        buff_waktuFileDR.append([0 for x in range(0,len(dbList[i]))])
        buff_statusFileDR.append([0 for x in range(0,len(dbList[i]))]) 
        buff_lokasiFileDR.append([0 for x in range(0,len(dbList[i]))])
        fileDR.append([0 for x in range(0,len(dbList[i]))])
        indexFileDR.append([0 for x in range(0,len(dbList[i]))])
        waktuFileDR.append([0 for x in range(0,len(dbList[i]))])
        statusFileDR.append([0 for x in range(0,len(dbList[i]))])
        lokasiFileDR.append([0 for x in range(0,len(dbList[i]))])
        indexMaster.append([0 for x in range(0,len(dbList[i]))])
        buff_type_relay.append([0 for x in range(0,len(dbList[i]))])
        type_relay.append([0 for x in range(0,len(dbList[i]))])
        buff_rak_lokasi.append([0 for x in range(0,len(dbList[i]))])
        rak_lokasi.append([0 for x in range(0,len(dbList[i]))])
        buff_statusRelay.append([0 for x in range(0,len(dbList[i]))])
        statusRelay.append([0 for x in range(0,len(dbList[i]))])
        statusRelay1.append(['' for x in range(0,len(dbList[i]))])
        relayTeks.append(['' for x in range(0,len(dbList[i]))])
        buff_mode.append(['' for x in range(0,len(dbList[i]))])
        mode.append(['' for x in range(0,len(dbList[i]))])
        buff_port_address.append(['' for x in range(0,len(dbList[i]))])
        port_address.append(['' for x in range(0,len(dbList[i]))])
        flagIndex.append([0 for x in range(0,len(dbList[i]))])
        flagIndex1.append([0 for x in range(0,len(dbList[i]))])


    
    hitung = 0
    for i in range(0,len(dbList[0])):
        idPort = 0
        
        buff_id_Micom[idPort][i] = dbList[idPort][i][1]
        buff_type_relay[idPort][i] = dbList[idPort][i][2]
        indexPort[idPort][i] = dbList[idPort][i][4]
        buff_port_address[idPort][i] = dbList[idPort][i][5]
        buff_rak_lokasi[idPort][i] = dbList[idPort][i][6]
        buff_baudrate[idPort][i] = dbList[idPort][i][7]
        buff_stop_bit[idPort][i] = dbList[idPort][i][12]
        buff_parity[idPort][i] = dbList[idPort][i][13]
        buff_byte_size[idPort][i] = dbList[idPort][i][14]
        buff_statusRelay[idPort][i] = dbList[idPort][i][15]
        buff_mode[idPort][i] = dbList[idPort][i][17]


        if buff_parity[idPort][i] == 'N':
            buff_parity[idPort][i] = serial.PARITY_NONE

        elif buff_parity[idPort][i] == 'E':
            buff_parity[idPort][i] = serial.PARITY_EVEN

        elif buff_parity[idPort][i] == 'O':
            buff_parity[idPort][i] = serial.PARITY_ODD

        elif buff_parity[idPort][i] == 'M':
            buff_parity[idPort][i] = serial.PARITY_MARK

        elif buff_parity[idPort][i] == 'S':
            buff_parity[idPort][i] = serial.PARITY_SPACE



        if int(buff_stop_bit[idPort][i]) == 1 :
            buff_stop_bit[idPort][i] = serial.STOPBITS_ONE
            
        elif int(buff_stop_bit[idPort][i]) == 1.5:
            buff_stop_bit[idPort][i] = serial.STOPBITS_ONE_POINT_FIVE
        
        elif int(buff_stop_bit[idPort][i]) == 2:
            buff_stop_bit[idPort][i] = serial.STOPBITS_TWO



        if int(buff_byte_size[idPort][i]) == 8:
            buff_byte_size[idPort][i] = serial.EIGHTBITS
            
        elif int(buff_byte_size[idPort][i]) == 7:
            buff_byte_size[idPort][i] = serial.SEVENBITS

        elif int(buff_byte_size[idPort][i]) == 6:
            buff_byte_size[idPort][i] = serial.SIXBITS
        
        elif int(buff_byte_size[idPort][i]) == 5:
            buff_byte_size[idPort][i] = serial.FIVEBITS


        mycursor = mydb1.cursor()
        sql = "SELECT * FROM dataregisterp141 WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb1.commit()
        mycursor.close()
        
        if len(dbDR) == 0:
            mycursor = mydb1.cursor()
            sql = "INSERT INTO dataregisterp141(port_device, id_device, geser_register, geser_param, period, id_pool, jumlah_data, indexDR, indexError, indexLoop, flagDtDR, flagDtDR1,flag, dateDR) VALUES('"+str(idPort)+"', '"+str(indexPort[idPort][i])+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"','"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"', '"+str(0)+"') "
            mycursor.execute(sql)
            mydb1.commit()
            mycursor.close()
            
            buff_count[idPort][i] = 0
            buff_countCH[idPort][i] = 0
            buff_id_pool[idPort][i] = 0
            buff_jmlDtDR[idPort][i] = 0
            buff_indexDR[idPort][i] = 0
            buff_hitungError[idPort][i] = 0
            buff_hitungLoop[idPort][i] = 0 
            buff_flagDtDR[idPort][i] = 0
            buff_flagDtDR1[idPort][i] = 0
            buff_flagCF[idPort][i] = 0
            buff_DRdate[idPort][i] = ''
        else :
            for j in dbDR :
                buff_count[idPort][i] = int(j[2])
                buff_countCH[idPort][i] = int(j[3])
                # buff_period[idPort][i] = int(j[4])
                buff_id_pool[idPort][i] = int(j[5])
                buff_jmlDtDR[idPort][i] = int(j[6])
                buff_indexDR[idPort][i] = int(j[7])
                buff_hitungError[idPort][i] = int(j[8])
                buff_hitungLoop[idPort][i] = int(j[9])
                buff_flagDtDR[idPort][i] = j[10]
                buff_flagDtDR1[idPort][i] = j[11]
                buff_flagCF[idPort][i] = j[12]
                buff_DRdate[idPort][i] = str(j[13])


        mycursor = mydb.cursor()
        sql = "SELECT * FROM fileDR WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexPort[idPort][i])+"' "
        mycursor.execute(sql)
        dbDR = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        
        if len(dbDR) == 0:
            mycursor = mydb.cursor()
            sql = "INSERT INTO fileDR(port_device, id_device, data, jumlah_data, status, waktu, lokasi) VALUES('"+str(idPort)+"', '"+str(indexPort[idPort][i])+"', '""','"+str(0)+"', '""', '""', '""') "
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()
            
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


        try:
            buff_ser[idPort][i] = serial.Serial(port = '/dev/ttyUSB'+str(indexPort[idPort][i]), baudrate = int(buff_baudrate[idPort][i]), parity = buff_parity[idPort][i], stopbits = buff_stop_bit[idPort][i], bytesize = buff_byte_size[idPort][i],timeout = .500 )
        except serial.SerialException as e:
            print('Port'+str(indexPort[idPort][i])+' RS-485 tidak terdeteksi')

        else:    
            arduinoData = ''
            countDt = 0
            buffer.clear()
            timeout = .100
            flagbuff = False

            timeout_start = time.time()

            Writeregister1(idPort,i,3, 64, int(buff_id_Micom[idPort][i]), 0, 0, 0, 0)
            while (time.time() < timeout_start + timeout):
                if buff_ser[idPort][i].in_waiting > 0:
                    for arduinoData in buff_ser[idPort][i].read():
                        buffer.append(arduinoData)
                        countDt += 1
                        if countDt == 9:
                            flagbuff = True


            if flagbuff == True and buff_type_relay[idPort][i] == 'MICOM P141':
                countDt = 0
                buffer.clear()
                Writeregister1(idPort,i,7, 123, int(buff_id_Micom[idPort][i]), 0, 7, 20, [6, 0])
                timeout_start1 = time.time()
                while (time.time() < timeout_start1 + timeout):
                    if buff_ser[idPort][i].in_waiting > 0:
                        for arduinoData in buff_ser[idPort][i].read():
                            countDt += 1
                            if countDt > 11 and countDt < 16 :
                                buffer.append(chr(arduinoData))
                
                relayTeks[idPort][hitung] = ''.join(buffer)
                
#                 print(relayTeks[idPort][hitung])
                buffcekKoneksi.append(buff_ser[idPort][i])
                
                indexMaster[idPort][hitung] = str(indexPort[idPort][i])
                id_Micom[idPort][hitung] = buff_id_Micom[idPort][i] 
                rak_lokasi[idPort][hitung] = buff_rak_lokasi[idPort][i]
                type_relay[idPort][hitung] = buff_type_relay[idPort][i]
                baudrate[idPort][hitung] = buff_baudrate[idPort][i]
                stop_bit[idPort][hitung] = buff_stop_bit[idPort][i] 
                parity[idPort][hitung] = buff_parity[idPort][i] 
                byte_size[idPort][hitung] = buff_byte_size[idPort][i]
                statusRelay[idPort][hitung] = buff_statusRelay[idPort][i]
                mode[idPort][hitung] = buff_mode[idPort][i]
                port_address[idPort][hitung] = buff_port_address[idPort][i]

                DRdate[idPort][hitung] = buff_DRdate[idPort][i]
                jmlDtDR[idPort][hitung] = buff_jmlDtDR[idPort][i]
                indexDR[idPort][hitung] = buff_indexDR[idPort][i]
                hitungError[idPort][hitung] = buff_hitungError[idPort][i]
                hitungLoop[idPort][hitung] = buff_hitungLoop[idPort][i]
                id_pool[idPort][hitung] = buff_id_pool[idPort][i]
                countCH[idPort][hitung] = buff_countCH[idPort][i]
                countCF[idPort][hitung] = 1
                
                if int(countCH[idPort][i]) > 0:
                    flagDtDR[idPort][hitung] = 1
                    flagDtDR1[idPort][hitung] = 0
                    count[idPort][hitung] = 0
                    
                else:
                    flagDtDR[idPort][hitung] = 0
                    flagDtDR1[idPort][hitung] = 0
                    count[idPort][hitung] = buff_count[idPort][i]
                    
                
                fileDR[idPort][hitung] = buff_fileDR[idPort][i]
                indexFileDR[idPort][hitung] = buff_indexFileDR[idPort][i]
                waktuFileDR[idPort][hitung] = buff_waktuFileDR[idPort][i]
                statusFileDR[idPort][hitung] = buff_statusFileDR[idPort][i]
                lokasiFileDR[idPort][hitung] = buff_lokasiFileDR[idPort][i]

                flag[idPort][hitung] = True
                hitung += 1

            elif flagbuff == False:
                print('Port'+str(indexPort[idPort][i])+' RS-485 tidak dapat menerima data')
                
#         print(indexDR[idPort][i])
#         print(DRdate[idPort][i])
    ser.append(buffcekKoneksi)
#     print(ser)



def resetData():
    buff_id_pool.clear()
    id_pool.clear()
    flag.clear()
    buff_flagDtDR.clear()
    flagDtDR.clear()
    buff_flagDtDR1.clear()
    flagDtDR1.clear()
    buff_hitungError.clear()
    hitungError.clear()
    buff_hitungLoop.clear()
    hitungLoop.clear()
    tanggal.clear()
    bulan.clear()
    tahun.clear()
    jam.clear()
    menit.clear()
    detik.clear()
    buff_DRdate.clear()
    DRdate.clear()
    buff_id_Micom.clear()
    id_Micom.clear()
    buff_count.clear()
    count.clear()
    buff_count3.clear()
    count3.clear()
    buff_countCH.clear()
    countCH.clear()
    countCF.clear()
    buffBanyakData.clear()
    buffPanjangDataASDU.clear()
    buffAddrASDU.clear()
    buffCF.clear()
    buffAddrASDUIn.clear()
    buffIOA.clear()
    buffindexDR.clear()
    buff_indexDR.clear()
    indexDR.clear()
    indexNewDRLSB.clear()
    indexNewDRMSB.clear()
    buff_jmlDtDR.clear()
    jmlDtDR.clear()
    freq.clear()
    buffPollDtDR.clear()
    nameRelay.clear()
    buff_ser.clear()
    ser.clear()
    indexPort .clear()
    buff_baudrate .clear()
    baudrate.clear()
    buff_parity.clear()
    parity.clear()
    buff_stop_bit.clear()
    stop_bit.clear()
    buff_byte_size.clear()
    byte_size.clear()
    buff_fileDR.clear()
    buff_indexFileDR.clear() 
    buff_waktuFileDR.clear() 
    buff_statusFileDR.clear()
    buff_lokasiFileDR.clear()
    fileDR.clear()
    indexFileDR.clear() 
    waktuFileDR.clear()
    statusFileDR.clear() 
    lokasiFileDR.clear()
    buffcekKoneksi.clear()
    buffcekKoneksi1.clear()
    indexMaster.clear()
    buff_type_relay.clear()
    type_relay.clear()
    buff_rak_lokasi.clear()
    rak_lokasi.clear()
    buff_statusRelay.clear()
    statusRelay.clear()
    statusRelay1.clear()
    relayTeks.clear()
    buff_mode.clear()
    mode.clear()
    buff_port_address.clear()
    port_address.clear()
    buff_flagCF.clear()
    flagIndex.clear()
    flagIndex1.clear()
 


def micomP141(idPort,index):
    global flag
    global buffBanyakData
    global buffPanjangDataASDU
    global buffAddrASDU
    global buffCF
    global count
    global countCF
    global buffAddrASDUIn
    global buffIOA
    global flagDtDR
    global countCH
    global flagDtDR1
    global buffer
    global analogCFG
    global digitalCFG
    global lbdigitalCFG 
    global strdigitalCFG


    if flag[idPort][index] == True and int(buffPanjangDataASDU[idPort][index]) != 5 and int(flagDtDR[idPort][index]) == 0 and int(flagDtDR1[idPort][index]) == 0 :
        if int(count[idPort][index]) == 4:
            regAddRTU1[4][3] = indexNewDRLSB[idPort][index]
            regAddRTU1[4][4] = indexNewDRMSB[idPort][index]
        
        Writeregister(idPort, index, regLengthASDU[count[idPort][index]], regCF[countCF[idPort][index]], id_Micom[idPort][index], regTypeID[count[idPort][index]], regVSQ[count[idPort][index]], regCOT[count[idPort][index]], regAddRTU1[count[idPort][index]])
        flag[idPort][index] = False
        
    elif flag[idPort][index] == True and int(buffPanjangDataASDU[idPort][index]) != 5 and int(flagDtDR[idPort][index]) == 1 and int(flagDtDR1[idPort][index]) == 0:
        Writeregister(idPort, index, 7, regCF[countCF[idPort][index]], id_Micom[idPort][index], 0, 7, 20, regChangevalueAddr[countCH[idPort][index]]) 
        count[idPort][index] = -1
        flagDtDR1[idPort][index] = 1
        flagDtDR[idPort][index] = 0
        flag[idPort][index] = False

    elif flag[idPort][index] == True and int(buffPanjangDataASDU[idPort][index]) != 5 and int(flagDtDR[idPort][index]) == 0 and int(flagDtDR1[idPort][index]) == 1:
        Writeregister(idPort, index, 6, regCF[countCF[idPort][index]], id_Micom[idPort][index], 0, 6, 33, [count[idPort][index]])
        flag[idPort][index] = False


    if flag[idPort][index] == True and int(buffPanjangDataASDU[idPort][index]) == 5:
        Writeregister(idPort, index, 5, regCF[countCF[idPort][index]], id_Micom[idPort][index], 0, 5, 16, 0)
        flag[idPort][index] = False

    readMicom(idPort, index)


def readMicom(idPort, index):
    global flag
    global flag2
    global buffBanyakData
    global buffPanjangDataASDU
    global buffAddrASDU
    global buffCF
    global count
    global countCF
    global buffAddrASDUIn
    global buffIOA
    global flagDtDR
    global countCH
    global flagDtDR1
    global buffer
    global analogCFG
    global digitalCFG
    global lbdigitalCFG
    global strdigitalCFG
    global countflagbuff
    
    flagbuff = False
    timeout = .150
    timeout_start = time.time()
        
        
    while (time.time() < timeout_start + timeout):
        if ser[idPort][index].in_waiting > 0 :
            for arduinoData in ser[idPort][index].read():
                buffer.append(arduinoData)
                buffBanyakData[idPort][index] += 1

                if int(buffBanyakData[idPort][index]) == 2:
                    buffPanjangDataASDU[idPort][index] = arduinoData
                    # print(buffPanjangDataASDU)
                elif int(buffBanyakData[idPort][index]) == 5:
                    buffCF[idPort][index] = arduinoData

                elif int(buffBanyakData[idPort][index]) == 9:
                    buffAddrASDU[idPort][index] = arduinoData
                    # print(buffAddrASDU)
                
                elif int(buffBanyakData[idPort][index]) == 10:
                    buffAddrASDUIn[idPort][index] = arduinoData 
                    # print(buffAddrASDUIn)

                elif int(buffBanyakData[idPort][index]) == 11:
                    buffIOA[idPort][index] = arduinoData
                    # print(buffIOA)


                if int(arduinoData) == 22 and int(buffBanyakData[idPort][index]) >= int(buffPanjangDataASDU[idPort][index]) + 6:
#                     print(buffer)
#                     print(count[idPort][index])
#                     print(countCH[idPort][index])
                    
                    if int(buffPanjangDataASDU[idPort][index]) != 5:
                        count[idPort][index] += 1

                    if  int(count[idPort][index]) > 23 and int(flagDtDR1[idPort][index]) == 0 and int(flagDtDR[idPort][index]) == 0: 
                        flagDtDR[idPort][index] = 1
                        count[idPort][index] = 0
                        countCH[idPort][index] = 0
                        mycursor = mydb1.cursor()
                        sql = "UPDATE dataregisterp141 SET flagDtDR = '"+str(flagDtDR[idPort][index])+"', flagDtDR1 = '"+str(flagDtDR1[idPort][index])+"', geser_register = '"+str(count[idPort][index])+"', geser_param = '"+str(countCH[idPort][index])+"', period = '"+str(int(count[idPort][index])+ 1)+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                        mycursor.execute(sql)
                        mydb1.commit()
                        mycursor.close()
                        

                    elif (int(buffPanjangDataASDU[idPort][index]) != 5 and int(buffPanjangDataASDU[idPort][index]) != 7) and int(count[idPort][index]) <= 23 and int(flagDtDR1[idPort][index]) == 0 and int(flagDtDR[idPort][index]) == 0:
                        configDR(idPort,index,buffer,count[idPort][index])
                        mycursor = mydb1.cursor()
                        sql = "UPDATE dataregisterp141 SET flagDtDR = '"+str(flagDtDR[idPort][index])+"', flagDtDR1 = '"+str(flagDtDR1[idPort][index])+"', geser_register = '"+str(count[idPort][index])+"', geser_param = '"+str(countCH[idPort][index])+"', period = '"+str(int(count[idPort][index])+ 1)+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                        mycursor.execute(sql)
                        mydb1.commit()
                        mycursor.close()
                        

                    if int(buffPanjangDataASDU[idPort][index]) == 7 and int(buffAddrASDUIn[idPort][index]) == 17 and int(buffIOA[idPort][index]) == int(count[idPort][index])-1 and int(flagDtDR[idPort][index]) == 0 and int(flagDtDR1[idPort][index]) == 1:
                        flagDtDR1[idPort][index] = 0
                        flagDtDR[idPort][index] = 1
                        countCH[idPort][index] += 1
                        
                        mycursor = mydb1.cursor()
                        sql = "UPDATE dataregisterp141 SET flagDtDR = '"+str(flagDtDR[idPort][index])+"', flagDtDR1 = '"+str(flagDtDR1[idPort][index])+"', geser_register = '"+str(count[idPort][index])+"', geser_param = '"+str(countCH[idPort][index])+"', period = '"+str(int(count[idPort][index])+ 1)+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                        mycursor.execute(sql)
                        mydb1.commit()
                        mycursor.close()
                        

                        if int(countCH[idPort][index]) > 11:
                            bentukFile(idPort,index)
                            
                            flagDtDR1[idPort][index] = 0
                            flagDtDR[idPort][index] = 0
                            id_pool[idPort][index] += 1
                            count[idPort][index] = 0
                            countCH[idPort][index] = 0
                            count3[idPort][index] = 0
                            analogCFG = ['','','','','','','','','']
                            digitalCFG = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
                            lbdigitalCFG = []
                            strdigitalCFG = ''
                            
                            if int(id_pool[idPort][index]) > 9:
                                id_pool[idPort][index] = 0
                            
                            mycursor = mydb1.cursor()
                            sql = "UPDATE dataregisterp141 SET flagDtDR = '"+str(flagDtDR[idPort][index])+"', flagDtDR1 = '"+str(flagDtDR1[idPort][index])+"', geser_register = '"+str(count[idPort][index])+"', geser_param = '"+str(countCH[idPort][index])+"', period = '"+str(int(count[idPort][index])+ 1)+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                            mycursor.execute(sql)
                            mydb1.commit()
                            mycursor.close()
        
                    
                    elif (int(buffPanjangDataASDU[idPort][index]) != 5 and int(buffPanjangDataASDU[idPort][index]) != 7) and int(flagDtDR[idPort][index]) == 0 and int(flagDtDR1[idPort][index]) == 1:
                        pollDR(idPort,index)
                        mycursor = mydb1.cursor()
                        sql = "UPDATE dataregisterp141 SET flagDtDR = '"+str(flagDtDR[idPort][index])+"', flagDtDR1 = '"+str(flagDtDR1[idPort][index])+"', geser_register = '"+str(count[idPort][index])+"', geser_param = '"+str(countCH[idPort][index])+"', period = '"+str(int(count[idPort][index])+ 1)+"', id_pool = '"+str(id_pool[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                        mycursor.execute(sql)
                        mydb1.commit()
                        mycursor.close()


                    if int(buffCF[idPort][index]) != 0 and int(buffPanjangDataASDU[idPort][index]) != 3:
                        countCF[idPort][index] += 1
                        mycursor = mydb1.cursor()
                        sql = "UPDATE dataregisterp141 SET flag = '"+str(countCF[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                        mycursor.execute(sql)
                        mydb1.commit()
                        mycursor.close()

                    else:
                        count[idPort][index] = 0
                        countCF[idPort][index] = 0


                    if int(countCF[idPort][index]) > 1:
                        countCF[idPort][index] = 0
                        mycursor = mydb1.cursor()
                        sql = "UPDATE dataregisterp141 SET flag = '"+str(countCF[idPort][index])+"' WHERE port_device='"+str(idPort)+"' AND id_device='"+str(indexMaster[idPort][index])+"'"
                        mycursor.execute(sql)
                        mydb1.commit()
                        mycursor.close()
                        
                    buffer.clear()
                    countflagbuff = 0
                    
                    flag[idPort][index] = True
                    buffBanyakData[idPort][index] = 0
                    
                    flagbuff = True
                    

    if (time.time() >= timeout_start + timeout) and flagbuff == False:
        arduinoData = ''
        countDt = 0
        buffer.clear()
        timeout = .100
        flagbuff = False

        timeout_start = time.time()

        Writeregister(idPort,index,3, 64, int(id_Micom[idPort][index]), 0, 0, 0, 0)
        while (time.time() < timeout_start + timeout):
            if ser[idPort][index].in_waiting > 0:
                for arduinoData in ser[idPort][index].read():
                    buffer.append(arduinoData)
                    countDt += 1
                    if countDt == 9:
                        countCF[idPort][index] = 0
        
        
        
        hitungError[idPort][index] += 1
        flag[idPort][index] = True
        
        if hitungError[idPort][index] > 9:
            flag2 = True
            hitungError[idPort][index] = 0


# sistemconfig()
# 
# while True:    
#     for i in range(0, len(ser[0])):
#         idPort = 0
#         micomP141(idPort,i)