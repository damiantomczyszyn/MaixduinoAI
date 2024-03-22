'''
Experiment Name: PWM LED
Version: v2.0
Date: 2022.03
Changed by: TiagoTech [www.tiagotech.com]
Description: Pulsating LED using PWM
'''

from machine import Timer,PWM
import time
from board import board_info
from fpioa_manager import fm

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
ch = PWM(tim, freq=500000, duty=50, pin=board_info.PIN2)

duty=0
dir = True

while True:
    if dir:
        duty += 10
    else:
        duty -= 10
    if duty>100:
        duty = 100
        dir = False
    elif duty<0:
        duty = 0
        dir = True
    time.sleep(0.05)
    ch.duty(duty)
