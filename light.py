import cv2
import numpy as np
import time
import picamera
import picamera.array

def lightOn(img):
    return np.amax(img) > 254

def main():
    cam = picamera.PiCamera()
    cam.resolution = (100, 100)
    cam.framerate = 60 
    raw = picamera.array.PiRGBArray(cam)

    logF = open("randLog","w")
    
    frameCount = 0
    onStartTime = 0
    offStartTime = 0
    offTime = 0
    onTime = 0
    for frame in cam.capture_continuous(raw, format="bgr", use_video_port=True):
        if lightOn(frame.array):
            if frameCount == 0:
                onStartTime = time.time()
                offTime = onStartTime - offStartTime
                
            frameCount += 1
        else:
            if frameCount != 0:
                offStartTime = time.time()
                onTime = offStartTime - onStartTime
                cycleTime = onTime + offTime
                print frameCount
                print cycleTime
                frameCount = 0
                logF.write(str(cycleTime) + "\n")
        raw.truncate(0)                

if __name__ == "__main__": main()
