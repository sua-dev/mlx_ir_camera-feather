# # File Name: config.py
# # Author: Sherif Attia
# # Date created: 31/01/2024

# # Description: Main configuration file for the IR Thermal Camera project

import board
import busio
import time
import digitalio

# # external libraries
# import adafruit_pcf8523
# import adafruit_mlx90640

i2c = board.I2C()

# # RTC
# pc_rtc = adafruit_pcf8523.PCF8523(I2C)
# # rtc.datetime = time.struct_time((2024, 1, 31, 12, 31, 0, 0, -1, -1))
# current_time = pc_rtc.datetime
# # print("Time Set")

# # MLX90640
# mlx = adafruit_mlx90640.MLX90640(I2C)
