#!/bin/bash

function fontgen {
    rm -rf bmp/*.bmp
    ./bipfont.py unpack ./vendor/Mili_chaohu.ft
    ./dosfnt2bmp.py --latin $1 --dkb844 $2 --fontx $3
    ./ttf2bmp.py
    ./bipfont.py pack $4
}
set -e

fontgen ./fonts/latin/Bm437_IBM_PS2thin4.FON ./fonts/dkb844/H02.FNT ./fonts/fontx/04GZN16X.FNT ./output/ddalkkol.ft
fontgen ./fonts/latin/Bm437_IBM_PS2thin4.FON ./fonts/dkb844/H04.FNT ./fonts/fontx/04GZN16X.FNT ./output/ddungunmo.ft
