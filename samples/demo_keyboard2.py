from pynput import keyboard
from time import sleep

def key_pressed(key):
    try:
        print('key {0} pressed'.format(key.char))
    except AttributeError:
        print('key {0} pressed'.format(key))

def key_released(key):
    try:
        print('key {0} released'.format(key.char))
    except AttributeError:
        print('key {0} released'.format(key))

    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=key_pressed,on_release=key_released,suppress=True) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=key_pressed,on_release=key_released,suppress=True)
listener.start()

while 1:
    sleep (0.1)
    