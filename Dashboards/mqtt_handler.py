import json
import ssl
import threading

import paho.mqtt.client as mqtt
import config

# Latest MQTT data
latest_data = {}

# Latest actuator status (relay, room_led, status_led, new_led, circle, circle_plus)
latest_actuator_status = {}

# Connection status
connected = False

# Prevent multiple MQTT threads
started = False


def on_connect(client, userdata, flags, rc):
    global connected

    if rc == 0:
        connected = True
        print("✅ Connected to HiveMQ")

        client.subscribe(
            config.TOPIC,
            qos=1
        )

        print(f"Subscribed to {config.TOPIC}")

        client.subscribe(
            config.ACTUATOR_STATUS_TOPIC,
            qos=1
        )

        print(f"Subscribed to {config.ACTUATOR_STATUS_TOPIC}")

    else:
        print("Connection Failed:", rc)


def on_disconnect(client, userdata, rc):
    global connected

    connected = False

    print("Disconnected from HiveMQ")


def on_message(client, userdata, msg):
    global latest_data, latest_actuator_status

    try:
        payload = json.loads(msg.payload.decode())

    except Exception as e:
        print("JSON Error:", e)
        return

    if msg.topic == config.ACTUATOR_STATUS_TOPIC:
        latest_actuator_status = payload

    elif msg.topic == config.TOPIC:
        latest_data = payload


client = mqtt.Client(client_id="dashboard")

client.username_pw_set(
    config.USERNAME,
    config.PASSWORD
)

client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.tls_insecure_set(False)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message


def start():
    global started

    if started:
        return

    started = True

    client.connect(
        config.BROKER,
        config.PORT,
        keepalive=60
    )

    threading.Thread(
        target=client.loop_forever,
        daemon=True
    ).start()


def publish_manual_override(manual_mode: bool, actuator_states: dict):
    """
    Publishes a manual override command to the Pi.

    manual_mode      -> True to enter manual mode, False to return to AUTO
    actuator_states  -> dict with any of:
                         relay, room_led, status_led, new_led, circle, circle_plus
    """

    payload = json.dumps(
        {
            "manual_mode": manual_mode,
            **actuator_states,
        }
    )

    result = client.publish(
        config.MANUAL_TOPIC,
        payload,
        qos=1
    )

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Published Manual Override")
    else:
        print("Manual Override Publish Failed")