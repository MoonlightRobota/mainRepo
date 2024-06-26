from pyPS4Controller.controller import Controller
import serial
import gpt
import time

# ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
global depthCam

def transf(raw):
    temp = (raw+32767)/65534
    return round(temp*2 -1, 2)
    # Filter values that are too weak for the motors to move
    #if abs(temp) < 0.25:
    #    return 0
    # Return a value between 0.3 and 1.0
    #else:
    #    return round(temp, 1)

throttle = 0
turn = 0
max_speed = 1.0
min_speed = -1.0

def printThrust():
    #print("Throttle: ", throttle, " - Turn: ", turn)
    rwheel = throttle + turn
    lwheel = throttle - turn
    
    # Apply threshold check
    if abs(lwheel) > 0.1 or abs(rwheel) > 0.1:  # Adjust threshold as needed
        # Perform normalization
        if abs(lwheel) > max_speed or abs(rwheel) > max_speed:
            max_val = max(abs(lwheel), abs(rwheel))
            lwheel = (lwheel / max_val) * max_speed
            rwheel = (rwheel / max_val) * max_speed
        
        # Generate packet (commented out for now)
        packet = "R:", str(rwheel), "L:", lwheel
        # ser.write(packet.encode())
        print("R: ", rwheel, " - L: ", lwheel)
    


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.last_event_time = time.time()
        self.debounce_time = 0.5  # Adjust debounce time as needed (in seconds)
    
    # def on_R3_right(self, value):
    #     current_time = time.time()
    #     if current_time - self.last_event_time > self.debounce_time:
    #         if abs(value) > 0.1:  # Adjust threshold as needed
    #             print("on_R3_right:", value)
    #         self.last_event_time = current_time
    # def on_L2_release(self):
    #     print("on_L2_release")
    
    # def on_L1_press(self):
    #     return super().on_L1_press()

    def on_R2_release(self):
        print("R2 released, calling GPT backend")
        gpt.process_image_and_generate_speech()

    def on_x_press(self):
        print("X pressed")

    def on_x_release(self):
        print("X released")

    # def on_L3_up(self, value):
    #     global throttle
    #     throttle = transf(-value)
    #     printThrust()

    # def on_L3_down(self, value):
    #     global throttle
    #     throttle = transf(-value)
    #     printThrust()
    
    # def on_L3_right(self, value):
    #     global turn
    #     turn = transf(value)
    #     printThrust()

    # def on_L3_left(self, value):
    #     global turn
    #     turn = transf(value)
    #     printThrust()
