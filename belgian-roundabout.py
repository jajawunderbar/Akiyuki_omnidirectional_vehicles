#As seen in the video with 3 hubs.
from pybricks.hubs import ThisHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from umath import sin, cos, radians

HUB_ID = 1             # Unique hub id (set 1,2,3,4)
PHASE_OFFSET = 0       # Phase offset in ms for maneuver scheduling

# Phase durations (ms)
T1 = 800    # Phase 1: Arc out 
T2 = 2100   # Phase 2: Straight fast return (backward)
T3 = 800    # Phase 3: Arc in 
T4 = 3900   # Phase 4: Slow forward movement
T_total = T1 + T2 + T3 + T4

v_slow = 350   # Slow speed (deg/s)
v_fast = 1300  # Fast speed (deg/s)
dt = 10        # Update interval (ms)
t = 0          # Cycle time in ms

hub = ThisHub(observe_channels=[1], broadcast_channel=2)
motor_a = Motor(Port.A) 
motor_b = Motor(Port.B)  

# Reset angles for closed-loop control
motor_a.reset_angle(0)
motor_b.reset_angle(0)
target_angle_a = 0  
target_angle_b = 0 
# Wait for common start command via BLE
command_received = False
while not command_received:
    command = hub.ble.observe(1)
    if command is not None:
        command_received = True
        print("Hub", HUB_ID, "received command:", command)
    wait(10)

hub.light.on(Color.GREEN)  # LED green: running

# Pre-drive: For rovers 2-4, drive straight forward for increasing durations
if HUB_ID > 1:
    # Each subsequent rover drives longer before entering the main loop
    init_duration = (HUB_ID - 1) * 900  # in ms (e.g. HUB_ID=2 -> 1000ms, 3->2000ms, etc.)
    t_init = 0
    while t_init < init_duration:
        # 
        target_angle_a += v_slow * (dt / 1000)
        motor_a.run_target(v_slow, target_angle_a, wait=False)
        motor_b.run_target(v_slow, target_angle_b, wait=False)
        wait(dt)
        t_init += dt

# Main loop: Maneuver cycles via angle control
while True:
    cycle_time = (t + PHASE_OFFSET) % T_total

    if cycle_time < T1:
        # Phase 1: Arc out 
        u = cycle_time / T1
        heading = u * 90
        delta_b = v_fast * sin(radians(heading)) * (dt / 800)  
        delta_a = v_fast * cos(radians(heading)) * (dt / 1000)  
        current_v = v_fast
    elif cycle_time < T1 + T2:
        # Phase 2: Straight fast return (backward)
        delta_b = 0
        delta_a = -v_fast * (dt / 1000)
        current_v = v_fast
    elif cycle_time < T1 + T2 + T3:
        # Phase 3: Arc in 
        u = (cycle_time - T1 - T2) / T3
        heading = u * -90
        delta_b = v_fast * sin(radians(heading)) * (dt / 800)
        delta_a = v_fast * cos(radians(heading)) * (dt / 1000)
        current_v = v_fast
    else:
        # Phase 4: Slow forward movement
        delta_b = 0
        delta_a = v_slow * (dt / 1000)
        current_v = v_slow

    target_angle_b += delta_b
    target_angle_a += delta_a

    motor_b.run_target(current_v, target_angle_b, wait=False)
    motor_a.run_target(current_v, target_angle_a, wait=False)

    wait(dt)
    t += dt
