import random
import time
from paho.mqtt import client as mqtt_client
import json

#broker = "203.194.112.238"
#port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = 'python-mqtt-'+str(random.randint(0, 1000))
client2=None
username = 'das'
password = 'mgi2022'

class MQTT():
    def __init__(self,index):
        self.index = index
    def connect_mqtt(self,name,passw,broker,port):
        #client=1
        #userdata=2

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        #name=""
        #passw=""
        #print (name)
        client = mqtt_client.Client(client_id,clean_session=False)
        client = mqtt_client.Client(client_id)
        client.username_pw_set(name, passw)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    
    def publish(self,client):
        msg_count = 0
        while True:
            #time.sleep(1)
            msg = "messages: "+str(msg_count)
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print("Send "+msg+" to topic "+topic)
            else:
                print("Failed to send message to topic "+topic)
                break
            msg_count += 1
    def send(self,client,topic,message):
        global client2
        msg=message
        #topic=f"DASPOWER/{kode}/{idm}"
        dt=str(msg).replace("'", "\"")
        #print(dt)
        result = client.publish(topic, dt,qos=0)
        try:
            client2.publish(topic, dt,qos=0)
        except:
            print("fail save ")
        status = result[0]
        if status == 0:
            print("Send "+msg+" to topic "+topic)
        else:
            print("Failed to send message to topic "+topic)
    #def sendData(self,message):
       # send(message)

    def run(self):
        client = self.connect_mqtt()
        client.loop_start()
        self.send(client,"mqtt Connect")

mqtt=MQTT(0)
client2=mqtt.connect_mqtt("das","mgi2023","127.0.0.1",1883)
#mqtt.connect_mqtt(mqttUser, mqttPass, broker, port)
# if __name__ == '__main__':
    
#    mqtt=MQTT(0)
#    client=mqtt.connect_mqtt()
#    client.loop_start()
#    mqtt.send(client,"HAHAH")

    #MQTT(0).run()