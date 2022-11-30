import os
import shutil
import numpy as np
import matplotlib.pyplot as plt


def f(x, y):
    # The function to be used
    c = 1.2
    var = np.sqrt(x ** 2 + y ** 2 + c ** 2)
    return np.sin(var)/var


# config for the image
STEPS = 10
RANGE_X = (-20, 20)
RANGE_Y = (-20, 20)
ELLIPTICAL_MASK = True

RESOLUTION = 800  # pixels for the whole x range

# projector
ASPECT_RATIO = 4/3
PRINTABLE_WIDTH = 0.5


# If true removes all files in img folder before running
DELETE_PREVIOUS_FILES = False

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


def delete_all(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if not os.path.exists("./img"):
    os.makedirs("./img")

if DELETE_PREVIOUS_FILES:
    delete_all('./img/')

DPI = 100
for i, cutoff in enumerate(np.linspace(np.nanmin(arr), np.nanmax(arr), STEPS)):
    selected = (arr > cutoff)
    img = np.zeros((img_width, img_height), dtype=bool)
    if ELLIPTICAL_MASK:
        selected = np.bitwise_and(selected, mask)
    start_x = int((img_width - width)/2)
    start_y = int((img_height - height)/2)
    img[start_x:start_x + width,
        start_y:start_y + height] = selected
    fig = plt.figure(figsize=(img_height/DPI, img_width/DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, cmap='binary_r')
    ax.text(img_height, img_width, f'layer {i + 1}/{STEPS}',
            horizontalalignment='right', verticalalignment='bottom', color='w', fontsize=0.03*RESOLUTION)
    plt.savefig(f'./img/{i}.png', dpi=DPI)
