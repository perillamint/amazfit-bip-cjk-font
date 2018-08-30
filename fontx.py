#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from struct import unpack, pack
from PIL import ImageFont, ImageDraw, Image

class FontXFont:
    def __init__(self, fntfile):
        self._fntbin = open(fntfile, "rb")
        self._fntbin.seek(0, 0)
        self._header = self._loadHeader()
        self._font = dict()

        if self._header.flag == 1:
            self._loadShiftJIS()

    def _loadHeader(self):
        class header:
            pass

        fntbin = self._fntbin

        magic = fntbin.read(6)
        if magic.decode("UTF-8") != "FONTX2":
            raise ValueError("Invalid MAGIC")

        header.fontname = fntbin.read(8).decode("UTF-8")
        header.width = fntbin.read(1)[0]
        header.byteWidth = (header.width + 7) // 8
        header.height = fntbin.read(1)[0]
        header.flag = fntbin.read(1)[0]

        if header.flag == 0:
            raise ValueError("ANK is not supported yet")
        elif header.flag == 1:
            blkcnt = fntbin.read(1)[0]
            header.blocks = [None]*blkcnt

            for i in range(0, blkcnt):
                blkstart = unpack("<H", fntbin.read(2))[0]
                blkend = unpack("<H", fntbin.read(2))[0]
                header.blocks[i] = (blkstart, blkend)
        else:
            raise ValueError("Invalid encoding")

        return header

    def _grabChar(self, width, height):
        fntbin = self._fntbin
        byteWidth = (width + 7) // 8
        fnt = [None] * byteWidth * height
        for i in range(0, byteWidth * height):
            fnt[i] = fntbin.read(1)[0]

        return fnt

    def _loadShiftJIS(self):
        fntbin = self._fntbin
        header = self._header

        for i in range(0, len(header.blocks)):
            blk = header.blocks[i]
            for j in range(blk[0], blk[1]):
                char = self._grabChar(header.width, header.height)
                self._font[j] = char

    def renderChar(self, char):
        try:
            jischar = unpack(">H", chr(char).encode("Shift-JIS"))[0]
            header = self._header
            bitmap = [0x00] * header.byteWidth * header.height
            charbin = self._font[jischar]

            for i in range(0, header.byteWidth * header.height):
                bitmap[i] |= charbin[i]

            return bitmap
        except KeyError:
            raise ValueError("Unsupported character")

    def render(self, char):
        image = Image.new('1', (16, 16), "black")
        pixels = image.load()
        bitmap = self.renderChar(char)

        for i in range(0, self._header.height):
            for j in range(0, self._header.width):
                pixelpt = i * 8 * self._header.byteWidth + j
                fntByte = bitmap[pixelpt // 8]
                fntBit = (fntByte << (pixelpt % 8)) & 0x80

                if fntBit != 0:
                    pixels[(j, i)] = 0xFF
                else:
                    pixels[(j, i)] = 0x00

        return image
