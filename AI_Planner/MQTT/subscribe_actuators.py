import ssl
import time

import certifi
import paho.mqtt.client as mqtt

from backend.models import DeviceState
import json

from backend.stateParser import update_device_data

TOPIC_SENSORS = "hotel/room101/sensors"
TOPIC_ACTUATORS = "hotel/room101/actuator_status"


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="actuators_subscriber"
)

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(
    ca_certs=certifi.where(),
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.tls_insecure_set(False)

def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:

        print("\n===================================")
        print(" Connected to HiveMQ Cloud")
        print("===================================")

        client.subscribe(TOPIC_ACTUATORS, qos=1)

        print(f"Subscribed to: {TOPIC_ACTUATORS}")

    else:

        print(f"Connection Failed. Reason Code: {reason_code}")


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode("utf-8"))

    room_number = int(msg.topic.split("/")[1][4:])
    device = DeviceState()
    device.number = room_number
    device.lights = int(data["circle"])
    device.blinds = int(data["status_led"])
    device.ac = int(data["room_led"])
    device.heater = int(data["new_led"])
    device.ventilator = int(data["circle_plus"])
    device.air_purifier = int(data["relay"])
    device.windows = 0
    update_device_data(device)
    print("Actuator Data Updated: ", vars(device))
    time.sleep(1)


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):

    print("\nDisconnected from HiveMQ")


client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("Connecting to HiveMQ Cloud...")

try:

    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever()

except KeyboardInterrupt:

    print("\nStopping Subscriber...")

    client.disconnect()

except Exception as e:

    print("\nError:", e)
