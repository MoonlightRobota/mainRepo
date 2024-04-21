import pyrealsense2 as rs
import cv2 as cv
import serial


class depthCam:
    def __init__(self):
        print("initializeing depth camera")
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline.start(config)
        # ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)

    def runDepthCamLoop(self):
        print("running depth camera loop")
        try:
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                raise RuntimeError("Could not acquire a depth frame.")

            # Get the depth frame's dimensions
            width = depth_frame.get_width()
            height = depth_frame.get_height()

            arraySize = 0
            maxArraySize = 0
            arrayStruct = {'xStart' : 0,'xStop' : 0}
            for x in range(0, width, 10):

                # Get the distance of the pixel at (x, y) in meters
                distance = depth_frame.get_distance(x, int(height / 2))

                # Convert distance to centimeters
                distance_cm = distance * 100
                if(distance_cm!=0):
                    print (distance_cm)
                # Check if the pixel is within 10 centimeters
                if distance_cm <= 500 and distance_cm > 0:
                    print(f"The pixel at ({x}, {int(height/2)}) is {distance_cm} centimeters of the camera.")
                if(distance_cm > 500):
                    arraySize+=1
                    if(arraySize > maxArraySize):
                        arrayStruct['xStop'] = x
                        maxArrayStruct = arrayStruct.copy()
                else:
                    arraySize=0 #reset if not gud
                    arrayStruct['xStart'] = x
            #after loop is over, go to maxArray.size / 2 position
            
            print(maxArrayStruct)

        except Exception as e:
            print(e)
        finally:
            # Stop streaming
            # self.pipeline.stop()
            print("none")