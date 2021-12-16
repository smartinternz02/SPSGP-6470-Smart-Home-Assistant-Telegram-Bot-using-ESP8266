import wiotp.sdk.device
import time
import random


myConfig = { 
    "identity": {
        "orgId": "3cfp21",
        "typeId": "NodeMCU",
        "deviceId":"54321"
    },
    "auth": {
        "token": "12345678"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

while True:
    temp=random.randint(0,100)
    hum=random.randint(0,100)
    li=random.randint(100,300)
    myData={'Temperature':temp, 'Humidity':hum, 'LightIntensity':li}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    time.sleep(2)
client.disconnect()


