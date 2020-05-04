from common.gui import gui
import sys

# Global constants definitions
EOF = '\n'  # End of line
CONFIGURATION_EXAMPLE = 'Atari_C64_Amiga_Joystick_v3.1'
DEVICE_EXAMPLE = '25d1adf4'
USAGE = f'Usage:{EOF}'\
        f'  python usb_joystick_adapter.py [-c:"configuration"] [-d:"device"] [-g] [-l] [-r] [-t] [-w]{EOF}'\
        f'Switches:{EOF}'\
        f'  -c Specify Universal Serial Bus (USB) Human Interface Device (HID) configuration file name{EOF}'\
        f'  -d Specify device name{EOF}'\
        f'  -g Start application in Graphical User Interface (GUI) mode{EOF}'\
        f'  -l List compatible devices{EOF}'\
        f'  -r Read Device mode{EOF}'\
        f'  -t Test Device mode{EOF}'\
        f'  -w Write configuration data to device{EOF}'\
        f'Examples:{EOF}'\
        f'  python usb_joystick_adapter.py -c:"{CONFIGURATION_EXAMPLE}" -d:"{DEVICE_EXAMPLE}" -w{EOF}'\
        f'  python usb_joystick_adapter.py -d:"{DEVICE_EXAMPLE}" -r{EOF}'\
        f'  python usb_joystick_adapter.py -d:"{DEVICE_EXAMPLE}" -t{EOF}'\
        f'  python usb_joystick_adapter.py -g{EOF}'\
        f'  python usb_joystick_adapter.py -l'


def execute():
    # Manage input arguments
    if intersect(['-g'], sys.argv):
        gui.execute()

    # elif len(sys.argv) == 2:
    #     keys = sys.argv[2].split(':')

    else:
        print(USAGE)
        exit()

    return


def intersect(list1, list2):
    return [element for element in list1 if element in list2]
