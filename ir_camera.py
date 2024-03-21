# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio
import adafruit_mlx90640
from adafruit_datetime import datetime
from screen_dynamics import *
from config import buttonA, buttonB, buttonC, storage

import rtc
import gc
# import adafruit_ds3231
import adafruit_pcf8523

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

ds_rtc = adafruit_pcf8523.PCF8523(i2c)

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

def capture_frames(button_a):
    # gc.collect()
    maxval = 255
    frame = [0] * 768
    count = 1
    frame_number = []
    ascii_char = []
    update_flag = True
    update_frame_number_label = label.Label(terminalio.FONT, text="FRAME No. {}".format(count), x=10, y=30)
    display_group.append(update_frame_number_label)
    # Can also replace the line below with while True for number of frames is unknown 
    # while count < NUMBER_OF_FRAMES:
    while update_flag:
        
        # buttonB.update()
        # if buttonB.fell:
        #     update_flag = False
        #     print("Exited")
        #     setTextXY("Exited", 10, 30)
        #     clear_screen()
        #     # main_page()
        #     break
        # print("FRAME No. {}".format(count))
    # else:
        update_frame_number_label.text = "FRAME No. {}".format(count)
        display.show(display_group)

        frame_number.clear()
        ONBOARD_LED.value = True
        print("FRAME No. {}".format(count))
        # setTextXY("FRAME No. {}".format(count), 10, 30)
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
        #         if PRINT_TEMPERATURES:
        #             print("%0.1f, " % t, end="")
        #         if PRINT_ASCIIART:
        #             c = "&"
        #             # pylint: disable=multiple-statements
        #             if t < 20:
        #                 c = " "
        #             elif t < 23:
        #                 c = "."
        #             elif t < 25:
        #                 c = "-"
        #             elif t < 27:
        #                 c = "*"
        #             elif t < 29:
        #                 c = "+"
        #             elif t < 31:
        #                 c = "x"
        #             elif t < 33:
        #                 c = "%"
        #             elif t < 35:
        #                 c = "#"
        #             elif t < 37:
        #                 c = "X"
        #             # pylint: enable=multiple-statements
        #             print(c, end="")
        #             ascii_char.append(c)
        #     print()
        # print()
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
        updated_time = ds_rtc.datetime
        print("Stored in file: {:02}_{:02}_{}_{:02}_{:02}_{:02}__{}.pgm".format(
                updated_time[2],
                updated_time[1],
                updated_time[0],
                updated_time[3],
                updated_time[4],
                updated_time[5],
                count
            ))
        FILE_PATH_DATE ="/sd/Images/{:02}_{:02}_{}_{:02}_{:02}_{:02}__{}.pgm".format(
                updated_time[2],
                updated_time[1],
                updated_time[0],
                updated_time[3],
                updated_time[4],
                updated_time[5],
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
        # gc.collect()
            # for i in ascii_char:
            #     file.write(i)
            # file.write('\n')
        
        # Check if the button has been pressed whilst recording - unmount the device and stop writing data
        buttonA.update()
        if buttonA.fell:
            print("stopped logging")
            clear_screen()
            setTextArea("Stopped")
            update_flag = False
            image_file.close()
            storage.umount("/")
            break
