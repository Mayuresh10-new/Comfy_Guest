#!/usr/bin/env python3
# module_2_pir_sensor.py

import time
import grovepi

class PIRSensor:
    def __init__(
        self,
        port=8,
        timeout=60,
        update_interval=0.2
    ):

        self.port = port
        self.timeout = timeout
        self.update_interval = update_interval

        grovepi.pinMode(self.port, "INPUT")

        self.motion = False
        self.occupied = False

        self.updated = False

        self.last_motion_time = None
        self.last_update = 0

    # Update Sensor
    def update(self):
        now = time.time()
        self.updated = False
        if (now - self.last_update) < self.update_interval:
            return
        self.last_update = now

        try:
            value = grovepi.digitalRead(self.port)
            if value not in (0, 1):
                return
            self.motion = bool(value)
            if self.motion:
                self.last_motion_time = now
            if self.last_motion_time is None:
                self.occupied = False
            else:
                self.occupied = (
                    now - self.last_motion_time
                ) <= self.timeout
            self.updated = True

        except IOError:
            pass

    # Compatibility Functions
    def read(self):
        self.update()
        return self.motion

    def is_occupied(self):
        self.update()
        return self.occupied

    # Keeps your current main.py working
    def occupied(self):
        return self.is_occupied()

    # Helper
    def seconds_since_motion(self):
        if self.last_motion_time is None:
            return None

        return round(
            time.time() - self.last_motion_time,
            2
        )

    # Reset
    def reset(self):
        self.motion = False
        self.occupied = False
        self.last_motion_time = None

    # Debug
    def print_status(self):
        self.update()
        print("--------------------------------")
        print("PIR SENSOR")
        print("--------------------------------")
        print(f"Motion        : {self.motion}")
        print(f"Occupied      : {self.occupied}")
        print(f"Updated       : {self.updated}")
        print(f"Last Motion   : {self.seconds_since_motion()}")
        print("--------------------------------")


def main():
    pir = PIRSensor(
        port=8,
        timeout=15
    )
    print("Monitoring PIR Sensor...\n")

    while True:
        pir.update()
        pir.print_status()
        time.sleep(0.2)


if __name__ == "__main__":
    main()