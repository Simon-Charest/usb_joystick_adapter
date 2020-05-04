from src.datetime_ import datetime

__author__ = 'Retronic Design'
__email__ = 'info@retronicdesign.com'
__copyright__ = f'Copyright © {datetime.get_years(2012)} {__author__} <{__email__}>. All rights reserved.'
__project__ = 'USB Joystick Adapter'
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
        'organization': ['SLCIT, Inc.', 'Retronic Design'],
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
ADAPTOR = {
    'boot': {
        'vendor_id': 0x16C0,  # hex: 0x16C0, int: 5824, bin: 0b1011011000000
        'product_id': 0x5DF,  # hex: 0x5DF, int: 1503, bin: 0b10111011111
        'manufacturer_string': 'obdev.at',
        'product_string': 'HIDBoot'
    },
    'operation': {
        'vendor_id': 0x810,  # hex: 0x810, int: 2064, bin: 0b100000010000
        'product_id': 0xE501,  # hex: 0xE501, int: 58625, bin: 0b1110010100000001
        'manufacturer_string': 'retronicdesign.com',
        'product_string': 'Atari C64 Amiga Joystick v3.1'
    }
}
DEBUG = True
FIRMWARE = '../bin/*.hex'
ICON = '../img/1f579.png'
