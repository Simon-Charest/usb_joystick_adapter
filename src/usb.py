#!/usr/bin/python
# coding=utf-8

import constant
import hid  # Package: hidapi


def get_all_devices():
    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    return hid.enumerate(0, 0)


def get_device(devices, device_name):
    for device in devices:
        if get_identifier(device['path']) in device_name:
            return device

    return None


def get_device_names(devices):
    if not devices:
        return None

    device_names = list()

    for device in devices:
        device_names.append(f"{get_product_string(device)} ({get_identifier(device['path'])})")

    return device_names


def get_devices(vendor_id, product_id, manufacturer_string, product_string):
    hid_devices = hid.enumerate(0, 0)

    if constant.DEBUG:
        print(f'HID Devices: {hid_devices}')

    devices = list()

    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    for hid_device in hid_devices:
        if constant.DEBUG:
            print(f'HID Device: {hid_device}')

        if hid_device['vendor_id'] in vendor_id and hid_device['product_id'] in product_id:
            devices.append(hid_device)

    return devices


def get_file(files, file_name):
    for file in files:
        if file_name in file:
            return file

    return None


def get_identifier(path):
    string = path.decode()  # Convert bytes to string
    paths = string.split('#')
    identifiers = paths[2].split('&')
    identifier = identifiers[1]  # Keep unique identifier

    if constant.DEBUG:
        print(f'Path: {path}')
        print(f'String: {string}')
        print(f'Paths: {paths}')
        print(f'Identifiers: {identifiers}')
        print(f'Identifier: {identifier}')

    return identifier


def get_manufacturer_string(device):
    # Patches a bug in the hardware which prevents the manufacturer_string to be read correctly upon plugging of the device

    if device['manufacturer_string']:
        return device['manufacturer_string']

    elif device['vendor_id'] == constant.VENDOR_ID and device['product_id'] == constant.PRODUCT_ID:
        return constant.MANUFACTURER_STRING

    elif device['vendor_id'] == constant.BOOT_VENDOR_ID and device['product_id'] == constant.BOOT_PRODUCT_ID:
        return constant.BOOT_MANUFACTURER_STRING


def get_product_string(device):
    # Patches a bug in the hardware which prevents the product_string to be read correctly upon plugging of the device

    if device['product_string']:
        return device['product_string']

    elif device['vendor_id'] == constant.VENDOR_ID and device['product_id'] == constant.PRODUCT_ID:
        return constant.PRODUCT_STRING

    elif device['vendor_id'] == constant.BOOT_VENDOR_ID and device['product_id'] == constant.BOOT_PRODUCT_ID:
        return constant.BOOT_PRODUCT_STRING


def read(device):
    try:
        if constant.DEBUG:
            print(f'Opening device')

        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(1)

        if constant.DEBUG:
            print(f'Reading from device')

        integers = hid_device.read()
        hid_device.close()

        if constant.DEBUG:
            print(f'Device closed')

        return integers

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')


def write(device, data):
    try:
        if constant.DEBUG:
            print(f'Opening device')

        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(0)

        if constant.DEBUG:
            print(f'Writing to device')
            print(f'Data: {data}')

        for block in data:
            if constant.DEBUG:
                print(f'Block: {block}')

            hid_device.write(block)

        hid_device.close()

        if constant.DEBUG:
            print(f'Device closed')

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')
