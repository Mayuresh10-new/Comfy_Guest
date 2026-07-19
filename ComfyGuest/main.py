import sys
import time
import json

sys.path.insert(0, "/home/pi/Dexter/GrovePi/Software/Python")
sys.path.insert(0, "/home/pi/Dexter/GrovePi/Software/Python/grovepi")

from module_1_dht11 import DHT11Sensor
from module_2_pir_sensor import PIRSensor
from module_3_ultrasonic import UltrasonicSensor
from module_4_light_sensor import LightSensor
from module_5_output_controller import OutputController
from module_6_switch_controller import SwitchController
from module_7_mqtt_client import MQTTClient
from module_8_weather import WeatherSensor
from module_9_plugwise import PlugwiseController

dht = DHT11Sensor(port=2)

pir = PIRSensor(
    port=8,
    timeout=15
)

light = LightSensor(
    port=0,
    threshold=400
)

switch = SwitchController(port=3)

weather = WeatherSensor(
    api_key="458d5eaa4b0c933c08360cfe5c243d48",
    latitude=19.0760,
    longitude=72.8777,
    update_interval=300
)

outputs = OutputController(
    relay_port=5,
    room_led_port=6,
    status_led_port=7,
    new_led_port=4
)

plugwise = PlugwiseController(
    usb="/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A6010MU7-if00-port0",
    circle_plus_mac="000D6F0005692784",
    circle_mac="000D6F000416E6F4"
)

mqtt = MQTTClient()
mqtt.connect()

last_sensor_publish = 0
last_output_publish = 0
last_status_print = 0

SENSOR_PUBLISH_INTERVAL = 2.0
OUTPUT_PUBLISH_INTERVAL = 2.0
STATUS_PRINT_INTERVAL = 2.0

print("========================================")
print(" HOTEL AUTOMATION SYSTEM")
print("========================================")
print("Indoor Sensors : READY")
print("Weather Module : READY")
print("MQTT Client    : CONNECTED")
print("Waiting for AI Planner...")
print("========================================")

try:
    while True:
        now = time.time()
        mqtt.reconnect()
        plugwise.reconnect()
        manual_command = mqtt.get_latest_manual_command()

        if manual_command is not None:
            print("\n========= MANUAL OVERRIDE =========")
            print(manual_command)
            print("===================================")

            try:
                switch.apply_manual_command(
                    manual_command
                )
            except Exception as e:
                print(f"Invalid manual override : {e}")

            mqtt.clear_latest_manual_command()

        switch.update()
        dht.update()
        pir.update()
        light.update()
        weather.update()

        if switch.manual_mode:
            manual = switch.manual_states
            changed = False

            if manual["relay"] != outputs.relay_target:
                outputs.relay_on() if manual["relay"] else outputs.relay_off()
                changed = True

            if manual["room_led"] != outputs.room_light_target:
                outputs.room_light_on() if manual["room_led"] else outputs.room_light_off()
                changed = True

            if manual["status_led"] != outputs.status_target:
                outputs.status_led_on() if manual["status_led"] else outputs.status_led_off()
                changed = True

            if manual["new_led"] != outputs.new_target:
                outputs.new_led_on() if manual["new_led"] else outputs.new_led_off()
                changed = True

            if changed:
                outputs.update()

            if manual["circle"] != plugwise.circle_target:
                plugwise.circle_on() if manual["circle"] else plugwise.circle_off()

            if manual["circle_plus"] != plugwise.circle_plus_target:
                plugwise.circle_plus_on() if manual["circle_plus"] else plugwise.circle_plus_off()

            plugwise.update()
            
        sensor_data = {
            # Indoor Environment
            "inside_temperature": dht.temperature,
            "inside_humidity": dht.humidity,

            # Occupancy
            "motion": pir.motion,
            "occupied": pir.occupied,

            # Light
            "light_value": light.value,
            "dark": light.dark,

            # Manual Override
            "manual_mode": switch.manual_mode,
            "manual_relay": switch.manual_relay
        }

        if weather.weather_data:
            sensor_data.update(
                weather.weather_data
            )

        if now - last_sensor_publish >= SENSOR_PUBLISH_INTERVAL:
            mqtt.publish(sensor_data)
            last_sensor_publish = now

        if now - last_status_print >= STATUS_PRINT_INTERVAL:
            print("\n================ SENSOR DATA ================")
            for key, value in sensor_data.items():
                print(f"{key:25}: {value}")
            print("=============================================")
            last_status_print = now

        action = mqtt.get_latest_action()

        if action is not None:
            if switch.manual_mode:
                print(
                    "\n[AI Planner command ignored - "
                    "Manual Mode Active]"
                )
                mqtt.clear_latest_action()
            else:
                print("\n============= AI COMMAND =============")
                print(action)
                print("======================================")

                cooling = None
                heating = None
                blinds = None
                lights = None
                ventilation = None
                airpurifier = None

                for room, commands in action.items():
                    print(f"\nRoom : {room}")
                    for raw_command in commands:
                        print(f"Received : {raw_command}")
                        try:
                            device, value = raw_command.lower().split(":", 1)
                            device = device.strip()
                            value = bool(
                                int(value.strip())
                            )
                        except Exception as e:
                            print(
                                f"Invalid command: "
                                f"{raw_command} ({e})"
                            )
                            continue
                        print(
                            f"Parsed -> "
                            f"{device} = {value}"
                        )
                        if device == "cooling":
                            cooling = value

                        elif device == "heating":
                            heating = value

                        elif device == "blinds":
                            blinds = value

                        elif device == "lights":
                            lights = value

                        elif device == "ventilation":
                            ventilation = value

                        elif device == "airpurifier":
                            airpurifier = value

                        else:
                            print(
                                f"Unknown device: {device}"
                            )
                
                # Execute GrovePi Outputs
                if cooling is not None:
                    if cooling:
                        outputs.room_light_on()
                    else:
                        outputs.room_light_off()

                if heating is not None:
                    if heating:
                        outputs.new_led_on()
                    else:
                        outputs.new_led_off()

                if blinds is not None:
                    if blinds:
                        outputs.status_led_on()
                    else:
                        outputs.status_led_off()

                if airpurifier is not None:
                    if airpurifier:
                        outputs.relay_on()
                    else:
                        outputs.relay_off()

                if lights is not None:
                    if lights:
                        plugwise.circle_on()
                    else:
                        plugwise.circle_off()

                if ventilation is not None:
                    if ventilation:
                        plugwise.circle_plus_on()
                    else:
                        plugwise.circle_plus_off()

                outputs.update()
                plugwise.update()
                outputs.print_status()
                plugwise.print_status()
                mqtt.clear_latest_action()

        if dht.temperature is None:
            outputs.relay_off()
            outputs.update()

        if now - last_output_publish >= OUTPUT_PUBLISH_INTERVAL:
            output_states = outputs.get_states()
            plugwise_states = plugwise.get_states()

            actuator_status = {
                "relay": output_states["relay"],
                "room_led": output_states["room_led"],
                "status_led": output_states["status_led"],
                "new_led": output_states["new_led"],
                "circle": plugwise_states["circle"],
                "circle_plus": plugwise_states["circle_plus"]
            }

            mqtt.client.publish(
                mqtt.ACTUATOR_STATUS_TOPIC,
                json.dumps(actuator_status),
                qos=1
            )
            last_output_publish = now

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n")
    print("========================================")
    print("Stopping Hotel Automation System...")
    print("========================================")
except Exception as e:
    print("\n")
    print("========================================")
    print("Unexpected Error")
    print("========================================")
    print(e)
finally:
    try:
        outputs.cleanup()
    except Exception as e:
        print("Output Cleanup Error:", e)
    try:
        plugwise.cleanup()
    except Exception as e:
        print("Plugwise Cleanup Error:", e)
    try:
        mqtt.disconnect()
    except Exception as e:
        print("MQTT Disconnect Error:", e)
    print("\n========================================")
    print("Hotel Automation System Stopped")
    print("========================================")