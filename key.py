from pynput import keyboard


lastKey = ""

def on_press(key):
    try:
        global lastKey
        if key.char != lastKey:
            print('alphanumeric key {0} pressed'.format(
                key.char))
            lastKey = key.char
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global lastKey
    if key.char == lastKey:
        lastKey = ""
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
