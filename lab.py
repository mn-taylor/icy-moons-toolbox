from contour_analysis import contour_compute
from facet_analysis import facet_compute
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


threshold = 10 ** (1.5)
x = facet_compute(
    "images/true_fractures.png", 1.606400, 1.6657, "km", "5178r", (200, 13)
)
x.flood_count()
x.remove_facets([(778, 198)])

y = contour_compute(
    "images/Rhadamanthys-fractures2.png",
    0.227651,
    0.227651,
    "km",
    "Rhadamanthys",
    "Rhadamanthys.tif",
    (0, 0),
    None,
)
y.flood_count()
y.remove_facets([(0, 0), (505, 0), (350, 0), (376, 272)])

fig, ax = plt.subplots()

# x.perimeter_vs_surface()
split = x.split_dataset_by_surface(threshold)
slope, intercept, r_value, p_value, std_err = stats.linregress(
    np.log10(split[0][0]), np.log10(split[0][1])
)
print(
    f"5178r small| slope: {slope}| intercept: {intercept}| r_value: {r_value}| p_value:{p_value}| std_err: {std_err}"
)

x_axis = np.logspace(np.log10(min(split[0][0])), np.log10(max(split[0][0])), 50)
ax.plot(x_axis, (10**intercept) * (x_axis**slope), c="orange", linewidth=2)

slope, intercept, r_value, p_value, std_err = stats.linregress(
    np.log10(split[1][0]), np.log10(split[1][1])
)
print(
    f"5178r large| slope: {slope}| intercept: {intercept}| r_value: {r_value}| p_value:{p_value}| std_err: {std_err}"
)

x_axis = np.logspace(np.log10(min(split[1][0])), np.log10(max(split[1][0])), 50)
ax.plot(x_axis, (10**intercept) * (x_axis**slope), c="orange", linewidth=2)
ax.scatter(split[1][0], split[1][1], c="red", label="5178r")
ax.scatter(split[0][0], split[0][1], c="red")

rhad_surface_areas = [arr[0] for arr in y.data.values()]
rhad_perimeters = [arr[1] for arr in y.data.values()]
deviations = [arr[3] for arr in y.contour_data.values()]

slope, intercept, r_value, p_value, std_err = stats.linregress(
    np.log10(rhad_surface_areas), np.log10(rhad_perimeters)
)
print(
    f"Rhad| slope: {slope}| intercept: {intercept}| r_value: {r_value}| p_value:{p_value}| std_err: {std_err}"
)
x_axis = np.logspace(
    np.log10(min(rhad_surface_areas)), np.log10(max(rhad_surface_areas))
)
ax.plot(x_axis, (10**intercept) * x_axis**slope, c="blue", linewidth=2)

cm = plt.cm.get_cmap("cool")
im = ax.scatter(
    rhad_surface_areas, rhad_perimeters, c=deviations, label="Rhadamanthys", cmap=cm
)
fig.colorbar(im, ax=ax, label="Standard Deviation (km)")


ax.set_title("Rhadamanthys vs. 5178r")
ax.set_xlabel("Surface Area (km)")
ax.set_ylabel("Perimeter (km)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.legend()
plt.show()
# x.get_image().show()
