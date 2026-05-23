#!/usr/bin/env python3
"""
Bowling Ball Angle Finder

Converts a dual-angle bowling ball layout into approximate VLS-style
measurements using a spherical bowling ball model.

Input:
    drill_angle  pin_to_pap  val_angle

Example:
    python anglefinder.py 50 4.5 55

Output:
    PSA to PAP = 4 1/4"
    Pin to PAP = 4 1/2"
    Pin Buffer = 3 3/8"

Notes:
    - This script models the bowling ball as a sphere.
    - A bowling ball has an approximate circumference of 27 inches.
    - Radius is therefore approximately 27 / (2 * pi), which simplifies
      to 13.5 / pi.
    - Results are rounded to the nearest 1/8 inch.
    - Pin-to-PAP values above 6.75 inches generally do not make practical
      sense for standard layout geometry because 6.75 inches represents
      approximately 90 degrees around the ball surface.

Author:
    Matt Moran

Original Date:
    9/26/2019
"""

import argparse
import math
import sys
from fractions import Fraction


BALL_CIRCUMFERENCE_INCHES = 27.0
BALL_RADIUS_INCHES = BALL_CIRCUMFERENCE_INCHES / (2 * math.pi)
MAX_PRACTICAL_PIN_TO_PAP = BALL_CIRCUMFERENCE_INCHES / 4  # 6.75 inches
ROUNDING_DENOMINATOR = 8


def round_to_nearest_eighth(value):
    """
    Round a decimal inch value to the nearest 1/8 inch.
    """
    return round(value * ROUNDING_DENOMINATOR) / ROUNDING_DENOMINATOR


def format_inches(value):
    """
    Format a decimal inch value as a clean mixed fraction.

    Examples:
        4.0   -> 4"
        4.125 -> 4 1/8"
        4.25  -> 4 1/4"
        4.5   -> 4 1/2"
        3.375 -> 3 3/8"
    """
    rounded = round_to_nearest_eighth(value)

    whole_inches = int(rounded)
    fractional_part = rounded - whole_inches

    if math.isclose(fractional_part, 0.0, abs_tol=0.000001):
        return f'{whole_inches}"'

    fraction = Fraction(fractional_part).limit_denominator(ROUNDING_DENOMINATOR)

    # Handles rare case where rounding pushes fraction to 1 whole inch
    if fraction.numerator == fraction.denominator:
        return f'{whole_inches + 1}"'

    return f'{whole_inches} {fraction.numerator}/{fraction.denominator}"'


def validate_angle(name, value):
    """
    Validate that an angle is within a practical bowling-layout range.
    """
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0 degrees.")

    if value >= 180:
        raise ValueError(
            f"{name} must be less than 180 degrees. "
            "Typical bowling layout angles are usually much lower than this."
        )


def validate_pin_to_pap(value):
    """
    Validate pin-to-PAP distance.
    """
    if value <= 0:
        raise ValueError("Pin-to-PAP distance must be greater than 0 inches.")

    if value > MAX_PRACTICAL_PIN_TO_PAP:
        raise ValueError(
            f"Pin-to-PAP distance of {value} inches is above the practical "
            f"maximum of {MAX_PRACTICAL_PIN_TO_PAP:.2f} inches. "
            "For standard bowling ball layout geometry, pin-to-PAP should "
            "usually be between 0 and 6.75 inches."
        )


def calculate_psa_to_pap(drill_angle_degrees, pin_to_pap_inches):
    """
    Calculate approximate PSA-to-PAP distance in inches.

    Uses spherical geometry based on the surface of a bowling ball.
    """
    pin_angle_radians = pin_to_pap_inches / BALL_RADIUS_INCHES
    drill_angle_radians = math.radians(drill_angle_degrees)

    value = math.sin(pin_angle_radians) * math.cos(drill_angle_radians)

    # Protect against tiny floating point errors outside [-1, 1]
    value = max(-1.0, min(1.0, value))

    return math.acos(value) * BALL_RADIUS_INCHES


def calculate_pin_buffer(val_angle_degrees, pin_to_pap_inches):
    """
    Calculate approximate pin buffer in inches.

    Uses spherical geometry based on the surface of a bowling ball.
    """
    pin_angle_radians = pin_to_pap_inches / BALL_RADIUS_INCHES
    val_angle_radians = math.radians(val_angle_degrees)

    value = math.sin(pin_angle_radians) * math.sin(val_angle_radians)

    # Protect against tiny floating point errors outside [-1, 1]
    value = max(-1.0, min(1.0, value))

    return math.asin(value) * BALL_RADIUS_INCHES


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Convert a dual-angle bowling ball layout to approximate "
            "PSA-to-PAP and pin-buffer measurements."
        )
    )

    parser.add_argument(
        "drill_angle",
        type=float,
        help="Drilling angle in degrees. Example: 50"
    )

    parser.add_argument(
        "pin_to_pap",
        type=float,
        help="Pin-to-PAP distance in inches. Example: 4.5"
    )

    parser.add_argument(
        "val_angle",
        type=float,
        help="VAL angle in degrees. Example: 55"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        validate_angle("Drilling angle", args.drill_angle)
        validate_pin_to_pap(args.pin_to_pap)
        validate_angle("VAL angle", args.val_angle)

        psa_to_pap = calculate_psa_to_pap(args.drill_angle, args.pin_to_pap)
        pin_buffer = calculate_pin_buffer(args.val_angle, args.pin_to_pap)

        print(f"PSA to PAP = {format_inches(psa_to_pap)}")
        print(f"Pin to PAP = {format_inches(args.pin_to_pap)}")
        print(f"Pin Buffer = {format_inches(pin_buffer)}")

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
