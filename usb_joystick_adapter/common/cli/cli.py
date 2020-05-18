from usb_joystick_adapter.common.constant import constant
from usb_joystick_adapter.common.gui import gui
from usb_joystick_adapter.common.io_ import io
from usb_joystick_adapter.common.usb import usb
import sys

# Global constants definitions
EOF = '\n'  # End of line
CONFIGURATION_EXAMPLE = 'Atari_C64_Amiga_Joystick_v3.1'
DEVICE_EXAMPLE = '25d1adf4'
USAGE = f'Usage:{EOF}'\
        f'  python usb_joystick_adapter.py [-b] [-c:"configuration"] [-d:"device"] [-g] [-l:c | -l:d] [-r] [-t] [-w]' \
        f'{EOF}'\
        f'Switches:{EOF}'\
        f'  -b Load configuration data into HID Boot device{EOF}'\
        f'  -c Specify Universal Serial Bus (USB) Human Interface Device (HID) configuration file name{EOF}'\
        f'  -d Specify device name{EOF}'\
        f'  -g Start application in Graphical User Interface (GUI) mode{EOF}'\
        f'  -l:c List configuration file names{EOF}'\
        f'  -l:d List compatible devices{EOF}'\
        f'  -r Read Device mode{EOF}'\
        f'  -t Test Device mode{EOF}'\
        f'  -w Write configuration data to device{EOF}'\
        f'Examples:{EOF}'\
        f'  python usb_joystick_adapter.py -b -c:"{CONFIGURATION_EXAMPLE}"{EOF}'\
        f'  python usb_joystick_adapter.py -c:"{CONFIGURATION_EXAMPLE}" -d:"{DEVICE_EXAMPLE}" -w{EOF}'\
        f'  python usb_joystick_adapter.py -d:"{DEVICE_EXAMPLE}" -r{EOF}'\
        f'  python usb_joystick_adapter.py -d:"{DEVICE_EXAMPLE}" -t{EOF}'\
        f'  python usb_joystick_adapter.py -g{EOF}'\
        f'  python usb_joystick_adapter.py -l:a{EOF}'\
        f'  python usb_joystick_adapter.py -l:c{EOF}'\
        f'  python usb_joystick_adapter.py -l:d{EOF}'


def execute():
    if constant.ARGV_OVERRIDE:
        sys.argv = constant.ARGV_OVERRIDE.split(' ')

    if constant.DEBUG:
        print(f'sys.argv: {sys.argv}')
        print(f'len(sys.argv): {len(sys.argv)}')

    # Manage input arguments
    if len(sys.argv) == 3 and '-b' in sys.argv and is_substring_in(sys.argv, '-c:'):
        position = get_position(sys.argv, '-c:')
        configuration_file_name = sys.argv[position]
        usb.load_hid_boot_cli(configuration_file_name)

    elif len(sys.argv) == 4 and is_substring_in(sys.argv, '-c:') and is_substring_in(sys.argv, '-d:') \
            and '-w' in sys.argv:
        configuration_file_name_position = get_position(sys.argv, '-c:')
        device_name_position = get_position(sys.argv, '-d:')
        configuration_file_name = sys.argv[configuration_file_name_position]
        device_name = sys.argv[device_name_position]
        usb.write_cli(configuration_file_name, device_name)

    elif len(sys.argv) == 3 and is_substring_in(sys.argv, '-d:') and '-r' in sys.argv:
        device_name_position = get_position(sys.argv, '-d:')
        device_name = sys.argv[device_name_position]
        usb.read_cli(device_name)

    elif len(sys.argv) == 3 and is_substring_in(sys.argv, '-d:') and '-t' in sys.argv:
        device_name_position = get_position(sys.argv, '-d:')
        device_name = sys.argv[device_name_position]
        usb.test_cli(device_name)

    elif len(sys.argv) == 2 and sys.argv[1] == '-g':
        gui.execute()

    elif len(sys.argv) == 2 and sys.argv[1] == '-l:a':
        devices = usb.get_all_devices()
        device_names = usb.get_device_names(devices)
        print_list(device_names)

    elif len(sys.argv) == 2 and sys.argv[1] == '-l:c':
        files = io.get_files(constant.FIRMWARE)
        print_list(files)

    elif len(sys.argv) == 2 and sys.argv[1] == '-l:d':
        vendor_ids = [constant.ADAPTER['boot']['vendor_id'], constant.ADAPTER['operation']['vendor_id']]
        product_ids = [constant.ADAPTER['boot']['product_id'], constant.ADAPTER['operation']['product_id']]
        devices = usb.get_devices(vendor_ids, product_ids)
        device_names = usb.get_device_names(devices)
        print_list(device_names)

    else:
        print(USAGE)
        exit()


def get_position(arguments, needle):
    position = 0

    for argument in arguments:
        if argument.find(needle):
            return position

        position += 1


def is_substring_in(haystack, needle):
    return [string for string in haystack if needle in string]


def print_list(list_):
    if list_:
        for element in list_:
            print(element)
