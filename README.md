# holi-tie
Code for the holiday tie. Written in python using the circuitpython platform for the circuit playground express device. The idea behind the holi-tie came from the ampli-tie. However, the holi-tie has some interativity and some music.

# Compiling
First, in order to get the code onto the circuit playground express (cpx), it has to be compiled. The `compile` bash script will compile the python scripts to micropython format. It will also create binary versions of the python-structured songs. Simply just run `compile` in the directory. The location of the mpy-cross compiler will likely need to be configured within the script reflect where it is on your system.

# Deployment
Firt, all adafruit libraries will need to be removed. Second, there is a `deploy` script. It wil simply copy all of the `*.mpy` files to cpx. It will also copy the binary version of the song data. Lastly, it will copy `code.py`.
