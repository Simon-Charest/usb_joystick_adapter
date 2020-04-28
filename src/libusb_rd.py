#!/usr/bin/python
# coding=utf-8
from distutils.command.config import config
from tkinter import *
from tkinter import messagebox

from libusb import context

import constant_rd
import libusb  # Package: libusb


def read_device(devices, device_name, data_label):
    if device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device must be selected.')

        return

    """ TODO: This is a test using libusb """

    # Get device (TODO: Remove hardcoding)
    ctx = []
    context_ = libusb.init(*ctx)

    if constant_rd.DEBUG:
        print(f'Devices: {devices}')
        print(f'Device Name: {device_name}')
        print(f'Data Label: {data_label}')
        print(f'Context: {context_}')

    # device = libusb.open_device_with_vid_pid(context_, constant_rd.BOOT_VENDOR_ID, constant_rd.BOOT_PRODUCT_ID)
    libusb.close()

    return
