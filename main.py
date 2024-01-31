import board
import digitalio
import time


# External Libraries
from config import *
import adafruit_pcf8523
from adafruit_debouncer import Debouncer
from screen_dynamics import *
from ir_camera_init import *
from Drivers.SPI_SD import *

# Global Variables
but_pressed = -1
time_screen = 0
record_screen = 1
check_files_screen = 2
current_screen = 0
screen_state = 0
page_state = 0
temp_offset = -5

# Initialize RTC
rtc = adafruit_pcf8523.PCF8523(i2c)

# Initialize Buttons
buttonA = Debouncer(debouncable(board.D5))
buttonB = Debouncer(debouncable(board.D21))
buttonC = Debouncer(debouncable(board.D20))


def button_check(button_a, button_b, button_c):
        # ========== A Button =========== #
    button_a.update()
    if button_a.fell:  # and button_b.value and button_c.value:
        current_screen = time_screen

        print("Button A Pressed")
        print("Current Screen: ", current_screen)
        return current_screen

    # ========== B Button =========== #
    button_b.update()
    if button_b.fell:  # and button_a.value and button_c.value:
        current_screen = record_screen
        print("Button B Pressed")
        print("Current Screen: ", current_screen)
        return current_screen

    # ========== C Button =========== #
    button_c.update()
    if button_c.fell:  # and button_b.value and button_a.value:
        current_screen = check_files_screen
        print("Button C Pressed")
        print("Current Screen: ", current_screen)
        return current_screen

def current_time_page():
    loop_flag = True
    clear_screen()
    setTextArea("Current Time")
    # setTextXY("Date: " + str(rtc.datetime.tm_mday) + "/" + str(rtc.datetime.tm_mon) + "/" + str(rtc.datetime.tm_year), 10, 30)
    # setTextXY("Time: " + str(rtc.datetime.tm_hour) + ":" + str(rtc.datetime.tm_min) + ":" + str(rtc.datetime.tm_sec), 10, 50)
    updated_date = label.Label(terminalio.FONT, text="Date: " + str(rtc.datetime.tm_mday) + "/" + str(rtc.datetime.tm_mon) + "/" + str(rtc.datetime.tm_year), x=10, y=30)
    display_group.append(updated_date)
    updated_time = label.Label(terminalio.FONT, text="Time: " + str(rtc.datetime.tm_hour) + ":" + str(rtc.datetime.tm_min) + ":" + str(rtc.datetime.tm_sec), x=10, y=50)
    display_group.append(updated_time)
    # display.show(display_group)

    while loop_flag:
        buttonA.update()
        if buttonA.fell:
            print("Exited")
            clear_screen()
            main_page()
            loop_flag = False
        else:
            updated_date.text = "Date: " + str(rtc.datetime.tm_mday) + "/" + str(rtc.datetime.tm_mon) + "/" + str(rtc.datetime.tm_year)
            updated_time.text = "Time: " + str(rtc.datetime.tm_hour) + ":" + str(rtc.datetime.tm_min) + ":" + str(rtc.datetime.tm_sec)
            display.show(display_group)

def record_page():
    capture_flag = True
    clear_screen()
    setTextArea("Ready to Record")
    setTextXY("A - Record", 10, 30)
    setTextXY("B - Stop", 10, 40)
    setTextXY("C - Exit", 10, 50)



    while capture_flag:
        buttonA.update()
        if buttonA.fell:
            print("Recording")
            clear_screen()
            setTextArea("Recording")
            capture_frames()
            # capture_flag = False
            # break
        buttonB.update()
        if buttonB.fell:
            print("Stopped Recording")
            clear_screen()
            setTextArea("Stopped Recording")
            capture_flag = False
            break
        buttonC.update()
        if buttonC.fell:
            print("Exited")
            clear_screen()
            main_page()
            capture_flag = False
            break
        # else:
        #     print("Not Recording")
        #     clear_screen()
        #     setTextArea("Stopped Recording")
        #     capture_flag = False
            # break

def check_files_page():
    clear_screen()
    setTextArea("Checking Files")
    print_directory("/images/")
    # count total number of files in directory
    total_files = len(os.listdir("/images/"))
    latest_file = os.listdir("/images/")[-1]
    print("Latest File: ", latest_file)
    setTextXY("Latest File: ", 10, 30)
    setTextXY(latest_file, 10, 40)
    print("Total Files: ", total_files)
    setTextXY("Total Files: " + str(total_files), 10, 50)

def main_page():
    setTextArea("IR Thermal Camera\nMain Menu")

def main():
    main_page()

    while True:
        screen_state = button_check(buttonA, buttonB, buttonC)
        if screen_state == time_screen:
            current_time_page()
        elif screen_state == record_screen:
            record_page()
        elif screen_state == check_files_screen:
            check_files_page()


if __name__ == '__main__':
    main()