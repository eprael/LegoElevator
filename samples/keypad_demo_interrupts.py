#!/usr/bin/python

from pad4pi import rpi_gpio
import time
import pygame
import os, sys


APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

sound_path = os.path.join(APP_FOLDER, "sounds")


KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

ROW_PINS = [17, 27, 22, 5] # BCM numbering
COL_PINS = [23, 24, 25, 16] # BCM numbering

def print_key(key):
    print(f"Received key from interrupt:: {key}")
    if key == "D":
        sound_bell  = pygame.mixer.Sound(sound_path + '/bell1.wav')
        sound_bell.play()
    if key == "#":
        sound_bell  = pygame.mixer.Sound(sound_path + '/Telephone Ring2.wav')
        sound_bell.play()


try:
    
    
    pygame.init()
    
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS) # makes assumptions about keypad layout and GPIO pin numbers

    keypad.registerKeyPressHandler(print_key)

    print("Press buttons on your keypad. Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye")
finally:
    keypad.cleanup()