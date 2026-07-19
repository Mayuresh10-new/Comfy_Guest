#!/usr/bin/env python3
# module_7_mqtt_client.py

import json
import ssl
import time
import paho.mqtt.client as mqtt


class MQTTClient:
    # Constructor
    def __init__(self):
        # HiveMQ Cloud Configuration
        self.BROKER = "0feb8d03cd1341e49aab46dffa68e565.s1.eu.hivemq.cloud"
        self.PORT = 8883
        self.USERNAME = "IOT"
        self.PASSWORD = "Hoteliot"
        self.SENSOR_TOPIC = "hotel/room101/sensors"
        self.ACTUATOR_TOPIC = "hotel/room101/actuators"
        self.MANUAL_TOPIC = "hotel/room101/manual"
        self.ACTUATOR_STATUS_TOPIC = "hotel/room101/actuator_status"

        # Runtime Variables
        self.latest_action = None
        self.latest_manual_command = None
        self.connected = False
        self.last_reconnect_attempt = 0
        self.reconnect_interval = 5
        self.DEBUG = False

        # MQTT Client
        self.client = mqtt.Client(
            client_id="raspberry_pi"
        )
        self.client.username_pw_set(
            self.USERNAME,
            self.PASSWORD
        )
        self.client.tls_set(
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS_CLIENT
        )
        self.client.tls_insecure_set(False)
        # Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    # Connect
    def connect(self):
        print("\nConnecting to HiveMQ Cloud...")

        try:
            self.client.connect(
                self.BROKER,
                self.PORT,
                keepalive=60
            )
            self.client.loop_start()
        except Exception as e:
            print("Connection Error:", e)

    # Disconnect
    def disconnect(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()

        except Exception as e:
            print("Disconnect Error:", e)

    # Publish Sensor Data
    def publish(self, sensor_data):
        if not self.connected:
            return
        try:
            payload = json.dumps(sensor_data)
            result = self.client.publish(
                self.SENSOR_TOPIC,
                payload,
                qos=1
            )

            if self.DEBUG:
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print("Sensor data published.")
                else:
                    print("Publish failed.")
        except Exception as e:
            print("Publish Error:", e)

    # MQTT Connected
    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            self.connected = True
            print("\n===================================")
            print("Connected to HiveMQ Cloud")
            print("===================================")
            client.subscribe(
                self.ACTUATOR_TOPIC,
                qos=1
            )
            client.subscribe(
                self.MANUAL_TOPIC,
                qos=1
            )
            print("Subscribed to:")
            print(" -", self.ACTUATOR_TOPIC)
            print(" -", self.MANUAL_TOPIC)

        else:
            self.connected = False
            print("Connection Failed:", reason_code)

    # MQTT Disconnected
    def on_disconnect(self, client, userdata, flags, reason_code, properties=None):
        self.connected = False
        print("Disconnected from HiveMQ")

    # Incoming Messages
    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            if self.DEBUG:
                print("\n===================================")
                print("MQTT Message")
                print("Topic :", msg.topic)
                print("Payload :", payload)
                print("===================================")

            data = json.loads(payload)

        except json.JSONDecodeError:
            print("Invalid JSON received.")
            return

        except Exception as e:
            print("MQTT Parse Error:", e)
            return

        if msg.topic == self.ACTUATOR_TOPIC:
            self.latest_action = data

        elif msg.topic == self.MANUAL_TOPIC:
            self.latest_manual_command = data

    # Latest AI Action
    def get_latest_action(self):
        return self.latest_action

    def clear_latest_action(self):
        self.latest_action = None
    # Latest Manual Command
    def get_latest_manual_command(self):
        return self.latest_manual_command

    def clear_latest_manual_command(self):
        self.latest_manual_command = None

    # Connection Status
    def is_connected(self):
        return self.connected

    # Automatic Reconnect
    def reconnect(self):
        now = time.time()
        if self.connected:
            return
        if now - self.last_reconnect_attempt < self.reconnect_interval:
            return
        self.last_reconnect_attempt = now
        print("Attempting MQTT reconnect...")
        try:
            self.client.reconnect()
        except Exception as e:
            print("Reconnect Failed:", e)

    # Debug
    def print_status(self):
        print("\n========== MQTT ==========")
        print(f"Connected : {self.connected}")
        print(f"Broker    : {self.BROKER}")
        print("==========================")