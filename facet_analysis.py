from PIL import Image
from utilities import (
    targeted_rand_color,
    configure_boundary,
    color_pallete,
    is_color,
    convert_to_RGB,
)
from length_analysis import count

import matplotlib.pyplot as plt
import pandas as pd
import math
import time

white = (255, 255, 255)
black = (0, 0, 0)
neighbors = {"up": (0, +1), "down": (0, -1), "right": (+1, 0), "left": (-1, 0)}
root_colors = [
    (230, 159, 0),
    (86, 180, 233),
    (0, 158, 115),
    (240, 228, 66),
    (0, 114, 178),
    (213, 94, 0),
    (204, 121, 167),
]
palette = color_pallete(1000, root_colors, 15, 100)
random_color_func = targeted_rand_color(palette)


class facet_compute:
    def __init__(self, image, hscale, vscale, units, title, start=(0, 0), stop=None):
        self.output = convert_to_RGB(image)
        self.start = start
        if stop is None:
            self.stop = self.output.size
        else:
            self.stop = stop

        self.hscale = hscale
        self.vscale = vscale
        self.pixel_area = hscale * vscale
        self.units = units
        self.title = title

        self.data = {}
        self.counted = set()

        self.get_neighbors, self.next_pixel = configure_boundary(
            self.output, self.start, self.stop, self.counted
        )

    def flood_count(self):
        # function to fill in the facets
        curr = self.start
        while curr != (self.stop[0] - 1, self.stop[1] - 1):
            if curr in self.counted:
                curr = self.next_pixel(curr)
                continue

            if self.output.getpixel(curr) == white:  # border
                self.counted.add(curr)
            else:
                # Flood fill counting
                self.new_data_point(self.color_facet(curr))

            curr = self.next_pixel(curr)

    def color_facet(self, location, color=True):
        # performs a flood fill of a region with the same color and counts the number of pixels in the area
        surface_area = 0
        perimeter = 0
        color = random_color_func()
        # for pixel in self.facet_gen(location, new_counted=False):
        for pixel in self.test_gen(location):
            self.output.putpixel(pixel, color)
            surface_area += self.get_surface_area(pixel)
            perimeter += self.get_perimeter(pixel)

        return location, (surface_area, perimeter)

    def count_facet(self, location):
        surface_area = 0
        perimeter = 0
        for pixel in self.facet_gen(location, new_counted=False):
            surface_area += self.get_surface_area(pixel)
            perimeter += self.get_perimeter(pixel)
        return location, (surface_area, perimeter)

    def facet_gen(self, location, new_counted=False):
        # Generator that given a location, yields all of the indices in that facet in no particuar order
        agenda = [location]
        if new_counted:
            counted = set()
        else:
            counted = self.counted
        neighbors_func = configure_boundary(
            self.output, self.start, self.stop, counted
        )[0]
        while agenda:
            current = agenda.pop(0)
            neighbors = neighbors_func(current)
            counted.update(neighbors)
            agenda.extend(neighbors)
            yield current

    def test_gen(self, location):
        agenda = [location]
        while agenda:
            current = agenda.pop(0)
            neighbors = self.get_neighbors(current)
            self.counted.update(neighbors)
            agenda.extend(neighbors)
            yield current

    def get_surface_area(self, location):
        return self.pixel_area

    def get_perimeter(self, location):
        white_neighbors = set()
        for dir, delta in neighbors.items():
            try:
                if (
                    self.output.getpixel(
                        (location[0] + delta[0], location[1] + delta[1])
                    )
                    == white
                ):
                    white_neighbors.add(dir)
            except:
                pass

        if len(white_neighbors) == 4:
            perim = 1
        elif len(white_neighbors) == 3:
            perim = 1
        elif len(white_neighbors) == 2:
            if "up" in white_neighbors or "down" in white_neighbors:
                if "left" in white_neighbors or "right" in white_neighbors:
                    perim = math.sqrt(2)  # Corner
                else:  # Horizonal Tunnel
                    perim = 2
            else:  # Vertical Tunnel
                perim = 2
        else:
            return (
                len(white_neighbors) * (self.hscale + self.vscale) / 2
            )  # Handles 1 and 0 adjacent white pixels
        return perim * (self.hscale + self.vscale) / 2

    def new_data_point(self, data_point):
        if data_point[1][0] != self.pixel_area:  # Dont count single enclosed pixels
            self.data[data_point[0]] = (
                data_point[1][0],
                data_point[1][1],
            )
        # print(data_point[1])

    def remove_facets(self, locations):
        # Given an array of pixel locations, removes the data points that correspond to each pixels facet area.
        removed = []
        print(locations)
        for location in locations:
            print(location)
            if not self.in_bounds(location):
                print("not in bounds")
                continue
            for pixel in self.facet_gen(location, new_counted=True):
                # print("removing")
                self.output.putpixel((pixel), black)
                if pixel in self.data:
                    removed.append((location, self.data[pixel]))
                    print(f"Removed facet of size {self.data[pixel]}")
                    del self.data[pixel]
        return removed

    def analyze_surface_area(self, bucket_size, threshold=0):
        if self.data == {}:
            return
        nums = count([elt[0] for elt in self.data.values()], bucket_size)
        if threshold:
            nums = {k: v for k, v in nums.items() if v >= threshold}
        x = [bucket_size * (elt + 0.5) for elt in nums.keys()]
        y = nums.values()
        plt.bar(x, y, width=bucket_size * 0.9)
        plt.title(f"Surface Area Distribution ({self.title})")
        plt.xlabel(f"Surface Area ({self.units}^2)")
        plt.ylabel("# of Facets ")
        plt.show()

    def analyze_perimeter(self, bucket_size, threshold):
        if self.data == {}:
            return
        nums = count([elt[1] for elt in self.data.values()], bucket_size)
        if threshold:
            nums = {k: v for k, v in nums.items() if v >= threshold}
        x = [bucket_size * (elt + 0.5) for elt in nums.keys()]
        y = nums.values()
        plt.bar(x, y, width=bucket_size * 0.9)
        plt.title(f"Perimeter Distribution ({self.title})")
        plt.xlabel(f"Perimeter ({self.units})")
        plt.ylabel("# of Facets ")
        plt.show()
        pass

    def perimeter_vs_surface(self):
        if self.data == {}:
            return
        surface_areas = []
        perimeters = []
        for data in self.data.values():
            # surface_areas.append(data[0] / 10e6)
            surface_areas.append(data[0])
            # perimeters.append(data[1] / 10e3)
            perimeters.append(data[1])
        plt.title(f"Surface Area vs. Perimeter ({self.title})")
        plt.scatter(surface_areas, perimeters, marker="x")
        plt.xlabel(f"Surface Area ({self.units}^2)")
        plt.xscale("log")
        plt.ylabel(f"Perimeter ({self.units})")
        plt.yscale("log")

        """
        fig, axs = plt.subplots(1, 2)
        fig.suptitle("Surface Area vs. Perimeter (5178r)")

        axs[0].scatter(surface_areas, perimeters, marker="x")
        axs[0].set(
            xlabel=f"Surface Area ({self.units}^2)", ylabel=f"Perimeter ({self.units})"
        )

        axs[1].scatter(surface_areas, perimeters, marker="x")
        axs[1].set(
            xlabel=f"Surface Area ({self.units}^2)",
            xscale="log",
            yscale="log",
        )
        """
        plt.show()

    def in_bounds(self, location):
        if (
            location[0] < self.start[0]
            or location[0] > self.stop[0]
            or location[1] < self.start[1]
            or location[1] > self.stop[0]
        ):
            return False
        return True

    def offload_data(self, file_name="facet_data.csv"):
        if self.data == {}:
            return
        coulumn_names = ["Surface Area", "Perimeter", "Root Pixel"]
        df = pd.DataFrame(
            [[value[0], value[1], key] for key, value in self.data.items()],
            columns=coulumn_names,
        )
        df.to_csv(file_name)

    def get_image(self):
        return self.output

    def split_dataset_by_surface(self, threshold):
        below = [[], []]
        above = [[], []]

        for arr in self.data.values():
            if arr[0] < threshold:
                below[0].append(arr[0])  # surface area
                below[1].append(arr[1])  # perimeter
            else:
                above[0].append(arr[0])
                above[1].append(arr[1])

        return below, above


if __name__ == "__main__":
    pass
