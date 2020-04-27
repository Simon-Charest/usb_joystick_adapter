#!/usr/bin/python
# coding=utf-8

from tkinter import *
from tkinter import messagebox
import constant_rd
import hidapi_rd
import io_rd
import libusb_rd
import pyusb_rd


def run():
    # Display application
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.geometry('400x300')
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=constant_rd.ICON))
    root.title(constant_rd.__project__)

    """ First row """

    # Display label
    devices_label = Label(root, text='Device:')
    devices_label.grid(row=0, column=0)

    # Manage option menu
    devices = hidapi_rd.get_devices([constant_rd.VENDOR_ID, constant_rd.BOOT_VENDOR_ID],
                                    [constant_rd.PRODUCT_ID, constant_rd.BOOT_PRODUCT_ID])
    device_names = hidapi_rd.get_device_names(devices)

    # Display option menu
    device_name = StringVar(root)

    if constant_rd.DEBUG:
        print(f'Devices: {devices}')
        print(f'Device Names: {device_names}')
        print(f'Device Name: {device_name}')

    device_option_menu = OptionMenu(root, device_name, *device_names)
    device_option_menu.config(width=35)
    device_option_menu.grid(row=0, column=1, sticky=E)

    # Display button
    about_button = Button(root, text='About', command=lambda: show_about(root.winfo_rootx(), root.winfo_rooty()))
    about_button.grid(row=0, column=2)

    """ Second row """

    # Display label
    devices_label = Label(root, text='Configuration:')
    devices_label.grid(row=1, column=0)

    # Manage option menu
    files = io_rd.get_files(constant_rd.FIRMWARE)
    file_names = io_rd.get_file_names(files)

    # Display option menu
    file_name = StringVar(root)
    file_option_menu = OptionMenu(root, file_name, *file_names)
    file_option_menu.config(width=35)
    file_option_menu.grid(row=1, column=1, sticky=E)

    """ Third row """

    # Display button
    update_button = Button(root, text='Update Device',
                           command=lambda: update_device(devices, device_name.get(), files, file_name.get()))
    update_button.grid(row=2, column=1, sticky=E)

    """ Fourth row """

    # Display button
    read_button = Button(root, text='Read Device',
                         # command=lambda: hidapi_rd.read_device(devices, device_name.get(), data_label))
                         command=lambda: libusb_rd.read_device(devices, device_name.get(), data_label))
                         # command=lambda: pyusb_rd.read_device(devices, device_name.get(), data_label))
    read_button.grid(row=3, column=0)

    # Display label
    data_label = Label(root, text='')
    data_label.grid(row=3, column=1, columnspan=2)

    # Redraw
    root.mainloop()


def show_about(x=0, y=0):
    # Display form
    top_level = Toplevel()
    top_level.grab_set()
    top_level.resizable(0, 0)  # Remove maximize button
    top_level.wm_title(f'About {constant_rd.__project__}')
    top_level.geometry(f'+{x}+{y}')

    # Display label
    about_label = Label(top_level, text=f'{constant_rd.__project__}\n'
                                        f'Version {constant_rd.__version__}\n'
                                        f'{constant_rd.__copyright__}\n'
                                        f'\n'
                                        f'The {constant_rd.__project__} and its software are the propriety of {constant_rd.__author__}.\n'
                                        f'The hardware is sold without any warranty. The software is open-source and provided free of charge.\n'
                                        f'Both are to be used with specific devices with DB9 connectors.\n'
                                        f'\n'
                                        f'This product is license under the {constant_rd.__license__} License Terms.')
    about_label.grid()

    # Display button
    ok_button = Button(top_level, text='OK', command=top_level.destroy)
    ok_button.grid(row=1, column=0)


def update_device(devices, device_name, files, file_name):
    if device_name in ('', 'None') or file_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device and configuration must be selected.')

        return

    # Get device by name
    device = hidapi_rd.get_device(devices, device_name)

    # Get data from Intel HEX file
    file = hidapi_rd.get_file(files, file_name)
    intel_hex = io_rd.get_intel_hex(file)
    data = io_rd.get_data(intel_hex)

    # Write data to device
    hidapi_rd.write(device, data)

    messagebox.showinfo('Success', 'Configuration written to device successfully.')
