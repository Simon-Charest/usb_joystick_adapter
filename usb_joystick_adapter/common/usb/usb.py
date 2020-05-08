from common.constant import constant
from common.io_ import io
from tkinter import messagebox
import hid  # Package: hidapi
import keyboard
import subprocess


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

    if constant.DEBUG:
        print(f'HID Devices: {hid_devices}')

    devices = list()

    # Loop on all Universal Serial Bus (USB) Human Interface Devices (HID)
    for hid_device in hid_devices:
        if constant.DEBUG:
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

    if constant.DEBUG:
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

    elif device['vendor_id'] == constant.ADAPTOR['boot']['vendor_id'] and \
            device['product_id'] == constant.ADAPTOR['boot']['product_id']:
        return constant.ADAPTOR['boot']['manufacturer_string']

    elif device['vendor_id'] == constant.ADAPTOR['operation']['vendor_id'] and \
            device['product_id'] == constant.ADAPTOR['operation']['product_id']:
        return constant.ADAPTOR['operation']['manufacturer_string']


def get_product_string(device):
    """
        Get product name (ex: Atari C64 Amiga Joystick v3.2)
        Patches a bug in the hardware which prevents the product_string to be read correctly upon plugging the device
    """

    if device['product_string']:
        return device['product_string']

    elif device['vendor_id'] == constant.ADAPTER['boot']['vendor_id'] and \
            device['product_id'] == constant.ADAPTER['boot']['product_id']:
        return constant.ADAPTER['boot']['product_string']

    elif device['vendor_id'] == constant.ADAPTER['operation']['vendor_id'] and \
            device['product_id'] == constant.ADAPTER['operation']['product_id']:
        return constant.ADAPTER['operation']['product_string']


def load_hid_boot(files, file_name, data_label):
    if file_name in ('', 'None'):
        messagebox.showinfo('Information', 'Configuration must be selected.')

        return

    file = get_file(files, file_name)
    command = f'"{constant.BOOT_LOAD_HID}" -r "{file}"'

    if constant.DEBUG:
        print(f'Command: {command}')

    try:
        output_bytes = subprocess.check_output(command, stderr=subprocess.STDOUT)
        output_string = output_bytes.decode()

        if constant.DEBUG:
            print(f'Output Bytes: {output_bytes}')
            print(f'Output String: {output_string}')

        data_label['text'] = constant.SUCCESS

    except subprocess.CalledProcessError:
        data_label['text'] = constant.ERROR_COMMUNICATION


def read(devices, device_name, data_label):
    """ Read data from device """

    if device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Device must be selected.')

        return

    device = get_device(devices, device_name)  # Get device by name
    hid_device = hid.device()
    hid_device.open(device['vendor_id'], device['product_id'])

    try:
        if constant.DEBUG:
            print(f'Opening device')

        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(1)

        # TODO: Fix Input/Output Error Exception: get serial number string error
        # serial_number = hid_device.get_serial_number_string()

        # TODO: Fix Input/Output Error Exception: read error
        # feature_report = hid_device.get_feature_report(0x0, 0x80)

        # TODO: This is a test
        hid_device.send_feature_report(0x0)

        if constant.DEBUG:
            print(f'Device: {device}')
            print(f'HID Device: {hid_device}')
            print(f'Reading from device')

        # Read data from device
        data = None
        
        for address in range(0, 32512, 16):
            data = hid_device.read(address)  # TODO: Fix Input/Output Error Exception: read error
            print(f'Read: [Block: {int(address / 16)}, Address: {address}, Data: {data}]')

        hid_device.close()

        if constant.DEBUG:
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
    product = hid_device.get_product_string()

    try:
        # TODO: Fix test release (currently needs to hold escape key while using joystick)
        while not keyboard.is_pressed('escape'):
            data = hid_device.read(16)
            action = []

            """ Horizontal """

            if data[0] == 0:  # Left
                action += '←'

            elif data[0] == 128:  # Center
                pass

            elif data[0] == 255:  # Right
                action += '→'

            """ Vertical """

            if data[1] == 0:  # Up
                action += '↑'

            elif data[1] == 128:  # Center
                pass

            elif data[1] == 255:  # Down
                action += '↓'

            """ Buttons """

            if data[2] == 0:  # No Button
                pass

            elif data[2] in [1, 3]:  # Button 1 / A
                if 'Atari C64 Amiga Joystick' in product:
                    action += '1'

                elif 'Sega Genesis Joypad' in product:
                    action += 'A'

            elif data[2] == 8:  # Start button
                action += 'S'

            elif data[2] == 9:  # A and Start buttons
                action += 'AS'

            string = f'Data: {data}, Action: {action}'

            if constant.DEBUG:
                print(string)

            # Display data using a label
            # TODO: Fix display updating (currently only updates UI when exiting loop)
            data_label['text'] = string

    finally:
        hid_device.close()


def write(files, file_name, devices, device_name, data_label):
    if file_name in ('', 'None') or device_name in ('', 'None'):
        messagebox.showinfo('Information', 'Configuration and device must be selected.')

        return

    # Get data from Intel HEX file
    file = get_file(files, file_name)
    intel_hex = io.get_intel_hex(file)

    # Get device by name
    device = get_device(devices, device_name)

    # Write data to device
    try:
        if constant.DEBUG:
            print(f'Opening device')

        hid_device = hid.device(device['vendor_id'], device['product_id'])
        hid_device.open_path(device['path'])
        hid_device.set_nonblocking(0)

        if constant.DEBUG:
            print(f'Writing to device')

        for block in intel_hex:
            if constant.DEBUG:
                print(f'Block: {block}')

            if block['record_type'] != '01':  # if not End Of File
                # Write a block of 16 integer values
                # TODO: Dev/test this
                hid_device.write(block['data_int'])

                for byte in range(0, 16):
                    address_int = block['address_int'] + byte
                    address_hex = hex(address_int)
                    data_int = block['data_int'][byte]
                    data_hex = hex(byte)

                    if constant.DEBUG:
                        print(f'Byte: {byte}, Address (int): {address_int}, Address (hex): {address_hex}, '
                              f'Data (int): {data_int}, Data (hex): {data_hex}')

                    # Write an integer value, per address
                    # TODO: Fix Input/Output Error Exception: read error
                    # hid_device.get_feature_report(address_int, data_int)

        hid_device.close()

        if constant.DEBUG:
            print(f'Device closed')

        data_label['text'] = constant.SUCCESS

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')
