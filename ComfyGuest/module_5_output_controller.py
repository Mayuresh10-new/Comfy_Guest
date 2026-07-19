#!/usr/bin/env python3
# module_5_output_controller.py

import time
import grovepi


class OutputController:
    # Constructor
    def __init__(
        self,
        relay_port=5,
        room_led_port=6,
        status_led_port=7,
        new_led_port=4
):

        self.relay = relay_port
        self.room_led = room_led_port
        self.status_led = status_led_port
        self.new_led = new_led_port

        grovepi.pinMode(self.relay, "OUTPUT")
        grovepi.pinMode(self.room_led, "OUTPUT")
        grovepi.pinMode(self.status_led, "OUTPUT")
        grovepi.pinMode(self.new_led, "OUTPUT")

        # Output Write Delay (seconds)
        self.write_delay = 0.0020

        # Current States
        self.relay_state = False
        self.room_light_state = False
        self.status_state = False
        self.new_state = False

        # Target States
        self.relay_target = False
        self.room_light_target = False
        self.status_target = False
        self.new_target = False

        self.all_off()

    # Helper Function
    def _write(self, port, value):
        grovepi.digitalWrite(port, int(value))
        time.sleep(self.write_delay)

    # Apply pending outputs immediately
    def update(self):

        if self.relay_state != self.relay_target:
            try:
                self._write(self.relay, self.relay_target)
                self.relay_state = self.relay_target
            except IOError:
                print("Relay Write Error")

        if self.room_light_state != self.room_light_target:
            try:
                self._write(self.room_led, self.room_light_target)
                self.room_light_state = self.room_light_target
            except IOError:
                print("Room LED Write Error")

        if self.status_state != self.status_target:
            try:
                self._write(self.status_led, self.status_target)
                self.status_state = self.status_target
            except IOError:
                print("Status LED Write Error")

        if self.new_state != self.new_target:
            try:
                self._write(self.new_led, self.new_target)
                self.new_state = self.new_target
            except IOError:
                print("New LED Write Error")

    # Relay
    def relay_on(self):
        self.relay_target = True

    def relay_off(self):
        self.relay_target = False

    def relay_toggle(self):
        self.relay_target = not self.relay_target

    # Room LED
    def room_light_on(self):
        self.room_light_target = True

    def room_light_off(self):
        self.room_light_target = False

    def room_light_toggle(self):
        self.room_light_target = not self.room_light_target

    # Status LED
    def status_led_on(self):
        self.status_target = True

    def status_led_off(self):
        self.status_target = False

    def status_led_toggle(self):
        self.status_target = not self.status_target

    # New LED
    def new_led_on(self):
        self.new_target = True

    def new_led_off(self):
        self.new_target = False

    def new_led_toggle(self):
        self.new_target = not self.new_target

    # Apply planner/manual action
    def apply_action(self, action):

        if not isinstance(action, dict):
            return

        if "relay" in action:
            self.relay_target = bool(action["relay"])

        if "room_led" in action:
            self.room_light_target = bool(action["room_led"])

        if "status_led" in action:
            self.status_target = bool(action["status_led"])

        if "new_led" in action:
            self.new_target = bool(action["new_led"])

    # Utilities
    def all_off(self):
        self.relay_target = False
        self.room_light_target = False
        self.status_target = False
        self.new_target = False
        self.update()

    def cleanup(self):
        self.all_off()

    def get_states(self):
        return {
            "relay": self.relay_state,
            "room_led": self.room_light_state,
            "status_led": self.status_state,
            "new_led": self.new_state,
        }

    def get_targets(self):
        return {
            "relay": self.relay_target,
            "room_led": self.room_light_target,
            "status_led": self.status_target,
            "new_led": self.new_target,
        }

    def print_status(self):
        print("\n========== OUTPUT CONTROLLER ==========")
        print(f"Relay            : {self.relay_state}")
        print(f"Relay Target     : {self.relay_target}")
        print(f"Room LED         : {self.room_light_state}")
        print(f"Room LED Target  : {self.room_light_target}")
        print(f"Status LED       : {self.status_state}")
        print(f"Status Target    : {self.status_target}")
        print(f"New LED          : {self.new_state}")
        print(f"New LED Target   : {self.new_target}")
        print(f"Write Delay      : {self.write_delay:.3f} sec")
        print("=======================================")