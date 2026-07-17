#!/usr/bin/env python3
# module_5_output_controller.py

import time
import grovepi


class OutputController:

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
        time.sleep(0.1)
        grovepi.pinMode(self.room_led, "OUTPUT")
        time.sleep(0.1)
        grovepi.pinMode(self.status_led, "OUTPUT")
        time.sleep(0.1)
        grovepi.pinMode(self.new_led, "OUTPUT")
        time.sleep(0.1)

        self.relay_state = False
        self.room_light_state = False
        self.status_state = False
        self.new_state = False

        self.all_off()

    # Relay
    def relay_on(self):

        try:
            grovepi.digitalWrite(self.relay, 1)
            self.relay_state = True

        except IOError:
            print("Relay Write Error")

    def relay_off(self):

        try:
            grovepi.digitalWrite(self.relay, 0)
            self.relay_state = False

        except IOError:
            print("Relay Write Error")

    def relay_toggle(self):

        if self.relay_state:
            self.relay_off()
        else:
            self.relay_on()

    ########################################################
    # Room LED
    ########################################################

    def room_light_on(self):
        try:
            grovepi.digitalWrite(self.room_led, 1)
            time.sleep(0.05)
            self.room_light_state = True
        except IOError:
            print("Room LED Write Error")

    def room_light_off(self):

        try:
            grovepi.digitalWrite(self.room_led, 0)
            time.sleep(0.05)
            self.room_light_state = False

        except IOError:
            print("Room LED Write Error")

    def room_light_toggle(self):

        if self.room_light_state:
            self.room_light_off()
        else:
            self.room_light_on()

    ########################################################
    # Status LED
    ########################################################

    def status_led_on(self):

        try:
            grovepi.digitalWrite(self.status_led, 1)
            time.sleep(0.05)
            self.status_state = True

        except IOError:
            print("Status LED Write Error")

    def status_led_off(self):

        try:
            grovepi.digitalWrite(self.status_led, 0)
            time.sleep(0.05)
            self.status_state = False

        except IOError:
            print("Status LED Write Error")

    def status_led_toggle(self):

        if self.status_state:
            self.status_led_off()
        else:
            self.status_led_on()

    ########################################################
    # New LED
    ########################################################

    def new_led_on(self):

        try:
            grovepi.digitalWrite(self.new_led, 1)
            self.new_state = True

        except IOError:
            print("New LED Write Error")

    def new_led_off(self):

        try:
            grovepi.digitalWrite(self.new_led, 0)
            self.new_state = False

        except IOError:
            print("New LED Write Error")

    def new_led_toggle(self):

        if self.new_state:
            self.new_led_off()
        else:
            self.new_led_on()

    ########################################################
    # Blink Status LED
    ########################################################

    def status_led_blink(self, times=3, delay=0.2):

        for _ in range(times):
            self.status_led_on()
            time.sleep(delay)
            self.status_led_off()
            time.sleep(delay)

    ########################################################
    # Apply AI Planner Action
    ########################################################

    def apply_action(self, action):

        if not isinstance(action, dict):
            return

        # Relay
        if "relay" in action:

            if action["relay"]:
                self.relay_on()
            else:
                self.relay_off()

        # Room LED
        if "room_led" in action:

            if action["room_led"]:
                self.room_light_on()
            else:
                self.room_light_off()

        # Status LED
        if "status_led" in action:

            if action["status_led"]:
                self.status_led_on()
            else:
                self.status_led_off()

        # New LED
        if "new_led" in action:

            if action["new_led"]:
                self.new_led_on()
            else:
                self.new_led_off()

    ########################################################
    # Turn Everything OFF
    ########################################################

    def all_off(self):

        self.relay_off()
        self.room_light_off()
        self.status_led_off()
        self.new_led_off()

    ########################################################
    # Cleanup
    ########################################################

    def cleanup(self):

        self.all_off()

    ########################################################
    # Get States
    ########################################################

    def get_states(self):

        return {
            "relay": self.relay_state,
            "room_led": self.room_light_state,
            "status_led": self.status_state,
            "new_led": self.new_state
        }

    ########################################################
    # Print States
    ########################################################

    def print_status(self):

        print("-------------------------------------")
        print("OUTPUT CONTROLLER")
        print("-------------------------------------")
        print("Relay      :", self.relay_state)
        print("Room LED   :", self.room_light_state)
        print("Status LED :", self.status_state)
        print("New LED    :", self.new_state)
        print("-------------------------------------")