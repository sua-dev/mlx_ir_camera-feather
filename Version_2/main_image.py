import time
import board
import busio
import struct
import adafruit_mlx90640


FILE_PATH = "images/image.ppm"
FILE_PATH_ASCII = "images/image.txt"
DEGREE_SHIFT = 5

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])


def float_list_to_bytearray(float_list):
    byte_array = bytearray()

    for value in float_list:
        # Convert float to bytes using struct.pack
        byte_representation = struct.pack('!f', value)

        # Iterate over bytes and convert each to an integer
        for byte in byte_representation:
            byte_array.append(byte)

    return byte_array

#TODO: Go through each value individually, convert into an int,
#  then test out and write into a ppm image
def int_list_to_bytearray(float_list):
    byte_array = bytearray()
    int_list = []
    for value in float_list:
        # Convert float to bytes using struct.pack
        # byte_representation = struct.pack('!f', value)
        # int_representation = struct.pack('i',value)
        int_representation = int(value * DEGREE_SHIFT)
        int_list.append(int_representation)
    # print(int_list)
        # Iterate over bytes and convert each to an integer
        for byte in int_list:
            byte_array.append(byte)

    return byte_array

# # Example usage:
# float_list = [3.14, 2.718, 1.618]
# # result_bytearray = float_list_to_bytearray(float_list)

# print(result_bytearray)

# if using higher refresh rates yields a 'too many retries' exception,
# try decreasing this value to work with certain pi/camera combinations
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
maxval = 255
w = 0
h = 0
count = 1
frame = [0] * 768
t = None
while count > 0:
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue

    for h in range(24):
        for w in range(32):
            t = frame[h*32 + w]
            # print("%0.1f, " % t, end="")
    #     print()
    # print()
    for i in frame:
        if i < 24:
            print(i)
    image = int_list_to_bytearray(frame)
    # print((image))
    # print(type(t))
    count -= 1

    ppm_header = f"P3 {w+1} {h+1} {maxval}\n"
    print(ppm_header)
    with open(FILE_PATH, "wb") as image_file:
        #PPM Header - Portable PixMap
        image_file.write(bytearray(ppm_header, 'ascii'))
        image_file.write(image)
    print("Done")