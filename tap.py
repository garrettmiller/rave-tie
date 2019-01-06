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

from touchio import TouchIn

class Tap:
    """ Represents a tap, which is a touch followed by a lift off the pad """

    def __init__(self, pins, tap_event_callback):
        """
        Args:
           pins (list): List of board pins to monitor for taps
           tap_event_callback (def): Callback function to be called upon a
           tap. The function must be able to receive the board pin associated
           with the tap.
        """

        self.tap_event_callback = tap_event_callback
        self.pads = [(id(pin), pin, TouchIn(pin)) for pin in pins]
        self.activeTaps = {} # key=pinId, value=[pin, counter]

    def deinit(self):
        for pad in self.pads:
            pad[2].deinit()
        self.pads = None

    def read(self):
        """ Reads the pins to determine if any of the pads were touched. Must
            be called in the main processing loop.
        """

        anythingTapped = False

        # Loop through the pads to find any touches
        for pinId, pin, touchIn in self.pads:

            # If something was touched, start recording how many
            # times a pad has been continually being touched.
            # We'll want the one pad that has the greatest value.
            if touchIn.value:
                #print("touched")
                anythingTapped = True

                # Add the pin, counter if the pin doesn't yet exist
                if pinId not in self.activeTaps:
                    self.activeTaps[pinId] = [pin, 0]

                # Increment the counter
                self.activeTaps[pinId][1] += 1

        # If nothing was touched, check if something had been
        # touched. If so, then return the pin of the pad that
        # had the greatest amount of touches.
        if not anythingTapped:
            if len(self.activeTaps) > 0:
                candidateTap = None # [pin, counter]
                for pinId, pinAndCounter in self.activeTaps.items():
                    if candidateTap is None:
                        candidateTap = pinAndCounter
                    elif candidateTap[1] < pinAndCounter[1]:
                        candidateTap = pinAndCounter

                # Reset active taps to nothing
                self.activeTaps = {}

                # Notify the listener that a tap has occurred
                #print("tapped")
                self.tap_event_callback(candidateTap[0])
