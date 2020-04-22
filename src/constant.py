#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = 'Copyright © 2020 Retronic Design. All rights reserved.'
__credits__ = [
    'Simon Charest',
    'SLCIT, Inc.',
    'simoncharest@gmail.com',
    'https://www.facebook.com/simon.charest/',
    'https://github.com/Simon-Charest',
    'https://www.linkedin.com/in/simoncharest/',
    'https://twitter.com/scharest',

    'Francis-Olivier Gradel, Eng.',
    'Retronic Design',
    'info@retronicdesign.com',
    'https://www.ebay.com/usr/retronicdesign',
    'https://www.facebook.com/retronicdesign',
    'https://ca.linkedin.com/in/francis-gradel-ing-b620591a',
    'https://twitter.com/fogradel',
    'retronicdesign.com',
    'https://atariage.com/forums/profile/37766-nitz1976/',

    'Gary Bishop',
    'gb@cs.unc.edu',
    'https://github.com/gbishop',
    'https://twitter.com/gbishop',
    'http://www.cs.unc.edu/~gb/'
]
__email__ = 'info@retronicdesign.com'
__license__ = 'GNU'
__maintainer__ = 'Simon Charest and Francis-Olivier Gradel, Eng.'
__project__ = 'Retronic Design USB Joystick Adapter'
__status__ = 'Developement'
__version__ = '1.0.0'

DEBUG = True

VENDOR_ID = 2064  # 0x810, 2064, 0b100000010000
PRODUCT_ID = 58625  # 0xE501, 58625, 0b1110010100000001
MANUFACTURER_STRING = 'retronicdesign.com'
PRODUCT_STRING = 'Atari C64 Amiga Joystick v3.1'

BOOT_VENDOR_ID = 5824  # 0x16C0, 5824, 0b1011011000000
BOOT_PRODUCT_ID = 1503  # 0x5DF, 1503, 0b10111011111
BOOT_MANUFACTURER_STRING = 'obdev.at'
BOOT_PRODUCT_STRING = 'HIDBoot'

FIRMWARE = '../bin/*.hex'
