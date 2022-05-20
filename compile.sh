#!/bin/bash
compiler=./mpy-cross-7.3-macos.bin

for f in *.py; do
    if [[ $f != code.py ]]; then
	echo "compiling: $f"
	$compiler $f
    fi
done
