"""
Gives a rough value of the position of a variable capacitor of the size found in old
radios' tuning circuit. They are of the order of 10pf - 200pF and by pulsing a digital IO pin
connected to one side of the capacitor and making an analog reading on the other you can get
a rough reading that is fairly proportional to the capacitors position. It is not linear.
"""

import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn

NUM_READINGS = 20
MIN_READING = 0
MAX_READING = 65535
SCALE_READING = 65535


def sample_input(input_pin, output_pin):
    min = 65535
    max = 0
    accumulate = 0
    for i in range(0, NUM_READINGS):
        output_pin.value = True
        val = input_pin.value
        output_pin.value = False
        accumulate = accumulate + val

        if val < min:
            min = val
        if val > max:
            max = val

    average = float(accumulate) / float(NUM_READINGS)
    return int((average - MIN_READING) / (MAX_READING - MIN_READING) * SCALE_READING), min, max


print("hello")
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

digital_out = DigitalInOut(board.GP16)
digital_out.direction = Direction.OUTPUT

analog_in = AnalogIn(board.A0)

old_v = 0
blink = True


def changed(a, b):
    """Make our output a bit less jittery"""
    return abs(a - b) > 1


while True:
    v, low, high = sample_input(analog_in, digital_out)
    if changed(old_v, v):
        led.value = blink
        blink = not blink
        print("value", v, low, high)
        old_v = v

