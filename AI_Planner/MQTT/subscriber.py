import ssl
import time

import certifi
import paho.mqtt.client as mqtt

from backend.stateParser import parse_env_data
from stateParser import parse_sensor_data, parse_device_data
from problemGenerator import generate_problem
import json


TOPIC_SENSORS = "hotel/room101/sensors"
TOPIC_ACTUATORS = "hotel/room101/actuator_status"


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="sensor_subscriber"
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

        client.subscribe(TOPIC_SENSORS, qos=1)

        print(f"Subscribed to: {TOPIC_SENSORS}")

    else:

        print(f"Connection Failed. Reason Code: {reason_code}")


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode("utf-8"))
    room_number = int(msg.topic.split("/")[1][4:])
    print(data)
    room = parse_sensor_data(data, room_number)
    env = parse_env_data(data)
    device = parse_device_data(room_number)
    generate_problem(room, device, env)
    time.sleep(0.5)



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
