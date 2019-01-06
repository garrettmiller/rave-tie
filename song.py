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

import cpx_audio_tone
from time import monotonic
from struct import unpack

class Song:
    """
    Represents a playable song. The playing state of the song is maintained
    during the main processing loop. That is, there are no internal loops or
    sleeps. This allows for other processing to happen.
    Because this involves quite a bit of memory usage, begin() and end() must
    be called to setup and release as much of the resources as possible.
    """

    def __init__(self, song_file):
        """
        Args:
        notes (list): List of tuples (note, duration)
        """

        self.song_file = song_file
        self.notes = None
        self.cpx = None

    def begin(self):
        """
        Initialiez this song object to begin playing the song. Call end() to
        cleanup resources.
        """
        
        self.notes = self._read_song_data()
        self.cpx = cpx_audio_tone.CpxAudioTone()
        self.tone_start = None
        self.active_note = None

    def play(self):
        """ Play the song. Do nothing if song is already playing. """
        #print("song.play")
        
        # Do nothing if already playing
        if self.is_playing():
            return

        # Being playing the first note
        self.active_note = 0
        #print("note: " + str(self._get_active_note()))
        self.cpx.start_tone(self._get_active_note())
        self.tone_start = int(round(monotonic() * 1000))

    def update(self):
        """
        Update the song play state. Must be called in the main processing loop.
        """
        #print("song.update")
        
        # Nothing to update if not playing a song
        if not self.is_playing():
            return

        # Keep playing the note if it hasn't been played long enough yet
        now = int(round(monotonic() * 1000))
        if now - self.tone_start < self._get_active_duration():
            return

        # Desired duration has gone by so we can stop playing the note.
        self.cpx.stop_tone()

        # If was playing the last note, then we are done
        self.active_note += 1
        if self.active_note >= len(self.notes):
            self.active_note = None
            return

        # Play the new active note
        #print("note: " + str(self._get_active_note()))
        self.cpx.start_tone(self._get_active_note())
        self.tone_start = now

    def stop(self):
        """
        Stop playing the song. Call play() to start playing the song againg
        from the beginning.
        """
        #print("song.stop")
        
        if not self.is_playing():
            return
        self.cpx.stop_tone()
        self.active_note = None

    def end(self):
        """
        Destruct this song object to end playing the song. If called, begin()
        must be called to reinitialize for playing.
        """

        self.stop()
        self.notes = None
        self.cpx = None

    def is_playing(self):
        return self.active_note is not None
        
    def pause(self):
        """ Pause the song at the current note. """
        # TODO: implement
        pass
    
    def resume(self):
        """ Resume playing the song from where it was paused. """
        # TODO: implement
        pass

    def _read_song_data(self):
        """
        Read the song data from the file and return a list of tuples in this
        format: (note, duration)
        """
        notes = []
        with open(self.song_file, "rb") as song_data:
            while True:
                buf = song_data.read(4)
                if buf == b"":
                    break
                notes.append(unpack("<HH", buf))
        return notes
    
    def _get_active_note(self):
        return self.notes[self.active_note][0]

    def _get_active_duration(self):
        return self.notes[self.active_note][1]
