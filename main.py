from machine import Pin, PWM
import time

pwm = PWM(Pin(15))
pwm.freq(1000)

try:
    while True:
        # def: duty_u16 is 0 to 65535 (100%)
        # increase duty cycle by 500 steps / increase brightness
        # every 100ms
        for duty in range(0,65535,500): 
            pwm.duty_u16(duty)
            time.sleep(0.01)
        # decrease duty cycle by 500 steps / decrease brightness
        # every 100ms
        for duty in range(65535,0,-500):
            pwm.duty_u16(duty)
            time.sleep(0.01)

# clean-up 
finally:
    pwm.deinit()
    Pin(15,Pin.OUT).off()