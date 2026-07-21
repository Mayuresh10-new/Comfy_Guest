class RoomState:

    def __init__(self):
        self.number = None
        self.temperature = None
        self.humidity = None
        self.daytime = None
        self.air_quality = None
        self.motion = None
        self.occupied = None
        self.guest_near = None
        self.lights_on = None
        self.blinds_open = None
        self.cooling_on = None
        self.heating_on = None
        self.purifier_on = None
        self.ventilation_on = None
        self.lux = None
        self.dark = None

        self.manual_mode = None
        self.occupied = None
        self.checked_in = None

class DeviceState:
    def __init__(self):
        self.number = None
        self.lights = None
        self.blinds = None
        self.windows = None
        self.ac = None
        self.heater = None
        self.air_purifier = None
        self.ventilator = None

class envState:
    def __init__(self):
        self.number = None
        self.temperature = None