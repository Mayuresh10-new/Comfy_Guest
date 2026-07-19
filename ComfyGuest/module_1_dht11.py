#!/usr/bin/env python3
# module_1_dht11.py

import time
import math
import grovepi

class DHT11Sensor:
    def __init__(self, port=2, sensor_type=0, update_interval=2):

        self.port = port
        self.sensor_type = sensor_type
        self.update_interval = update_interval

        # Cached Values
        self.temperature = None
        self.humidity = None

        self.updated = False
        self.last_update = 0

    # Update Sensor
    def update(self):

        now = time.time()

        # Scheduler interval
        if now - self.last_update < self.update_interval:
            return False

        # Retry Reading
        for attempt in range(3):
            try:
                temperature, humidity = grovepi.dht(
                    self.port,
                    self.sensor_type
                )

                # Reject None
                if temperature is None or humidity is None:
                    continue

                # Reject NaN
                if math.isnan(temperature) or math.isnan(humidity):
                    continue

                # Reject GrovePi bogus readings
                if (
                    temperature <= 0
                    or temperature > 80
                    or humidity <= 0
                    or humidity > 100
                ):
                    continue

                # Valid Reading
                self.temperature = round(float(temperature), 1)
                self.humidity = round(float(humidity), 1)

                self.updated = True
                self.last_update = now

                return True

            except Exception:
                pass

            time.sleep(0.05)

        # Failed
        self.updated = False
        return False

    # Backwards Compatibility
    def read(self):
        self.update()
        return self.temperature, self.humidity

    # Age of Cached Reading
    def age(self):
        if self.last_update == 0:
            return None
        return round(time.time() - self.last_update, 1)

    # Debug
    def print_status(self):
        print("\n========== DHT11 ==========")
        print(f"Temperature : {self.temperature}")
        print(f"Humidity    : {self.humidity}")
        print(f"Updated     : {self.updated}")
        print(f"Age         : {self.age()} s")
        print("===========================")