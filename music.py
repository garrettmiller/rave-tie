# The MIT License (MIT)
#
# Copyright (c) 2018 Gary Fong
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

from micropython import const
from time import monotonic
from digitalio import DigitalInOut
from board import SPEAKER_ENABLE

import song

class Music:
    """
    Responsible for managing the songs for the holi-tie. When asked,
    sequentially play all the songs in a loop. Stop when asked.
    """

    def __init__(self):
        """ Initial the music manager. """

        self.active_song = None
        self.speaker_enable = None

        self.songs = [
            "jingle_bells.bin",
            "frosty_the_snowman.bin"]

    def play(self):
        """ Play the songs. """
        print("music.play")

        if self.is_playing():
            return

        self.speaker_enable = DigitalInOut(SPEAKER_ENABLE)
        self.speaker_enable.switch_to_output(value=False)
        self.speaker_enable.value = True

        self.active_song_index = 0
        self.active_song = None
        self.next_song_delay = const(2000)
        self.last_song_ended = None
        
        self._play()

    def _play(self):
        """ Internal method which plays the song """
        #print("music._play")

        # Begin sequentially playing the songs
        self.active_song = song.Song(self.songs[self.active_song_index]);
        self.active_song.begin()
        self.active_song.play()
        self.last_song_ended = None

    def update(self):
        """
        Update the playing state of the music. Must be called in the main
        processing loop.
        """

        # Can't update if not playing
        if not self.is_playing():
            return

        # Contiue to let the song play if it hasn't finished yet
        if self.active_song.is_playing():
            self.active_song.update()
            return

        # At this point, the active song has finished playing. If it has just
        # finished, set a time marker so that we can wait a bit before starting
        # the next song.
        if self.last_song_ended is None:
            self.last_song_ended = int(round(monotonic() * 1000))
            return

        # Have we waited enough time since the last song?
        if int(round(monotonic() * 1000)) - self.last_song_ended \
           < self.next_song_delay:
            return

        # We have waited enough time. So lets start the next song.
        self.play_next_song()

    def stop(self):
        """ Stop playing the songs. Release resources. """
        #print("music.stop")

        if self.is_playing():
            self.active_song.stop()
            self.active_song.end()
            self.active_song = None
            self.speaker_enable.value = False
            self.speaker_enable.deinit()
            self.speaker_enable = None

    def is_playing(self):
        """ Return true if this music manager is playing songs """
        return self.active_song is not None

    def play_next_song(self):
        #print("next song")

        if self.is_playing():
            self.active_song.stop()
            self.active_song.end()
            self.active_song = None

        # Next song
        self.active_song_index \
            = (self.active_song_index + 1) % len(self.songs)
        self._play()
