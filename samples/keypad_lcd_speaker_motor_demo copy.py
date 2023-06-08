#!/usr/bin/python
import RPi.GPIO as GPIO

from pad4pi import rpi_gpio

from pygame import mixer
import os, sys

import lcd_module
from time import sleep

from pynput import keyboard


# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcd_module.Lcd()


APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

sound_path = os.path.join(APP_FOLDER, "sounds")

in1 = 19
in2 = 13
en = 26

floor = 1

KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

ROW_PINS = [17, 27, 22, 5] # BCM numbering
COL_PINS = [23, 24, 25, 16] # BCM numbering


# setup motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)



def key_pressed(key):
    try:
        #print('key {0} pressed'.format(key.char))
        newKey = key.char
        process_key(newKey)
        
    except AttributeError:
        # print('key {0} pressed'.format(key))

        if key == keyboard.Key.up:
            print("forward")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)

        elif key == keyboard.Key.down:
            print("backward")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)

def key_released(key):
    #try:
        # print('key {0} released'.format(key.char))
    #except AttributeError:
        # print('key {0} released'.format(key))

    if key == keyboard.Key.up or key == keyboard.Key.down:
        print("motor stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

    if key == keyboard.Key.esc:
        # Stop listener
        return False


def print_key(key):
    process_key(key)
        
        
def process_key(key):
    global floor
    display.lcd_display_string(f"Key: {key}", 1)  # Write line of text to first line of display
    print (f"key pressed - {key}")
    if key == "A":
        print ("playing sound bell1-stop.wav")
        sound_bell  = mixer.Sound(sound_path + '/bell1-stop.wav')
        sound_bell.play()
    if key == "B":
        sound_bell  = mixer.Sound(sound_path + '/Down2.wav')
        sound_bell.play()
    if key == "C":
        sound_bell  = mixer.Sound(sound_path + '/MitsubishiModernChimeDown.wav')
        sound_bell.play()
    if key == "D":
        print ("playing sound bell1.wav")
        sound_bell  = mixer.Sound(sound_path + '/bell1.wav')
        sound_bell.play()
    if key == "#":
        sound_bell  = mixer.Sound(sound_path + '/Telephone Ring2.wav')
        sound_bell.play()

    if key == "r":
        print("run")
        sound_goingdown.play()
        
        while (mixer.get_busy()):
            sleep (0.1)
        
        sound_closedoor.play()
        
        while (mixer.get_busy()):
            sleep (0.1)
        
        if (floor == 1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            print("forward")
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("backward")
            
    elif key == "s":
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)

    elif key == "f":
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        floor = 2

    elif key == "l":
        print("low")
        p.ChangeDutyCycle(25)

    elif key == "m":
        print("medium")
        p.ChangeDutyCycle(50)

    elif key == "h":
        print("high")
        p.ChangeDutyCycle(75)

    elif key == "v":
        print("max")
        p.ChangeDutyCycle(95)

    elif key == "e":
        rpi_gpio.cleanup()


try:
    
    
    mixer.init()
    
#    display2 = pygame.display.set_mode((300, 300))
    
    sound_goingdown = mixer.Sound(sound_path + '/Down2.wav')
    sound_closedoor = mixer.Sound(sound_path + '/impulseclose1.wav')
    
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS) # makes assumptions about keypad layout and rpi_gpio pin numbers

    keypad.registerKeyPressHandler(print_key)

    print("Press buttons on your keypad. Press up/down arrow keys to adjust motor. Ctrl+C to exit.")
    
    # Collect events until released
    with keyboard.Listener(on_press=key_pressed,on_release=key_released,suppress=True) as listener:
        listener.join()
        
except KeyboardInterrupt:
     # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_display_string("Goodbye", 1)  # Write line of text to first line of display
    sleep(3)
finally:
    keypad.cleanup()
    display.lcd_clear()
