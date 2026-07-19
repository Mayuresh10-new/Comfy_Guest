#!/usr/bin/env python3
# module_4_light_sensor.py

import time
import grovepi

class LightSensor:
    def __init__(
        self,
        port=0,
        threshold=400,
        update_interval=0.5
    ):

        self.port = port
        self.threshold = threshold
        self.update_interval = update_interval

        self.value = None
        self.dark = False
        self.brightness = 0.0

        self.updated = False
        self.last_update = 0

    # Update Sensor
    def update(self):
        now = time.time()
        self.updated = False

        if (now - self.last_update) < self.update_interval:
            return
        self.last_update = now

        try:
            value = grovepi.analogRead(self.port)
            if 0 <= value <= 1023:
                self.value = value
                self.dark = (
                    value < self.threshold
                )
                self.brightness = round(
                    (value / 1023) * 100,
                    1
                )
                self.updated = True

        except IOError:
            pass

    # Compatibility Functions
    def read(self):
        self.update()
        return self.value

    def is_dark(self):
        self.update()
        return self.dark

    def brightness_percentage(self):
        self.update()
        return self.brightness

    # Helper
    def age(self):
        if self.last_update == 0:
            return None

        return round(
            time.time() - self.last_update,
            2
        )

    # Debug
    def print_status(self):
        self.update()
        print("--------------------------------")
        print("LIGHT SENSOR")
        print("--------------------------------")

        if self.value is None:
            print("Value       : ---")

        else:
            print(f"Value       : {self.value}")

        print(f"Dark        : {self.dark}")
        print(f"Brightness  : {self.brightness:.1f}%")
        print(f"Updated     : {self.updated}")
        print(f"Age         : {self.age()} sec")
        print("--------------------------------")

def main():
    light = LightSensor(
        port=0,
        threshold=400
    )
    print("Reading Light Sensor...\n")

    while True:
        light.update()
        light.print_status()
        time.sleep(0.2)

if __name__ == "__main__":
    main()