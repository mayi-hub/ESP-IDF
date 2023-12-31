#!/usr/bin/env python
#
# SPDX-FileCopyrightText: 2020-2023 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0
#

import argparse
import re
import subprocess
from typing import Tuple

argparser = argparse.ArgumentParser()

argparser.add_argument('readelf')
argparser.add_argument('elf')

args = argparser.parse_args()

# Get the content of the readelf command
contents = subprocess.check_output([args.readelf, '-S', args.elf]).decode()


# Define a class for readelf parsing error
class ParsingError(Exception):
    pass


# Look for the start address and size of any section
def find_partition_info(sectionname):  # type: (str) -> Tuple[int, int, int]
    match = re.search(sectionname + r'\s+PROGBITS\s+([a-f0-9]+) [a-f0-9]+ ([a-f0-9]+) \d+\s+[A-Z]+  0   0 (\d+)',
                      contents)
    if not match:
        raise ParsingError('ELF header parsing error')
    # Return the address of the section, the size and the alignment
    address = match.group(1)
    size = match.group(2)
    alignment = match.group(3)
    return (int(address, 16), int(size, 16), int(alignment, 10))


# Get address and size for .flash.appdesc section
app_address, app_size, app_align = find_partition_info('.flash.appdesc')

# Same goes for .flash.rodata section
rodata_address, _, rodata_align = find_partition_info('.flash.rodata')

# Assert than everything is as expected:
# appdesc is aligned on 16
# rodata is aligned on 64
# appdesc ends where rodata starts
assert app_align == 16, '.flash.appdesc section should have been aligned on 16!'
assert rodata_align == 64, '.flash.rodata section should have been aligned on 64!'
assert app_address + app_size == rodata_address, ".flash.appdesc's end address and .flash.rodata's begin start must have no gap in between!"
