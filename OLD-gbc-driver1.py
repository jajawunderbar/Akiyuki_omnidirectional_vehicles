# Old code for the GBC modul  from video 1 with central hub and without calibration and battery management
from pybricks.hubs import ThisHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

HUB_ID = 1  # This is Hub 1 

# Initialize hub: listen on channel 1, broadcast finished messages on channel 2
hub = ThisHub(observe_channels=[1], broadcast_channel=2)
motor_a = Motor(Port.A)  # horizontal
motor_b = Motor(Port.B)  # Vertical

def execute_command_1(cycle):

    hub.light.on(Color.GREEN)
    SIDE_DISTANCE = 1600  # Distance for each edge / not used
    
	motor_b.run_angle(900, -1155, then=Stop.HOLD, wait=True)
    wait(700)
    motor_b.run_angle(900, 200, then=Stop.HOLD, wait=True)
    motor_a.run_angle(900, -1670, then=Stop.HOLD, wait=True)
    motor_b.run_angle(900, 1420, then=Stop.HOLD, wait=True)
    wait(700)
    motor_b.run_angle(900, -480, then=Stop.HOLD, wait=True)
    motor_a.run_angle(900, 1665, then=Stop.HOLD, wait=True)

    
    hub.light.on(Color.RED)

def execute_command(cmd_id, cycle):
    if cmd_id == 1:
        execute_command_1(cycle)
    else:
        print("Unknown command:", cmd_id)

last_cycle = None

while True:
    hub.light.on(Color.RED)  # Idle state
    command = hub.ble.observe(1)
    if command is not None:
        # Expected format: (command_id, delay_offset, cycle)
        cmd_id, delay_offset, cmd_cycle = command
        if last_cycle != cmd_cycle:
            last_cycle = cmd_cycle
            additional_delay = (HUB_ID - 1) * delay_offset
            wait(additional_delay)
            print("Hub", HUB_ID, "executing command", command, "after delay of", additional_delay, "ms")
            execute_command(cmd_id, cmd_cycle)
            hub.ble.broadcast((HUB_ID, cmd_id, cmd_cycle))
            print("Hub", HUB_ID, "sent finished message:", (HUB_ID, cmd_id, cmd_cycle))
    wait(10)
