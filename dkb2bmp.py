#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import ImageFont, ImageDraw, Image

def printBitmap(bitmap, x, y):
    for i in range(0, y):
        for j in range(0, x):
            pixelpt = i * 16 + j
            fntByte = bitmap[pixelpt // 8]
            fntBit = (fntByte << (pixelpt % 8)) & 0x80

            if (fntBit != 0):
                print("■", end='')
            else:
                print("□", end='')
        print("\n", end='')

class LatinFont:
    def __init__(self, fntfile):
        fntbin = open(fntfile, "rb")
        self._fntrom = [None] * 256

        for i in range(0, 256):
            self._fntrom[i] = self.grabChar(fntbin)

    def grabChar(self, fntbin):
        fnt = [None] * 16
        for i in range(0, 16):
            fnt[i] = fntbin.read(1)[0]

        return fnt

    def renderChar(self, char):
        bitmap = [0x00] * 16
        for i in range(0, 16):
            bitmap[i] |= self._fntrom[char][i]

        return bitmap

    def render(self, char):
        image = Image.new('1', (16, 16), "black")
        pixels = image.load()
        bitmap = self.renderChar(char)

        for i in range(0, 16):
            for j in range(0, 8):
                pixelpt = i * 8 + j
                fntByte = bitmap[pixelpt // 8]
                fntBit = (fntByte << (pixelpt % 8)) & 0x80

                if fntBit != 0:
                    pixels[(j, i)] = 0xFF
                else:
                    pixels[(j, i)] = 0x00

        return image

# choLookup1, 2: Key is jungIdx
# jungLookup   : Key is choIdx
# jongLookup   : Key is jungIdx
# Idx          0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
choLookup1  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1, 2, 4, 4, 4, 2, 1, 3, 0]
choLookup2  = [0, 5, 5, 5, 5, 5, 5, 5, 5, 6, 7, 7, 7, 6, 6, 7, 7, 7, 6, 6, 7, 5]
jungLookup1 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
jungLookup2 = [0, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3]
jongLookup  = [0, 0, 2, 0, 2, 1, 2, 1, 2, 3, 0, 2, 1, 3, 3, 1, 2, 1, 3, 3, 1, 1]

class Hangul844Font:
    def __init__(self, fntfile):
        self._choSet = [None] * 8
        self._jungSet = [None] * 4
        self._jongSet = [None] * 4

        fntbin = open(fntfile, "rb")

        for i in range(0, 8):
            self._choSet[i] = [None] * 20
            for j in range(0, 20):
                self._choSet[i][j] = self.grabChar(fntbin)

        for i in range(0, 4):
            self._jungSet[i] = [None] * 22
            for j in range(0, 22):
                self._jungSet[i][j] = self.grabChar(fntbin)

        for i in range(0, 4):
            self._jongSet[i] = [None] * 28
            for j in range(0, 28):
                self._jongSet[i][j] = self.grabChar(fntbin)

        fntbin.close()

    def grabChar(self, fntbin):
        fnt = [None] * 32
        for i in range(0, 32):
            fnt[i] = fntbin.read(1)[0]

        return fnt

    def renderChar(self, char):
        image = Image.new('1', (16, 16), "black")
        choIdx = 0
        jungIdx = 0
        jongIdx = 0
        if char >= 0x1100 and char <= 0x1112:
            choIdx = char - 0x1100 + 1
        elif char >= 0x1161 and char <= 0x1175:
            jungIdx = char - 0x1161 + 1
        elif char >= 0x11A8 and char <= 0x11C2:
            jongIdx = char - 0x11A8 + 1
        elif char >= 0xAC00 and char <= 0xD7A3:
            nchr = char - 0xAC00
            choIdx = nchr // (0x0015 * 0x001C) + 1
            jungIdx = (nchr // 0x001C) % 0x0015 + 1;
            jongIdx = nchr % 0x001C;
        else:
            print("Invalid character!!")
            return image

        choSet = self._choSet[0]
        jungSet = self._jungSet[0]
        jongSet = self._jongSet[0]
        if choIdx != 0 and jungIdx == 0 and jongIdx == 0:
            choSet = self._choSet[1]
        elif choIdx == 0 and jungIdx != 0 and jongIdx == 0:
            jungSet = self._jungSet[0]
        elif choIdx == 0 and jungIdx == 0 and jongIdx == 0:
            jongSet = self._jongSet[0]
        elif choIdx != 0 and jungIdx != 0 and jongIdx == 0:
            # With choseong and jungseong
            choSet = self._choSet[choLookup1[jungIdx]]
            jungSet = self._jungSet[jungLookup1[choIdx]]
        elif choIdx != 0 and jungIdx != 0 and jongIdx != 0:
            choSet = self._choSet[choLookup2[jungIdx]]
            jungSet = self._jungSet[jungLookup2[choIdx]]
            jongSet = self._jongSet[jongLookup[jungIdx]]

        renderTmp = [0] * 32

        for i in range(0, 32):
            renderTmp[i] |= choSet[choIdx][i]
            renderTmp[i] |= jungSet[jungIdx][i]
            renderTmp[i] |= jongSet[jongIdx][i]

        return renderTmp

    def render(self, char):
        img = Image.new('1', (16, 16), "black")
        pixels = img.load()
        bitmap = self.renderChar(char)

        #printBitmap(bitmap, 16, 16)
        for i in range(0, 16):
            for j in range(0, 16):
                pixelpt = i * 16 + j
                fntByte = bitmap[pixelpt // 8]
                fntBit = (fntByte << (pixelpt % 8)) & 0x80

                if fntBit != 0:
                    pixels[(j, i)] = 0xFF
                else:
                    pixels[(j, i)] = 0x00

        return img

def renderInRange(charRange, fontRenderer):
    for i in range(charRange[0], charRange[1] + 1):
        image = fontRenderer.render(i)
        image.save("{}{:04x}4.bmp".format('./bmp/', i), "bmp")

hangulFontRenderer = Hangul844Font("./H04.FNT")
latinFontRenderer = LatinFont("./VGA-ROM.F16")

# ASCII
renderInRange((0x0000, 0x007F), latinFontRenderer)

# Hangul Jamo
renderInRange((0x1100, 0x1112), hangulFontRenderer)
renderInRange((0x1161, 0x1175), hangulFontRenderer)
renderInRange((0x11A8, 0x11C2), hangulFontRenderer)

# Hangul Syllables
renderInRange((0xAC00, 0xD7A3), hangulFontRenderer)
