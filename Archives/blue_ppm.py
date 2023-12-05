def create_ppm_file(width, height, filename):
    # Create PPM header
    header = f"P6\n{width} {height}\n255\n"

    # Create pixel data (red square)
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            if 100 <= x <= 200 and 100 <= y <= 200:
                pixels += bytes([255, 0, 0])  # Red pixel
            else:
                pixels += bytes([0, 0, 255])  # Black pixel

    # Write header and pixel data to file
    with open(filename, "wb") as ppm_file:
        ppm_file.write(header.encode("ascii"))
        ppm_file.write(pixels)

# Example usage:
create_ppm_file(200, 200, "images/output.ppm")
print("Done")