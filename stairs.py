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

from board import A1, A6
from time import monotonic
import tap

class Stairs:
    """ Represents 3 LEDs climbing up and down the stairs displaying various
    colors and moving at various speeds. Tapping A1 varies the colors. Tapping
    A6 varies the speeds.
    """

    def __init__(self, pixels):
        """
        Args:
            pixels (NeoPixel): NeoPixel object
        """

        self.pixels = pixels

    def begin(self):
        #print("stairs: begin")

        # List of varying colors
        # Each: saturated color, lighter variant
        self.colors = [
            ((255, 0, 0), (25, 0, 0)), # red
            ((128, 0, 128), (12, 0, 12)), # purple
            ((0, 255, 0), (0, 20, 0)), # green
            ((0, 0, 255), (0, 0, 25)), # blue
            ((255, 215, 0), (25, 21, 0))] # gold

        # List of varying delays
        # Each: step delay, turn delay
        self.delays = [
            (1, 10),
            (150, 500),
            (300, 1000)]
        
        self.pixels.fill(0)
        self.pixels.show()
        self.currPos = 1
        self.step = 1
        self.then = 0
        self.active_colors = 0
        self.active_delays = 0
        self.active_delay = self.delays[self.active_delays][0]

        # key: pinId, value: tuple: (pin, method)
        self.tap_effects = {
            id(A1): (A1, self.__change_color),
            id(A6): (A6, self.__change_delays)}

        # Create tap object
        # TODO may need to clean this up post animation
        self.tap = tap.Tap(
            [v[0] for k, v in self.tap_effects.items()],
            self.__tap_event_callback)

    def __change_color(self):
        """ Change to the next color """
        self.active_colors = (self.active_colors + 1) % len(self.colors)
        #print("active colors: " + str(self.active_colors))

    def __change_delays(self):
        """ Change to the next delay """
        self.active_delays = (self.active_delays + 1) % len(self.delays)
        #print("active delays: " + str(self.active_delays))

    def __tap_event_callback(self, pin):
        """ Depending on the pin tapped, invoke the associated action
        function
        """
        self.tap_effects[id(pin)][1]()

    def update(self):

        # Read any taps
        self.tap.read();

        # This is how the speed is controlled. Wait to show the step until the
        # desired amount of time has passed.
        now = int(round(monotonic() * 1000))
        if now - self.then <= self.active_delay:
            return

        # We'll now show the step
        self.then = now

        # Remove prior step
        self.pixels.fill(0)
        self.pixels.show()

        # There are 3 LEDs that are stepping in unison:
        #   <lighter> <saturated> <ligher>
        # The saturated LED goes to the actual end implying only 2 LEDs will be
        # lit at that moment.
        if self.currPos - 1 >= 0:
            self.pixels[self.currPos - 1] = self.colors[self.active_colors][1]
        self.pixels[self.currPos] = self.colors[self.active_colors][0]
        if self.currPos + 1 < len(self.pixels):
            self.pixels[self.currPos + 1] = self.colors[self.active_colors][1]
        self.pixels.show()

        # Prepare for the next step. This is where the speed (or delay will
        # change) in anticipation of stepping to the end or stepping away from
        # the end.
        if self.currPos + self.step < 0:
            self.step = 1
            self.active_delay = self.delays[self.active_delays][1]
        elif self.currPos + self.step == len(self.pixels):
            self.step = -1
            self.active_delay = self.delays[self.active_delays][1]
        else: # Not turning, so change to step delay
            self.active_delay = self.delays[self.active_delays][0]
        
        # Take the step. Won't be shown until next update.
        self.currPos += self.step

    def end(self):
        #print("stairs: end")
        self.colors = None
        self.delays = None
        self.tap_effects = None
        self.tap.deinit()
        self.tap = None
