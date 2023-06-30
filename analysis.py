import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

x_scale = 1.606400e03
y_scale = 1.606400e03

x_axis_units = 1e3
bucket_size = 25


# Transforms each data point based on its bounding rectangle
def fracture_data_transform(file_name):
    def convert_length(length, border_width, border_height):
        """
        aspect_ratio = border_width / border_height
        if aspect_ratio < 0.75:
            return length * y_scale / x_axis_units
        elif aspect_ratio > 4 / 3:
            return length * x_scale / x_axis_units
        else:
            return length * (x_scale + y_scale) / 2 / x_axis_units
        """

        # Weighted Average
        return (
            (border_width * x_scale + border_height * y_scale)
            / (border_width + border_height)
            * length
            / x_axis_units
        )

    data = pd.read_csv(file_name)
    points = np.array(
        [
            convert_length(length, border_width, border_height)
            for border_width, border_height, length in zip(
                data["Width"], data["Height"], data["Length"]
            )
        ]
    )
    return points


# Given an array of data,  returns a dictionary that groups elemetns in the data set into "buckets"
def count(arr, bucket_size):
    N = {}
    for val in arr:
        bucket = val // bucket_size
        if bucket not in N:
            N[bucket] = 0
        N[bucket] += 1
    return N
    x = list(N.keys())
    x.sort()
    print(x)
    return (x, [N[m] for m in x])


def average_over_data():
    # Counts the number of fractures of size N and avergaes this value over all of the data sets.
    aggregate_data = {}
    for i, f in enumerate(sys.argv[1:]):
        lengths = fracture_data_transform(f)
        nums = count(lengths, bucket_size)
        for k, v in nums.items():
            if k not in aggregate_data:
                aggregate_data[k] = []
            aggregate_data[k].append(v)

    return dict(
        (k, sum(v) / len(v)) if v else (k, 0) for k, v in aggregate_data.items()
    )


if __name__ == "__main__":
    lengths = fracture_data_transform("Results.csv")
    print(lengths)
    nums = count(lengths, 25)
    print
    # Filters out outliers
    nums = {k: v for k, v in nums.items() if v > 5}

    # nums = average_over_data()
    x = [bucket_size * length for length in nums.keys()]
    y = nums.values()
    plt.bar(x, y, width=25 * 0.9)
    plt.title("Distribution of Fracture Lengths in 5189r")
    plt.xlabel("Lengths of Fractures (10^3 km)")
    plt.ylabel("# of Fractures")
    plt.show()
