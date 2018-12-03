#!/usr/bin/env python3
"""
@author = Paolo Grasso
"""

import paho.mqtt.client as PahoMQTT
import time
import datetime
import json

BROKER_IP = '192.168.1.28'

class MyPublisher(object):
    def __init__(self, clientID, serverIP):
        self.clientID = clientID
        self.messageBroker = serverIP
        self._paho_mqtt = PahoMQTT.Client(self.clientID, False)
        self._paho_mqtt.on_connect = self.my_on_connect  # Association

    def start(self):
        self._paho_mqtt.connect(self.messageBroker, 1883)
        self._paho_mqtt.loop_start()

    def stop(self):
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def my_publish(self, topic, message):
        self._paho_mqtt.publish(topic, message, 2)

    def my_on_connect(self, client, userdata, flags, rc):
        global loop_flag
        print ("Connected to %s - Result code: %d" % (self.messageBroker, rc))
        loop_flag = 0


if __name__ == "__main__":
    pub = MyPublisher("Pub1", BROKER_IP)
    loop_flag = 1
    flag = 1
    pub.start()

    while loop_flag:
        print("Waiting for connection...")
        time.sleep(.01)

    while True:
        timestamp = str(time.time())
        jtime = {"timestamp": timestamp}
        print("Publishing on topic '/timestamp: %s" % (jtime))
        pub.my_publish('/timestamp', json.dumps(jtime))

        if flag == 1:
            datemessage = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            jdate = {"datetime": datemessage}
            print("Publishing on topic '/datetime: %s" % (jdate))
            pub.my_publish('/datetime', json.dumps(jdate))
            flag = 0

        elif flag == 0:
            flag = 1

        time.sleep(30)

    pub.stop()
