# MaixduinoAI - By: damian tomczyszyn - Fri Mar 1 2024

import sensor, image, time
from fpioa_manager import fm
from Maix import GPIO
import utime

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

##################

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
    print('Zmieniamy ledy na 1')
    pin_13.value(1)
    pin_12.value(1)
    pin_11.value(1)


    utime.sleep_ms(1500)
    print('Zmieniamy ledy na 0')
    pin_13.value(0)
    pin_12.value(0)
    pin_11.value(0)


    utime.sleep_ms(1500)
