#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image

class LatinFont:
    def __init__(self, fntfile, headersz, width, height):
        fntbin = open(fntfile, "rb")
        fntbin.seek(headersz, 0)

        self._byteWidth = (width + 7) // 8
        self._width = width
        self._height = height
        self._fntrom = [None] * 256

        for i in range(0, 256):
            self._fntrom[i] = self.grabChar(width, height, fntbin)

    def grabChar(self, width, height, fntbin):
        byteWidth = (width + 7) // 8
        fnt = [None] * byteWidth * height
        for i in range(0, byteWidth * height):
            fnt[i] = fntbin.read(1)[0]

        return fnt

    def renderChar(self, char):
        bitmap = [0x00] * self._byteWidth * self._height
        for i in range(0, self._byteWidth * self._height):
            bitmap[i] |= self._fntrom[char][i]

        return bitmap

    def render(self, char):
        image = Image.new('1', (16, 16), "black")
        pixels = image.load()
        bitmap = self.renderChar(char)

        for i in range(0, 16):
            for j in range(0, self._width):
                pixelpt = i * 8 + j
                fntByte = bitmap[pixelpt // 8]
                fntBit = (fntByte << (pixelpt % 8)) & 0x80

                if fntBit != 0:
                    pixels[(j, i)] = 0xFF
                else:
                    pixels[(j, i)] = 0x00

        return image
