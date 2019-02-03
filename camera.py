from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (2592, 1944)
camera.framerate = 15

camera.start_preview()
#sleep for a period of time long enough to get spectometer aligned
sleep(100)
camera.capture('/home/pi/Desktop/focustest.png')
camera.stop_preview()
