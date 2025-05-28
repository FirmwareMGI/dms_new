from sqlite3 import register_adapter
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import mqtt
import time
import IEC61850.db

dbMqtt = db.readDb.network_mqtt(0)

mqtt = mqtt.MQTT(0)
flagConnect = 0


def reconnectMqtt():
    global client
    global flagConnect
    try:
        dbMqtt = db.readDb.network_mqtt(0)
        mqttUser = dbMqtt[0]['mqtt_username']
        mqttPass = dbMqtt[0]['mqtt_pass']
        broker = dbMqtt[0]['mqtt_server']
        port = dbMqtt[0]['mqtt_port']
        client = mqtt.connect_mqtt(mqttUser, mqttPass, broker, port)
        client.loop_start()
        # mqtt.loop_forever()
    except:
        print("mqtt Not Connect")
        time.sleep(2)
        if(flagConnect < 5):
            reconnectMqtt()
        flagConnect = flagConnect+1


reconnectMqtt()


def readMeasurement(con, units):
    global client
    try:
        baca = con.read_holding_registers(address=48, count=8, unit=units)
        baca2 = con.read_holding_registers(address=18, count=2, unit=units)
        print(baca.registers)
        param = ["IA", "IB", "IC", "IN"]

        j = 0
        print(str(units))
        for i in range(len(param)):
            dataOut = {
                f"alias": f"{param[i]}", "val": baca.registers[j]/100, "dataType": "float"}
            idModbus = str(units)
            kode_wilayah = "0001"
            try:
                mqtt.send(
                    client, f"DMS/{kode_wilayah}/MODBUS/{idModbus}/{param[i]}", str(dataOut))
            except:
                print("mqtt err")
            j = j+2
            time.sleep(0.5)
        print("TRIP")
        bufTrip = False
        if(baca2.registers[0] == 2):
            bufTrip = True
        else:
            bufTrip = False
        dataOut = {f"alias": f"TRIP", "val": bufTrip, "dataType": "Boolean"}
        mqtt.send(
            client, f"DMS/{kode_wilayah}/MODBUS/{idModbus}/TRIP", str(dataOut))
        time.sleep(0.5)
    except:
        print("register err")
