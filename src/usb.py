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


def get_file(files, file_name):
    for file in files:
        if file_name in file:
            return file

    return None


def get_device_names(devices):
    device_names = list()

    for device in devices:
        device_names.append(f"{device['product_string']} ({get_identifier(device['path'])})")

    return device_names


def get_devices(vendor_id, product_id, manufacturer_string, product_string):
    devices = list()

    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    for device in hid.enumerate(0, 0):
        if device['vendor_id'] in vendor_id and \
                device['product_id'] in product_id and \
                device['manufacturer_string'] in manufacturer_string and \
                device['product_string'] in product_string:
            devices.append(device)

    return devices


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


def write(device, data):
    try:
        print(f'Opening device')
        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(1)

        if constant.DEBUG:
            print(f'Manufacturer: {hid_device.get_manufacturer_string()}')
            print(f'Product: {hid_device.get_product_string()}')
            print(f'Data: {data}')

        for block in data:
            if constant.DEBUG:
                print(f'Block: {block}')

            hid_device.write(block)

        hid_device.close()
        print(f'Device closed')

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')
