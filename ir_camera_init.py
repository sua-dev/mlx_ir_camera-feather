# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio
import adafruit_mlx90640
from adafruit_datetime import datetime
from screen_dynamics import i2c

import rtc

import adafruit_ds3231

ONBOARD_LED = digitalio.DigitalInOut(board.LED)
ONBOARD_LED.direction = digitalio.Direction.OUTPUT


PRINT_TEMPERATURES = False
PRINT_ASCIIART = True
DEGREE_SHIFT = 5

NUMBER_OF_FRAMES = 5000


TEMP_PATH = "images/temperature"
ASCIIART_PATH = "images/ascii"

# i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)



mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
# print([hex(i) for i in mlx.serial_number])

ds_rtc = adafruit_ds3231.DS3231(i2c)

# print("Setting time")
# # REFERENCE : (2017, 10, 29, 15, 14, 15, 0, -1, -1)
# t = time.struct_time((2024,1,30,15,5,0,0,-1,-1))
# ds_rtc.datetime = t
# print("Time Set")
current_time = ds_rtc.datetime

# print(current_time)


mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

def int_list_to_bytearray(float_list):
    byte_array = bytearray()
    int_list = []
    for value in float_list:
        # Convert float to bytes using struct.pack
        # byte_representation = struct.pack('!f', value)
        # int_representation = struct.pack('i',value)
        int_representation = int(value *  DEGREE_SHIFT)
        int_list.append(int_representation)
    # print(int_list)
        # Iterate over bytes and convert each to an integer
    for byte in int_list:
        byte_array.append(byte)

    return byte_array

def capture_frames():
    maxval = 255
    frame = [0] * 768
    count = 1
    frame_number = []
    ascii_char = []
    # Can also replace the line below with while True for number of frames is unknown 
    # while count < NUMBER_OF_FRAMES:
    while True:
        frame_number.clear()
        ONBOARD_LED.value = True
        print("FRAME No. {}".format(count))
        stamp = time.monotonic()
        try:
            mlx.getFrame(frame)
        except ValueError:
            # these happen, no biggie - retry
            continue
        print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
        for h in range(24):
            for w in range(32):
                t = frame[h * 32 + w]
                frame_number.append(t)
                if PRINT_TEMPERATURES:
                    print("%0.1f, " % t, end="")
                if PRINT_ASCIIART:
                    c = "&"
                    # pylint: disable=multiple-statements
                    if t < 20:
                        c = " "
                    elif t < 23:
                        c = "."
                    elif t < 25:
                        c = "-"
                    elif t < 27:
                        c = "*"
                    elif t < 29:
                        c = "+"
                    elif t < 31:
                        c = "x"
                    elif t < 33:
                        c = "%"
                    elif t < 35:
                        c = "#"
                    elif t < 37:
                        c = "X"
                    # pylint: enable=multiple-statements
                    print(c, end="")
                    ascii_char.append(c)
            print()
        print()
        # print(frame_number)

        image = int_list_to_bytearray(frame_number)

        # tp = None
        # temp_path = TEMP_PATH + "_" + "{}".format(count) + ".txt"
        # with open(temp_path, 'w') as file:
        #     for h in range(24):
        #         for w in range(32):
        #             tp = frame[h * 32 + w]
        #             file.write("{}".format(tp) + " ")
        #         file.write('\n')
        #     file.write('\n')


        # ascii_path = ASCIIART_PATH + "_" + "{}".format(count) + ".txt"
        # with open(ascii_path, 'w') as file_ascii:
        #     for h in range(24):
        #         for w in range(32):
        #             tp = frame[h * 32 + w]
        #             c = "&"
        #             # pylint: disable=multiple-statements
        #             if tp < 20:
        #                 c = " "
        #             elif tp < 23:
        #                 c = "."
        #             elif t < 25:
        #                 c = "-"
        #             elif tp < 27:
        #                 c = "*"
        #             elif tp < 29:
        #                 c = "+"
        #             elif tp < 31:
        #                 c = "x"
        #             elif tp < 33:
        #                 c = "%"
        #             elif t < 35:
        #                 c = "#"
        #             elif tp < 37:
        #                 c = "X"
        #             # pylint: enable=multiple-statements
        #             file_ascii.write(c)
        #             # file.write("{}".format(temp), end="")
        #         file_ascii.write('\n')
        #     file_ascii.write('\n')

        # r = rtc.RTC()
        # rtc.set_time_source()
        # r.datetime = current_time
        # x = current_time
        print("Stored in file: {:02}_{:02}_{}_{:02}_{:02}_{:02}__{}.pgm".format(
                current_time[2],
                current_time[1],
                current_time[0],
                current_time[3],
                current_time[4],
                current_time[5],
                count
            ))
        FILE_PATH_DATE ="images/{:02}_{:02}_{}_{:02}_{:02}_{:02}__{}.pgm".format(
                current_time[2],
                current_time[1],
                current_time[0],
                current_time[3],
                current_time[4],
                current_time[5],
                count
            )
        
        pgm_header = f"P5 {w+1} {h+1} {maxval}\n"
        print(pgm_header)
        with open(FILE_PATH_DATE, "wb") as image_file:
            #PGM Header - Portable PixMap
            image_file.write(bytearray(pgm_header, 'ascii'))
            image_file.write(image)

        print("Done")
        ONBOARD_LED.value = False
        time.sleep(1)
        count +=1
            # for i in ascii_char:
            #     file.write(i)
            # file.write('\n')