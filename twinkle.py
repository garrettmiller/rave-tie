# The MIT License (MIT)
#
# Copyright (c) 2019 Gary Fong
#
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

from random import randint, choice
from board import A1, A6
from time import monotonic
import tap

class Twinkle:
    """ Represents randomly lit pixels """

    def __init__(self, pixels):
        """
        Args:
            pixels (NeoPixel): NeoPixel object
        """
        self.pixels = pixels

    def begin(self):
        print("twinkle: begin")

        self.pixel_states = []

        self.twinkle_durations = [
            [(1000, 2000), # min, max twinkle duration
             (200, 1000)], # min, max next twinkle duration
            [(100, 1000),
             (50, 500)]
        ]

        self.twinkle_colors = [
            [(255, 0, 0)], # red
            [(128, 0, 128)], # purple
            [(0, 255, 0)], # green
            [(0, 0, 255)], # blue
            [(255, 215, 0)], # gold
            [(255, 0, 0), # All colors
             (128, 0, 128),
             (0, 255, 0),
             (0, 0, 255),
             (255, 215, 0)]]

        self.tap_effects = {
            id(A1): (A1, self._change_color),
            id(A6): (A6, self._change_delays)}

        # Create tap object
        # TODO may need to clean this up post animation
        self.tap = tap.Tap(
            [v[0] for k, v in self.tap_effects.items()],
            self._tap_event_callback)

        self.pixels.fill(0)
        self.pixels.show()
        self.active_colors = 0
        self.active_twinkle_durations = 0

        # Each pixel has a current state represented by a tuple
        #   (pixel_index, twinkle_start_time, twinkle_duration)
        # If the start time is 0, then it is off.
        self.pixel_states = [(i, 0, 0) for i in range(0, len(self.pixels))]

        # Start time of last pixel twinkled
        self.last_active_twinkle_time = 0

        # How to to wait before twinkling the next pixel
        self.active_next_twinkle_duration \
            = self._get_next_twinkle_duration()

    def update(self):

        # Read any taps
        self.tap.read();

        now = int(round(monotonic() * 1000))

        # Determine which pixels to turn off
        turn_off = self._determine_which_pixels_to_turn_off(now)
        self._turn_off(turn_off)

        # Determine if enough time has gone by before twinking another pixel
        if (now - self.last_active_twinkle_time) \
           < self.active_next_twinkle_duration:
            return

        self._twinkle_a_pixel(now)

        # Record when one was twinkled and change the wait for when the next
        # one can twinkle
        self.last_active_twinkle_time = now
        self.active_next_twinkle_duration \
            = self._get_next_twinkle_duration()
        
    def end(self):
        print("twinkle: end")
        self.pixel_states = []
        self.twinkle_durations = None
        self.twinkle_colors = None
        self.tap_effects = None
        

    def _tap_event_callback(self, pin):
        """
        Depending on the pin tapped, invoke the associated action function
        """

        #print("tapped")
        self.tap_effects[id(pin)][1]()

    def _change_color(self):
        """ Change active color """
        self.active_colors \
            = (self.active_colors + 1) % len(self.twinkle_colors)
        print("active colors: " + str(self.active_colors))
        # Change any existing twinkles to the new set of colors
        for ps in self.pixel_states:
            if ps[1] > 0:
                self.pixels[ps[0]] = self._get_twinkle_color()

    def _change_delays(self):
        """ Change active delays """
        self.active_twinkle_durations \
            = (self.active_twinkle_durations + 1) % len(self.twinkle_durations)
        print("active durations: " + str(self.active_twinkle_durations))

    def _determine_which_pixels_to_turn_off(self, now):
        return list(filter(
            lambda ps: ps[1] > 0 and (now - ps[1]) > ps[2], self.pixel_states))

    def _turn_off(self, turn_off):
        if len(turn_off) > 0:
            for ps in turn_off:
                self.pixels[ps[0]] = (0, 0, 0)
                self.pixel_states[ps[0]] = (ps[0], 0, 0)
            self.pixels.show()

    def _twinkle_a_pixel(self, now):
        pixel = self._get_pixel_to_turn_on()
        if pixel == -1:
            return
        self.pixel_states[pixel] \
            = (pixel, now, self._get_twinkle_duration())
        self.pixels[pixel] = self._get_twinkle_color()
        self.pixels.show()

    def _get_next_twinkle_duration(self):
        return randint(
            self.twinkle_durations[self.active_twinkle_durations][1][0],
            self.twinkle_durations[self.active_twinkle_durations][1][1])

    def _get_twinkle_duration(self):
        return randint(
            self.twinkle_durations[self.active_twinkle_durations][0][0],
            self.twinkle_durations[self.active_twinkle_durations][0][1])
    
    def _get_pixel_to_turn_on(self):
        """ Return an available pixel to turn on """

        off_pixel_states = list(filter(
            lambda ps: ps[1] == 0, self.pixel_states))
        if len(off_pixel_states) == 0:
            return -1
        else:
            return choice(off_pixel_states)[0]

    def _get_twinkle_color(self):
        return choice(self.twinkle_colors[self.active_colors])
