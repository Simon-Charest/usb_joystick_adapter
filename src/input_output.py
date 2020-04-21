#!/usr/bin/python
# coding=utf-8

import constants


def print_keys(device):
    keys = device.keys()
    print()

    for key in keys:
        print(f'{key}: {device[key]}')


def read_lines(file):
    with open(file) as stream:
        lines = stream.readlines()

        # for line in lines:

    return lines


def read(file):
    with open(file, 'r') as stream:
        return read_hexadecimal(stream)


def read_hexadecimal(stream):
    return ['{:02x}'.format(ord(c)) for c in stream.read()]
