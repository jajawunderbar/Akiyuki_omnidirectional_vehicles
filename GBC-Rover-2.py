from pybricks.hubs import ThisHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

HUB_ID = 2  

BATTERY_LIMIT = 6000      # Warning threshold (mV)
PARK_BATTERY_LIMIT = 5500 # Critical threshold (mV)
calibration_interval = 5
cmd_cycle = 0
dutylimit = 50

# Initialize hub: listen/ broadcast
hub = ThisHub(broadcast_channel=1)
motor_a = Motor(Port.A)  # Horizontal
motor_b = Motor(Port.B)  # Vertical

def execute_command_1(cycle):

    global cmd_cycle
        # Update LED based on battery voltage
    if hub.battery.voltage() < BATTERY_LIMIT:
        hub.light.blink(Color.ORANGE, (200, 200))
    else:
        hub.light.on(Color.GREEN)

    motor_a.run_angle(900, -1700, then=Stop.HOLD, wait=True)
    motor_b.run_angle(900, 1620, then=Stop.HOLD, wait=True)
    wait(600)
    motor_b.run_angle(900, -380, then=Stop.HOLD, wait=True)
    motor_a.run_angle(900, 1700, then=Stop.HOLD, wait=True)
    motor_b.run_angle(900, -1355, then=Stop.HOLD, wait=True)
    if cmd_cycle == calibration_interval:
            calibrate_stall()
            cmd_cycle = 0
    else:
            print("Battery voltage:", hub.battery.voltage(), "mV") #debug

            if hub.battery.voltage() < PARK_BATTERY_LIMIT:
                hub.light.blink(Color.RED, (100, 100))
                print("Entering park mode.")
                motor_b.run_angle(900, 130, then=Stop.HOLD, wait=True)
                motor_a.run_angle(900, -2400, then=Stop.HOLD, wait=True)
                while True:
                    wait(1000)

            wait(600)
            motor_b.run_angle(900, 130, then=Stop.HOLD, wait=True)

def calibrate_stall():

    hub.light.blink(Color.BLUE, (300, 300))
    print("Calibration starting.")

    if hub.battery.voltage() > 7500: #Motor ist stronger with full batteries
        dutylimit = 30
    else:
        dutylimit = 50

    motor_b.run_until_stalled(-200, duty_limit=dutylimit)
    motor_b.stop()
    motor_b.run_angle(900, 100, then=Stop.HOLD, wait=True)
    motor_a.run_until_stalled(200, duty_limit=dutylimit)
    motor_a.stop()
    motor_a.run_angle(900, -100, then=Stop.HOLD, wait=True)

    hub.ble.broadcast((HUB_ID, 3, 0))
    print("Calibration finished; Hub2.")
    hub.light.on(Color.RED) 
    wait(1000) #to be Rover 1 always first
 
print(cmd_cycle, calibration_interval) # debug

calibrate_stall()

while True:

    execute_command_1(cmd_cycle)
    hub.ble.broadcast((HUB_ID, 0, 9)) # Clear Message
    #print(cmd_cycle, calibration_interval) #debug
    cmd_cycle += 1
                
    wait(10)