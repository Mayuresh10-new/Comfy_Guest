#!/usr/bin/env python3
# main.py

import sys

sys.path.insert(0, "/home/pi/Dexter/GrovePi/Software/Python")
sys.path.insert(0, "/home/pi/Dexter/GrovePi/Software/Python/grovepi")


import time

from module_1_dht11 import DHT11Sensor
from module_2_pir_sensor import PIRSensor
from module_3_ultrasonic import UltrasonicSensor
from module_4_light_sensor import LightSensor
from module_5_output_controller import OutputController
from module_6_switch_controller import SwitchController
from module_7_mqtt_client import MQTTClient
from module_8_weather import WeatherSensor
from module_9_plugwise import PlugwiseController


############################################################
# INITIALIZE SENSORS
############################################################

# Indoor DHT11
dht = DHT11Sensor(
    port=2
)

# PIR Motion Sensor
pir = PIRSensor(
    port=8,
    timeout=15
)

# Ultrasonic Sensor
# ultrasonic = UltrasonicSensor(
# port=4,
# threshold=50
# )

# Light Sensor
light = LightSensor(
    port=0,
    threshold=400
)

# Manual Switch
switch = SwitchController(
    port=3
)

############################################################
# WEATHER MODULE
############################################################

weather = WeatherSensor(

    api_key="458d5eaa4b0c933c08360cfe5c243d48",

    latitude=19.0760,

    longitude=72.8777,

    update_interval=300

)

############################################################
# OUTPUT CONTROLLER
############################################################

outputs = OutputController(

    relay_port=5,

    room_led_port=6,

    status_led_port=7,

    new_led_port = 4

)


############################################################
# PLUGWISE CONTROLLER
############################################################

plugwise = PlugwiseController(

    usb="/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A6010MU7-if00-port0",

    circle_plus_mac="000D6F0005692784",

    circle_mac="000D6F000416E6F4"

)

############################################################
# MQTT CLIENT
############################################################

mqtt = MQTTClient()

mqtt.connect()

############################################################

print("========================================")
print(" HOTEL AUTOMATION SYSTEM")
print("========================================")
print("Indoor Sensors : READY")
print("Weather Module : READY")
print("MQTT Client    : CONNECTED")
print("Waiting for AI Planner...")
print("========================================")

############################################################

try:

    while True:

        ####################################################
        # READ INDOOR SENSORS
        ####################################################

        temperature, humidity = dht.read()

        motion = pir.read()

        occupied = pir.occupied()

        # distance = ultrasonic.read()

        # guest_near = ultrasonic.guest_detected()

        light_value = light.read()

        dark = light.is_dark()

        switch.update()

        ####################################################
        # READ WEATHER
        ####################################################

        weather_data = weather.read()
        ####################################################
        # Create Sensor Payload
        ####################################################

        sensor_data = {

            ################################################
            # Indoor Environment
            ################################################

            "inside_temperature": temperature,

            "inside_humidity": humidity,

            ################################################
            # Occupancy
            ################################################

            "motion": motion,

            "occupied": occupied,

            ################################################
            # Ultrasonic
            ################################################

            # "distance": distance,

            # "guest_near": guest_near,

            ################################################
            # Light
            ################################################

            "light_value": light_value,

            "dark": dark,

            ################################################
            # Manual Override
            ################################################

            "manual_mode": switch.manual_mode,

            "manual_relay": switch.manual_relay

        }

        ####################################################
        # Add Weather Data
        ####################################################

        if weather_data:

            sensor_data.update(weather_data)

        ####################################################
        # Publish Sensor Data
        ####################################################

        mqtt.publish(sensor_data)

        ####################################################
        # Display Sensor Data
        ####################################################

        print("\n================ SENSOR DATA ================")

        for key, value in sensor_data.items():

            print(f"{key:25}: {value}")

        print("=============================================")

        ####################################################
        # Check for AI Planner Commands
        ####################################################

        action = mqtt.get_latest_action()

        if action is not None:

            print("\n============= AI COMMAND =============")

            print(action)

            print("======================================")

            ################################################
            # Execute AI Planner Commands
            ################################################

            # Parse payload into desired states
            cooling = heating = blinds = lights = ventilation = airpurifier = None

            for room, commands in action.items():

                print(f"Room : {room}")

                for raw_command in commands:

                    print(f"Received : {raw_command}")

                    try:
                        device, value = raw_command.lower().split(":", 1)
                        device = device.strip()
                        value = bool(int(value.strip()))
                    except Exception as e:
                        print(f"Invalid command : {raw_command} ({e})")
                        continue

                    print(f"Parsed -> Device={device}, Value={value}")

                    if device == "cooling":
                        cooling = value
                    elif device == "heating":
                        heating = value
                    elif device == "blinds":
                        blinds = value
                    elif device == "airpurifier":
                        airpurifier = value
                    elif device == "lights":
                        lights = value
                    elif device == "ventilation":
                        ventilation = value
                    else:
                        print(f"Unknown device : {device}")

            ################################################
            # Execute GrovePi outputs (I2C)
            ################################################

            grove_queue = []

            if cooling is not None:
                grove_queue.append(outputs.room_light_on if cooling else outputs.room_light_off)

            if heating is not None:
                grove_queue.append(outputs.new_led_on if heating else outputs.new_led_off)

            if blinds is not None:
                grove_queue.append(outputs.status_led_on if blinds else outputs.status_led_off)

            if airpurifier is not None:
                grove_queue.append(outputs.relay_on if airpurifier else outputs.relay_off)

            # Give GrovePi a moment before the first write
            time.sleep(0.10)

            for i, operation in enumerate(grove_queue):
                if i == 0:
                    operation()
                    time.sleep(0.05)
                    operation()
                else:
                    operation()
                time.sleep(0.20)

            ################################################
            # Execute Plugwise outputs (USB)
            ################################################

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

            ################################################
            # Display Output Status
            ################################################

            outputs.print_status()
            plugwise.print_status()

            ################################################
            # Clear Latest Command
            ################################################

            mqtt.clear_latest_action()

        ####################################################
        # Manual Mode Override
        ####################################################

        if switch.manual_mode:

            if switch.manual_relay:

                outputs.relay_on()

            else:

                outputs.relay_off()

        ####################################################
        # Optional Safety Logic
        ####################################################

        # Turn OFF relay if DHT11 reading is unavailable
        if temperature is None:

            outputs.relay_off()

        ####################################################
        # Print Current Output States
        ####################################################

        relay_state, room_led_state, status_led_state, new_led_state = outputs.get_states().values()

        circle_state, circle_plus_state = plugwise.get_states().values()

        print("\n--------------- OUTPUTS ----------------")

        print(f"Relay      : {'ON' if relay_state else 'OFF'}")

        print(f"Room LED   : {'ON' if room_led_state else 'OFF'}")

        print(f"Status LED : {'ON' if status_led_state else 'OFF'}")

        print(f"New LED : {'ON' if new_led_state else 'OFF'}")

        print(f"Circle      : {'ON' if circle_state else 'OFF'}")

        print(f"Circle+     : {'ON' if circle_plus_state else 'OFF'}")

        print("----------------------------------------")

        ####################################################
        # Loop Delay
        ####################################################

        time.sleep(0.1)
    ############################################################

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

    ########################################################
    # Turn OFF all outputs
    ########################################################

    try:

        outputs.cleanup()

    except Exception as e:

        print("Output Cleanup Error:", e)
    
    try:

        plugwise.cleanup()
    
    except Exception as e:
    
        print("Plugwise Cleanup Error:", e)

    ########################################################
    # Disconnect MQTT
    ########################################################

    try:

        mqtt.disconnect()

    except Exception as e:

        print("MQTT Disconnect Error:", e)

    ########################################################

    print("\n========================================")
    print("Hotel Automation System Stopped")
    print("========================================")