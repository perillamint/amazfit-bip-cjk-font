#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image
from latin import LatinFont
from dkb import Hangul844Font

def printBitmap(bitmap, x, y):
    for i in range(0, y):
        for j in range(0, x):
            pixelpt = i * 16 + j
            fntByte = bitmap[pixelpt // 8]
            fntBit = (fntByte << (pixelpt % 8)) & 0x80

            if fntBit != 0:
                print("■", end='')
            else:
                print("□", end="")
        print("\n", end='')



def renderInRange(charRange, fontRenderer):
    for i in range(charRange[0], charRange[1] + 1):
        image = fontRenderer.render(i)
        image.save("{}{:04x}4.bmp".format('./bmp/', i), "bmp")

hangulFontRenderer = Hangul844Font("./H04.FNT")
#latinFontRenderer = LatinFont("./VGA-ROM.F16", 0, 8, 16)
latinFontRenderer = LatinFont("./Bm437_IBM_PS2thin4.FON", 1626, 8, 16)

# ASCII
renderInRange((0x0000, 0x007F), latinFontRenderer)

# Hangul Jamo
renderInRange((0x1100, 0x1112), hangulFontRenderer)
renderInRange((0x1161, 0x1175), hangulFontRenderer)
renderInRange((0x11A8, 0x11C2), hangulFontRenderer)

# Hangul Compat Jamo
renderInRange((0x3131, 0x314E), hangulFontRenderer)
renderInRange((0x314F, 0x3163), hangulFontRenderer)

# Hangul Syllables
renderInRange((0xAC00, 0xD7A3), hangulFontRenderer)
