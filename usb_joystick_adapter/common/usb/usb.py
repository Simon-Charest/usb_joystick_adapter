from common.constant import constant
from common.io_ import io
from tkinter import messagebox
import hid  # Package: hidapi
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


def write(files, file_name, devices, device_name):
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

            # TODO: Dev/test this
            hid_device.write(block['data_int'])

            # TODO: Fix TypeError: an integer is required
            # hid_device.get_feature_report(int(block['address'], 16), block['data_int'])

            # SET_IDLE Request
            # 0000   1c 00 50 60 3d 9a 06 9c ff ff 00 00 00 00 1b 00
            # 0010   00 01 00 1a 00 00 02 08 00 00 00 00 21 0a 00 00
            # 0020   00 00 00 00

            # SET_IDLE Response
            # 0000   1c 00 50 60 3d 9a 06 9c ff ff 00 00 00 00 08 00
            # 0010   01 01 00 1a 00 00 02 00 00 00 00 03

            # GET DESCRIPTOR Request STRING
            # 0000   1c 00 b0 e2 27 9b 06 9c ff ff 00 00 00 00 0b 00
            # 0010   00 01 00 1a 00 80 02 08 00 00 00 00 80 06 01 03
            # 0020   09 04 02 02

            # GET DESCRIPTOR Response STRING
            # 0000   1c 00 b0 e2 27 9b 06 9c ff ff 00 00 00 00 08 00
            # 0010   01 01 00 1a 00 80 02 12 00 00 00 03 12 03 6f 00
            # 0020   62 00 64 00 65 00 76 00 2e 00 61 00 74 00

            # GET DESCRIPTOR Request STRING
            # 0000   1c 00 b0 52 7d 92 06 9c ff ff 00 00 00 00 0b 00
            # 0010   00 01 00 1a 00 80 02 08 00 00 00 00 80 06 02 03
            # 0020   09 04 02 02

            # GET DESCRIPTOR Response STRING
            # 0000   1c 00 b0 52 7d 92 06 9c ff ff 00 00 00 00 08 00
            # 0010   01 01 00 1a 00 80 02 10 00 00 00 03 10 03 48 00
            # 0020   49 00 44 00 42 00 6f 00 6f 00 74 00

            # GET_REPORT Request
            # 0000   1c 00 a0 e9 d2 8f 06 9c ff ff 00 00 00 00 1b 00
            # 0010   00 01 00 1a 00 80 02 08 00 00 00 00 a1 01 01 03
            # 0020   00 00 84 00

            # GET_REPORT Response
            # 0000   1c 00 a0 e9 d2 8f 06 9c ff ff 00 00 00 00 08 00
            # 0010   01 01 00 1a 00 80 02 07 00 00 00 03 01 80 00 00
            # 0020   80 00 00

            # [...]

            # GET_REPORT Request
            # 0000   1c 00 a0 e9 67 99 06 9c ff ff 00 00 00 00 1b 00
            # 0010   00 01 00 1a 00 00 02 0f 00 00 00 00 21 09 01 03
            # 0020   00 00 07 00 01 00 7f 00 01 80 00

            # GET_REPORT Response
            # 0000   1c 00 a0 e9 67 99 06 9c ff ff 11 00 00 c0 08 00
            # 0010   01 01 00 1a 00 00 02 00 00 00 00 03

        hid_device.close()

        if constant.DEBUG:
            print(f'Device closed')

    except IOError as io_error:
        print(f'Input/Output Error Exception: {io_error}')

    except ValueError as value_error:
        print(f'Value Error Exception: {value_error}')

    messagebox.showinfo('Success', 'Successfully written configuration to device.')
