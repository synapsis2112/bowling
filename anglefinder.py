"""Bowling ball angle finder

This script takes the dual angle layout of a bowling ball in degrees and
converts it to inches.
It expects 3 arguments in the following order:
a drill angle, a pin to pap distance, and a val angle.

Example usage:
$ python anglefinder.py 50 4.5 55
PSA to PAP = 4-2/8in
Pin to PAP = 4.5in
Pin Buffer = 3-3/8in

Author: Matt Moran
Date: 9/26/2019
"""

import math
import sys


def get_nearest_eighth(num):
    """Round a number to the nearest 8th of an inch.

    Arguments:
    num -- The psa2pap or pin_buffer to round.
    """

    low_num = math.floor(num * 8) / 8
    high_num = math.ceil(num * 8) / 8
    if (num - low_num) < (high_num - num):
        return low_num
    return high_num

if __name__ == '__main__':
    drill_angle = sys.argv[1]
    pin2pap = sys.argv[2]
    val_angle = sys.argv[3]

    psa2pap = math.acos(math.sin(float(pin2pap)*math.pi/13.5)*math.cos(float(
        drill_angle)*math.pi/180))*13.5/math.pi
    pin_buffer = math.asin(math.sin(float(pin2pap)*math.pi/13.5)*math.sin(
        float(val_angle)*math.pi/180))*13.5/math.pi

    psa2pap_rounded = get_nearest_eighth(psa2pap)
    pin_buffer_rounded = get_nearest_eighth(pin_buffer)

    print("PSA to PAP = {}-{}/8in".format(int(psa2pap_rounded),
          int(round(psa2pap_rounded % 1, 3) * 8)))
    print("Pin to PAP = {}in".format(pin2pap))
    print("Pin Buffer = {}-{}/8in".format(int(pin_buffer_rounded),
          int(round(pin_buffer_rounded % 1, 3) * 8)))

