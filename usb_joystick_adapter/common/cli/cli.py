from usb_joystick_adapter.common.constant import constant
from usb_joystick_adapter.common.gui import gui
from usb_joystick_adapter.common.io_ import io
from usb_joystick_adapter.common.usb import usb
import sys

# Global constants definitions
EOF = '\n'  # End of line
CONFIGURATION_EXAMPLE = 'Atari_C64_Amiga_Joystick_v3.1'
DEVICE_EXAMPLE = '388b5e99'
# DEVICE_EXAMPLE = '25d1adf4'
CLI_EXECUTE = 'python -m usb_joystick_adapter'
# CLI_EXECUTE = 'python usb_joystick_adapter.py'
USAGE = f'Usage:{EOF}'\
        f'  {CLI_EXECUTE} [-b] [-c:"configuration"] [-d:"device"] [-g] [-l:c | -l:d] [-r] [-t] [-w]' \
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
        f'  {CLI_EXECUTE} -b -c:"{CONFIGURATION_EXAMPLE}"{EOF}'\
        f'  {CLI_EXECUTE} -c:"{CONFIGURATION_EXAMPLE}" -d:"{DEVICE_EXAMPLE}" -w{EOF}'\
        f'  {CLI_EXECUTE} -d:"{DEVICE_EXAMPLE}" -r{EOF}'\
        f'  {CLI_EXECUTE} -d:"{DEVICE_EXAMPLE}" -t{EOF}'\
        f'  {CLI_EXECUTE} -g{EOF}'\
        f'  {CLI_EXECUTE} -l:a{EOF}'\
        f'  {CLI_EXECUTE} -l:c{EOF}'\
        f'  {CLI_EXECUTE} -l:d{EOF}'


def execute():
    if constant.ARGV_OVERRIDE:
        sys.argv = constant.ARGV_OVERRIDE.split(' ')

    if constant.DEBUG:
        print(f'sys.argv: {sys.argv}')
        print(f'len(sys.argv): {len(sys.argv)}')

    # Extract keys and values from arguments
    configuration_key = '-c:'
    configuration_argument = get_argument(get_sublist(sys.argv, configuration_key))
    configuration_file_name = get_file_name(configuration_argument)
    device_key = '-d:'
    device_argument = get_argument(get_sublist(sys.argv, device_key))
    device_name = get_device(device_argument)

    if constant.DEBUG:
        print(f'configuration_key: {configuration_key}')
        print(f'configuration_argument: {configuration_argument}')
        print(f'configuration_file_name: {configuration_file_name}')
        print(f'device_key: {device_key}')
        print(f'device_argument: {device_argument}')

    # Manage input arguments
    if len(sys.argv) == 3 and '-b' in sys.argv and configuration_argument:
        usb.load_hid_boot_cli(configuration_file_name)

    elif len(sys.argv) == 4 and configuration_argument and device_argument and '-w' in sys.argv:
        usb.write_cli(configuration_file_name, device_name)

    elif len(sys.argv) == 3 and device_argument and '-r' in sys.argv:
        usb.read_cli(device_name)

    elif len(sys.argv) == 3 and device_argument and '-t' in sys.argv:
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


def get_argument(sublist):
    if sublist:
        return sublist[0]

    return None


def get_file_name(argument):
    if not argument:
        return None

    start = argument.find(':') + 1
    file_name = argument[start:]

    return f'{constant.ROOT_DIR}/data/{file_name}.hex'


def get_device(device_argument):
    # TODO: Dev this
    return ''


def get_sublist(list_, substring):
    """ Return sublist of elements where substring is found in list_ """

    sublist = [string for string in list_ if substring in string]

    if constant.DEBUG:
        print(f'Haystack: {list_}')
        print(f'Needle: {substring}')
        print(f'Value: {sublist}')

    return sublist


def get_value(string, substring):
    """
    Extract value starting after substring
    Example: get_value('-c:"Atari_C64_Amiga_Joystick_v3.1"', '-c:') == 'Atari_C64_Amiga_Joystick_v3.1'
    """

    start_position = string.find(substring) + len(substring)
    value = string[start_position:]

    return value


def print_list(list_):
    if list_:
        for element in list_:
            print(element)
