#!/usr/bin/python
# coding=utf-8

from tkinter import *
import constant
import io_
import usb


def show():
    root = Tk()
    root.geometry('800x600')
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=constant.ICON))
    root.title(constant.__project__)

    devices_label = Label(root, text='Device')
    devices_label.pack(anchor=W)

    devices = usb.get_devices([constant.VENDOR_ID, constant.BOOT_VENDOR_ID],
                              [constant.PRODUCT_ID, constant.BOOT_PRODUCT_ID],
                              [constant.MANUFACTURER_STRING, constant.BOOT_MANUFACTURER_STRING],
                              [constant.PRODUCT_STRING, constant.BOOT_PRODUCT_STRING])
    device_names = usb.get_device_names(devices)

    device_name = StringVar(root)
    device_option_menu = OptionMenu(root, device_name, *device_names)
    device_option_menu.pack(anchor=W)

    devices_label = Label(root, text='Configuration')
    devices_label.pack(anchor=W)

    files = io_.get_files(constant.FIRMWARE)
    file_names = io_.get_file_names(files)

    file = StringVar(root)
    file_option_menu = OptionMenu(root, file, *file_names)
    file_option_menu.pack(anchor=W)

    update_button = Button(root, text='Update', command=lambda: update(devices, device_name, file))
    update_button.pack(anchor=W)

    about_button = Button(root, text='About', command=lambda: show_about(root.winfo_rootx(), root.winfo_rooty()))
    about_button.pack(anchor=W)

    root.mainloop()


def update(devices, device_name, file):
    # TODO: Dev this
    print(file)

    # Get device by name
    # device = usb.get_device(devices, device_name)

    # Read Intel HEX file
    # intel_hex = io_.get_intel_hex(file)
    # data = io_.get_data(intel_hex)

    # Write to USB device
    # device.write(data)


def show_about(x=0, y=0):
    top_level = Toplevel()
    top_level.grab_set()
    top_level.resizable(0, 0)  # Remove maximize button
    top_level.wm_title(f'About {constant.__project__}')
    top_level.geometry(f'+{x}+{y}')

    about_label = Label(top_level, text=f'{constant.__project__}\n'
                                        f'Version {constant.__version__}\n'
                                        f'{constant.__copyright__}\n'
                                        f'\n'
                                        f'The {constant.__project__} and its software are the propriety of {constant.__author__}.\n'
                                        f'The hardware is sold without any warranty. The software is open source and provided free of charge.\n'
                                        f'Both are to be used with specific devices with DB9 connectors.\n'
                                        f'\n'
                                        f'This product is license under the {constant.__license__} License Terms.')
    about_label.grid()

    ok_button = Button(top_level, text='OK', command=top_level.destroy)
    ok_button.grid(row=1, column=0)