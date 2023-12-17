import RPi.GPIO as GPIO
import time
import random

 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
 

class SegmentDisplay(object):
    def __init__(self, id, segment_pin1, segment_pin2, segment_pin3, segment_pin4, segment_pin5, segment_pin6, segment_pin7, segment_pin8,
                 digit_pin1, digit_pin2, digit_pin3, digit_pin4):
        self.id=id
        GPIO.setmode(GPIO.BCM)
 
        # GPIO ports for the 7seg pins
        self.segments =  (segment_pin1, segment_pin2, segment_pin3, segment_pin4, segment_pin5, segment_pin6, segment_pin7, segment_pin8)
        # self.segments =  (11,4,23,8,7,10,18,25)
        # 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
        
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
        
        # GPIO ports for the digit 0-3 pins
        self.digits = (digit_pin1, digit_pin2, digit_pin3, digit_pin4) 
        # self.digits = (22,27,17,24)
        # 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
        
        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    def display_time(self, s_time):
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(self.segments[loop], num[s_time[digit]][loop])
                if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)


    def cleanup(self):
        GPIO.cleanup()
    
    


def display_time_on_segment_display(display, delay, callback, stop_event):
    
    while not stop_event.is_set():
        n = time.ctime()[11:13]+time.ctime()[14:16]
        s = str(n).rjust(4)

        display.display_time(s)

        callback(s[0], s[1], s[2], s[3], display.id)
        time.sleep(delay)
