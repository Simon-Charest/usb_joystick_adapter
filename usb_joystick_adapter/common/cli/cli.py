from common.constant import constant
from common.gui import gui
import sys

# Global constants definitions
EOF = '\n'  # End of line
CONFIGURATION_EXAMPLE = 'Atari_C64_Amiga_Joystick_v3.1'
DEVICE_EXAMPLE = '25d1adf4'
USAGE = f'Usage:{EOF}'\
        f'  python usb_joystick_adapter.py [-c:"configuration"] [-d:"device"] [-g] [-l:c | -l:d] [-r] [-t] [-w]{EOF}'\
        f'Switches:{EOF}'\
        f'  -c Specify Universal Serial Bus (USB) Human Interface Device (HID) configuration file name{EOF}'\
        f'  -d Specify device name{EOF}'\
        f'  -g Start application in Graphical User Interface (GUI) mode{EOF}'\
        f'  -l:c List configuration file names{EOF}'\
        f'  -l:d List compatible devices{EOF}'\
        f'  -r Read Device mode{EOF}'\
        f'  -t Test Device mode{EOF}'\
        f'  -w Write configuration data to device{EOF}'\
        f'Examples:{EOF}'\
        f'  python usb_joystick_adapter.py -c:"{CONFIGURATION_EXAMPLE}" -d:"{DEVICE_EXAMPLE}" -w{EOF}'\
        f'  python usb_joystick_adapter.py -d:"{DEVICE_EXAMPLE}" -r{EOF}'\
        f'  python usb_joystick_adapter.py -d:"{DEVICE_EXAMPLE}" -t{EOF}'\
        f'  python usb_joystick_adapter.py -g{EOF}'\
        f'  python usb_joystick_adapter.py -l:c{EOF}'\
        f'  python usb_joystick_adapter.py -l:d{EOF}'


def execute():
    if constant.ARGV_OVERRIDE:
        sys.argv = constant.ARGV_OVERRIDE.split(' ')

    # Manage input arguments
    if len(sys.argv) == 4 and '-w' in sys.argv:
        print('TODO: Write configuration data to device')

    elif len(sys.argv) == 3 and '-r' in sys.argv:
        print('TODO: Read Device mode')

    elif len(sys.argv) == 3 and '-t' in sys.argv:
        print('TODO: Test Device mode')

    elif len(sys.argv) == 2 and sys.argv[1] == '-g':
        gui.execute()

    elif len(sys.argv) == 2 and sys.argv[1] == '-l:c':
        print('TODO: List configuration file names')

    elif len(sys.argv) == 2 and sys.argv[1] == '-l:d':
        print('TODO: List compatible devices')

    else:
        print(USAGE)
        exit()
