from time import sleep
from threading import Thread, Timer, Lock
from pynput.mouse import Button, Controller
from Xlib.display import Display
import weakref

MOUSE_MOVE_STEP_DEFAULT = 10
MOUSE_HIDE_DELAY_DEFAULT = -1
MOUSE_SWIPE_DIST_DEFAULT = 400

def _move_task(weak_self):
    self = weak_self()
    while not self.end:
        sleep(.01)
        if self.move_step_x == 0 and self.move_step_y == 0:
            if self.mouse_moving and self.mouse_hide_delay >= 0:
                self.hide_deferred((self.mouse_hide_delay))
            self.mouse_moving = False
            continue
        self.mouse_moving = True
        self.move(self.move_step_x, self.move_step_y)

class Mouse:
    hide_timer = None
    cursor_visible = True
    hide_lock = Lock()
    move_step_x = 0
    move_step_y = 0
    mouse_moving = False
    mouse_thread = None
    end = False
    screen = None
    display = None
    mouse = Controller()

    def __init__(self, config=None):
        if config.get('params') is not None:
            if config['params'].get('mouse_move_step') is not None:
                self.mouse_move_step = config['params']['mouse_move_step']
            else:
                self.mouse_move_step = MOUSE_MOVE_STEP_DEFAULT
            if config['params'].get('mouse_hide_delay') is not None:
                self.mouse_hide_delay = config['params']['mouse_hide_delay']
            else:
                self.mouse_hide_delay = MOUSE_HIDE_DELAY_DEFAULT
            if config['params'].get('mouse_swipe_dist') is not None:
                self.mouse_swipe_dist = config['params']['mouse_swipe_dist']
            else:
                self.mouse_swipe_dist = MOUSE_SWIPE_DIST_DEFAULT

        self.mouse_thread = Thread(target=_move_task,
                args=(weakref.ref(self),), daemon=True)
        self.mouse_thread.start()
        self.display = Display()
        xfixes_version = self.display.xfixes_query_version()
        print("XFIXES version %d.%d" % (xfixes_version.major_version, xfixes_version.minor_version))
        self.screen = self.display.screen()
        if self.mouse_hide_delay >= 0:
            self.hide()

    def __del__(self):
        self.end = True
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
        if self.mouse_hide_delay >= 0:
            self.hide()
        dist = self.mouse_swipe_dist
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

    def actions(self, actions, release=False):
        for action in actions:
            if not release:
                if action == 'click':
                    self.mouse.click(Button.left, 1)
                elif action == 'left':
                    self.move_step_x = -self.mouse_move_step
                elif action == 'right':
                    self.move_step_x = self.mouse_move_step
                elif action == 'up':
                    self.move_step_y = -self.mouse_move_step
                elif action == 'down':
                    self.move_step_y = self.mouse_move_step
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
