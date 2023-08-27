from facet_analysis import facet_compute
from utilities import elevation_function, color_pallete, targeted_rand_color
from analysis import count

import math
import matplotlib.pyplot as plt
import numpy as np

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


class contour_compute(facet_compute):
    def __init__(
        self,
        image,
        hscale,
        vscale,
        units,
        title,
        contour_file,
        start=(0, 0),
        stop=None,
    ):
        super().__init__(image, hscale, vscale, units, title, start, stop)
        self.get_elevation, self.null_elevation = elevation_function(contour_file)
        self.contour_data = {}  # Surface Area, Perimeter, and elevation stats

    def color_facet(self, location, color=True):
        # performs a flood fill of a region with the same color and counts the number of pixels in the area
        surface_area = 0
        perimeter = 0
        color = random_color_func()
        elevations = []
        # for pixel in self.facet_gen(location, new_counted=False):
        for pixel in self.test_gen(location):
            # print(surface_area)
            self.output.putpixel(pixel, color)
            surface_area += self.get_surface_area(pixel)
            # surface_area += self.pixel_area
            perimeter += self.get_perimeter(pixel)
            elevation = self.get_elevation(pixel[0], pixel[1]) / 1000
            if elevation > self.null_elevation:
                elevations.append(elevation)

        return location, (
            surface_area,
            perimeter,
            np.average(elevations),
            np.std(elevations),
        )

    def new_data_point(self, data):
        location, surface_area, perimeter, elev_ave, elev_stdev = (
            data[0],
            data[1][0],
            data[1][1],
            data[1][2],
            data[1][3],
        )
        if surface_area != self.pixel_area:  # Only facets larger than one pixel
            super().new_data_point((location, (surface_area, perimeter)))
            self.contour_data[location] = (
                surface_area,
                perimeter,
                elev_ave,
                elev_stdev,
            )

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
                    del self.contour_data[pixel]
        return removed

    def elevation_vs_surface_area(self):
        if self.contour_data == {}:
            return

        elevations = []
        surface_areas = []
        for arr in self.contour_data.values():
            elevations.append(arr[2])
            surface_areas.append(arr[0])

        plt.title(f"Surface Area vs. Average Elevation ({self.title})")
        plt.scatter(surface_areas, elevations, marker="x")
        plt.xlabel(f"Surface Area ({self.units}^2)")
        plt.xscale("log")
        plt.ylabel(f"Elevation (km)")
        # plt.yscale("log")
        plt.show()

    def elev_deviations_vs_surface_area(self):
        if self.contour_data == {}:
            return

        deviations = []
        surface_areas = []
        for arr in self.contour_data.values():
            deviations.append(arr[3])
            surface_areas.append(arr[0])

        max_dev = max(deviations)
        min_dev = min(deviations)
        cm = plt.cm.get_cmap("viridis")

        fig, ax = plt.subplots()
        im = ax.scatter(surface_areas, deviations, marker="x", c=deviations, cmap=cm)
        ax.set_title(f"Surface Area vs. Standard Deviation ({self.title})")
        ax.set_xlabel(f"Surface Area ({self.units}^2)")
        ax.set_ylabel(f"Standard Deviation (km)")
        ax.set_xscale("log")
        # ax.set_yscale("log")
        fig.colorbar(im, ax=ax, label="Standard Deviation (km)")
        plt.show()

        """
        plt.title(f"Surface Area vs. Standard Deviation ({self.title})")
        plt.scatter(surface_areas, deviations, marker="x")
        plt.xlabel(f"Surface Area ({self.units}^2)")
        plt.xscale("log")
        plt.ylabel(f"Standard Deviation (km)")
        # plt.yscale("log")
        plt.show()
        """

    def perimeter_vs_surface_stdev(self):
        if self.contour_data == {}:
            return
        surface_areas = []
        perimeters = []
        deviations = []

        for arr in self.contour_data.values():
            deviations.append(arr[3])
            perimeters.append(arr[1])
            surface_areas.append(arr[0])

        cm = plt.cm.get_cmap("viridis")

        fig, ax = plt.subplots()

        ax.set_title(f"Surface Area vs. Perimeter ({self.title})")
        im = ax.scatter(surface_areas, perimeters, marker="x", c=deviations, cmap=cm)
        ax.set_xlabel(f"Surface Area ({self.units}^2)")
        ax.set_xscale("log")
        ax.set_ylabel(f"Perimeter ({self.units})")
        ax.set_yscale("log")
        fig.colorbar(im, ax=ax, label="Standard Deviation (km)")
        plt.show()

    """
    def get_surface_area(self, pixel):
        dx, dy = 0, 0
        # horizatal gradient df/dx
        x_neighbors = []
        for delta in [neighbors["left"], neighbors["right"]]:
            if self.in_bounds((delta[0] + pixel[0], delta[1] + pixel[1])):
                if (
                    self.output.getpixel((delta[0] + pixel[0], delta[1] + pixel[1]))
                    != white
                ):
                    x_neighbors.append(delta)
        x = self.get_elevation(pixel[0], pixel[1]) / 1000
        if len(x_neighbors) == 0:
            dx = 0
        elif len(x_neighbors) == 1:
            delta = x_neighbors[0]
            x_1 = self.get_elevation(delta[0] + pixel[0], delta[1] + pixel[1]) / 1000
            dx = (x_1 - x) / self.hscale
        else:
            delta1 = x_neighbors[0]
            delta2 = x_neighbors[1]
            x_1 = self.get_elevation(delta1[0] + pixel[0], delta1[1] + pixel[1]) / 1000
            x_2 = self.get_elevation(delta2[0] + pixel[0], delta2[1] + pixel[1]) / 1000
            # dx = (x_2 - x_1)/self.hscale

            dx = (1 / 2) * (abs(x_1 - x) + abs(x_2 - x)) / self.hscale

        # vertical gradient df/dy
        y_neighbors = []
        for delta in [neighbors["up"], neighbors["down"]]:
            if self.in_bounds((delta[0] + pixel[0], delta[1] + pixel[1])):
                if (
                    self.output.getpixel((delta[0] + pixel[0], delta[1] + pixel[1]))
                    != white
                ):
                    y_neighbors.append(delta)
        y = self.get_elevation(pixel[0], pixel[1]) / 1000
        if len(y_neighbors) == 0:
            dy = 0
        elif len(y_neighbors) == 1:
            delta = y_neighbors[0]
            y_1 = self.get_elevation(delta[0] + pixel[0], delta[1] + pixel[1]) / 1000
            dy = (y_1 - y) / self.vscale
        else:
            delta1 = y_neighbors[0]
            delta2 = y_neighbors[1]
            y_1 = self.get_elevation(delta1[0] + pixel[0], delta1[1] + pixel[1]) / 1000
            y_2 = self.get_elevation(delta2[0] + pixel[0], delta2[1] + pixel[1]) / 1000
            dy = (1 / 2) * (abs(y_1 - y) + abs(y_2 - y)) / self.vscale
        # print(self.pixel_area * math.sqrt(1 + dx**2 + dy**2))
        # return self.pixel_area * math.sqrt(1 + dx**2 + dy**2)
        # print(self.pixel_area)
        scaled_area = math.sqrt(1 + dx**2 + dy**2)
        if scaled_area > 10**4:
            return self.pixel_area
        else:
            return self.pixel_area * math.sqrt(1 + dx**2 + dy**2)
    """


if __name__ == "__main__":
    x = contour_compute(
        "images/Rhadamanthys-fractures.png",
        0.2276509363851,
        0.2276509363851,
        "km",
        "Rhadamanthys",
        "Rhadamanthys.tif",
        (0, 0),
        (505, 350),
    )

    # print(x.get_surface_area((187, 337)))

    x.flood_count()
    x.remove_facets([(0, 0), (505, 0), (350, 0), (376, 272)])
    # x.perimeter_vs_surface_stdev()
    # x.elev_deviations_vs_surface_area()
    # x.get_image().show()
    print(f"# of facets : {len(x.contour_data)}")
    # x.elevation_vs_surface_area()
    # x.elev_deviations_vs_surface_area()

    y = facet_compute(
        "images/Rhadamanthys-fractures.png",
        0.2276509363851,
        0.2276509363851,
        "km",
        "Rhadamanthys",
        (0, 0),
        None,
    )

    x.perimeter_vs_surface_stdev()
    # x.elev_deviations_vs_surface_area()

    y.flood_count()
    y.remove_facets([(0, 0), (505, 0), (350, 0), (376, 272)])

    flat, corrected = [], []
    max = 0
    for key in x.data:
        flat.append(y.data[key][0])
        corrected.append(x.data[key][0])
        if y.data[key][0] > max:
            max = y.data[key][0]

    fig, ax = plt.subplots()
    ax.scatter(flat, corrected)
    # ax.set_xlabel("Flat Surface Area (km^2)")
    # ax.set_ylabel("Curved Surface Area (km^2)")
    ax.plot([0, max], [0, max], "red")
    plt.show()
    """
    x_1, y_1 = [], []
    for arr in x.data.values():
        x_1.append(arr[0])
        y_1.append(arr[1])

    x_2, y_2 = [], []
    for arr in y.data.values():
        x_2.append(arr[0])
        y_2.append(arr[1])

    fig, ax = plt.subplots()
    ax.set_title(f"Surface Area vs. Perimeter (Rhadamanthys)")
    ax.scatter(x_1, y_1, marker="x", c="r", label="With Elevation Correction")
    ax.scatter(x_2, y_2, marker="o", c="b", label="Without Elevation Correction")
    ax.set_xlabel(f"Surface Area (km^2)")
    ax.set_xscale("log")
    ax.set_ylabel(f"Perimeter (km)")
    ax.set_yscale("log")
    ax.scatter(x_1, y_1, c="r", marker="x")
    ax.legend()
    plt.show()
    # plt.scatter(x_2, y_2, c="g", marker="x")
    # plt.show()
    # x.get_image().show()
    # x.analyze_perimeter(bucket_size=25, threshold=0)
    """
