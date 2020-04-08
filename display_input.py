import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import sys
from time import sleep
from display_code import CHAT_FILE, write_pwm
ADC.setup()
ANALOG_PIN="P9_33"
TOP_BUT = "P9_11"
BOT_BUT = "P9_13"
GPIO.setup(TOP_BUT, GPIO.IN)
GPIO.setup(BOT_BUT, GPIO.IN)
WAIT = 0.3
MODES = 10

def pwm_level(read_level, **kwargs):
   write_pwm(100 - read_level)


MODE_LIST = [ ("pwm_level", pwm_level)]
def get_percentage():
   #print(ADC.read(ANALOG_PIN))
   return int(100 * ADC.read(ANALOG_PIN))


def get_buttons(top, bottom):
    return (GPIO.input(top), GPIO.input(bottom))
   
def handle_mode(top, bottom, mode, mode_max=MODES):
    def plus1(mode):
        if mode < mode_max:
            return mode + 1
        else:
            return mode

    def minus1(mode):
        if mode > 0:
            return mode - 1
        else:
            return mode

    def same(mode):
        return mode

    modes = {
            (False, False) : same, 
            (True, False)  : plus1,
            (False, True)  : minus1,
            (True, True)   : same
            }
    return modes[(top,bottom)](mode)


def write_to_chat_file(file_input):
    with open(CHAT_FILE,'w') as chat_file:
        if type(file_input) is int:
            chat_file.write("{} %".format(file_input))
        else:
            chat_file.write("{}".format(file_input))


def save_old_value():
    with open(CHAT_FILE) as chat_file:
        return chat_file.read()

def main():
    old_value = 0
    cache = save_old_value()
    mode = 0
    while True:
        read_value = get_percentage()
        top, bottom = get_buttons(TOP_BUT, BOT_BUT)
        mode = handle_mode(top, bottom, mode)
        if read_value != old_value:
            cache = cache if cache else save_old_value()
            print(cache)
            print("is in cache")
            write_to_chat_file(read_value)
            try:
                MODE_LIST[mode][1](
                       read_value, 
                       button=(top,bottom)
                       )
            except Exception as e:   
                #write_to_chat_file("read : " + str(e))
                write_to_chat_file(read_value)

            cooldown = 5
        elif mode != old_mode:
            cache = cache if cache else save_old_value()
            try:
                write_to_chat_file(MODE_LIST[mode][0])
                MODE_LIST[mode][1](
                       read_velue=read_value, 
                       button=(top,bottom)
                       )
            except Exception as e:   
                #write_to_chat_file("mode :" + str(e))
                write_to_chat_file("mode : " + str(mode))

            cooldown = 3
        elif cooldown > 0:
            cooldown -= 1
        elif cache is not None and cooldown == 0:
            print(cache)
            print("written")
            write_to_chat_file(cache)
            cache = None
        old_value = read_value
        old_mode  = mode
        sleep(WAIT)

if __name__ == "__main__":
    main()
