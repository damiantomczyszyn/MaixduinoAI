'''
Experiment Name: Pan Tilt Servo Control
Version: v1.0
Date: 2022.03
Author: 01Studio [www.01Studio.org]
Changed by: TiagoTech [www.tiagotech.com]
Description: Control two servos to rotate to different angles in a range
'''

from  machine  import  Timer , PWM
from board import board_info
from fpioa_manager import fm
import  time

#PWM is configured through the timer and connected to the IO21 pin (Pin2 Maixduino Board)
tim  =  Timer ( Timer . TIMER0 , Timer . CHANNEL0 , mode = Timer . MODE_PWM )
tim2  =  Timer ( Timer . TIMER0 , Timer . CHANNEL1 , mode = Timer . MODE_PWM )
S1 = PWM(tim, freq=50, duty=3, pin=board_info.PIN2)
S2 = PWM(tim2, freq=50, duty=3, pin=board_info.PIN3)

def  Servo ( servo , angle ):
    S1.duty(((angle*9.45)/180)+2.95)
    S2.duty(((angle*9.45)/180)+2.95)
    time.sleep(0.03)
    #time.sleep(0.2)
while True:
    for i in range (50,140,1):
        Servo ( S1 , i )
        Servo ( S2 , i )
        print('Degrees:', i)
    for i in range (140,50,-1):
        Servo ( S1 , i )
        Servo ( S2 , i )
        print('Degrees:', i)