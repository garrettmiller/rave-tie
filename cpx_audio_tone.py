# The MIT License (MIT)
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2017-2018 Kattni Rembor for Adafruit Industries
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

# Modifications
# 2019/01/01 Gary fong
#   Exracted only the ability to play/stop audio tones for circuit playground
#   express.

from audioio import RawSample, AudioOut
from array import array
from math import sin, pi
from board import SPEAKER

TONE_VOLUME = const(32767) # (2 ** 15) - 1
SHIFT = const(32768) # (2 ** 15)

class CpxAudioTone:
    """
    Responsible for actually playing the audio tone on the circuit playground
    express. Mostly all of the code for this class was extract directly from the
    adafruit_circuitplayground.express module. See the link below for reference:
    https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/_modules/adafruit_circuitplayground/express.html
    """

    # TODO: Remove an annoying clicking sound after the tone is played. FWIW, it
    # also exists in Adafruit's implementation.

    def __init__(self):
        self._sample = None
        self._sine_wave = None
        self._sine_wave_sample = None

    def __del__(self):
        self._sine_wave_sample = None
        self._sine_wave = None
        self._teardown()

    def start_tone(self, freq):
        #print("start tone: " + str(freq))
        length = 350000 // freq if 100 * freq > 350000 else 100
        self._generate_sample(length)
        self._sine_wave_sample.sample_rate = int(len(self._sine_wave) * freq)
        if not self._sample.playing:
            self._sample.play(self._sine_wave_sample, loop=True)

    def stop_tone(self):
        #print("stop tone")
        self._teardown()

    def _teardown(self):
        if self._sample is not None and self._sample.playing:
            self._sample.stop()
            # TODO: find out if deinit() should be called on non-playing samples
            self._sample.deinit()
        self._sample = None
        
    @staticmethod
    def _sine_sample(length):
        #tone_volume = (2 ** 15) - 1
        #shift = 2 ** 15
        for i in range(length):
            yield int(TONE_VOLUME * sin(2*pi*(i / length)) + SHIFT)

    def _generate_sample(self, length=100):
        if self._sample is not None:
            return
        self._sine_wave \
            = array("H", CpxAudioTone._sine_sample(length))
        self._sine_wave_sample = RawSample(self._sine_wave)
        self._sample = AudioOut(SPEAKER)
