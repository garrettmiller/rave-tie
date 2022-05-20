#!/bin/bash

dest=/Volumes/CIRCUITPY/

echo "Deploying: modules"
cp *.mpy $dest

echo "Deploying: code.py"
cp code.py $dest
