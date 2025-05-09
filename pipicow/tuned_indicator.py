import board
import pwmio
import math

# We wired up the tuned indicator in series with a
# 1K ohm resistor and an LED and carefully ramped up 
# the PWM output to derive this value.
# NB the tuned indicator is a straight DC device so do
# not wire it up backwards or the needle will bury into
# the endstop.

MAX_DEFLECTION = 14000

angle = 0.0 
step = math.pi * 2.0 / 30000.0

# 900Hz was arbitrary, you can hear the coil whine a bit at this
# rate. At 2000Hz it is not audible.
pwm = pwmio.PWMOut(board.GP17, frequency=900) 

while True:
    if angle > math.pi * 2.0:
        angle = 0.0
        
    pwm.duty_cycle = int((math.sin(angle) + 1.0) / 2.0 * MAX_DEFLECTION)
    angle = angle + step
