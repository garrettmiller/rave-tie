# Rave-Tie
Code for the "Rave tie". Written in Python using the CircuitPython platform for the Circuit Playground Express microcontroller. The idea behind the Rave-Tie came from the [Ampli-Tie](https://learn.adafruit.com/led-ampli-tie) by Beck Stern, and much code is from gwfong's Holi-Tie. The Holi-Tie was an improvement in that it has multiple NeoPixel animations, color and speed interactivity, and holiday music.

Holi-Tie Video: https://youtu.be/t3gc5sFV1Mk

# Compiling
In order to get the code onto the Circuit Playground Express (cpx), it has to be compiled. This will reduce the byte size of he modules. The `compile` bash script will compile the python scripts to Micropython format. It will also create binary versions of the python-structured songs. Simply just run `compile` in the directory. The location of the mpy-cross compiler will likely need to be configured within the script reflect where it is on your system, though a semi-current one is provided in this repository.

# Deployment
The Rave-Tie does not use any special external Adafruit CircuitPython libraries. It only needs what the flash UF2 provides. All libraries should be removed from CPX otherwise the Holi-Tie code may not fit even after they have been compiled.

To get the code onto the CPX, it just needs to be copied. There is a `deploy` script which makes this easy. It wil simply copy all of the `*.mpy` files to the CPX. It will also copy the binary version of the song data and the heart of the program, `code.py`.
