import RPi.GPIO as GPIO          
from time import sleep
import pygame
import os, sys

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))

sound_path = os.path.join(APP_FOLDER, "sounds")

in1 = 19
in2 = 13
en = 26
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-fwd b-back l-low m-medium h-high v-max e-exit")
print("\n")    

pygame.init()
sound_goingdown = pygame.mixer.Sound(sound_path + '/Down2.wav')
sound_closedoor = pygame.mixer.Sound(sound_path + '/impulseclose1.wav')

while(1):

    x=input()
    
    if x=='r':
        print("run")
        sound_goingdown.play()
        
        while (pygame.mixer.get_busy()):
          sleep (0.1)
          
        sound_closedoor.play()
        
        while (pygame.mixer.get_busy()):
          sleep (0.1)
        
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'

    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
     
    elif x=='v':
        print("max")
        p.ChangeDutyCycle(95)
        x='z'
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")