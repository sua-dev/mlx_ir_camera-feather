# # File Name: config.py
# # Author: Sherif Attia
# # Date created: 31/01/2024

# # Description: Main configuration file for the IR Thermal Camera project

import board
import busio
import time
import digitalio
from adafruit_debouncer import Debouncer

# # external libraries
# import adafruit_pcf8523
# import adafruit_mlx90640

i2c = board.I2C()


def debouncable(pin):
    switch_io = digitalio.DigitalInOut(pin)
    switch_io.direction = digitalio.Direction.INPUT
    switch_io.pull = digitalio.Pull.UP
    return switch_io

# Initialize Buttons                        UM Feather S2   Feather M4
buttonA = Debouncer(debouncable(board.D5))  # 1              9
buttonB = Debouncer(debouncable(board.D21)) # 38            6 
buttonC = Debouncer(debouncable(board.D20)) # 33            5
# # RTC
# pc_rtc = adafruit_pcf8523.PCF8523(I2C)
# # rtc.datetime = time.struct_time((2024, 1, 31, 12, 31, 0, 0, -1, -1))
# current_time = pc_rtc.datetime
# # print("Time Set")

# # MLX90640
# mlx = adafruit_mlx90640.MLX90640(I2C)
