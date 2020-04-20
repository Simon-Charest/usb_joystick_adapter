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
    'https://github.com/gbishop/cython-hidapi',
    'https://twitter.com/gbishop',
    'http://www.cs.unc.edu/~gb/'
]
__email__ = 'info@retronicdesign.com'
__license__ = 'GNU'
__maintainer__ = 'Simon Charest and Francis-Olivier Gradel, Eng.'
__project__ = 'Retronic Design USB Joystick Adapter'
__status__ = 'Developement'
__version__ = '4.0.0'

"""
    For use with the Atari C64 Amiga Joystick v3.1 by Retronic Design
"""

import hid  # Package: hidapi

VENDOR_ID = 2064  # 0x810, 2064, 0b100000010000
PRODUCT_ID = 58625  # 0xE501, 58625, 0b1110010100000001
MANUFACTURER_STRING = 'retronicdesign.com'
PRODUCT_STRING = 'Atari C64 Amiga Joystick v3.1'
BOOT_VENDOR_ID = 5824  # 0x16C0, 5824, 0b1011011000000
BOOT_PRODUCT_ID = 1503  # 0x5DF, 1503, 0b10111011111
BOOT_MANUFACTURER_STRING = 'obdev.at'
BOOT_PRODUCT_STRING = 'HIDBoot'
DEBUG = True
FIRMWARE = '../bin/Sega_Genesis_Joypad_v3.1.hex'


def main():
    devices = get_devices([VENDOR_ID, BOOT_VENDOR_ID], [PRODUCT_ID, BOOT_PRODUCT_ID],
                          [MANUFACTURER_STRING, BOOT_MANUFACTURER_STRING], [PRODUCT_STRING, BOOT_PRODUCT_STRING])

    for device in devices:
        if DEBUG:
            print_keys(device)  # Debug

        try:
            hid_device = hid.device(VENDOR_ID, PRODUCT_ID)
            hid_device.open_path(device['path'])
            hid_device.set_nonblocking(1)

            if DEBUG:
                print(f'Manufacturer: {hid_device.get_manufacturer_string()}')  # Debug
                print(f'Product: {hid_device.get_product_string()}')  # Debug

            firmware = read(FIRMWARE)

            if DEBUG:
                print(f'Firmware: {firmware}')

            hid_device.write(firmware)  # Write data to device

            # TODO: Read back the hexadecimal code that has been written
            # print(hid_device.read(5))

            hid_device.close()

        except IOError as io_error:
            print(f'Input/Output Error Exception: {io_error}')

        except ValueError as value_error:
            print(f'Value Error Exception: {value_error}')


def get_all_devices():
    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    return hid.enumerate(0, 0)


def get_devices(vendor_id, product_id, manufacturer_string, product_string):
    devices = list()

    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    for device in hid.enumerate(0, 0):
        if device['vendor_id'] in vendor_id and \
                device['product_id'] in product_id and \
                device['manufacturer_string'] in manufacturer_string and \
                device['product_string'] in product_string:
            devices.append(device)

    return devices


def read(file):
    with open(file, 'r') as stream:
        return read_integer(stream)


def read_hexadecimal(stream):
    return ['{:02x}'.format(ord(c)) for c in stream.read()]


def read_integer(stream):
    return [ord(c) for c in stream.read()]


def print_keys(device):
    keys = device.keys()
    print()

    for key in keys:
        print(f'{key}: {device[key]}')


if __name__ == '__main__':
    main()
