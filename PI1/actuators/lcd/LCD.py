
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime
import random
 
 
class LCD(object):
    def __init__(self, id, pin_rs=0, pin_e=2, pin_db1=4, pin_db2 = 5, pin_db3 = 6, pin_db4 = 7):
        self.id=id
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.

        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=[pin_db1, pin_db2, pin_db3, pin_db4]
    
    def setup_lcd(self):
        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(self.PCF8574A_address)
            except:
                print ('I2C Address Error !')
                # exit(1)
                return 
            
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs = self.pin_rs, pin_e = self.pin_e, pins_db = self.pins_db, GPIO=self.mcp)

    def get_time_now(self): 
        return datetime.now().strftime('    %H:%M:%S')
        
    def display_time(self):
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns
       
        #lcd.clear()
        self.lcd.setCursor(0,0)  # set cursor position
        self.lcd.message( 'Hello boss, current time:\n' )
        self.lcd.message( self.get_time_now() ) 

    def display_pass_message(self):
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns
       
        #lcd.clear()
        self.lcd.setCursor(0,0)  # set cursor position
        self.lcd.message( 'Hello boss, if you have password,\n' )
        self.lcd.message( "you can enter garage" ) 
            
    def destroy(self):
        self.lcd.clear()
    


def run_lcd_loop(lcd, delay, callback, stop_event):
    
    while not stop_event.is_set():
        rnd = random.random()
        if rnd < 0.5:
            lcd.display_time()
            text = "Hello boss, if you have password,\nyou can enter garage" 
            callback(text, lcd.id)
        else:
            lcd.display_pass_message()
            text = 'Hello boss, current time:\n'+ lcd.get_time_now() 
            callback(text, lcd.id)
        sleep(delay)
