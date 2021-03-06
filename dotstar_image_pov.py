# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#!/usr/bin/python3

# Persistence-of-vision (POV) example for Adafruit DotStar RGB LED strip.
# Loads image, displays column-at-a-time on LEDs at very high speed,
# suitable for naked-eye illusions.
# See dotstar_simpletest.py for a much simpler example script.
# See dotstar_image_paint.py for a slightly simpler light painting example.
# This code accesses some elements of the dotstar object directly rather
# than through function calls or setters/getters...this is poor form as it
# could break easily with future library changes, but is the only way right
# now to do the POV as quickly as possible.
# May require installing separate libraries.

import board
import math
import time
from PIL import Image
import adafruit_dotstar as dotstar

NUMPIXELS = 72  # Length of DotStar strip
FILENAME = "sized2.png"  # Image file to load
ORDER = dotstar.BGR  # Change to GBR for older DotStar strips

# First two arguments in strip declaration identify the clock and data pins
# (here we're using the hardware SPI pins).
DOTS = dotstar.DotStar(
    board.SCK,
    board.MOSI,
    NUMPIXELS,
    auto_write=False,
    brightness=1.0,
    pixel_order=ORDER,
)

# Load image in RGB format and get dimensions:
print("Loading...")
#time.sleep(20000)
IMG = Image.open(FILENAME).convert("RGB")
PIXELS = IMG.load()
WIDTH = IMG.size[0]
HEIGHT = IMG.size[1]
print("%dx%d pixels" % IMG.size)
print(WIDTH)
print(HEIGHT)


# Calculate gamma correction table, makes mid-range colors look 'right':
GAMMA = bytearray(256)
brightness = 0.25
for i in range(256):
    GAMMA[i] = int(pow(float(i) / 255.0, 2.7) * brightness * 255.0 + 0.5)

# Allocate list of lists, one for each column of image.
print("Allocating...")
COLUMN = [0 for x in range(WIDTH)]
for x in range(WIDTH):
    COLUMN[x] = [[0, 0, 0, 0] for _ in range(HEIGHT)]

# Convert entire RGB image into columnxrow 2D list.
print("Converting...")
for x in range(WIDTH):  # For each column of image
    for y in range(HEIGHT):  # For each pixel in column
        value = PIXELS[x, y]  # Read RGB pixel in image
        COLUMN[x][y][0] = GAMMA[value[0]]  # Gamma-corrected R
        COLUMN[x][y][1] = GAMMA[value[1]]  # Gamma-corrected G
        COLUMN[x][y][2] = GAMMA[value[2]]  # Gamma-corrected B
        COLUMN[x][y][3] = 0.5  # Brightness

print("Displaying...")

FINAL = [0 for x in range(360)]
for x in range(360):
    FINAL[x] = [[0, 0, 0, 0] for _ in range(72)]
ratio = 128/72
distance = 0.0
for x in range(360):  # For each column of image
    for y in range(72):  # For each pixel in column
        distance = ratio * y
        fx = round((distance * math.cos(math.radians(x))) + 128)
        fy = round((-1 * distance * math.sin(math.radians(y))) + 128)
        FINAL[x][y][0] = COLUMN[fx][fy][0]  # Gamma-corrected R
        FINAL[x][y][1] = COLUMN[fx][fy][1]  # Gamma-corrected G
        FINAL[x][y][2] = COLUMN[fx][fy][2]  # Gamma-corrected B
        FINAL[x][y][3] = 0.5  # Brightness
#print(FINAL[0])

while True:  # Loop forever
    print("rotation")
    for x in range(360):  # For each column of image...
        DOTS[0 : DOTS.n] = FINAL[x]  # Copy column to DotStar buffer
        DOTS.show()  # Send data to strip
