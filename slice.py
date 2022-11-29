import numpy as np
import matplotlib.pyplot as plt

# The function to be used
def f(x, y):
    c = 0
    var = np.sqrt(x ** 2 + y ** 2 + c ** 2)
    return np.sin(var)/var

# config for the image
STEPS = 50
RANGE_X = (-20, 20)
RANGE_Y = (-20, 20)
ELLIPTICAL_MASK = False

RESOLUTION = 2000  # pixels for the whole x range

# projector
ASPECT_RATIO = 4/3
PRINTABLE_WIDTH = 2/3




####################################################################
del_x = RANGE_X[1] - RANGE_X[0]
del_y = RANGE_Y[1] - RANGE_Y[0]
aspect = del_y/del_x
width = int(RESOLUTION)
height = int(RESOLUTION * aspect)


def my_f(xs, ys):
    xs = xs/len(xs) * del_x + RANGE_X[0]
    ys = ys/len(xs) * del_x + RANGE_Y[0]
    return f(xs, ys)


arr = np.fromfunction(my_f, (width, height))
# plt.imshow(arr)
# plt.show()

def mask_f(x, y):
    return (x-width/2)**2 / (width/2)**2 + (y-height/2)**2 / (height/2)**2
mask = (np.fromfunction(mask_f, (width, height)) < 1)

img_width = 0
img_height = 0

if width > height:
    img_width = int(width / PRINTABLE_WIDTH)
    img_height = int((width / PRINTABLE_WIDTH) * ASPECT_RATIO)
else:
    img_width = int(height / PRINTABLE_WIDTH)
    img_height = int((height / PRINTABLE_WIDTH) * ASPECT_RATIO)

for i, cutoff in enumerate(np.linspace(np.nanmin(arr), np.nanmax(arr), STEPS)):
    selected = (arr > cutoff)
    img = np.zeros((img_width, img_height), dtype=bool)
    if ELLIPTICAL_MASK:
        selected = np.bitwise_and(selected, mask)
    start_x = int((img_width - width)/2)
    start_y = int((img_height - height)/2)
    img[start_x:start_x+width,
        start_y:start_y + height] = selected
    plt.imsave(f'./img/{i}.png', img, cmap='binary_r')
