# #!/usr/bin/env python3

# import time
# import plugwise

# USB = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A6010MU7-if00-port0"

# # Devices
# CIRCLE_PLUS = "000D6F0005692784"
# CIRCLE = "000D6F000416E6F4"

# print("Connecting...")

# stick = plugwise.stick(
#     USB,
#     print_progress=False
# )

# stick.connect()
# stick.initialize_stick()
# stick.scan()

# print("\nWaiting for devices...")

# circle_plus = None
# circle = None

# while circle_plus is None or circle is None:
#     if circle_plus is None:
#         circle_plus = stick.node(CIRCLE_PLUS)

#     if circle is None:
#         circle = stick.node(CIRCLE)

#     time.sleep(1)

# print("\nBoth devices found!")

# print(f"Circle+ : {CIRCLE_PLUS}")
# print(f"Circle  : {CIRCLE}")

# # -------------------------------------------------------------------
# # Circle+
# # -------------------------------------------------------------------

# print("\n========== Circle+ ==========")

# print("Current State:", circle_plus.get_relay_state())

# print("Turning Circle+ ON")
# circle_plus.set_relay_state(True)
# time.sleep(5)

# print("Turning Circle+ OFF")
# circle_plus.set_relay_state(False)
# time.sleep(5)

# # -------------------------------------------------------------------
# # Circle
# # -------------------------------------------------------------------

# print("\n========== Circle ==========")

# print("Current State:", circle.get_relay_state())

# print("Turning Circle ON")
# circle.set_relay_state(True)
# time.sleep(5)

# print("Turning Circle OFF")
# circle.set_relay_state(False)
# time.sleep(5)

# stick.disconnect()

# print("\nFinished.")






#!/usr/bin/env python3

import time
import plugwise

USB = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A6010MU7-if00-port0"

# Device MAC addresses
CIRCLE_PLUS = "000D6F0005692784"   # Fan
CIRCLE = "000D6F000416E6F4"        # Lamp

print("Connecting...")

stick = plugwise.stick(
    USB,
    print_progress=False
)

stick.connect()
stick.initialize_stick()
stick.scan()

print("\nWaiting for devices...")

circle_plus = None
circle = None

while circle_plus is None or circle is None:

    if circle_plus is None:
        circle_plus = stick.node(CIRCLE_PLUS)

    if circle is None:
        circle = stick.node(CIRCLE)

    time.sleep(1)

print("\nBoth devices found!")
print(f"Circle+ (Fan)  : {CIRCLE_PLUS}")
print(f"Circle  (Lamp) : {CIRCLE}")

print("\nCurrent States")
print("---------------------------")
print("Fan  :", "ON" if circle_plus.get_relay_state() else "OFF")
print("Lamp :", "ON" if circle.get_relay_state() else "OFF")

print("\nWhat would you like to turn ON?")
print("--------------------------------")
print("1 - Fan")
print("2 - Lamp")
print("3 - Fan + Lamp")
print("4 - Nothing")

choice = input("\nEnter choice (1-4): ").strip()

# Turn everything OFF first
circle_plus.set_relay_state(False)
circle.set_relay_state(False)

time.sleep(1)

if choice == "1":
    print("\nTurning Fan ON...")
    circle_plus.set_relay_state(True)

elif choice == "2":
    print("\nTurning Lamp ON...")
    circle.set_relay_state(True)

elif choice == "3":
    print("\nTurning Fan and Lamp ON...")
    circle_plus.set_relay_state(True)
    circle.set_relay_state(True)

elif choice == "4":
    print("\nLeaving everything OFF.")

else:
    print("\nInvalid choice. Everything will remain OFF.")

time.sleep(1)

print("\nFinal States")
print("---------------------------")
print("Fan  :", "ON" if circle_plus.get_relay_state() else "OFF")
print("Lamp :", "ON" if circle.get_relay_state() else "OFF")

print("\nDisconnecting...")

try:
    stick.disconnect()
except Exception as e:
    print("Disconnect warning:", e)

# Give Plugwise threads time to stop
time.sleep(2)

print("\nProgram finished successfully.")