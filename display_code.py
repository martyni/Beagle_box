# -*- coding: utf-8 -*-
import math
import time
import Adafruit_CharLCD as Disp
import Adafruit_BBIO.PWM as PWM

# Configure the BeagleBone Black as follows:
disp_rs = 'P8_8'
disp_en = 'P8_10'
disp_d4 = 'P8_18'
disp_d5 = 'P8_16'
disp_d6 = 'P8_14'
disp_d7 = 'P8_12'
disp_illuminate = 'P8_7'
disp_pwm = 'P9_14'
PWM.start(disp_pwm, 0)
# No. of columns and rows of LCD. Following means that the LCD is an 16 X 2
DISP_COLS = 16
DISP_ROWS = 2
CHAT_FILE = 'chat_file'
CURSOR_POSITION = False
# Initialization of the LCD
LCD = Disp.Adafruit_CharLCD(disp_rs, disp_en, disp_d4, disp_d5, disp_d6, disp_d7,
        DISP_COLS, DISP_ROWS, disp_illuminate)
LCD.autoscroll(False)
#Display Hello World message
def read_file(filename):
    with open(filename) as open_file:
        return open_file.readlines()

def write_pwm(level, pwm_pin=disp_pwm):
    PWM.set_duty_cycle(pwm_pin, level)


def start_of_next_line():
    pass

def display_lines(lines, cursor=True):
    LCD.clear()
    line_length = DISP_COLS * DISP_ROWS
    for line in lines:
        if len(line) > line_length:
            for i in range(0,len(line), line_length):
                if cursor  == True:
                    LCD.clear()
                    end_character='\n'
                print_line = line[i:i + line_length] + end_character
                print(print_line)
                LCD.message(print_line)
                cursor = not cursor
                end_character=''
                #time.sleep(1)

        else:
            LCD.message(line)
            '''print(line)'''
            cursor != cursor

def main(chat):
    old_cache = False
    while True:
        with open(chat) as chat_file:
            cache = chat_file.readlines()
            if cache != old_cache:
                display_lines(cache)
        old_cache = cache
        #time.sleep(1)
            

if __name__ == "__main__":
    main(CHAT_FILE)
    LCD.clear()

# If you need you can print two line message LCD.message('Hello\nworld!')

# Wait 5 seconds
#time.sleep(4)

# Clear the LCD screen.
