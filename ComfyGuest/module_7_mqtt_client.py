#!/usr/bin/env python3
# module_7_mqtt_client.py

import json
import ssl
import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(self):

        #####################################################
        # HiveMQ Cloud Configuration
        #####################################################

        self.BROKER = "0feb8d03cd1341e49aab46dffa68e565.s1.eu.hivemq.cloud"
        self.PORT = 8883

        self.USERNAME = "IOT"
        self.PASSWORD = "Hoteliot"

        self.SENSOR_TOPIC = "hotel/room101/sensors"
        self.ACTUATOR_TOPIC = "hotel/room101/actuators"
        self.MANUAL_TOPIC = "hotel/room101/manual"
        self.ACTUATOR_STATUS_TOPIC = "hotel/room101/actuator_status"

        #####################################################

        self.latest_action = None
        self.latest_manual_command = None

        self.client = mqtt.Client(client_id="raspberry_pi")

        self.client.username_pw_set(
            self.USERNAME,
            self.PASSWORD
        )

        self.client.tls_set(
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS_CLIENT
        )

        self.client.tls_insecure_set(False)

        #####################################################
        # MQTT Callbacks
        #####################################################

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    #########################################################

    def connect(self):

        print("Connecting to HiveMQ Cloud...")

        self.client.connect(
            self.BROKER,
            self.PORT,
            keepalive=60
        )

        self.client.loop_start()

    #########################################################

    def disconnect(self):

        self.client.loop_stop()
        self.client.disconnect()

    #########################################################

    def publish(self, sensor_data):

        try:

            payload = json.dumps(sensor_data)

            result = self.client.publish(
                self.SENSOR_TOPIC,
                payload,
                qos=1
            )

            if result.rc == mqtt.MQTT_ERR_SUCCESS:

                print("Published Sensor Data")

            else:

                print("Publish Failed")

        except Exception as e:

            print("Publish Error :", e)

    #########################################################

    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:

            print("===================================")
            print("Connected to HiveMQ Cloud")
            print("===================================")

            client.subscribe(
                self.ACTUATOR_TOPIC,
                qos=1
            )

            print("Subscribed to:", self.ACTUATOR_TOPIC)

            client.subscribe(
                self.MANUAL_TOPIC,
                qos=1
            )

            print("Subscribed to:", self.MANUAL_TOPIC)

        else:

            print("Connection Failed :", rc)

    #########################################################

    def on_disconnect(self, client, userdata, rc):

        print("Disconnected from HiveMQ")

    #########################################################

    def on_message(self, client, userdata, msg):

        payload = msg.payload.decode()

        print("\n===================================")
        print("Message Received")
        print("Topic :", msg.topic)
        print("Payload :", payload)
        print("===================================")

        try:

            data = json.loads(payload)

        except json.JSONDecodeError:

            print("Invalid JSON received.")
            return

        if msg.topic == self.MANUAL_TOPIC:

            self.latest_manual_command = data

        elif msg.topic == self.ACTUATOR_TOPIC:

            self.latest_action = data

    #########################################################

    def get_latest_action(self):

        return self.latest_action

    #########################################################

    def clear_latest_action(self):

        self.latest_action = None

    #########################################################

    def get_latest_manual_command(self):

        return self.latest_manual_command

    #########################################################

    def clear_latest_manual_command(self):

        self.latest_manual_command = None

    #########################################################

    def is_connected(self):

        return self.client.is_connected()

    #########################################################

    def reconnect(self):

        try:

            if not self.client.is_connected():

                print("Reconnecting...")

                self.client.reconnect()

        except Exception as e:

            print("Reconnect Failed :", e)