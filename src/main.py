#!/usr/bin/python
# coding=utf-8

import ui
import constant
import io_
import usb


def main():
    usb.manage_usb_joystick_adapter()
    files = io_.get_files(constant.FIRMWARE)

    for file in files:
        intel_hex = io_.get_intel_hex(file)
        data = io_.get_data(intel_hex)

    ui.run()


if __name__ == '__main__':
    main()
