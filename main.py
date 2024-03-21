# MaixduinoAI - By: damian tomczyszyn - Fri Mar 1 2024

import sensor, image, time
from fpioa_manager import fm
from Maix import GPIO
from machine import Pin, PWM

from machine import I2C# ,Pin - nie ma pinu dla maixduino jak jest dla ESP



from servo import Servo
import pcf8575
import time
import utime
#from hcsr04 import HCSR04
import hcsr04
import KPU as kpu #do zarządzania pamięcią, np karta SD
#Load the AI models from SD Card
#task_fd = kpu.load("/sd/FaceDetection.smodel")
#task_ld = kpu.load("/sd/FaceLandmarkDetection.smodel")
#task_fe = kpu.load("/sd/FeatureExtraction.smodel")

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)


#################
print('pins init')

fm.register(3, fm.fpioa.GPIO0)
fm.register(10, fm.fpioa.GPIO1)
fm.register(11, fm.fpioa.GPIO2)

pin_13 = GPIO(GPIO.GPIO0, GPIO.OUT)
pin_12 = GPIO(GPIO.GPIO1, GPIO.OUT)
pin_11 = GPIO(GPIO.GPIO2, GPIO.OUT)

#pin 10 to 13 w kodzie
#pin 9  to 12 w kodzie
##################

sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

clock = time.clock()



motor=Servo(pin=22) # A changer selon la broche utilisée
motor.move(0) # tourne le servo à 0°
time.sleep(0.3)
motor.move(90) # tourne le servo à 90°
time.sleep(0.3)
motor.move(180) # tourne le servo à 180°
time.sleep(0.3)
motor.move(90) # tourne le servo à 90°
time.sleep(0.3)
motor.move(0) # tourne le servo à 0°
time.sleep(0.3)


while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
    print('Zmieniamy ledy na 1')
    pin_13.value(1)
    pin_12.value(1)
    pin_11.value(1)

    #pomiar dystansu
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')


    utime.sleep_ms(1500)
    print('Zmieniamy ledy na 0')
    pin_13.value(0)
    pin_12.value(0)
    pin_11.value(0)


    utime.sleep_ms(1500)
