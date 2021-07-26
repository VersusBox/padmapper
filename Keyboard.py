from pynput.keyboard import Key, Controller as Controller

class Keyboard:
    keyboard = None

    def __init__(self):
        self.keyboard = Controller()

    def keyname(self, key):
        if len(key) == 1:
            return key
        else:
            return Key[key]

    def press(self, key):
        self.keyboard.press(self.keyname(key))

    def release(self, key):
        self.keyboard.release(self.keyname(key))
