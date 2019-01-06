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

import jingle_bells
import frosty_the_snowman
import struct

songs = [
    (jingle_bells.song, "jingle_bells.bin"),
    (frosty_the_snowman.song, "frosty_the_snowman.bin")
]

for song in songs:
    data=song[0]
    file=song[1]
    i = 0
    with open(song[1], "rb") as bin_file:
        while True:
            buf = bin_file.read(4)
            if buf == b"":
                break
            note, dur = struct.unpack("<HH", buf)
            print((note, dur))
            note_data = song[0][i][0]
            dur_data = song[0][i][1]
            if note != note_data:
                raise ValueError("note " + str(i) + ": file=" + str(note) + ", song=" + str(ntoe_data))
            if dur != dur_data:
                raise ValueError("dur " + str(i) + ": file=" + str(dur) + ", song=" + str(dur_data))
            i += 1
print("song data is valid")
