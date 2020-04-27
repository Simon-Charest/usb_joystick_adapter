#!/usr/bin/python
# coding=utf-8

from tkinter import *
from tkinter import messagebox
import libusb  # Package: libusb


def read_device(devices, device_name, data_label):
    if device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device must be selected.')

        return

    """ TODO: This is a test using libusb """
    return
