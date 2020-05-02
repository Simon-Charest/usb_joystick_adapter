#!/usr/bin/python
# coding=utf-8

from tkinter import messagebox
import constant_rd
import hid  # Package: hidapi
import io_rd
import keyboard


def get_all_devices():
    """ Get all Universal Serial Bus (USB) Human Interface Devices (HID) """

    return hid.enumerate(0, 0)


def get_device(devices, device_name):
    """ Get device by its unique identifier """

    for device in devices:
        if get_identifier(device['path']) in device_name:
            return device

    return None


def get_device_names(devices):
    """ Get device names, with identifiers (ex: 'Atari C64 Amiga Joystick v3.2 (8bf7757)') """

    if not devices:
        return None

    device_names = list()

    for device in devices:
        device_names.append(f"{get_product_string(device)} ({get_identifier(device['path'])})")

    return device_names


def get_devices(vendor_ids, product_ids):
    """ Return all devices which fit the vendor_ids and product_ids """

    hid_devices = get_all_devices()

    if constant_rd.DEBUG:
        print(f'HID Devices: {hid_devices}')

    devices = list()

    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    for hid_device in hid_devices:
        if constant_rd.DEBUG:
            print(f'HID Device: {hid_device}')

        if hid_device['vendor_id'] in vendor_ids and hid_device['product_id'] in product_ids:
            devices.append(hid_device)

    return devices


def get_file(files, file_name):
    """ Get file name by its unique identifier """

    for file in files:
        if file_name in file:
            return file

    return None


def get_identifier(path):
    """ Return unique identifier from device's path (ex: 8bf7757) """

    string = path.decode()  # Convert bytes to string
    paths = string.split('#')
    identifiers = paths[2].split('&')
    identifier = identifiers[1]  # Keep unique identifier

    if constant_rd.DEBUG:
        print(f'Path: {path}')
        print(f'String: {string}')
        print(f'Paths: {paths}')
        print(f'Identifiers: {identifiers}')
        print(f'Identifier: {identifier}')

    return identifier


def get_manufacturer_string(device):
    """
        Get manufacturer name (ex: retronicdesign.com)
        Patches a bug in the hardware which prevents the manufacturer_string to be read correctly upon plugging the device
    """

    if device['manufacturer_string']:
        return device['manufacturer_string']

    elif device['vendor_id'] == constant_rd.VENDOR_ID and device['product_id'] == constant_rd.PRODUCT_ID:
        return constant_rd.MANUFACTURER_STRING

    elif device['vendor_id'] == constant_rd.BOOT_VENDOR_ID and device['product_id'] == constant_rd.BOOT_PRODUCT_ID:
        return constant_rd.BOOT_MANUFACTURER_STRING


def get_product_string(device):
    """
        Get product name (ex: Atari C64 Amiga Joystick v3.2)
        Patches a bug in the hardware which prevents the product_string to be read correctly upon plugging the device
    """

    if device['product_string']:
        return device['product_string']

    elif device['vendor_id'] == constant_rd.VENDOR_ID and device['product_id'] == constant_rd.PRODUCT_ID:
        return constant_rd.PRODUCT_STRING

    elif device['vendor_id'] == constant_rd.BOOT_VENDOR_ID and device['product_id'] == constant_rd.BOOT_PRODUCT_ID:
        return constant_rd.BOOT_PRODUCT_STRING


def read(devices, device_name, data_label):
    """ Read data from device """

    if device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device must be selected.')

        return

    device = get_device(devices, device_name)  # Get device by name
    hid_device = hid.device()
    hid_device.open(device['vendor_id'], device['product_id'])

    try:
        if constant_rd.DEBUG:
            print(f'Opening device')

        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(1)

        if constant_rd.DEBUG:
            print(f'Device: {device}')
            print(f'HID Device: {hid_device}')
            print(f'Reading from device')

        # Read data from device (TODO: Dev/fix this)
        for address in range(0, 32512, 16):
            data = hid_device.read(address)
            print(f'Read: [Block: {int(address / 16)}, Address: {address}, Data: {data}]')

        hid_device.close()

        if constant_rd.DEBUG:
            print(f'Device closed')

        # Display data using a label
        data_label['text'] = data

        return data

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')


def test(devices, device_name, data_label):
    """ Let the user perform a joystick test """

    if device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device must be selected.')

        return

    device = get_device(devices, device_name)  # Get device by name
    hid_device = hid.device()
    hid_device.open(device['vendor_id'], device['product_id'])

    try:
        # TODO: Fix test release (currently needs to hold escape key while using joystick)
        while not keyboard.is_pressed('escape'):
            data = hid_device.read(16)
            action = []

            # Atari 2600 CX40 Joystick

            if data[0] == 0:
                action += 'L'

            if data[0] == 255:
                action += 'R'

            if data[1] == 0:
                action += 'U'

            if data[1] == 255:
                action += 'D'

            if data[2] == 1:
                action += '1'

            string = f'Data: {data}, Action: {action}'

            if constant_rd.DEBUG:
                print(string)

            # Display data using a label
            # TODO: Fix display updating (currently only updates UI when exiting loop)
            data_label['text'] = string

    finally:
        hid_device.close()


def write(files, file_name, devices, device_name):
    if file_name in ('', 'None') or device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Configuration and device must be selected.')

        return

    # Get data from Intel HEX file
    file = get_file(files, file_name)
    intel_hex = io_rd.get_intel_hex(file)
    data = io_rd.get_data(intel_hex)

    # Get device by name
    device = get_device(devices, device_name)

    # Write data to device
    try:
        if constant_rd.DEBUG:
            print(f'Opening device')

        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(0)

        if constant_rd.DEBUG:
            print(f'Writing to device')
            print(f'Data: {data}')

        for block in data:
            if constant_rd.DEBUG:
                print(f'Block: {block}')

            hid_device.write(block)

        hid_device.close()

        if constant_rd.DEBUG:
            print(f'Device closed')

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')

    messagebox.showinfo('Success', 'Successfully written configuration to device.')
