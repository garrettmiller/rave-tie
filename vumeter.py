# The MIT License (MIT)
#
# Copyright (c) 2017 Dan Halbert for Adafruit Industries
# Copyright (c) 2017 Kattni Rembor, Tony DiCola for Adafruit Industries
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

# Modified work:
# Copyright (c) 2019 Gary Fong

from array import array
from math import pow, sqrt
from micropython import const

from audiobusio import PDMIn
from board import MICROPHONE_CLOCK, MICROPHONE_DATA

class VuMeter:

    def __init__(self, pixels, input_floor, input_ceiling):
        self.curve = const(2)
        self.scale_exponent = pow(10, self.curve * -0.1)
        self.peak_color = (100, 0, 255)
        self.num_samples = const(160)
        self.pixels = pixels
        self.num_pixels = len(pixels)
        self.input_floor = input_floor
        # Corresponds to sensitivity: lower means more pixels light up with
        # lower sound. Adjust this as you see fit.
        self.input_ceiling = input_floor + input_ceiling

        self.peak = 0

    # Restrict value to be between floor and ceiling.
    def _constrain(self, value, floor, ceiling):
        return max(floor, min(value, ceiling))

    # Scale input_value between output_min and output_max, exponentially.
    def _log_scale(self,
                    input_value, input_min, input_max,
                    output_min, output_max):

        normalized_input_value \
            = (input_value - input_min) / (input_max - input_min)
        return output_min \
            + pow(normalized_input_value, self.scale_exponent) \
            * (output_max - output_min)

    # Remove DC bias before computing RMS.
    def _normalized_rms(self, values):
        minbuf = int(self._mean(values))
        samples_sum = sum(
            float(sample - minbuf) * (sample - minbuf)
            for sample in values
        )
        return sqrt(samples_sum / len(values))

    def _mean(self, values):
        return sum(values) / len(values)

    def _volume_color(self, volume):
        return 200, volume * (255 // self.num_pixels), 0

    def begin(self):
        print("vu meter: begin")

        self.samples = array('H', [0] * self.num_pixels)
        self.mic \
            = PDMIn(MICROPHONE_CLOCK,
                    MICROPHONE_DATA,
                    sample_rate=16000, bit_depth=16)
        
        self.pixels.fill(0)
        self.pixels.show()

    def update(self):
        self.mic.record(self.samples, len(self.samples))
        magnitude = self._normalized_rms(self.samples)
        #print(magnitude)
        
        # Compute scaled logarithmic reading in the range 0 to NUM_PIXELS
        c = self._log_scale(
            self._constrain(magnitude, self.input_floor, self.input_ceiling),
            self.input_floor, self.input_ceiling, 0, self.num_pixels)
        
        # Light up pixels that are below the scaled and interpolated magnitude.
        self.pixels.fill(0)
        for i in range(self.num_pixels):
            if i < c:
                self.pixels[i] = self._volume_color(i)
                # Light up the peak pixel and animate it slowly dropping.
                if c >= self.peak:
                    self.peak = min(c, self.num_pixels - 1)
                elif self.peak > 0:
                    self.peak = self.peak - 1
                    if self.peak > 0:
                        self.pixels[int(self.peak)] = self.peak_color
                        self.pixels.show()

    def end(self):
        print("vu meter: end")
        self.samples = None
        self.mic.deinit()
        self.mic = None
