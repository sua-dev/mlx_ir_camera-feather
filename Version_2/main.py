import board
import busio
import time
import digitalio
import storage
import wifi
import terminalio

# Import External Modules
import adafruit_sdcard  # SD Card SPI
import sdcardio  # SD Card I/O
import adafruit_pcf8523  # RTC I2C

import adafruit_display_text.bitmap_label as label
from adafruit_debouncer import Debouncer
# Import Custom Modules
from screen_dynamics import *

RECORDING = True

# Initialize SPI Bus
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# Initialize SD Card
# print("Initializing SD Card...")
# cs = board.D5
# sdcard = sdcardio.SDCard(spi, cs)
# # vfs = storage.VfsFat(sdcard)
# storage.mount(sdcard)
# print("SD Card Initialized")

# print("Writing to SD Card...")
# with open("/sd/test.txt", "w") as f:
#     f.write("Hello World!")
# print("Write Complete")



# # Initialize RTC
rtc = adafruit_pcf8523.PCF8523(i2c)
# rtc.datetime = time.struct_time((2023, 12, 11, 15, 57, 0, 0, -1, -1))

# print("Date: " + str(rtc.datetime.tm_mday) + "/" + str(rtc.datetime.tm_mon) + "/" + str(rtc.datetime.tm_year))
# print("Time: " + str(rtc.datetime.tm_hour) + ":" + str(rtc.datetime.tm_min) + ":" + str(rtc.datetime.tm_sec))

# Initialize WiFi
# wifi.radio.connect("SSID", "PASSWORD")

# Initialize Onboard LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def led_blink(period):
    led.value = True
    time.sleep(period)
    led.value = False
    time.sleep(period)

# Debouncer function
def debouncable(pin):
    switch_io = digitalio.DigitalInOut(pin)
    switch_io.direction = digitalio.Direction.INPUT
    switch_io.pull = digitalio.Pull.UP
    return switch_io

buttonA = Debouncer(debouncable(board.D5))
buttonB = Debouncer(debouncable(board.D21))
buttonC = Debouncer(debouncable(board.D20))

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
            
def main_page():
    setTextArea("IR Thermal Camera\nMain Menu")


def main():
    global RECORDING
    main_page()
    # main_page()
    # clear_screen()

    while True:
        buttonA.update()
        if buttonA.fell:
            print("Button A Pressed")
            current_time_page()
            # led.value = True
            # time.sleep(0.25)
            # led.value = False
            # time.sleep(0.25)
        
        buttonB.update()
        if buttonB.fell:
            print("Setting Up Camera System...")
            clear_screen()
            setTextArea("Setting Up\nCamera System...")
            while True:
                try:
                    import adafruit_mlx90640 as mlx
                    break
                except ImportError:
                    print("Camera System not set up")
                    setTextArea("Camera System\nnot set up")
                    time.sleep(0.5)
                    led_blink()
            # import mlx90640 camera module
            # import adafruit_mlx90640 as mlx
            clear_screen()
            print("Camera System Set Up")
            setTextArea("Camera System\nSet Up")
            # buttonC.update()
            if buttonB.fell:
                clear_screen()
                print("Recording...")
                setTextArea("Recording...")
                while RECORDING:
                    led_blink(1)
                    buttonA.update()
                    if buttonA.fell:
                        RECORDING = False
                        print("Recording Stopped")
                        clear_screen()
                        setTextArea("Recording\nStopped")
                    # led.value = True
                    # time.sleep(0.25)
                    # led.value = False
                    # time.sleep(0.25)

            # led_blink()
        # MOUNT SD CARD
        buttonC.update()
        if buttonC.fell:
            print("Mounting SD Card...")
            clear_screen()
            setTextArea("Mounting\nSD Card...")
            cs = board.D13
            sdcard = sdcardio.SDCard(spi, cs)
            # vfs = storage.VfsFat(sdcard)
            while True:
                try:
                    storage.mount(sdcard)
                    break
                except OSError:
                    print("SD Card not mounted")
                    setTextArea("SD Card not\nmounted")
                    time.sleep(0.5)
                    led_blink()
            # storage.mount(sdcard)
            print("SD Card Mounted")
            # print("Button C Pressed")
            # led.value = True
            # time.sleep(0.25)
            # led.value = False
            # time.sleep(0.25)

if __name__ == '__main__':
    main()
    