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
# print(mesin_mesin)
mqtt = mqtt.MQTT(0)
flagConnect = 0

client_local = None
client_server = None


def int_to_8bit(integer):
    # if integer < 0 or integer > 255:
    #     raise ValueError("Integer harus dalam rentang 0-255")

    # Mengonversi integer ke representasi biner
    # menghilangkan '0b' dan menambahkan 0 di depan jika kurang dari 8 bit
    binary = bin(integer)[2:].zfill(16)
    return binary


def reconnectMqtt():
    global client_local
    global client_server
    global flagConnect

    try:
        dbMqtt = db.readDb.network_mqtt(0)
        mqttUser = dbMqtt[0]['mqtt_username']
        mqttPass = dbMqtt[0]['mqtt_pass']
        broker = dbMqtt[0]['mqtt_server']
        port = dbMqtt[0]['mqtt_port']
        client_local = mqtt.connect_mqtt('', '', 'localhost', 1883)
        client_local.loop_start()
        client_server = mqtt.connect_mqtt(mqttUser, mqttPass, broker, port)        
        client_server.loop_start()
        # mqtt.loop_forever()
    except:
        print("mqtt Not Connect")
        time.sleep(2)
        if (flagConnect < 5):
            reconnectMqtt()
        flagConnect = flagConnect+1


reconnectMqtt()


def readMeasurement(con, units):
    global client_local
    global client_server
    baca = con.read_holding_registers(address=1, count=102, unit=8)
    print(baca)
    # baca = con.read_holding_registers(address=7, count=36, unit=units)
    measur1 = baca.registers[6:18]
    measur2 = baca.registers[22:35]
    suhu_list = baca.registers[100:102]
    boolmu = baca.registers[0:5]
    # print(baca.registers)
    param = ["VRS", "VST", "VRT", "VRN", "VSN", "VTN", "IR", "IS", "IT", "FR"]
    param2 = ["BV", "BC", "BC2", "BC3", "ODC", "OA",
              "IV", "OP", "IAP", "AP1", "AP2", "AP3", "ARP"]
    param3 = ["Temp P1", "Temp P2"]
    idModbus = str(units)
    # print(baca2.registers)

    # bolean
    param4 = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
              "A9", "A10", "A11", "A12", "A13", "A14", "A15", "A16"]
    dataLamp = int_to_8bit(boolmu[0])
    # print(dataLamp)
    for i in range(len(dataLamp)):
        dt = False
        if (int(dataLamp[i])) == 0:
            dt = "False"
        elif (int(dataLamp[i])) == 1:
            dt = "True"
        dataOut = {
            f"alias": f"{param4[i]}", "val": dt, "dataType": "boolean"}
        dataOut = str(dataOut).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param4[i]}"
        print(dataOut)
        try:
            # mqtt_publish.single(topic, str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
            #     port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
        except:
            print("mqtt err")
            # print(dataOut)
            time.sleep(0.5)
    dataLamp = int_to_8bit(boolmu[1])
    param5 = ["A17", "A18", "A19", "A20", "A21", "A22", "A23",
              "A24", "A25", "A26", "A27", "OO", "O1", "A30", "A31", "A32"]
    # print(dataLamp)
    for i in range(len(dataLamp)):
        dt = False
        if (int(dataLamp[i])) == 0:
            dt = "False"
        elif (int(dataLamp[i])) == 1:
            dt = "True"
        dataOut = {
            f"alias": "tes", f"{param5[i]}": dt, "dataType": "boolean"}
        dataOut = str(dataOut).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param5[i]}"
        print(dataOut)
        try:
            # mqtt_publish.single(topic, str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
            #     port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
        except:
            print("mqtt err")
            # print(dataOut)
            time.sleep(0.5)
    dataLamp = int_to_8bit(boolmu[3])
    param7 = ["O2", "A50", "A51", "A52", "A53", "A54", "A55",
              "A56", "A57", "A58", "A59", "O3", "O4", "A62", "A63", "A64"]
    # print(dataLamp)
    for i in range(len(dataLamp)):
        dt = False
        if (int(dataLamp[i])) == 0:
            dt = "False"
        elif (int(dataLamp[i])) == 1:
            dt = "True"
        dataOut = {
            f"alias": f"{param7[i]}", "val": dt, "dataType": "boolean"}
        dataOut = str(dataOut).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param7[i]}"
        # print(dataOut)
        try:
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
            # mqtt_publish.single(topic, str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
            #     port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
        except:
            print("mqtt err")
            # print(dataOut)
            time.sleep(0.5)

    dataLamp = int_to_8bit(boolmu[4])
    walek = dataLamp[::-1]
    param8 = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8",
              "S9", "S10", "S11", "S12", "S13", "O5", "O6", "O7"]
    # print(walek)
    for i in range(len(walek)):
        dt = False
        if (int(walek[i])) == 0:
            dt = "False"
        elif (int(walek[i])) == 1:
            dt = "True"
        dataOut = {
            f"alias": f"{param8[i]}", "val": dt, "dataType": "boolean"}
        dataOut = str(dataOut).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param8[i]}"
        print(dataOut)
        try:
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
            # mqtt_publish.single(topic, str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
            #     port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
        except:
            print("mqtt err")
            # print(dataOut)
            time.sleep(0.5)

    # SUHU
    for i in range(len(suhu_list)):
        dataOut = {
            "alias": f"{mesin_mesin}{idModbus}{param3[i]}", "val": suhu_list[i], "dataType": "float"}
        dataOut = str(dataOut).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param3[i]}"

        try:
            # mqtt_publish.single(topic, str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
            #         port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
        except:
            print("mqtt err")
        print(dataOut)
        time.sleep(0.5)

    # PARAM
    for i in range(len(param)):
        dataOut = {
            f"alias": f"{mesin_mesin}{idModbus}{param[i]}", "val": measur1[i], "dataType": "float"}
        dataOut = str(dataOut).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param[i]}"
        try:
            # mqtt_publish.single(topic, str(dataOut), hostname=dbMqtt[0]['mqtt_server'],
            #         port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
        except:
            print("mqtt err")
        print(dataOut)
        time.sleep(0.5)

    for i in range(len(param2)):
        dataOut1 = {
            f"alias": f"{mesin_mesin}{idModbus}{param2[i]}", "val": measur2[i], "dataType": "float"}
        print(dataOut1)
        dataOut1 = str(dataOut1).replace("'", "\"")
        topic = f"DMS/{mesin_mesin}/MODBUS/{idModbus}/{param2[i]}"
        try:
            # mqtt_publish.single(topic, str(dataOut1), hostname=dbMqtt[0]['mqtt_server'],
            #         port=dbMqtt[0]['mqtt_port'], auth={'username':dbMqtt[0]['mqtt_username'], 'password':dbMqtt[0]['mqtt_pass']})
            mqtt.send(client_local, topic, str(dataOut))
            mqtt.send(client_server, topic, str(dataOut))
        except:
            print("mqtt err")
        time.sleep(0.1)
