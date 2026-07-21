from models import RoomState, DeviceState, envState
from CurrentStateDB import get_cursor, print_db
from datetime import datetime


def set_temperature(temp):
    if temp >= 25:
        temp = "high"
    elif temp in range(18, 25):
        temp = 'comfy'
    else:
        temp = "high"
    return temp


def set_lux(lux):
    if lux >= 700:
        lux = 'high'
    elif lux in range(400, 700):
        lux = 'comfy'
    else:
        lux = 'low'
    return lux

def set_daytime():
    hour = datetime.now().hour
    return 1 if 6 <= hour < 18 else 0


def parse_sensor_data(room_data, room_number):

    room = RoomState()
    cursor, db = get_cursor()
    data = cursor.execute('SELECT * FROM room_data WHERE room_id = ?', (room_number,))
    data = data.fetchone()
    room.number = room_number
    room.temperature = set_temperature(room_data['inside_temperature'])
    room.lux = set_lux(room_data['light_value'])

    room.daytime = data[4]
    # room.air_quality = "good" if room_data['aqi_level'] == 'Good' else "poor"
    room.air_quality = "poor"
    room.humidity = 'low' if room_data['inside_humidity'] <= 55.0 else 'high'
    room.motion = room_data['motion']
    room.occupied = 1 if room_data['occupied'] else 0
    room.manual_mode = data[15]
    room.checked_in = data[16]

    return room

# def rectify_illegal_states(data, cursor, db):
#
#     if data[5] == 'good':
#         cursor.execute("UPDATE room_data SET purifier_on = ? WHERE room_id = ?", (1, 101))
#     else:
#         cursor.execute("UPDATE room_data SET purifier_on = ? WHERE room_id = ?", (0, 101))
#
#     if data[2] == 'high':
#         cursor.execute("UPDATE room_data SET ventilation_on = ? WHERE room_id = ?", (1, 101))
#     else:
#         cursor.execute("UPDATE room_data SET ventilation_on = ? WHERE room_id = ?", (0, 101))
#
#     if data[4] == 0:
#         cursor.execute("UPDATE room_data SET lux = ? WHERE room_id = ?", ('comfy', 101))
#
#     if data[11] == 1 or data[12] == 1:
#         cursor.execute("UPDATE room_data SET windows_open = ? WHERE room_id = ?", (0, 101))
#         cursor.execute("UPDATE room_data SET temperature = ? WHERE room_id = ?", ('comfy', 101))
#
#     db.commit()

def parse_device_data(room_number):
    device = DeviceState()
    device.number = room_number
    cursor, db = get_cursor()
    data = cursor.execute('SELECT * FROM room_data WHERE room_id = ?', (room_number,))
    data = data.fetchone()
    device.lights = data[8]
    device.blinds = data[9]
    device.windows = data[10]
    device.ac = data[11]
    device.heater = data[12]
    device.air_purifier = data[13]
    device.ventilator = data[14]
    return device

def update_device_data(device):
    room_number = device.number
    cursor, db = get_cursor()
    cursor.execute("UPDATE room_data SET lights_on = ? WHERE room_id = ?", (device.lights, 101))
    cursor.execute("UPDATE room_data SET blinds_open = ? WHERE room_id = ?", (device.blinds, 101))
    cursor.execute("UPDATE room_data SET cooling_on = ? WHERE room_id = ?", (device.ac, 101))
    cursor.execute("UPDATE room_data SET heating_on = ? WHERE room_id = ?", (device.heater, 101))
    cursor.execute("UPDATE room_data SET purifier_on = ? WHERE room_id = ?", (device.air_purifier, 101))
    cursor.execute("UPDATE room_data SET ventilation_on = ? WHERE room_id = ?", (device.ventilator, 101))
    db.commit()

def parse_env_data(data):
    env = envState()
    env.temperature = "high"
    # env.temperature = set_temperature(data['outside_temperature'])

    return env
