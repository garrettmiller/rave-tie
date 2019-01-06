# Description
The songs are stored as musical notes and durations in a python struction. But
because they take up too much memory, they are converted into binary format.

# Usage
convert_to_binary.py:
This will convert the songs from python to binary format. The binary format is
fixed to little endian of two shorts. The first represents the note, the second,
the duration.

validate_binary.py:
This will validate that the binary data was written as expected.
