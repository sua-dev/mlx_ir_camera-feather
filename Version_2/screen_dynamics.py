import board
import terminalio
import displayio
import adafruit_displayio_sh1107
import adafruit_display_text.bitmap_label as label

# Initialize I2C Bus
# i2c = busio.I2C(board.SCL, board.SDA)
i2c = board.I2C()

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

# Initialize Display
display_group = displayio.Group()
displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)
display.auto_refresh = True
# splash = displayio.Group()

def setTextArea(text):
    # text = "City Sensing Toolkit Dashboard"
    text_area_title = label.Label(terminalio.FONT, text=text)
    text_area_title.x = 10
    text_area_title.y = 10
    display_group.append(text_area_title)

def setTextXY(text, x, y):
    text_area_title = label.Label(terminalio.FONT, text=text)
    text_area_title.x = x
    text_area_title.y = y
    display_group.append(text_area_title)

def clear_screen():
    color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x00  # White
