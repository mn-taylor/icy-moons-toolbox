from PIL import Image
from utilities import color_pallete

width = 100
height = 100

img = Image.new(mode="RGB", size=(width, height), color=(0, 0, 0))


def make_fractures(locations):
    for location in locations:
        img.putpixel(location, (255, 255, 255))


roots = [
    (51, 34, 136),
    (17, 119, 51),
    (68, 170, 153),
    (136, 204, 238),
    (221, 204, 119),
    (204, 102, 119),
    (170, 68, 153),
    (136, 34, 85),
]
colors = color_pallete(10000, roots, 100, 1000)
zero = (255, 194, 10)
for color in colors[1:]:
    if color == zero:
        print("repeat")
for i in range(width):
    for j in range(height):
        img.putpixel((i, j), colors[i * width + j])

make_fractures([])
img.show()
img.save("images/test.png")
