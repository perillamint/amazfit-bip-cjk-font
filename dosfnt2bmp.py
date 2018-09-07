#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import argparse
import sys
from PIL import ImageFont, ImageDraw, Image
from latin import LatinFont
from dkb844 import Hangul844Font
from fontx import FontXFont

def renderInRange(charRange, fontRenderer):
    for i in range(charRange[0], charRange[1] + 1):
        try:
            image = fontRenderer.render(i)
            image.save("{}{:04x}4.bmp".format('./bmp/', i), "bmp")
        except (UnicodeEncodeError, ValueError):
            print("WARN: Unsupported char 0x{:04x}".format(i))

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--latin', nargs='?', help='Latin font file')
parser.add_argument('--dkb844', nargs='?', help='Dokkaebi 844 font file')
parser.add_argument('--fontx', nargs='?', help='FONTX font file')

args = parser.parse_args()

hangulFontRenderer = Hangul844Font(args.dkb844)
#latinFontRenderer = LatinFont("./VGA-ROM.F16", 0, 8, 16)
latinFontRenderer = LatinFont(args.latin, 1626, 8, 16)
japaneseFontRenderer = FontXFont(args.fontx)

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

# CJK Symbols and Punctuation
renderInRange((0x3000, 0x303F), japaneseFontRenderer)

# Hiragana
renderInRange((0x3040, 0x309F), japaneseFontRenderer)

# Katakana
renderInRange((0x30A0, 0x30FF), japaneseFontRenderer)

# CJK Unified ideograph
renderInRange((0x4E00, 0x9FFF), japaneseFontRenderer)

# CJK Unified ideograph Extension A
renderInRange((0x3400, 0x4DBF), japaneseFontRenderer)
