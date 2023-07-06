import random
import re


def process_dice_input(dice_input):
    pattern = re.compile(r'(\d*)D(3|6)\+*(\d*)')
    match = pattern.match(dice_input)

    if match:
        dice_count = match.group(1)
        dice_value = int(match.group(2))
        if dice_count == '':  # Default to 1 if no dice count is provided
            dice_count = 1
        else:
            dice_count = int(dice_count)

        plus_value = match.group(3)
        if plus_value == '':  # Default to 0 if no plus value is provided
            plus_value = 0
        else:
            plus_value = int(plus_value)

        dice_output = sum(max(1, random.randint(1, dice_value)) for _ in range(dice_count)) + plus_value
    elif dice_input.isdigit():
        dice_output = int(dice_input)
    else:
        print(f"Invalid attack input: '{dice_input}'")
        raise ValueError("Invalid attack input. Please enter a number or a format like '3D6' or 'D6+1' or 'D3'.")

    return dice_output


def process_input_value(input_value):
    if isinstance(input_value, str):
        if 'D' in input_value:
            return input_value
        elif input_value.isdigit():
            return int(input_value)
        else:
            raise ValueError("Invalid input. Please enter a number or a format like '3D6'.")
    elif isinstance(input_value, int):
        return input_value
    else:
        raise ValueError("Invalid input. Please enter a number or a format like '3D6'.")
