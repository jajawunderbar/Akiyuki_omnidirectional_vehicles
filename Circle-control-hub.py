# Simple example for a controll hub and up to 4 and more Rover hubs
# Similar to video 2, but there with ellipses not circles

from pybricks.hubs import ThisHub
from pybricks.parameters import Color
from pybricks.tools import wait

# Controller hub: send command on channel 1
hub = ThisHub(broadcast_channel=1)

COMMAND_ID = 1   # Command: start continuous circle mode
DELAY_OFFSET = 0
cycle = 1

# Send command once to start continuous circle mode
command = (COMMAND_ID, DELAY_OFFSET, cycle)
hub.ble.broadcast(command)
print("Sent command:", command)

# Remain idle; drivers run continuously after receiving command.
while True:
    wait(1000)