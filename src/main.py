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
    'https://ca.linkedin.com/in/francis-gradel-ing-b620591a',
    'https://twitter.com/fogradel',
    'retronicdesign.com',

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

import constant
import input_output
import usb
# import kivy  # Package: Kivy
# kivy.require('1.11.1')
# from kivy.app import App
# from kivy.uix.label import Label


def main():
    usb.manage_usb_joystick_adapter()
    intel_hex = input_output.get_intel_hex(constant.FIRMWARE)
    print(f'Intel HEX: {intel_hex}')


if __name__ == '__main__':
    main()
