# Copy this script to each Rover and change Hub-id und start-angle

from pybricks.hubs import ThisHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from umath import sin, cos, radians

HUB_ID = 1                # Hub identifier
START_ANGLE = 0           # Starting angle in degrees
DIAMETER = 2150           # Desired circle diameter
RADIUS = DIAMETER / 2

v = 1000                  # Base motor speed (deg/s)
omega = 2 * v / DIAMETER  # Angular velocity (rad/s)
dt = 10                   # Update interval (ms)
# Angle increment per update (degrees)
delta_angle = (omega * (dt / 1000)) * (180 / 3.14159)

# Initialize hub and motors
hub = ThisHub(observe_channels=[1], broadcast_channel=2)
motor_a = Motor(Port.A)   # horizontal movement
motor_b = Motor(Port.B)   # vertical movement

# Wait for start command via BLE
command_received = False
while not command_received:
    command = hub.ble.observe(1)
    if command is not None:
        command_received = True
        print("Hub", HUB_ID, "received command:", command)
    wait(10)

hub.light.on(Color.GREEN)  # LED green: running

theta = START_ANGLE
while True:
    # Calculate raw speeds from circle equation
    raw_speed_x = v * cos(radians(theta))
    raw_speed_y = v * sin(radians(theta))
    # Scale speeds so that the sum of abs values equals v (for constant effective speed)
    denom = abs(cos(radians(theta))) + abs(sin(radians(theta)))
    if denom != 0:
        speed_x = raw_speed_x / denom
        speed_y = raw_speed_y / denom
    else:
        speed_x = raw_speed_x
        speed_y = raw_speed_y

    # Assign speeds to correct motors (motor_a: horizontal, motor_b: vertical)
    motor_a.run(speed_x)  
    motor_b.run(speed_y)  

    wait(dt)  # Update interval
    theta = (theta + delta_angle) % 360
