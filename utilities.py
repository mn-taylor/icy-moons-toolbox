import random
import rasterio
from PIL import Image

white = (255, 255, 255)
black = (0, 0, 0)


def is_color(color):
    # test
    return all(0 <= x <= 255 for x in color)


def convert_to_RGB(file_name):
    # if input image is not an RBG image, returns a copy.
    img = Image.open(file_name).copy()
    if isinstance(img.getpixel((0, 0)), tuple):
        return img
    else:
        new_image = Image.new(
            mode="RGB", size=(img.size[0], img.size[1]), color=(0, 0, 0)
        )
        for row in range(img.size[0]):
            for col in range(img.size[1]):
                if img.getpixel((row, col)) == 255:
                    new_image.putpixel((row, col), white)
        return new_image


def rand_color():
    # returns a random color, used for visualizing the flood count
    return (
        random.randrange(1, 255),
        random.randrange(1, 255),
        random.randrange(1, 255),
    )


def targeted_rand_color(palette):
    length = len(palette)
    return lambda: palette[random.randrange(0, length)]


def color_pallete(num_colors, root_colors, shift, radius):
    def color_shift(color, root):
        candidates = [
            (color[0] + shift, color[1], color[2] + shift),
            (color[0] - shift, color[1], color[2] + shift),
            (color[0] - shift, color[1], color[2] - shift),
            (color[0] + shift, color[1], color[2] - shift),
            (color[0] + shift, color[1] + shift, color[2]),
            (color[0] + shift, color[1] - shift, color[2]),
            (color[0] - shift, color[1] - shift, color[2]),
            (color[0] - shift, color[1] + shift, color[2]),
            (color[0], color[1] + shift, color[2] + shift),
            (color[0], color[1] + shift, color[2] - shift),
            (color[0], color[1] - shift, color[2] + shift),
            (color[0], color[1] - shift, color[2] - shift),
        ]

        for candidate in candidates:
            good_candidate = False
            if (
                (candidate[0] - root[0]) ** 2
                + (candidate[1] - root[1]) ** 2
                + (candidate[2] - root[2]) ** 2
                < radius**2
                and candidate not in global_colors
                and is_color(candidate)
            ):
                good_candidate = True
            if not good_candidate:
                candidates.remove(candidate)

        return candidates

    pallete = {color: ([color], {color}) for color in root_colors}
    global_colors = set(root_colors)
    i = 0
    while len(global_colors) < num_colors:
        x = len(global_colors)
        for color in pallete:
            new_colors = color_shift(pallete[color][0][i], color)
            pallete[color][0].extend(new_colors)
            global_colors.update(new_colors)
        # print(len(global_colors))
        i += 1

    return list(color for color in global_colors if is_color(color))


def configure_boundary(image, start, stop, counted):
    """
    image -> PIL Image Object
    start -> tuple
    stop -> tuple

    """
    deltas = {(0, +1), (0, -1), (+1, 0), (-1, 0)}

    def get_neighbors_func(location, new_counted=False):
        # returns a set of the pixels above, below, and to the right and left of the given pixel
        # given that they are in bounds and havent been visited
        x, y = location[0], location[1]
        # counted = set()
        neighbors = set()
        for dx, dy in deltas:
            if (x + dx, y + dy) in counted:
                continue
            elif x + dx < start[0] or x + dx >= stop[0]:
                continue
            elif y + dy < start[1] or y + dy >= stop[1]:
                continue
            elif image.getpixel((x + dx, y + dy)) == white:
                continue
            else:
                neighbors.add((x + dx, y + dy))
        for neighbor in neighbors:
            if image.getpixel(neighbor) == white:
                raise Exception
        return neighbors

    def next_pixel_func(location):
        if location[0] + 1 != stop[0]:
            return (location[0] + 1, location[1])
        else:
            return (start[0], location[1] + 1)

    return get_neighbors_func, next_pixel_func


def string_to_tuples(string):
    num = ""
    string_nums = []
    for char in string:
        try:
            int(char)
            num += char
        except:
            if num:
                string_nums.append(num)
            num = ""
    if num != "":
        string_nums.append(num)
    result = []
    for i in range(len(string_nums) // 2):
        result.append((int(string_nums[2 * i]), int(string_nums[2 * i + 1])))
    return result


def elevation_function(file):
    # Takes in a TIF file and returns a look up function and the minimum elevation in the TIF file
    with rasterio.open(file) as dataset:
        band = dataset.read(1)

        shape = band.shape
        min = 10**20
        for row in range(shape[0]):
            for col in range(shape[1]):
                x = band[row, col]
                if min > x > -(10**20):
                    min = x

        # [col, row] because the pixels in the image are refereced with x, y
        return lambda row, col: band[col, row], min

def split_dataset_by_surface(data, threshold):
    below = [[], []]
    above = [[], []]

    for arr in data.values():
        if arr[0] > threshold:
            below[0].append(arr[0]) # surface area
            below[1].append(arr[1]) # perimeter
        else:
            above[0].append(arr[0])
            above[1].append(arr[1])
        
    return below, above


if __name__ == "__main__":
    
    pass
