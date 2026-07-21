import json
import ssl
import time

import certifi
import paho.mqtt.client as mqtt

from planParser import PlannerRunner, PlanParser

ACTION_TO_COMMAND = {
    "turn-on-lights in room101": "lights:1",
    "turn-off-lights in room101": "lights:0",

    "open-blinds in room101": "blinds:1",
    "close-blinds in room101": "blinds:0",

    "open-windows in room101": "windows:1",
    "close-windows in room101": "windows:0",

    "turn-on-cooling in room101": "cooling:1",
    "continue-cooling in room101": "cooling:1",
    "turn-off-cooling in room101": "cooling:0",

    "turn-on-heating in room101": "heating:1",
    "continue-heating in room101": "heating:1",
    "turn-off-heating in room101": "heating:0",

    "turn-on-ventilation in room101": "ventilation:1",
    "turn-off-ventilation in room101": "ventilation:0",

    "turn-on-airpurifier in room101": "airpurifier:1",
    "turn-off-airpurifier in room101": "airpurifier:0",
}

IDLE_COMMANDS = [
    "lights:0",
    "blinds:0",
    "windows:0",
    "cooling:0",
    "heating:0",
    "ventilation:0",
    "airpurifier:0",
]


TOPIC = "hotel/room101/actuators"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="planner_publisher"
)

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(
    ca_certs=certifi.where(),
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.tls_insecure_set(False)

print("Connecting to HiveMQ...")

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

planner = PlannerRunner()
parser = PlanParser()

try:

    while True:

        planner_output = planner.run()

        plan = parser.parse(planner_output)
        actions = parser.extract_actions(plan)

        print("\nPlanner Actions:")
        print(actions)

        mqtt_commands = []

        if "toidlemode in room101" in actions:

            mqtt_commands = IDLE_COMMANDS.copy()

        else:

            for action in actions:

                command = ACTION_TO_COMMAND.get(action)

                if command is not None:
                    mqtt_commands.append(command)
                  
        mqtt_commands = list(dict.fromkeys(mqtt_commands))

        if mqtt_commands:

            payload = json.dumps({
                "room101": mqtt_commands
            })

            print("\nPublishing:")
            print(payload)

            result = client.publish(
                TOPIC,
                payload,
                qos=1
            )

            result.wait_for_publish()

            print("Published successfully.")

        else:

            print("\nNo actuator commands generated.")

        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping publisher...")

finally:

    client.loop_stop()
    client.disconnect()
