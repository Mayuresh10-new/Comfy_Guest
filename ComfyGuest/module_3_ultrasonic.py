#!/usr/bin/env python3
# module_3_ultrasonic.py

import grovepi


class UltrasonicSensor:
    def __init__(self, port=4, threshold=50):
        """
        Initialize Ultrasonic Sensor

        port      : Digital port number
        threshold : Guest detection distance (cm)
        """

        self.port = port
        self.threshold = threshold

        self.distance = None

        # Use Raspberry Pi hardware I2C
        grovepi.set_bus("RPI_1")

    def read(self):
        """
        Reads the ultrasonic sensor.

        Returns:
            Distance in centimeters.
        """

        try:
            distance = grovepi.ultrasonicRead(self.port)

            # Accept only valid readings
            if 2 <= distance <= 400:
                self.distance = distance

        except Exception:
            pass

        return self.distance

    def guest_detected(self):
        """
        Returns True if a guest is within the threshold distance.
        """

        distance = self.read()

        if distance is None:
            return False

        return distance <= self.threshold