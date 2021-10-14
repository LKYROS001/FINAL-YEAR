import sys
from PIL import Image
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
an_image = Image.open("hello.png")
image_sequence = an_image.getdata()
image_array = np.array(image_sequence)

print(image_array)