#!/usr/bin/python
# coding=utf-8

from tkinter import *
from tkinter import messagebox
import constant_rd

# Package: PyUSB
import usb
import usb.core
import usb.util
import usb.backend
import usb.backend.libusb0 as libusb0
import usb.backend.libusb1 as libusb1
import usb.backend.openusb as openusb


def get_hid_report(device):
    transferred_bytes = device.ctrl_transfer(0xA1, 1, 0x200, 0x00, 64)

    return transferred_bytes


def read_device(devices, device_name, data_label):
    if device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device must be selected.')

        return

    """ TODO: This is a test using PyUSB """

    # Get device (TODO: Remove hardcoding)
    device = usb.core.find(idVendor=constant_rd.BOOT_VENDOR_ID, idProduct=constant_rd.BOOT_PRODUCT_ID)
    interface_number = device[0].interfaces()[0].bInterfaceNumber
    endpoint = device[0].interfaces()[0].endpoints()[0]
    endpoint_address = endpoint.bEndpointAddress
    device.reset()
    device.set_configuration()

    # Read data from device
    # Errors:
    #     usb.core.USBError: could not claim interface 0, invalid configuration 0
    #     usb.core.USBError: could not set config 1: win error: The parameter is incorrect.
    #     usb.core.USBError: reaping request failed, win error:
    #       The I/O operation has been aborted because of either a thread exit or an application request.
    #     usb.core.USBError: sending control message failed, win error: A device which does not exist was specified.
    #     usb.core.USBError: timeout error

    data = device.read(endpoint_address, 1)  # Method 1
    # data = get_hid_report(device)  # Method 2

    if constant_rd.DEBUG:
        print(f'Device: {device}')
        print(f'Endpoint: {endpoint}')
        print(f'Interface Number: {interface_number}')
        print(f'Endpoint Address: {endpoint_address}')
        print(f'Data: {data}')

    # Display data using a label
    data_label['text'] = data
