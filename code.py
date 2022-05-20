# Rave-Tie Main Python File
# (c) 2022 Garrett Miller
# Heavily based on work that is copyright (c) 2019 Gary Fong
# 
# The MIT License (MIT)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import gc

from neopixel import NeoPixel
from board import D4, A3

from button import Button

import pixelsoff
import vumeter
import stairs
import twinkle

print("gc: " + str(gc.isenabled()))

active_led_animation = 0
def next_led_animation(jump_to_animation = -1):
    global led_animations, active_led_animation

    # End the old animation
    led_animations[active_led_animation].end()

    # Determine the next animation
    if jump_to_animation == -1:
        active_led_animation = (active_led_animation + 1) % len(led_animations)
    else:
        active_led_animation = jump_to_animation
    print("active led animation ", led_animations[active_led_animation])

    # Begin the new animation
    led_animations[active_led_animation].begin()

def button_a_pressed():
    next_led_animation()

#Arguments are data port, number of LEDs, brightness, auto-write
pixels = NeoPixel(A3, 60, brightness=0.5, auto_write=False)

led_animations = [
    pixelsoff.PixelsOff(pixels),
    vumeter.VuMeter(pixels, 100, 400),
    stairs.Stairs(pixels),
    twinkle.Twinkle(pixels)
]

buttonA = Button(D4, button_a_pressed);

pixels.fill(0)
pixels.show()

while True:
    buttonA.read()
    led_animations[active_led_animation].update()
    gc.collect()
