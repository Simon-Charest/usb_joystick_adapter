#!/usr/bin/python
# coding=utf-8

import constant
import io_
import ui
import usb


def main():
    # Debug
    # usb.manage_usb_joystick_adapter()
    # files = io_.get_files(constant.FIRMWARE)
    #
    # for file in files:
    #     intel_hex = io_.get_intel_hex(file)
    #     data = io_.get_data(intel_hex)

    ui.show()


if __name__ == '__main__':
    main()
