#!/usr/bin/env python3
# module_9_plugwise.py

import time
import plugwise

class PlugwiseController:

    # Constructor
    def __init__(self, usb, circle_plus_mac, circle_mac):
        self.usb = usb
        self.circle_plus_mac = circle_plus_mac
        self.circle_mac = circle_mac
        self.stick = None
        self.circle = None
        self.circle_plus = None

        # Current relay states
        self.circle_state = False
        self.circle_plus_state = False

        # Desired relay states
        self.circle_target = False
        self.circle_plus_target = False

        # Scheduler
        self.last_update = 0
        self.update_interval = 0.10
        self.connected = False
        self.connect()

    # Connect
    def connect(self):
        print("--------------------------------------")
        print("Connecting to Plugwise...")
        print("--------------------------------------")

        try:
            self.stick = plugwise.stick(
                self.usb,
                print_progress=False
            )
            self.stick.connect()
            self.stick.initialize_stick()
            self.stick.scan()
            print("Searching for Plugwise devices...")
            while self.circle is None or self.circle_plus is None:
                if self.circle is None:
                    self.circle = self.stick.node(
                        self.circle_mac
                    )

                if self.circle_plus is None:
                    self.circle_plus = self.stick.node(
                        self.circle_plus_mac
                    )
                time.sleep(0.5)

            # Read Initial States
            self.circle_state = self.circle.get_relay_state()
            self.circle_plus_state = (
                self.circle_plus.get_relay_state()
            )
            self.circle_target = self.circle_state
            self.circle_plus_target = self.circle_plus_state
            self.connected = True
            print("Plugwise Ready")

        except Exception as e:
            print("Plugwise Connection Error:", e)
            self.connected = False

    # Scheduler Update
    def update(self):
        now = time.time()
        if now - self.last_update < self.update_interval:
            return
        self.last_update = now
        if not self.connected:
            return

        # Circle
        if self.circle_state != self.circle_target:
            try:
                self.circle.set_relay_state(
                    self.circle_target
                )
                self.circle_state = self.circle_target
            except Exception as e:
                print("Circle Update Error:", e)

        # Circle+
        if self.circle_plus_state != self.circle_plus_target:
            try:
                self.circle_plus.set_relay_state(
                    self.circle_plus_target
                )

                self.circle_plus_state = (
                    self.circle_plus_target
                )

            except Exception as e:
                print("Circle+ Update Error:", e)

    # Circle Commands
    def circle_on(self):
        self.circle_target = True

    def circle_off(self):
        self.circle_target = False

    def circle_toggle(self):
        self.circle_target = not self.circle_target

    # Circle+ Commands
    def circle_plus_on(self):
        self.circle_plus_target = True

    def circle_plus_off(self):
        self.circle_plus_target = False

    def circle_plus_toggle(self):
        self.circle_plus_target = (
            not self.circle_plus_target
        )

    # Connection Status
    def is_connected(self):
        return self.connected

    # Reconnect
    def reconnect(self):
        if self.connected:
            return
        print("Reconnecting Plugwise...")
        try:
            self.connect()
        except Exception as e:
            print("Reconnect Failed:", e)

    # Current States
    def get_states(self):
        return {
            "circle": self.circle_state,
            "circle_plus": self.circle_plus_state
        }

    # Target States
    def get_targets(self):
        return {
            "circle": self.circle_target,
            "circle_plus": self.circle_plus_target
        }

    # Debug
    def print_status(self):
        print("\n========== PLUGWISE ==========")
        print(f"Connected        : {self.connected}")
        print(f"Circle           : {self.circle_state}")
        print(f"Circle Target    : {self.circle_target}")
        print(f"Circle+          : {self.circle_plus_state}")
        print(f"Circle+ Target   : {self.circle_plus_target}")
        print("==============================")

    # Cleanup
    def cleanup(self):
        try:
            if self.stick is not None:
                self.stick.disconnect()
                self.connected = False
                print("Plugwise Disconnected")
        except Exception as e:
            print("Plugwise Disconnect Error:", e)