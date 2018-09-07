#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Amazfit Bip(米动手表 青春版) 한글 글자 비트맵 이미지 생성기
Amazfit Bip(米动手表 青春版) Korean Hangul glyph bitmap image generator
Copyright (c) 2018 Youngbin Han <sukso96100@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from PIL import ImageFont, ImageDraw, Image

fontPath = "./fonts/ttf/NotoSansSymbols-Light.ttf"
destPath = "./bmp/"
marginLeft = 0
marginTop = -9

bmpdir = destPath
basefilemap = {}
for i in os.listdir(bmpdir):
    key = i[0:4]
    basefilemap[key] = i

def printInRange(charRange, font):
    for i in range(charRange[0], charRange[1]):
        image = Image.new('1', (16, 16), "black")
        draw = ImageDraw.Draw(image)
        draw.text((marginLeft, marginTop), chr(i), font=font, fill="white")
        imageKey = "{:04x}".format(i)
        if imageKey in basefilemap:
            os.unlink("{}/{}".format(bmpdir, basefilemap[imageKey]))
        image.save("{}{:04x}4.bmp".format(destPath, i), "bmp")

def printInArray(charArray, font):
    for i in charArray:
        image = Image.new('1', (16, 16), "black")
        draw = ImageDraw.Draw(image)
        draw.text((marginLeft, marginTop), chr(i), font=font, fill="white")
        image.save("{}{:04x}4.bmp".format(destPath, i), "bmp")

font = ImageFont.truetype(fontPath, 15)

# Unicode block: Miscellaneous Symbols
printInRange((0x2600, 0x26FF), font)
