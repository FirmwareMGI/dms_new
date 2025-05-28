import db
import requests

dbMqtt = db.readDb.network_mqtt(0)
print(dbMqtt)


def connectMqtt(mqtt):
    global mqttRetry
    global client
    # if (client != None):
    #     print("rekonnect mqtt")
    #     client.disconnect()
    dbMqtt = db.readDb.network_mqtt(0)
    mqttUser = dbMqtt[0]['mqtt_username']
    mqttPass = dbMqtt[0]['mqtt_pass']
    broker = dbMqtt[0]['mqtt_server']
    port = dbMqtt[0]['mqtt_port']
    print(mqttUser)
    print(mqttPass)
    print(broker)
    print(port)


resp = requests.post(
    'https://api.telegram.org/bot866502411:AAE7efXmuRG6KSOfu1hB275pEplEKMrAq5E/sendMessage?chat_id=966975362&text='+"test")
print(resp)
