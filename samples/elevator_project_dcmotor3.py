from gpiozero import Motor
from time import sleep

motor = Motor(forward=4, backward=14)

motor.stop()

while True:
    motor.forward(0.6)
    sleep(0.05)
    motor.forward(0.3)
    sleep(5)
    motor.backward(0.6)
    sleep(0.05)
    motor.backward(0.3)
    sleep(5)
    motor.stop()
    break
