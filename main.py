# import lidar
from pathlib import Path
from flask import Flask, send_file
import ps4controller
import multiprocessing

# lidProc = multiprocessing.Process(target = lidar.runDepthCam()) # start parallel process

global depthCam

if __name__ == '__main__':
    # depthCam = lidar.depthCam()
    controller = ps4controller.MyController(interface="/dev/input/js0",
                          connecting_using_ds4drv=False)
    controller.listen(timeout=60)

    

    print("finished")
