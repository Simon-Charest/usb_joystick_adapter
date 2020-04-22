#!/usr/bin/python
# coding=utf-8

from tkinter import *
import constant
import io_
import usb


def run():
    root = Tk()
    root.geometry('400x300')
    root.title(constant.__project__)

    devices_label = Label(root, text='Device')
    devices_label.pack(anchor=W)

    devices = usb.get_devices([constant.VENDOR_ID, constant.BOOT_VENDOR_ID],
                              [constant.PRODUCT_ID, constant.BOOT_PRODUCT_ID],
                              [constant.MANUFACTURER_STRING, constant.BOOT_MANUFACTURER_STRING],
                              [constant.PRODUCT_STRING, constant.BOOT_PRODUCT_STRING])
    device_names = usb.get_device_names(devices)

    device = StringVar(root)
    device_option_menu = OptionMenu(root, device, *device_names)
    device_option_menu.pack(anchor=W)

    devices_label = Label(root, text='Configuration')
    devices_label.pack(anchor=W)

    files = io_.get_files(constant.FIRMWARE)
    file_names = io_.get_file_names(files)

    file = StringVar(root)
    file_option_menu = OptionMenu(root, file, *file_names)
    file_option_menu.pack(anchor=W)

    update_button = Button(root, text='Update')
    update_button.pack(anchor=W)

    root.mainloop()
