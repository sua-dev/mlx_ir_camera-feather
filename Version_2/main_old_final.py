import time
import board
import busio
import adafruit_mlx90640 
import array

# I2C Address at 0x33
# i2c = board.I2C()
import terminalio # maybe redundant
import simpleio


PRINT_TEMPERATURES = False
PRINT_ASCIIART = True
FILE_PATH = "images/image.ppm"
FILE_PATH_ASCII = "images/image.txt"


i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
number_of_colors = 64
last_color = number_of_colors - 1 # last color in the palette

## Heatmap code inspired from: http://www.andrewnoske.com/wiki/Code_-_heatmaps_and_color_gradients
color_A = [
    [0, 0, 0],
    [0, 0, 255],
    [0, 255, 255],
    [0, 255, 0],
    [255, 255, 0],
    [255, 0, 0],
    [255, 255, 255],
]
color_B = [[0, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 0], [255, 0, 0]]
color_C = [[0, 0, 0], [255, 255, 255]]
color_D = [[0, 0, 255], [255, 0, 0]]

color = color_A
NUM_COLORS = len(color)

# def MakeHeatMapColor():
#     for c in range(number_of_colors):
#         value = c * (NUM_COLORS - 1) / last_color
#         idx1 = int(value)  # Our desired color will be after this index.
#         if idx1 == value:  # This is the corner case
#             red = color[idx1][0]
#             green = color[idx1][1]
#             blue = color[idx1][2]
#         else:
#             idx2 = idx1 + 1  # ... and before this index (inclusive).
#             fractBetween = value - idx1  # Distance between the two indexes (0-1).
#             red = int(
#                 round((color[idx2][0] - color[idx1][0]) * fractBetween + color[idx1][0])
#             )
#             green = int(
#                 round((color[idx2][1] - color[idx1][1]) * fractBetween + color[idx1][1])
#             )
#             blue = int(
#                 round((color[idx2][2] - color[idx1][2]) * fractBetween + color[idx1][2])
#             )
#         palette[c] = (0x010000 * red) + (0x000100 * green) + (0x000001 * blue)


# MakeHeatMapColor()

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
def raw_bytes():
    frame = [0] * 768
    t = 0
    maxval = 255
    # count = 1
    # while count > 0:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        print("No frames")
        # these happen, no biggie - retry
        # continue
    print(type(frame))
    # print(frame)
    print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if PRINT_TEMPERATURES:
                print("%0.1f, " % t, end="")
            if PRINT_ASCIIART:
                c = "&"
                # pylint: disable=multiple-statements
                # print(t, end=" ")
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
                # # pylint: enable=multiple-statements
                print(c, end="")
                # raw_image = t

                # image.flush()
        print()
    print()
    
    print("Width: {}".format(w))
    print("Height: {}".format(h))
    print("Max Value: {}".format(maxval))
    # image = array.array('B', [0, 0, 255] * w * h)
    # image_2 = array.array(frame)
    # print(t)        
    #                
    # with open(FILE_PATH, "w") as image:
    #     while count > 0:
    #         stamp = time.monotonic()
    #         try:
    #             mlx.getFrame(frame)
    #         except ValueError:
    #             # these happen, no biggie - retry
    #             continue
    #         print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
    #         for h in range(24):
    #             print("in here with h: {}".format(h))
    #             for w in range(32):
    #                 print('in here with w: {}'.format(w))
    #                 t = frame[h * 32 + w]
    #                 if PRINT_TEMPERATURES:
    #                     print("%0.1f, " % t, end="")
    #                 if PRINT_ASCIIART:
    #                     print('t: {}'.format(t))
    # #     image.write(("Read 2 frames in %0.2f s" % (time.monotonic() - stamp)))
    #                     image.write(str(t) + "\n")
    #             image.write("\n")
    #         image.write("\n")
        # count -= 1
    #     image.flush()
    ppm_header = f"P6 {w} {h} {maxval}\n"
    print(ppm_header)
    with open(FILE_PATH, "wb") as image_file:
        #PPM Header - Portable PixMap
        image_file.write(bytearray(ppm_header, 'ascii'))
    #     image_file.write(bytearray(int(frame)))

    with open(FILE_PATH_ASCII, "w") as ascii_pxl_file:
        #PPM Header - Portable PixMap
        # image_file.write(bytearray(ppm_header, 'ascii'))
        ascii_pxl_file.write(bytearray(frame))
        # frame.tofile(image)
        # image.tofile(image_file)
        # with open(FILE_PATH, "w") as image:
        #     image.write(raw_image, end="")
        # image.flush()

if __name__ == '__main__':
    raw_bytes()
    



