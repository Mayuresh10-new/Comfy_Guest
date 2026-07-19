# ComfyGuest – AI Smart Hotel Room Automation

ComfyGuest is an AI-powered Smart Hotel Room Automation System developed on a Raspberry Pi using GrovePi sensors, Plugwise smart plugs, MQTT communication, and an AI Planner. The system continuously monitors the room environment and occupancy, allowing both autonomous AI control and manual user control through a Streamlit dashboard.

---

# Features

- Real-time environmental monitoring
- AI-based room automation
- Manual dashboard override
- MQTT communication using HiveMQ Cloud
- Plugwise smart plug integration
- GrovePi sensor and actuator support
- Weather API integration
- Live Streamlit dashboard

---

# System Architecture

```
                    +----------------------+
                    | Streamlit Dashboard  |
                    +----------+-----------+
                               |
                               | MQTT
                               |
                    +----------v-----------+
                    |    HiveMQ Cloud      |
                    +----------+-----------+
                               |
               +---------------+----------------+
               |                                |
               |                                |
       Sensor Publishing                 AI Planner
               |                                |
               |                                |
        +------v------+                 +-------v------+
        | Raspberry Pi|                 | AI Planning  |
        |   Main.py   |                 |   Service    |
        +------+------+
               |
    +----------+-----------+
    |                      |
GrovePi Sensors      Plugwise Devices
    |                      |
Relay / LEDs         Circle / Circle+
```

---

# Hardware

## Controller

- Raspberry Pi 3B+

## GrovePi Sensors

- DHT11 Temperature & Humidity Sensor
- PIR Motion Sensor
- Grove Light Sensor

## GrovePi Outputs

- Relay Module
- Room LED
- Status LED
- New LED

## Plugwise Devices

- Plugwise Circle
- Plugwise Circle+

---

# Software Stack

- Python 3
- GrovePi Library
- Plugwise Library
- Paho MQTT
- HiveMQ Cloud
- Streamlit
- OpenWeatherMap API

---

# Folder Structure

```
ComfyGuest/
│
├── main.py
│
├── module_1_dht11.py
├── module_2_pir_sensor.py
├── module_3_ultrasonic.py
├── module_4_light_sensor.py
├── module_5_output_controller.py
├── module_6_switch_controller.py
├── module_7_mqtt_client.py
├── module_8_weather.py
├── module_9_plugwise.py
│
├── Dashboards/
│   ├── dashboard.py
│   ├── mqtt_handler.py
│   ├── config.py
│   └── requirements.txt
│
└── README.md
```

---

# GrovePi Connections

| Device | Port |
|---------|------|
| DHT11 | D2 |
| Push Button | D3 |
| New LED | D4 |
| Relay | D5 |
| Room LED | D6 |
| Status LED | D7 |
| PIR Sensor | D8 |
| Light Sensor | A0 |

---

# Plugwise Devices

| Device | Purpose |
|---------|----------|
| Circle | Lights |
| Circle+ | Ventilation |

---

# MQTT Topics

## Sensors

```
hotel/room101/sensors
```

Publishes:

- Temperature
- Humidity
- Motion
- Occupancy
- Light Level
- Weather
- Manual Mode

---

## AI Commands

```
hotel/room101/actuators
```

Receives AI Planner commands.

Example

```json
{
    "room101":[
        "cooling:1",
        "lights:0",
        "airpurifier:1"
    ]
}
```

---

## Manual Override

```
hotel/room101/manual
```

Receives manual dashboard commands.

---

## Actuator Status

Publishes

```json
{
    "relay":true,
    "room_led":false,
    "status_led":true,
    "new_led":false,
    "circle":true,
    "circle_plus":false
}
```

---

# Operating Modes

## Automatic Mode

The AI Planner controls all devices based on sensor data.

Examples

- Cooling
- Heating
- Lighting
- Blinds
- Ventilation
- Air Purifier

---

## Manual Mode

Manual Mode overrides AI completely.

Dashboard controls

- Relay
- Room LED
- Status LED
- New LED
- Plugwise Circle
- Plugwise Circle+

When Manual Mode is enabled, AI commands are ignored until Manual Mode is disabled.

---

# Sensor Update Flow

```
Read Sensors

↓

Build Sensor Payload

↓

Publish MQTT

↓

AI Planner

↓

Receive Actions

↓

Update Outputs

↓

Publish Actuator Status
```

---

# Modules

## module_1_dht11.py

Reads

- Temperature
- Humidity

---

## module_2_pir_sensor.py

Detects

- Motion
- Room Occupancy

---

## module_3_ultrasonic.py

Ultrasonic distance sensor.

(Currently optional.)

---

## module_4_light_sensor.py

Reads

- Ambient Light
- Dark / Bright status

---

## module_5_output_controller.py

Controls GrovePi outputs

- Relay
- Room LED
- Status LED
- New LED

Features

- Target state management
- Immediate hardware updates
- Configurable write delay

---

## module_6_switch_controller.py

Controls

- Manual Mode
- Local push-button
- Dashboard manual commands

---

## module_7_mqtt_client.py

Handles

- MQTT connection
- Publishing sensor data
- Receiving AI commands
- Receiving manual commands

---

## module_8_weather.py

Downloads

- Outdoor Temperature
- Humidity
- Weather Conditions

using OpenWeatherMap.

---

## module_9_plugwise.py

Controls

- Plugwise Circle
- Plugwise Circle+

Includes

- Automatic reconnect
- State synchronization

---

# Dashboard

Built using Streamlit.

Displays

- Live sensor values
- Weather
- Occupancy
- Actuator status
- Manual controls
- AI status

---

# Current Development Status

Completed

- GrovePi sensor integration
- Plugwise integration
- MQTT communication
- HiveMQ Cloud
- Streamlit dashboard
- Manual override
- AI command execution
- Weather API integration
- Automatic reconnection
- Status publishing

Currently Improving

- GrovePi actuator responsiveness
- Digital output timing
- I²C communication stability

---

# Installation

Clone the repository

```bash
git clone https://github.com/Mayuresh10-new/Comfy_Guest.git
```

Create a virtual environment

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

Dashboard

```bash
streamlit run Dashboards/dashboard.py
```

---

# Future Improvements

- AI scheduling
- Energy consumption optimization
- Multiple hotel rooms
- Occupancy prediction
- Database logging
- Historical analytics
- OTA updates
- Mobile application
- Voice assistant integration
- Predictive maintenance

---

# Authors

Mayuresh Shendkar.
Anish Tangadpalliwar.
Yusuf Sayeed.

University of Stuttgart

---

# License

This project is intended for academic research and educational purposes.