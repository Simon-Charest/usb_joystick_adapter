from common.datetime_ import datetime

__author__ = 'Retronic Design'
__email__ = 'info@retronicdesign.com'
__copyright__ = f'Copyright © {datetime.get_years(2012)} {__author__} <{__email__}>. All rights reserved.'
__project__ = 'DB9 to USB Game Controller Adapter'
__credits__ = {
    'Francis-Olivier Gradel, Eng.': {
        'organization': f'{__author__}',
        'product': f'{__project__}',
        'email': f'{__email__}',
        'eBay': 'https://www.ebay.com/usr/retronicdesign',
        'Facebook': 'https://www.facebook.com/retronicdesign',
        'LinkedIn': 'https://ca.linkedin.com/in/francis-gradel-ing-b620591a',
        'Twitter': 'https://twitter.com/fogradel',
        'Website': 'retronicdesign.com',
        'AtariAge': 'https://atariage.com/forums/profile/37766-nitz1976/'
       },
    'Simon Charest': {
        'organization': ['SLCIT, Inc.', f'{__author__}'],
        'email': ['simoncharest@gmail.com', 'simoncharest@retronicdesign.com'],
        'Facebook': 'https://www.facebook.com/simon.charest/',
        'GitHub': 'https://github.com/Simon-Charest',
        'LinkedIn': 'https://www.linkedin.com/in/simoncharest/',
        'Twitter': 'https://twitter.com/scharest'
    },
    'Gary Bishop': {
        'organization': 'University of North Carolina - Computer Science',
        'product': 'HIDAPI',
        'email': 'gb@cs.unc.edu',
        'GitHub': 'https://github.com/gbishop',
        'Twitter': 'https://twitter.com/gbishop',
        'Website': 'http://www.cs.unc.edu/~gb/'
    }
}
__license__ = 'GNU'
__maintainer__ = 'Francis-Olivier Gradel, Eng. and Simon Charest'
__status__ = 'Developement'
__version__ = '4.0.0'

ABOUT = f'{__project__}\n' \
        f'Version {__version__}\n' \
        f'{__copyright__}\n' \
        f'\n' \
        f'The {__project__} and its software are the propriety of ' \
        f'{__author__}.\n' \
        f'The hardware is sold without any warranty. The software is open-source and ' \
        f'provided free of charge.\n' \
        f'Both are to be used with specific devices with DB9 connectors.\n' \
        f'\n' \
        f'This product is license under the {__license__} License Terms.'
ADAPTER = {
    'boot': {
        'vendor_id': 0x16C0,  # hex: 0x16C0, int: 5824, bin: 0001 0110 1100 0000
        'vendor_description': 'Van Ooijen Technische Informatica',
        'vendor_owner': 'Wouter van Ooijen',
        'vendor_address': 'Utrechtseweg 173, 3818 ED Amersfoort, Netherlands',
        'vendor_phone': '+31 6 38150444',
        'vendor_website': 'https://www.voti.nl/e_index.html',
        'product_id': 0x5DF,  # hex: 0x5DF, int: 1503, bin: 0101 1101 1111
        'product_description': 'HID device except mice, keyboards, and joysticks',
        'manufacturer_string': 'obdev.at',
        'manufacturer_description': 'Objective Development Software GmbH',
        'manufacturer_address': 'Grosse Schiffgasse 1A / 7, 1020 Vienna, Austria',
        'manufacturer_website': 'https://www.obdev.at/',
        'manufacturer_github': 'https://github.com/obdev',
        'manufacturer_linkedin': 'https://www.linkedin.com/company/objective-development-software-gmbh/people/',
        'product_string': 'HIDBoot'
    },
    'operation': {
        'vendor_id': 0x810,  # hex: 0x810, int: 2064, bin: 1000 0001 0000
        'product_id': 0xE501,  # hex: 0xE501, int: 58625, bin: 1110 0101 0000 0001
        'manufacturer_string': 'retronicdesign.com',
        'manufacturer_address': '3292, rue de Bergerac, Longueuil (Québec), J4M 2X8, Canada',
        'product_string': 'Atari C64 Amiga Joystick v3.1'
    }
}
# ARGV_OVERRIDE = 'usb_joystick_adapter.py -c:"Atari_C64_Amiga_Joystick_v3.1" -d:"25d1adf4" -w'
# ARGV_OVERRIDE = 'usb_joystick_adapter.py -d:"25d1adf4" -r'
# ARGV_OVERRIDE = 'usb_joystick_adapter.py -d:"25d1adf4" -t'
ARGV_OVERRIDE = 'usb_joystick_adapter.py -g'
# ARGV_OVERRIDE = 'usb_joystick_adapter.py -l:c'
# ARGV_OVERRIDE = 'usb_joystick_adapter.py -l:d'
BOOT_LOAD_HID = 'bin/bootloadHID.exe'
DEBUG = True
DEVICE_SIZE = 32768  # hex: 0x8000, int: 32768, bin: ‭1000 0000 0000 0000

# Output messages
ERROR_COMMUNICATION = 'Communication error with device.'
ERROR_DEVICE_NOT_FOUND = 'The specified device was not found'
ERROR_NO_SUCH_FILE = 'No such file or directory'
LAST_ADDRESSES = '0x07f00 ... 0x07f80'
SUCCESS = 'Successfully written configuration to device.'

FIRMWARE = 'data/*.hex'
ICON = 'resources/1f579.png'
PAGE_SIZE = 128  # hex: 0x80, int: 128, bin: 1000 0000
UPLOADING = 32640  # hex: 0x7f80, int: 32640, bin: 0111 1111 1000 0000

# Wireshark - USBPcap - usb.idVendor == 0x16C0

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
