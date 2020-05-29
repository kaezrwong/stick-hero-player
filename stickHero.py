import numpy as np
from time import sleep
from PIL import Image
from ppadb.client import Client as AdbClient

# Establish connection between device and computer
# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = devices[0]

phone_height_pixels = 2280
height = int(phone_height_pixels * 0.75)

for repeats in range(1000):
    borders = [] # [Right edge of start tower, Left edge of target tower, Right edge of target tower]
    found_start = False # Found left edge of start tower
    black = True # Is the current pixel black

    # Takes screenshot
    image = device.screencap()
    with open("screencapture.png", "wb") as fp:
        fp.write(image)

    # Open PIL image
    image = Image.open("screencapture.png")

    # Convert image to numpy array
    image = np.array(image)
    for i in range(1080):
        
        # Find leftmost edge of starting tower
        if not found_start:
            if (image[1800][i][0] < 10):
                found_start = True
            else:
                continue
        
        # No black to black transition
        if image[height][i][0] < 10 and not black:
            borders.append(i)
            black = not black
        
        # Black to not black transition
        if image[height][i][0] > 10 and black:
            borders.append(i)
            black = not black
    
    # Solves the case when the target tower spans to the
    # right edge of the screen.
    if (len(borders) < 3):
        borders.append(1079)

    gap = borders[1] - borders[0]
    platform_width = borders[2] - borders[1]
    distance = gap + platform_width/2 # Ninja to the red target
    distance = distance * 0.98 # Scaling factor

    # Input press to phone app
    device.shell("input touchscreen swipe 500 500 500 500 {}".format(int(distance)))

    # Wait for next level to load
    sleep(2.8)