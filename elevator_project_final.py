# —-----------------------------------------------------
# Comp 9 Term 3 Project - Raspberry Pi controlled Lego Elevator
# By Evan Prael, June 1, 2023
#
# This program runs on a Raspberry Pi and controls a motor, LCD screen, 
# and more to drive an elevator up and down a 3 floor building.  
#
#  Links:
#
#  - A video of the running code and hardware
#      https://youtu.be/kJOom7PcedM
#
#  - This code on Github
#      https://github.com/eprael/LegoElevator/blob/main/elevator_project_final.py
#
#  - GPIO reference and tutorials
#       https://gpiozero.readthedocs.io/en/stable/recipes.html
#       https://projects.raspberrypi.org/en/projects/physical-computing/0
#
#
#  - Google Code Blocks for coloring source code in Google Docs
#       https://workspace.google.com/marketplace/app/code_blocks/100740430168
#
# —-----------------------------------------------------

# IMPORT LIBRARIES
# =======================================================

# modules for system access, file access, time delay, etc
import os, sys, time

# module for GPIO pins
import RPi.GPIO as GPIO

#module for keypad
from pad4pi import rpi_gpio

# module for audio
from pygame import mixer

# module for LCD display
import lcd_module

# module for keyboard
from pynput import keyboard

# module for file system
from pathlib import Path


# VARIABLES & PINS
# =======================================================

# full path to sounds folder
APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
SOUND_PATH = os.path.join(APP_FOLDER, "sounds")

# keypad map
KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

# GPIO Pins for keypad
ROW_PINS = [16, 20, 21, 18] # BCM numbering
COL_PINS = [23, 24, 25, 12] # BCM numbering

# GPIO pins for motor 
motor_en = 17
motor_in1 = 27
motor_in2 = 22

# GPIO pins for floor buttons
button_floor1 = 13
button_floor2 = 19
button_floor3 = 26

# motor direction
motion_stop = 0
motion_forward = 1
motion_backward  = 2

# sound playback
wait = True
dont_wait = False

# general
ignore_all_input = False    
elevator_initialized = False
building_name = "Evan Tower"


# functions
# ================================================================

def play_sound(soundFile, waitTillDone):

    soundFile_path = os.path.join(SOUND_PATH, soundFile)
    
    if Path(soundFile_path).is_file():
        print (f"Playing {soundFile}...")
        sound = mixer.Sound(soundFile_path)
        sound.play()

        if waitTillDone:
            # sleep until sound has finished playing
            while mixer.get_busy():
                time.sleep (0.1)
            
    else:
        print (f"Playing {soundFile}... (not found)")


def show_display (message, line):
    if display == None:
        return
    display.lcd_display_string(message, line) 


def control_motor (motion):
    
    if motion == motion_forward:
        print("motor forward")
        GPIO.output(motor_in1,GPIO.LOW)
        GPIO.output(motor_in2,GPIO.HIGH)
        
    elif motion == motion_backward:
        print("motor backward")
        GPIO.output(motor_in1,GPIO.HIGH)
        GPIO.output(motor_in2,GPIO.LOW)
        
    elif motion == motion_stop:
        print("motor stop")
        GPIO.output(motor_in1,GPIO.LOW)
        GPIO.output(motor_in2,GPIO.LOW)


def keyboard_pressed(key):
    
    if ignore_all_input == True:
        return
    
    if key == keyboard.Key.up:
        print ("up-arrow pressed")
        control_motor (motion_forward)

    elif key == keyboard.Key.down:
        print ("down-arrow pressed")
        control_motor (motion_backward)


def keyboard_released(key):

    global elevator_initialized, current_floor
    
    if ignore_all_input == True:
        return

    if key == keyboard.Key.enter:
        print ("Elevator reset. Press buttons to select floor")
        elevator_initialized = True
        current_floor = 1
    
    if key == keyboard.Key.up:
        print ("up-arrow released")
        control_motor (motion_stop)

    if key == keyboard.Key.down:
        print ("down-arrow released")
        control_motor (motion_stop)

    if key == keyboard.Key.esc:
        # motion_stop listener
        return False


def move_to_floor (goto_floor):
    global current_floor
    global ignore_all_input
    
    if goto_floor == current_floor:
        print (f"already on floor {current_floor}")
        return

    # ignore all input while elevator is moving
    ignore_all_input = True
        
    play_sound ("doors_closing_alert.wav",wait)
    play_sound ("doors_closing.wav",wait)

    if goto_floor > current_floor:
        play_sound ("going_up.wav", wait)
    else:
        play_sound ("going_down.wav", wait)

    play_sound ("elevator_moving.wav", dont_wait)
        
    while current_floor != goto_floor:
    
        # check if going up or down
        if goto_floor > current_floor:
            control_motor (motion_forward)
            # sleep until motor travels one full floor
            # depends on motor speed got sleep length from trying different numbers
            if current_floor == 1:
                time.sleep (3.7)  
            elif current_floor == 2:
                time.sleep (3.55)  
            current_floor = current_floor + 1
        else:
            control_motor (motion_backward)
            if current_floor == 3:
                time.sleep (3.4)  
            elif current_floor == 2:
                time.sleep (3.5)  
            current_floor = current_floor - 1
        
        show_display (f"Floor {current_floor}", 2)
            
    # destination reached
    control_motor (motion_stop)
    play_sound ("bell.wav", wait) 
    play_sound (f"floor_{current_floor}.wav", wait) 
    
    ignore_all_input = False


def floor1_button_pressed(channel):
    
    print("Button pressed: 1")

    if ignore_all_input or not elevator_initialized:
        return
    
    move_to_floor (1)
    

def floor2_button_pressed(channel):
    print("Button pressed: 2")
    
    if ignore_all_input or not elevator_initialized:
        return
    
    move_to_floor (2)
    
    
def floor3_button_pressed(channel):
    print("Button pressed: 3")
    
    if ignore_all_input or not elevator_initialized:
        return

    move_to_floor (3)


def keypad_pressed(key):

    print (f"keypad pressed: {key}")
    if ignore_all_input or not elevator_initialized:
        print ("ignoring input")
        return
    
    keyPressed = f"{key}"
    
    if keyPressed == "A": 
        play_sound ("closing_door.wav",wait)

    if keyPressed == "B": 
        play_sound ("opening_door.wav",wait)

    if keyPressed == "1": 
        print ("moving to floor 1")
        move_to_floor (1)

    if keyPressed == "2": 
        move_to_floor (2)

    if keyPressed == "3": 
        move_to_floor (3)
 
 
def clear_screen():
    print ("\033[2J\033[0;0f", end="")

# ----------------- MAIN CODE -------------------

try:
    
    # INITIALIZE DEVICES
    # --------------------------------------------------

    # screen
    # --------------------------------------------------
    os.system("")

    # sound
    # --------------------------------------------------
    mixer.init()

    # lcd display
    # --------------------------------------------------
    try:
        display = lcd_module.Lcd()
        show_display (building_name, 1)
    except:
        print("error using display!")

    # keypad 
    # --------------------------------------------------
    keypad = rpi_gpio.KeypadFactory().create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS) 
    keypad.registerKeyPressHandler(keypad_pressed)

    # motor
    # --------------------------------------------------
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_in1,GPIO.OUT)
    GPIO.setup(motor_in2,GPIO.OUT)
    GPIO.setup(motor_en,GPIO.OUT)
    GPIO.output(motor_in1,GPIO.LOW)
    GPIO.output(motor_in2,GPIO.LOW)

    # PWM = Pulse Width Modulation
    p=GPIO.PWM(motor_en,1000)
    p.start(25)
    # set motor speed to 85%
    p.ChangeDutyCycle(85)
    
    # outside buttons
    # --------------------------------------------------
    # setup pins and tell it what function to call when pressed

    GPIO.setup(button_floor1, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(button_floor1,GPIO.RISING,callback=floor1_button_pressed,bouncetime = 250) 

    GPIO.setup(button_floor2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(button_floor2,GPIO.RISING,callback=floor2_button_pressed, bouncetime = 250) # Setup event on pin 10 rising edge

    GPIO.setup(button_floor3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(button_floor3,GPIO.RISING,callback=floor3_button_pressed, bouncetime = 250) # Setup event on pin 10 rising edge

    clear_screen()
    print(f"""
          Welcome to {building_name}!
          
          Please use the down arrow key to bring the elevator to the ground floor. 
          
          Once on the ground floor, press enter to continue.""")
    
    # setup keyboard to wait for key presses.  It calls the keyboard_pressed function 
    # when a key is pressed and the keyboard_released function when a key is released
    
    with keyboard.Listener(
        on_press  = keyboard_pressed,
        on_release= keyboard_released,
        suppress  =True) as listener:
            listener.join()
        
except KeyboardInterrupt:
     # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_display_string("Goodbye", 1)  # Write line of text to first line of display
    time.sleep(3)

finally:
    # make sure motor stops just in case
    control_motor (motion_stop)
    GPIO.cleanup()
    keypad.cleanup()
    if display != None:
        display.lcd_clear()
