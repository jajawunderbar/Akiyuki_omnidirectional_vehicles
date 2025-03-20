# Old code for the GBC modul  from video 1 with central hub and without calibration and battery management
from pybricks.hubs import ThisHub
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Color

# Controller hub: broadcast commands on channel 1, observe responses on channel 2
hub = ThisHub(broadcast_channel=1, observe_channels=[2])

COMMAND_ID = 1         # Command: square driving pattern along platform edges
DELAY_OFFSET = 0       # Base delay per rover (ms)
active_hubs = [1, 2]   # Active rover hub IDs
MAX_WAIT = 6000        # Maximum wait time in ms
cycle = 1

def wait_for_responses(current_cycle):
    """
    Wait until all active rovers send their finished message for the current cycle.
    """
    hub.light.on(Color.RED)  # Idle state
    responses = set()
    timer = StopWatch()
    timer.reset()
    while timer.time() < MAX_WAIT:
        response = hub.ble.observe(2)
        if response is not None:
            hub_id, cmd_id, resp_cycle = response
            if cmd_id == COMMAND_ID and resp_cycle == current_cycle:
                responses.add(hub_id)
                print("Received response from Hub", hub_id, "for cycle", current_cycle)
                if set(active_hubs).issubset(responses):
                    break
        wait(10)
    return responses

while True:

    hub.light.on(Color.GREEN)  # Driving phase
    command = (COMMAND_ID, DELAY_OFFSET, cycle)
    hub.ble.broadcast(command)
    print("Sent command:", command)
    responses = wait_for_responses(cycle)
    print("Cycle", cycle, "responses received from:", responses)
    cycle += 1
    wait(1000)
