from pyPS4Controller.controller import Controller
import gpt
import threading
import time
import serial

# Define global variables
FRAME_COUNT = 60
throttle = 0
turn = 0

ser = serial.Serial('/dev/ttyACM0', 9600)

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

        #throttle is the y value
        #turn is the x value

        #if(turn > 0)
        if(turn > 0.1):
            s1 = s3 = (throttle) * abs(turn)
            s2 = s4 = throttle
            print("turning right")
        elif(turn < -0.1):
            s1 = s3 = throttle
            s2 = s4 = throttle * abs(turn)
            print("turning left")


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
