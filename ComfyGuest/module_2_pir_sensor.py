#!/usr/bin/env python3
# module_2_pir_sensor.py

import time
import grovepi


class PIRSensor:

    def __init__(self, port=8, timeout=60):
        """
        PIR Motion Sensor

        port    : Grove digital port
        timeout : Seconds to keep room occupied after
                  the last detected motion.
        """

        self.port = port
        self.timeout = timeout

        grovepi.pinMode(self.port, "INPUT")

        self.last_motion_time = None

    ########################################################
    # Read PIR Sensor
    ########################################################

    def read(self):
        """
        Returns instantaneous PIR state.

        True  -> Motion detected
        False -> No motion
        """

        try:

            value = grovepi.digitalRead(self.port)

            # Ignore invalid GrovePi reads
            if value not in (0, 1):
                return False

            if value == 1:
                self.last_motion_time = time.time()
                return True

            return False

        except IOError:

            return False

    ########################################################
    # Occupancy
    ########################################################

    def occupied(self):

        if self.last_motion_time is None:
            return False

        return (time.time() - self.last_motion_time) <= self.timeout

    ########################################################
    # Time Since Last Motion
    ########################################################

    def seconds_since_motion(self):

        if self.last_motion_time is None:
            return None

        return round(time.time() - self.last_motion_time, 2)

    ########################################################
    # Reset Occupancy
    ########################################################

    def reset(self):

        self.last_motion_time = None

    ########################################################
    # Debug
    ########################################################

    def print_status(self):

        motion = self.read()

        print("--------------------------------")
        print("PIR SENSOR")
        print("--------------------------------")
        print(f"Motion    : {motion}")
        print(f"Occupied  : {self.occupied()}")
        print(f"Last Seen : {self.seconds_since_motion()}")
        print("--------------------------------")