from sqlite3 import register_adapter
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import mqtt
import time
import IEC61850.db as db
import paho.mqtt.publish as mqtt_publish

dbMqtt = db.readDb.network_mqtt(0)
DBdataMMesin = db.readDb.m_mesin(0)
mesin_mesin = DBdataMMesin[0]['kode_mesin']
#print(mesin_mesin)
mqtt = mqtt.MQTT(0)
flagConnect = 0

mqtt_client_server = None
mqtt_client_local = None

def reconnectMqtt():
    global mqtt_client_local
    global mqtt_client_server
    global flagConnect
    try:
        dbMqtt = db.readDb.network_mqtt(0)
        mqttUser = dbMqtt[0]['mqtt_username']
        mqttPass = dbMqtt[0]['mqtt_pass']
        broker = dbMqtt[0]['mqtt_server']
        port = dbMqtt[0]['mqtt_port']
        mqtt_client_local = mqtt.connect_mqtt('', '', 'localhost', 1883)
        mqtt_client_local.loop_start()
        mqtt_client_server = mqtt.connect_mqtt(mqttUser, mqttPass, broker, port)
        mqtt_client_server.loop_start()
    except:
        print("mqtt Not Connect")
        time.sleep(2)
        if(flagConnect < 5):
            reconnectMqtt()
        flagConnect = flagConnect+1


reconnectMqtt()

def int_to_8bit(integer):
    if integer < 0 or integer > 255:
        raise ValueError("Integer harus dalam rentang 0-255")

    # Mengonversi integer ke representasi biner
    binary = bin(integer)[2:].zfill(8)  # menghilangkan '0b' dan menambahkan 0 di depan jika kurang dari 8 bit
    return binary

def readMeasurement(con, units):
    global client
    try:
        baca = con.read_holding_registers(address=48, count=8, unit=units)
        baca2 = con.read_holding_registers(address=18, count=2, unit=units)
        #baca3 = con.read_holding_registers(address=4608, count=2, unit=units)
        #print(baca.registers)
        param = ["IA", "IB", "IC", "IN"]
        param2=["T4","T3","T2","T1","HEALTHY","ALARM","TRIP"]

        j = 0
        #print(str(units))
        for i in range(len(param)):
            dataOut = {
                f"alias": f"{param[i]}", "val": baca.registers[j]/100, "dataType": "float"}
            idModbus = str(units)
            #kode_wilayah = "0001"
            try:
                mqtt.send(
                    client, f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param[i]}", str(dataOut))
            except:
                print("mqtt err")
            j = j+2
            print(baca)
            time.sleep(0.5)
        #print("TRIP")
#        bufTrip = False
#        if(baca2.registers[0] == 2):
#            bufTrip = True
#            dataOut = {f"alias": f"TRIP", "val": "true", "dataType": "Boolean"}
#        else:
#            bufTrip = False
#            dataOut = {f"alias": f"TRIP", "val": "false", "dataType": "Boolean"}
#        #dataOut = {f"alias": f"TRIP", "val": bufTrip, "dataType": "Boolean"}
#        mqtt.send(
#            client, f"DMS/{mesin_mesin}/MODBUS/{idModbus}/TRIP", str(dataOut))
#        time.sleep(0.5)
        #print(baca2.registers[0])
        dataLamp=int_to_8bit(baca2.registers[0] )
        print(dataLamp)
        for i in range(len(param2)):
            dt =False
        if(int(dataLamp[i]))==0:
            dt="False"
        elif (int(dataLamp[i]))==1 :
            dt="True"
        dataOut = {
            f"alias": f"{idModbus}{param2[i]}", "val": dt, "dataType": "boolean"}
        try:
            mqtt.send(
                 client, f"DMS/{kode_wilayah}/MODBUS/{idModbus}/{param2[i]}", str(dataOut))
        except NameError:
            print(NameError)
            reconnectMqtt()
        #print(dataOut)
        time.sleep(0.5)
    except:
        print("register err")
        
def readMeasurementSingle(con,units):
    global client
    try:
        baca = con.read_holding_registers(address=48, count=8, unit=units)
        baca2 = con.read_holding_registers(address=12, count=2, unit=units)
        #baca3 = con.read_holding_registers(address=4608, count=2, unit=units)
        #print(baca.registers)
        param = ["IA", "IB", "IC", "IN"]
        param2=["T4","T3","T2","T1","HEALTHY","ALARM","TRIP"]
        #print(idModbus)
        j = 0
        print(str(units))
        for i in range(len(param)):
            dataOut = {
                f"alias": f"{mesin_mesin}{str(units)}{param[i]}", "val": baca.registers[j]/100, "dataType": "float"}
            idModbus = str(units)
            dataOut = str(dataOut)
            dataOut = dataOut.replace("'", '"')
            #kode_wilayah = "0001"
            try:
                mqtt_publish.single(f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param[i]}", str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
                    port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
                #mqtt_publish.single(f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param[i]}", str(dataOut), hostname='localhost',
                #    port=1883)
                mqtt.send(
                    mqtt_client_local, f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param[i]}", str(dataOut))
            except:
                print("mqtt err")
            j = j+2
            time.sleep(0.5)
    
        #print("BACA REGISTER", baca2.registers[0])
        dataLamp=int_to_8bit(baca2.registers[0] )
        print("DATALAMP",dataLamp)
        for i in range(len(param2)):
            dt =False
            if(int(dataLamp[i]))==0:
                dt="False"
            elif (int(dataLamp[i]))==1 :
                dt="True"
            dataOut = {
                f"alias": f"{mesin_mesin}{str(units)}{param2[i]}", "val": dt, "dataType": "boolean"}
            print(dataOut)
            dataOut = str(dataOut)
            dataOut = dataOut.replace("'", '"')
            topic = f"DMS/{mesin_mesin}/MODBUS/{str(units)}/{param2[i]}"
            print(topic)
            try:
                mqtt_publish.single(topic, dataOut, hostname=dbMqtt[0]['mqtt_server'],
                    port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
                #mqtt_publish.single(f"DMS/{mesin_mesin}/MODBUS/{str(units)}/{param2[i]}", dataOut, hostname='localhost',
                #    port=1883)
                mqtt.send(
                    mqtt_client_local, f"DMS/{mesin_mesin}/MODBUS/{str(units)}/{param2[i]}", str(dataOut))
            except NameError:
                print(NameError)
            time.sleep(0.5)
    except:
        print("register err")
