#!/bin/bash

set -e
rm -rf bmp/*.bmp
./dkb2bmp.py
./ttf2bmp.py
./bipfont.py pack dgm.ft
