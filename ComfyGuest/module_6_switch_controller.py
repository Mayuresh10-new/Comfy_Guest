#!/usr/bin/env python3
# module_6_switch_controller.py

import time
import grovepi

class SwitchController:
    def __init__(self, port=3, debounce_time=0.2):

        self.port = port
        self.debounce_time = debounce_time

        grovepi.pinMode(self.port, "INPUT")

        self.last_state = 0
        self.last_press_time = 0

        # Operating Mode
        # False = Planner Mode
        # True  = Manual Mode
        self.manual_mode = False

        # Manual actuator states
        self.manual_states = {
            "relay": False,
            "room_led": False,
            "status_led": False,
            "new_led": False,
            "circle": False,
            "circle_plus": False,
        }

    # Scheduler Update
    def update(self):
        try:
            current = grovepi.digitalRead(self.port)

        except IOError as e:
            print(f"Switch read error: {e}")
            return False

        now = time.time()
        changed = False

        # Rising Edge Detection + Debounce
        if (
            current == 1
            and self.last_state == 0
            and (now - self.last_press_time) >= self.debounce_time
        ):
            self.last_press_time = now
            changed = True

            # Toggle Operating Mode
            self.manual_mode = not self.manual_mode

            if self.manual_mode:
                print("\n========== SWITCH ==========")
                print("Manual Mode Enabled")
                print("============================")
            else:
                print("\n========== SWITCH ==========")
                print("Planner Mode Enabled")
                print("============================")
        self.last_state = current
        return changed

    # Dashboard Manual Commands
    def apply_manual_command(self, command):
        if not isinstance(command, dict):
            return

        # Manual Mode
        if "manual_mode" in command:
            self.manual_mode = bool(command["manual_mode"])

        # Manual Actuator States
        for key in self.manual_states:
            if key in command:
                self.manual_states[key] = bool(command[key])

    # Force Planner Mode
    def auto_mode(self):
        self.manual_mode = False
        for key in self.manual_states:
            self.manual_states[key] = False
        print("Planner Mode Enabled")

    # Force Manual Mode
    def manual_mode_on(self):
        self.manual_mode = True
        print("Manual Mode Enabled")

    # Mode
    def get_mode(self):
        return "MANUAL" if self.manual_mode else "PLANNER"

    # Manual States
    def get_states(self):
        return self.manual_states.copy()

    # Compatibility Property
    @property
    def manual_relay(self):
        return self.manual_states["relay"]

    # Debug
    def print_status(self):
        print("\n========== SWITCH ==========")
        print(f"Mode : {self.get_mode()}")

        for key, value in self.manual_states.items():
            print(f"{key:12}: {value}")

        print("============================")