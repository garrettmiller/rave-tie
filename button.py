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

from digitalio import DigitalInOut, Direction, Pull

class Button:
    """ Represents a button. Designed to fire events based on the various
    state of the button press
    """

    def __init__(self, pin, release_event_callback):
        """
        Args
            pin (Board.Pin): The board pin to listen for press activity.
            release_event_callback (def): Callback function to be called upon
            the release of a button press.
        """
        
        self.release_event_callback = release_event_callback
        self.button = DigitalInOut(pin)
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.DOWN
        self.button_pressed_down = False

    def deinit(self):
        self.button.deinit()
        self.button = None

    def read(self):
        """
        Reads the pin to determine if the button was pressed. Must be called in
        the main processing loop.
        """

        # Record that the button is being pressed down.
        if self.button.value:
            self.button_pressed_down = True
            return

        # For a button which was pressed but is no longer being pressed, invoke
        # the release callback.
        if self.button_pressed_down:
            self.button_pressed_down = False
            if self.release_event_callback:
                self.release_event_callback()
