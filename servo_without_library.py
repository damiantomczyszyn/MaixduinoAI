'''
Experiment Name: Servo Control
Version: v2.0
Date: 2022.03
Author: 01Studio [www.01Studio.org]
Changed by: TiagoTech [www.tiagotech.com]
Description: Control the servo to rotate to different angles through programming
'''

from  machine  import  Timer , PWM
from board import board_info
from fpioa_manager import fm
import  time

#PWM is configured through the timer and connected to the IO21 pin (Pin2 Maixduino Board)
tim  =  Timer ( Timer . TIMER0 , Timer . CHANNEL0 , mode = Timer . MODE_PWM )
S1 = PWM(tim, freq=50, duty=0, pin=21) # pin=board_info.PIN2)

def  Servo ( servo , angle ):
    S1.duty(((angle*9.45)/180)+2.95)

while True:
    #180 degrees
    Servo ( S1 , 180 )
    time.sleep(1)
    #135 degree
    Servo ( S1 , 135 )
    time.sleep(1)
    #90 degrees
    Servo ( S1 , 90 )
    time.sleep(1)
    #45 degree
    Servo ( S1 , 45 )
    time.sleep(1)
    #0 degree
    Servo ( S1 , 0 )
    time.sleep(1)
