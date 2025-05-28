from ast import Return
import code
from time import time
from pymodbus.client.sync  import ModbusSerialClient as ModbusClient
import struct
from datetime import date, datetime, timedelta
import database_event as databaseEvent

import time
fileName=""
cekStatus=""
_event_Dict = []

class eventp123:
    global _event_Dict

    addrCount = []

    def __init__(self,inputIdPort,inputIndex):
        self.index = inputIndex
        self.idPort = inputIdPort
        

    def pollEvent(self,port, unit):
        self.clearData()
        self.config()
        global fileName
        global cekStatus
        cekStatus = ModbusClient(method='rtu', port='/dev/ttyUSB'+str(port),  stopbits = 1 , bytesize = 8, parity = 'N',baudrate= 19200, timeout=1)
        connection = cekStatus.connect()

        buffP=["",""]
        eventData = ''
        
        indexEvent = 0
        readHead = cekStatus.read_holding_registers(address =0, count =10,unit= unit)
        #print(readHead.registers)
        buffP[0]=(hex(readHead.registers[0]))[2:]
        buffP[1]= (hex(readHead.registers[1]))[2:]
        pName = (bytes.fromhex(buffP[0]).decode("ASCII"))+(bytes.fromhex(buffP[1]).decode("ASCII"))
        #print(fileName)
        eventData+=self.header(pName)
        
        for i in range(0,250):
            eventp123.addrCount[self.idPort][self.index] = i
            # connection = micomp123.client[self.index][self.idPort].connect()
           
            if connection:
                # readData = micomp123.client[self.index][self.idPort].read_holding_registers(address = 13568 + int(i), count =9,unit= int(micomp123.id_micom[self.index][self.idPort]))
                readData = cekStatus.read_holding_registers(address = 13568 + int(i), count =9,unit= unit)

                if readData.isError():
                    # print('Port'+str(micomp123.indexMaster[self.index][self.idPort])+' RS-485 tidak dapat menerima data')
                    print('Port'+str(0)+' RS-485 tidak dapat menerima data EVENT')
                    
                else:
                    #print(readData.registers)
                  
                    code = readData.registers[0]
                    linkedValue = readData.registers[1]
                    linkTabel = readData.registers[2]
                    second_1 = hex(readData.registers[4])[2:]
                    second_2 = hex(readData.registers[5])[2:]
                    milisec_1 = readData.registers[6]
                    milisec_2 = readData.registers[7]
                    Acknowledgement = readData.registers[8]

                    second_1f = second_1.rjust(4,'0')
                    second_2f = second_2.rjust(4,'0')

                    secTot = struct.unpack('>i', bytes.fromhex(second_2f + second_1f))
                    base_date = datetime(1994,1,1)

                    dateNow = base_date + timedelta(seconds=int(secTot[0])) + timedelta(milliseconds=milisec_1)
                    dateNow = dateNow.strftime("%m/%d/%Y,%H:%M:%S.%f")

                    hasilDataEvent = [dateNow, i+1,code,linkedValue,linkTabel,Acknowledgement,'0']
                    eventp123.eventDict(self,hasilDataEvent)
                    
            else:
                # print('Port'+str(micomp123.indexMaster[self.index][self.idPort])+' RS-485 tidak terhubung')
                print('Port'+str(0)+' RS-485 tidak terhubung')


        for i in range(0,25):
            eventp123.addrCount[self.index][self.idPort] = i
            # connection = micomp123.client[self.index][self.idPort].connect()
           
            if connection:
                # readData = micomp123.client[self.index][self.idPort].read_holding_registers(address = 13568 + int(i), count =9,unit= int(micomp123.id_micom[self.index][self.idPort]))
                readData = cekStatus.read_holding_registers(address = 14080 + int(i), count =15,unit= unit)
                #res=''.join(str(readData.registers))
                #f = open("data/register", "a")
                #f.write(res +"\n")
                #f.close()

                if readData.isError():
                    # print('Port'+str(micomp123.indexMaster[self.index][self.idPort])+' RS-485 tidak dapat menerima data')
                    print('Port'+str(0)+' RS-485 tidak dapat menerima data FAULT')
                    
                else:
                    readData1 = cekStatus.read_holding_registers(address = 288, count =1,unit= unit)
                    
                    num = readData.registers[0]
                    second_1 = hex(readData.registers[1])[2:]
                    second_2 = hex(readData.registers[2])[2:]
                    milisec_1 = readData.registers[3]
                    milisec_2 = readData.registers[4]
                    season = readData.registers[5]
                    grpFormat = readData.registers[6]
                    faultType = readData.registers[7]
                    faultProtect = readData.registers[8]
                    faultAmplitude = readData.registers[9]*readData1.registers[0]/800
                    phaseA = readData.registers[10]*readData1.registers[0]/800
                    phaseB = readData.registers[11]*readData1.registers[0]/800
                    phaseC = readData.registers[12]*readData1.registers[0]/800
                    earthCurrent = readData.registers[13]
                    earthDerived = readData.registers[14]
                    

                    second_1f = second_1.rjust(4,'0')
                    second_2f = second_2.rjust(4,'0')

                    secTot = struct.unpack('>i', bytes.fromhex(second_2f + second_1f))
                    base_date = datetime(1994,1,1)

                    dateNow = base_date + timedelta(seconds=int(secTot[0])) + timedelta(milliseconds=milisec_1)
                    dateNow = dateNow.strftime("%m/%d/%Y,%H:%M:%S.%f")

                    hasilDataEvent = [dateNow, num,season,grpFormat,faultType,faultProtect,'1',faultAmplitude,phaseA,phaseB,phaseC,earthCurrent,earthDerived]
                    eventp123.eventDict(self,hasilDataEvent)

            else:
                # print('Port'+str(micomp123.indexMaster[self.index][self.idPort])+' RS-485 tidak terhubung')
                print('Port'+str(0)+' RS-485 tidak terhubung')
        
        
        ordered_data = sorted(_event_Dict,key=lambda x:datetime.strptime(x[0],'%m/%d/%Y,%H:%M:%S.%f'),reverse=True)
        # print("ordered Data: " + ordered_data[0][0])

        # print(len(ordered_data))
                
        for i in range(0,len(ordered_data)):
            indexEvent = i + 1

            if ordered_data[i][6] == '0':
                _lineCount = len(self.eventValueNumber(ordered_data[i][2]))
                eventData += '[Event '+ str(indexEvent)+']\n'
                eventData += 'Date='+ ordered_data[i][0][:-16]+'\n'
                eventData += 'Time='+ ordered_data[i][0][:23]+'\n'
                eventData += 'Type=Event\n'
                eventData += 'Ack='+ str(ordered_data[i][5])+'\n'
                eventData += 'Num='+str(ordered_data[i][1])+'\n'
                eventData += 'Code='+str(ordered_data[i][2])+'\n'
                eventData += 'LinkedValue='+str(ordered_data[i][3])+'\n'
                eventData += 'Title='+ordered_data[i][0][:23]+' Event : '+str(self.CodeNumber(ordered_data[i][2]))+'\n'
                eventData += 'Line '+str(1).rjust(3,'0')+'=Event Label : '+str(self.CodeNumber(ordered_data[i][2]))+'\n'

                if int(ordered_data[i][2]) == 50:
                    eventData += 'Line '+str(2).rjust(3,'0')+'=Linked Value : '+str(' '.join(str(bin(ordered_data[i][3]))[2:].rjust(9,'0')))+'\n'
                    for j in range(0,_lineCount):
                        eventData += 'Line '+str(j+3).rjust(3,'0')+'=-'+str(self.eventValueNumber(ordered_data[i][2])[j])+str(bin(ordered_data[i][3]))[2:].rjust(9,'0')[_lineCount-(j+1)]+'\n'

                    if int(ordered_data[i][5]) == 0:
                        eventData += 'Line '+str(_lineCount+3).rjust(3,'0')+'=Acknowledgment : Not acknowleged\n'
                    elif int(ordered_data[i][5]) == 1:
                        eventData += 'Line '+str(_lineCount+3).rjust(3,'0')+'=Acknowledgment : acknowleged\n'
                    
                    eventData += 'LineCount='+str(_lineCount+3)+'\n'

                else:
                    if str(self.eventValueNumber(ordered_data[i][2])[0]) !='0':
                        for j in range(0,_lineCount):
                            eventData += 'Line '+str(j+2).rjust(3,'0')+'=-'+str(self.eventValueNumber(ordered_data[i][2])[j])+str(hex(ordered_data[i][3]).lstrip("0x")).rjust(4,'0')+'h\n'

                        if int(ordered_data[i][5]) == 0:
                            eventData += 'Line '+str(_lineCount+2).rjust(3,'0')+'=Acknowledgment : Not acknowleged\n'
                        elif int(ordered_data[i][5]) == 1:
                            eventData += 'Line '+str(_lineCount+2).rjust(3,'0')+'=Acknowledgment : acknowleged\n'
                        
                        eventData += 'LineCount='+str(_lineCount+2)+'\n'
                    
                    else:
                        if int(ordered_data[i][5]) == 0:
                            eventData += 'Line '+str(_lineCount+1).rjust(3,'0')+'=Acknowledgment : Not acknowleged\n'
                        elif int(ordered_data[i][5]) == 1:
                            eventData += 'Line '+str(_lineCount+1).rjust(3,'0')+'=Acknowledgment : acknowleged\n'
                        
                        eventData += 'LineCount='+str(_lineCount+1)+'\n'
            
                eventData += 'Filter='+str(self.filterNumber(ordered_data[i][2]))+'\n'
                eventData += 'FileType=0'+'\n\n\n'

            else:
                eventData += '[Event '+ str(indexEvent)+']\n'
                eventData += 'Date='+ ordered_data[i][0][:-16]+'\n'
                eventData += 'Time='+ ordered_data[i][0][11:]+'\n'
                eventData += 'Type=Fault\n'
                eventData += 'Ack=0\n'
                eventData += 'Num='+str(ordered_data[i][1])+'\n'
                eventData += 'Code='+str(ordered_data[i][5])+'\n'
                eventData += 'LinkedValue='+str(ordered_data[i][4])+'\n'
                eventData += 'Title='+ordered_data[i][0]+' Fault : '+str(self.FaultNumber(ordered_data[i][5]))+'\n'
                eventData += 'Line '+str(1).rjust(3,'0')+'=Fault Type : '+str(self.FaultNumber(ordered_data[i][5]))+'\n'
                eventData += 'Line '+str(2).rjust(3,'0')+'=Faulty Phase : '+str(self.FaultValueNumber(ordered_data[i][5]))+'\n'
                eventData += 'Line '+str(3).rjust(3,'0')+'=Magnitudes : \n'
                eventData += 'Line '+str(4).rjust(3,'0')+'=-  Fault Magnitude Value ............................... '+str(ordered_data[i][7])+' A\n'
                eventData += 'Line '+str(5).rjust(3,'0')+'=-  Phase A Magnitude (RMS) ............................. '+str(ordered_data[i][8])+' A\n'
                eventData += 'Line '+str(6).rjust(3,'0')+'=-  Phase B Magnitude (RMS) ............................. '+str(ordered_data[i][9])+' A\n'
                eventData += 'Line '+str(7).rjust(3,'0')+'=-  Phase C Magnitude (RMS) ............................. '+str(ordered_data[i][10])+' A\n'
                eventData += 'Line '+str(8).rjust(3,'0')+'=-  Earth/Ground Magnitude (RMS) ........................ '+str(ordered_data[i][11])+' A\n'
                eventData += 'Line '+str(9).rjust(3,'0')+'=Active Configuration Group : '+str(ordered_data[i][3])+'\n'
                eventData += 'Line '+str(10).rjust(3,'0')+'=Fault Number : '+str(ordered_data[i][1])+'\n'
                eventData += 'LineCount =10\n'
                eventData += 'Filter ='+str(self.filterFaultNumber(ordered_data[i][5]))+'\n'
                eventData += 'FileType =0\n\n\n'

        
        
        self.saveFile(fileName+".eve",eventData)
        print(eventData)
        time.sleep(0.1)
            

    def eventDict(self,value):  
            _event_Dict.append(value)
            

    def CodeNumber(self,code):
        return databaseEvent.code_value(code)

    def filterNumber(self,code):
        return databaseEvent.filter(code)
    
    def eventValueNumber(self,code):
        return databaseEvent.event_value(code)
   
    def FaultNumber(self,code):
        return databaseEvent.FaultCode_value(code)

    def FaultValueNumber(self,code):
        return databaseEvent.FaultPhase(code)

    def filterFaultNumber(self,code):
        return databaseEvent.filterFault(code)
        
    def config(self):
        for i in range(0, 2):
            eventp123.addrCount.append([0 for x in range(0, 1)])      

    def clearData(self):
        eventp123.addrCount.clear()
        _event_Dict.clear()
    def saveFile(self,name,res):
        print("datasaved")
        f = open("dataEV/"+name, "w")
        f.write(res)
        print(f"{name} saved")
        f.close()
       # exit()
        
    def header(self,pnme):
        #readData = self.pollEvent.cekStatus.read_holding_registers(address = 13568, count =9,unit= 1)
        #print(readData)
        eventData=''
        eventData +="[General]\n"
        eventData +="Version=1.A\n"
        eventData +="Language=44\n\n"
        eventData +="[Relay]\n"
        eventData +="Name=MiCOM "+pnme+" BXXXXXX V12.E\n"
        eventData +="Address=1\n"
        eventData +="Version=12.E\n\n"
        eventData += "[Events]\n"
        eventData +="Count=275\n\n"
        #print(eventData)
        return eventData

# eventp123(0,0).CodeNumber('50')
#eventp123(0,0).pollEvent()