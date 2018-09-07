# amazfit-bip-cjk-font

![Sample render](img/example.jpg?raw=true)

FontROM builder for Xiaomi Amazfit Bip

This script set converts MS-DOS era bitmap font into Amazfit Bip fontROM.

Currently it supports

* Typical latin bitmap font file
* 844 Dokkaebi font file
* DOS/V FONTX file (Shift-JIS only -- I need ANK file to hack on it)

# I want other fonts!

You can grab any MS-DOS bitmap font from web and give it a try. (You should edit dosfnt2bmp.py in that case)

Or, you can try fonts in this repository: https://github.com/perillamint/dkbfnts/

# TODO

Source FLOSS compatible Han bitmap font file and add support for it.

# Special thanks
* [Seongik Kim](https://twitter.com/noerror_kr) for documenting 844 Johab mechanism
* Joongtae Kim for Dokkaebi Hangul font file
* [Elm-ChaN](http://elm-chan.org/) for documenting [DOS/V FONTX file format](http://elm-chan.org/docs/dosv/fontx_e.html)
* [水城珠洲](http://minashiro.net/) for their [FreeDOS/V project and DOS/V font file](http://dos.minashiro.net/)

# License notice
* ttf2bmp.py - BSD 3-clause https://github.com/sukso96100/amazfit-bip-kr
* Bm437_IBM_PS2thin4.FON - CC-BY-SA 4.0 https://int10h.org/oldschool-pc-fonts/
* 04GZN16X.FNT - GNU GPL v2 http://dos.minashiro.net/freedosvd.html
