from time import sleep
from threading import Thread, Timer, Lock
from pynput.mouse import Button, Controller
from Xlib.display import Display

MOUSE_MOVE_STEP = 10
MOUSE_HIDE_DELAY = 3

class Mouse:
    hide_timer = None
    cursor_visible = True
    hide_lock = Lock()
    move_step_x = 0
    move_step_y = 0
    mouse_thread = None
    screen = None
    display = None
    mouse = Controller()

    def __init__(self):
        self.mouse_thread = Thread(target=self.move_task)
        self.mouse_thread.start()
        self.display = Display()
        xfixes_version = self.display.xfixes_query_version()
        print("XFIXES version %d.%d" % (xfixes_version.major_version, xfixes_version.minor_version))
        self.screen = self.display.screen()

    def __del__(self):
        self.mouse_thread.join()

    def hide(self):
        self.hide_lock.acquire()
        if self.cursor_visible:
            self.screen.root.xfixes_hide_cursor()
            self.display.sync()
            self.cursor_visible = False
        self.hide_lock.release()

    def hide_deferred(self, delay):
        self.hide_lock.acquire()
        if self.hide_timer is not None:
            self.hide_timer.cancel()
        self.hide_timer = Timer(delay, self.hide)
        self.hide_timer.start()
        self.hide_lock.release()

    def show(self):
        self.hide_lock.acquire()
        if self.hide_timer is not None:
            self.hide_timer.cancel()
        if not self.cursor_visible:
            self.screen.root.xfixes_show_cursor()
            self.display.sync()
            self.cursor_visible = True
        self.hide_lock.release()

    def swipe(self, step_x, step_y):
        dist = 400
        x = dist
        y = dist
        self.mouse.position = (x, y)
        self.mouse.press(Button.left)
        for i in range(0, dist):
            self.mouse.position = (x + i * step_x, y + i * step_y)
        self.mouse.release(Button.left)

    def move(self, step_x, step_y):
        self.show()
        self.mouse.move(step_x, step_y)
        self.hide_deferred((MOUSE_HIDE_DELAY))

    def move_task(self):
        while True:
            sleep(.01)
            if self.move_step_x == 0 and self.move_step_y == 0:
                continue
            self.move(self.move_step_x, self.move_step_y)

    def actions(self, actions, release=False):
        for action in actions:
            if not release:
                if action == 'click':
                    self.mouse.click(Button.left, 1)
                elif action == 'left':
                    self.move_step_x = -MOUSE_MOVE_STEP
                elif action == 'right':
                    self.move_step_x = MOUSE_MOVE_STEP
                elif action == 'up':
                    self.move_step_y = -MOUSE_MOVE_STEP
                elif action == 'down':
                    self.move_step_y = MOUSE_MOVE_STEP
                if action == 'swipe_left':
                    self.swipe(-1, 0)
                elif action == 'swipe_right':
                    self.swipe(1, 0)
                elif action == 'swipe_up':
                    self.swipe(0, -1)
                elif action == 'swipe_down':
                    self.swipe(0, 1)
                elif action == 'swipe_left_up':
                    self.swipe(-1, -1)
                elif action == 'swipe_left_down':
                    self.swipe(-1, 1)
                elif action == 'swipe_right_up':
                    self.swipe(1, -1)
                elif action == 'swipe_right_down':
                    self.swipe(1, 1)
                elif action == 'hide':
                    self.hide()
            else:
                if action == 'left' or action == 'right':
                    self.move_step_x = 0
                elif action == 'up' or action == 'down':
                    self.move_step_y = 0
