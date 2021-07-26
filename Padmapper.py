import pygame

class Padmapper:
    keyboard = None
    mouse = None
    config = None
    joysticks = []

    def __init__(self, keyboard, mouse, config):
        self.keyboard = keyboard
        self.mouse = mouse
        self.config = config
        pygame.init()
        for i in range(0, pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            print(joystick.get_name())
            self.joysticks.append(joystick)

    def special_actions(self, actions, end=False):
        if actions['mouse'] != None:
            self.mouse.actions(actions['mouse'], end)

    def start_actions(self, actions):
        print("press {}".format(actions))
        for action in actions:
            if type(action) is dict:
                self.special_actions(action)
            else:
                self.keyboard.press(action)

    def stop_actions(self, actions):
        print("release {}".format(actions))
        for action in actions:
            if type(action) is dict:
                self.special_actions(action, end=True)
            else:
                self.keyboard.release(action)

    def handle_events(self):
        while True:
            try:
                event = pygame.event.wait()
                if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                    joyid = str(event.joy)
                    button = str(event.button)
                    actions = self.config[joyid]['buttons'][button]
                    if event.type == pygame.JOYBUTTONDOWN:
                        print("JOYBUTTONDOWN %d: %d => " % (event.joy, event.button), end='')
                        self.start_actions(actions)
                    elif event.type == pygame.JOYBUTTONUP:
                        print("JOYBUTTONUP %d: %d => " % (event.joy, event.button), end='')
                        self.stop_actions(actions)
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis > 1:
                        continue
                    joyid = str(event.joy)
                    axis = str(event.axis)
                    direction = str(int(event.value))
                    print("JOYAXISMOTION %d: %d %d => " % (event.joy, event.axis, event.value), end='')
                    if direction != '0':
                        actions = self.config[joyid]['joystick'][axis][direction]
                        self.start_actions(actions)
                    else:
                        actions = []
                        for direction in self.config[joyid]['joystick'][axis]:
                            actions = actions + self.config[joyid]['joystick'][axis][direction]
                        self.stop_actions(actions)
            except KeyError:
                pass
