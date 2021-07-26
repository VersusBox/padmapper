#!/usr/bin/python3

import sys
import json

from Keyboard import Keyboard
from Mouse import Mouse
from Padmapper import Padmapper

if len(sys.argv) != 2:
    print("Usage: %s <config.json>" % sys.argv[0])
    sys.exit(1)

keyboard = Keyboard()
mouse = Mouse()
mouse.hide()

config_file = open(sys.argv[1], "r")
config = json.load(config_file)
config_file.close()

padmapper = Padmapper(keyboard, mouse, config)
padmapper.handle_events()

print("Terminating padmapper")
del padmapper
del keyboard
del mouse
