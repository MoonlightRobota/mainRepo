from pyPS4Controller.controller import Controller
import gpt
import threading
import time
import serial

# Define global variables
FRAME_COUNT = 60
throttle = 0
turn = 0

def transf(raw):
    temp = (raw + 32767) / 65534
    return round(temp * 2 - 1, 2)

# Define the printThrust function
def printThrust():
    global throttle, turn
    rwheel = throttle + turn
    lwheel = throttle - turn
    # Printing the thrust values
    # print("R: ", rwheel, " - L: ", lwheel)

def writeToSer():
    global throttle, turn
    while True:
        print(throttle, turn)
        time.sleep(0.2)

# Define the MyController class
class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        
    def on_L3_up(self, value):
        global throttle
        throttle = transf(-value)
        printThrust()
        
    def on_L3_down(self, value):
        global throttle
        throttle = transf(-value)
        printThrust()
        
    def on_L3_right(self, value):
        global turn
        turn = transf(value)
        printThrust()
        
    def on_L3_left(self, value):
        global turn
        turn = transf(value)
        printThrust()
        

# Create and start the thread for writeToSer function
write_thread = threading.Thread(target=writeToSer)
write_thread.daemon = True  # Daemonize the thread so it automatically exits when the main program ends
write_thread.start()

# Initialize the controller with your custom controller class
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

# Start listening for events
controller.listen()
