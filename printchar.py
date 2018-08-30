#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def printBitmap(bitmap, x, y):
    print("---------------------------------")
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
    print("---------------------------------")
