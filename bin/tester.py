#!/usr/bin/env python
import os
import sys
import time

from phuey.hue_bridge import HueBridge
# ------------------------------------------------------------------------------
def test_light(name):
    light = bridge.get_light(name)

    # light.on(False)
    print(light.name())
    print(light.on())
    print(light.color())

    light.color((255,0,0))
    print(light.color())
    time.sleep(1)

    light.color((0,255,0))
    print(light.color())
    time.sleep(1)

    light.color((0,0,255))
    print(light.color())
    time.sleep(1)

    light.reset()

    print(light.on())
    print(light.color())
# ------------------------------------------------------------------------------
host = "http://192.168.1.93"
token = None

try:
    token = sys.argv[1]
    light_name = sys.argv[2]
except Exception as e:
    print(F"Usage: {sys.argv[0]} <TOKEN> <LIGHT_NAME>")
else:
    bridge = HueBridge(host, token)
    test_light(light_name)











#
