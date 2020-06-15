from usb_joystick_adapter import app
import hid
import time


# TODO: Continue this
def test(vendor_id=0x810, product_id=0xE501):  # Read Mode (Atari C64 Amiga Joystick v3.1)
    # Write Mode (HIDBoot)
    # vendor_id = 0x16C0
    # product_id = 0x5DF

    print('Get all HID devices')
    devices = hid.enumerate()

    print('Get path of first Retronic Design device in Read Mode')
    path = None

    for device in devices:
        if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
            path = device['path']

            break

    print(f'path: {path}')

    print('Get instance of HID Device object')
    hid_device = hid.device(vendor_id, product_id)
    print(f'vendor_id: {vendor_id}')
    print(f'product_id: {product_id}')
    print(f'hid_device: {hid_device}')

    print('Open Retronic Design device')
    hid_device.open(vendor_id, product_id)

    print('Get manufacturer')
    manufacturer = hid_device.get_manufacturer_string()
    print(f'manufacturer: {manufacturer}')

    print('Get product')
    product = hid_device.get_product_string()
    print(f'product: {product}')

    # OSError: get serial number string error
    # print('Get serial number')
    # serial_number = hid_device.get_serial_number_string()
    # print(serial_number)

    print('Set device non-blocking')
    hid_device.set_nonblocking(1)

    # print('Open device path')
    # hid_device.open_path(path)

    # OSError: read error
    # print('Get feature report')
    # feature_report = hid_device.get_feature_report(0x0, 0x80)

    # print('Send feature report')
    # hid_device.send_feature_report(0x0)

    address_min = 0x0000
    address_max = 0x7f00
    size = 16

    # Source: https://github.com/gbishop/cython-hidapi/blob/master/try.py
    print('Write to device')
    for address_start in range(address_min, address_max, size):
        for i in [0, 1]:
            for j in [0, 1]:
                data = [0x80, i, j]
                hid_device.write(data)

                print(f'data: {data}')

    print('Read from device')
    for address_start in range(address_min, address_max, size):
        block = int(address_start / size)
        address_end = address_start + size - 1
        data = hid_device.read(address_start)

        print(f'block: {block}, address: [{address_start}-{address_end}], data: {data}')

    print('Closing device')
    hid_device.close()

    print('Done')


if __name__ == '__main__':
    app.run()
    # test()
