from common.constant import constant
import glob
import os


def get_bytes(data, left_trim=0, right_trim=0):
    return [data[x:x + 2] for x in range(left_trim, len(data) - right_trim, 2)]


def convert_to_int(bytes_):
    int_ = [int(b, 16) for b in bytes_]

    return int_


def get_file_names(files):
    return [os.path.splitext(os.path.basename(file))[0] for file in files]


def get_files(path):
    files = glob.glob(path)

    if constant.DEBUG:
        print(f'Path: {path}')
        print(f'Files: {files}')

    return glob.glob(path)


def get_intel_hex(file):
    lines = read_lines(file)
    intel_hex = list()

    for line in lines:
        line = line.rstrip()
        start_code = line[0:1]
        byte_count = line[1:3]
        byte_count_decimal = int(byte_count, 16)
        address = line[3:7]
        record_type = line[7:9]
        record_type_description = get_record_type(record_type)

        if record_type == '00':
            data = line[9:(2 * byte_count_decimal + 9)]

        else:
            data = ''

        data_justified = data.ljust(32, 'F')
        data_bytes = get_bytes(data_justified)
        data_int = convert_to_int(data_bytes)
        checksum = line[-2:]
        checksum_decimal = int(checksum, 16)
        bytes_ = get_bytes(line, 1, 2)
        sum_ = get_sum(bytes_)
        json = {
            'start_code': start_code,
            'byte_count': byte_count,
            'byte_count_decimal': byte_count_decimal,
            'address': address,
            'record_type': record_type,
            'record_type_description': record_type_description,
            'data': data,
            'data_justified': data_justified,
            'data_bytes': data_bytes,
            'data_int': data_int,
            'checksum': checksum,
            'checksum_decimal': checksum_decimal,
            'bytes_': bytes_,
            'sum_': sum_
        }

        if checksum_decimal != sum_:
            print(f"Calculated checksum {format(sum_, 'X')} mismatch checksum {checksum} in {intel_hex}")
            raise ValueError('Value Error: Checksum mismatch.')

        intel_hex.append(json)

    if constant.DEBUG:
        print(f'Intel HEX: {intel_hex}')

    return intel_hex


def get_record_type(hex_code):
    record_type = ''

    if hex_code == '00':
        record_type = 'Data'

    elif hex_code == '01':
        record_type = 'End Of File'

    elif hex_code == '02':
        record_type = 'Extended Segment Address'

    elif hex_code == '03':
        record_type = 'Start Segment Address'

    elif hex_code == '04':
        record_type = 'Extended Linear Address'

    elif hex_code == '05':
        record_type = 'Start Linear Address'

    return record_type


def get_sum(bytes_):
    sum_ = 0

    for byte in bytes_:
        sum_ += int(byte, 16)

    sum_ = sum_ % 256

    if sum_ > 0:
        sum_ = 256 - sum_

    return sum_


def print_keys(device):
    keys = device.keys()
    print()

    for key in keys:
        print(f'{key}: {device[key]}')


def read(file):
    with open(file) as stream:
        return read_hexadecimal(stream)


def read_hexadecimal(stream):
    return ['{:02x}'.format(ord(c)) for c in stream.read()]


def read_integer(stream):
    return [ord(c) for c in stream.read()]


def read_lines(file):
    with open(file) as stream:
        lines = stream.readlines()

    return lines
