#!/bin/bash

set -e
rm -rf bmp/*.bmp
./dosfnt2bmp.py
./ttf2bmp.py
./bipfont.py pack dgm.ft
