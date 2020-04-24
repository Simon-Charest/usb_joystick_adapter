#!/usr/bin/python
# coding=utf-8


def get_hid_report(device):
    transferred_bytes = device.ctrl_transfer(0xA1, 1, 0x200, 0x00, 64)

    return transferred_bytes
