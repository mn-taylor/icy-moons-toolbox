import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from facet_area import facet_compute


def handle_image_input(string):
    global global_image, computation
    print(string)
    try:
        Image.open(string).save("images/image_analysis.png")
        computation = None
        global_image = ImageTk.PhotoImage(formated_image())
        analyze_button.config(state="normal")
        plot_button.config(state="disabled")
        image_label.config(image=global_image)
        ui.update_idletasks()

    except:
        messagebox.showerror("Image not found")


def clear_image():
    blank = Image.new(mode="RGB", size=(500, 500), color=(0, 0, 0))
    blank.save("images/image_analysis.png")

    try:
        plt.close()
    except:
        pass
    # blank.save("resize_image.png")


def formated_image():
    # Takes the image "image_analysis" file and resizes it to fit the window and stores the result in
    # resize image file
    return Image.open("images/image_analysis.png").resize((500, 500), Image.ANTIALIAS)


def analyze():
    global global_image, computation
    start = [0, 0]
    stop = [0, 0]
    print(start_x.get() != "")
    try:
        if start_x.get() != "":
            start[0] = int(start_x.get())
        print("here")
        if start_y.get() != "":
            start[1] = int(start_y.get())
        if stop_x.get() != "" and int(stop_x.get()) > start[0]:
            stop[0] = int(stop_x.get())
        if stop_y.get() != "" and int(stop_y.get()) > start[1]:
            stop[1] = int(stop_y.get())
    except TypeError:
        messagebox.showerror("Make sure inputs are integers")

    if stop[0] == 0 and stop[1] == 0:
        computation = facet_compute(file_name.get(), tuple(start))
    else:
        computation = facet_compute(file_name.get(), tuple(start), tuple(stop))
    computation.flood_count()
    computation.get_image().save("images/image_analysis.png")
    global_image = ImageTk.PhotoImage(formated_image())
    image_label.config(image=global_image)
    plot_button.config(state="normal")
    ui.update_idletasks()


def plot_window():
    global computation, plot_inputs_frame

    def perimeter_widgets():
        global plot_inputs_frame

        try:
            plt.close()
        except:
            pass

        plot_type.set("Perimeter")

        plot_inputs_frame.destroy()
        plot_inputs_frame = Frame(plot_window)
        plot_inputs_frame.pack(side="bottom")

        bucket_frame = Frame(plot_inputs_frame)
        bucket_frame.pack(side="top")

        bucket_size = StringVar()
        bucket_size.set("0")
        bucket_size_label = Label(bucket_frame, text="Bucket Size")
        bucker_size_entry = Entry(bucket_frame, textvariable=bucket_size)
        quick_pack([bucket_size_label, bucker_size_entry])

        threshold_frame = Frame(plot_inputs_frame)
        threshold_frame.pack(side="top")

        threshold = StringVar()
        threshold.set("0")
        threshold_label = Label(threshold_frame, text="Threshold")
        threshold_entry = Entry(threshold_frame, textvariable=threshold)
        quick_pack([threshold_label, threshold_entry])

        plot_button_frame = Frame(plot_inputs_frame)
        plot_button_frame.pack(side="top")

        plot_button = Button(
            plot_button_frame,
            text="PLOT",
            command=lambda: computation.analyze_perimeter(
                float(bucket_size.get()), float(threshold.get())
            ),
        )
        plot_button.pack()

    def surface_perim_widgets():
        global plot_inputs_frame

        try:
            plt.close()
        except:
            pass

        plot_type.set("Surface Area vs. Perimeter")

        plot_inputs_frame.destroy()
        plot_inputs_frame = Frame(plot_window)
        plot_inputs_frame.pack(side="bottom")

        plot_button_frame = Frame(plot_inputs_frame)
        plot_button_frame.pack(side="top")

        plot_button = Button(
            plot_button_frame,
            text="PLOT",
            command=lambda: computation.perimeter_vs_surface(),
        )
        plot_button.pack()

        pass

    def surface_widgets():
        global plot_inputs_frame

        try:
            plt.close()
        except:
            pass
        plot_type.set("Surface Area")

        plot_inputs_frame.destroy()
        plot_inputs_frame = Frame(plot_window)
        plot_inputs_frame.pack(side="bottom")

        bucket_frame = Frame(plot_inputs_frame)
        bucket_frame.pack(side="top")

        bucket_size = StringVar()
        bucket_size.set("0")
        bucket_size_label = Label(bucket_frame, text="Bucket Size")
        bucker_size_entry = Entry(bucket_frame, textvariable=bucket_size)
        quick_pack([bucket_size_label, bucker_size_entry])

        threshold_frame = Frame(plot_inputs_frame)
        threshold_frame.pack(side="top")

        threshold = StringVar()
        threshold.set("0")
        threshold_label = Label(threshold_frame, text="Threshold")
        threshold_entry = Entry(threshold_frame, textvariable=threshold)
        quick_pack([threshold_label, threshold_entry])

        plot_button_frame = Frame(plot_inputs_frame)
        plot_button_frame.pack(side="top")

        plot_button = Button(
            plot_button_frame,
            text="PLOT",
            command=lambda: computation.analyze_surface_area(
                float(bucket_size.get()), float(threshold.get())
            ),
        )
        plot_button.pack()

    plot_window = Toplevel(ui)
    plot_frame = Frame(plot_window)
    plot_frame.pack()

    plot_inputs_frame = Frame(plot_window)
    plot_inputs_frame.pack(side="bottom")

    plot_type = StringVar()
    plot_type.set("Plot Type")
    plot_type_menubutton = Menubutton(plot_frame, textvariable=plot_type)
    plot_type_menubutton.pack()
    plot_type_menubutton.menu = Menu(
        plot_type_menubutton,
    )
    plot_type_menubutton["menu"] = plot_type_menubutton.menu

    plot_type_menubutton.menu.add_command(label="Perimeter", command=perimeter_widgets)
    plot_type_menubutton.menu.add_command(label="Surface Area", command=surface_widgets)
    plot_type_menubutton.menu.add_command(
        label="Perimeter vs. Surface Area", command=surface_perim_widgets
    )
    print("plot_inputs_frame" in locals())


def quick_pack(args):
    for elt in args:
        elt.pack(side="left")


clear_image()
ui = Tk()
ui.title("Image Analysis Workspace")
ui.resizable(False, False)
global_image = None
computation = None
plot_inputs_frame = None

image_input_frame = Frame(ui)
image_input_frame.pack()

file_input_label = Label(image_input_frame, text="File Name")
file_name = StringVar()
file_name.set("fractures.png")
file_input_entry = Entry(image_input_frame, textvariable=file_name)
file_input_button = Button(
    image_input_frame, text="LOAD", command=lambda: handle_image_input(file_name.get())
)

quick_pack([file_input_label, file_input_entry, file_input_button])

image_frame = Frame(ui)
image_frame.pack()

img = ImageTk.PhotoImage(formated_image())
image_label = Label(image_frame, image=img)
image_label.pack()

control_frame = Frame(ui)
control_frame.pack()

start_frame = Frame(control_frame)
stop_frame = Frame(control_frame)
analyze_button_frame = Frame(control_frame)
plot_button_frame = Frame(control_frame)
quick_pack([start_frame, stop_frame, analyze_button_frame, plot_button_frame])

start_label = Label(start_frame, text="START")
start_inputs = Frame(start_frame)
start_label.pack()
start_inputs.pack()

start_x = StringVar()
start_x_label = Label(start_inputs, text="x:")
start_x_entry = Entry(start_inputs, textvariable=start_x, width=3)
start_y = StringVar()
start_y_label = Label(start_inputs, text="y:")
start_y_entry = Entry(start_inputs, textvariable=start_y, width=3)
quick_pack([start_x_label, start_x_entry, start_y_label, start_y_entry])


stop_label = Label(stop_frame, text="START")
stop_inputs = Frame(stop_frame)
stop_label.pack()
stop_inputs.pack()

stop_x = StringVar()
stop_y = StringVar()
stop_x_label = Label(stop_inputs, text="x:")
stop_x_entry = Entry(stop_inputs, textvariable=stop_x, width=3)
stop_y_label = Label(stop_inputs, text="y:")
stop_y_entry = Entry(stop_inputs, textvariable=stop_y, width=3)
quick_pack([stop_x_label, stop_x_entry, stop_y_label, stop_y_entry])

analyze_button = Button(
    analyze_button_frame, text="ANALYZE", command=analyze, state="disabled"
)
analyze_button.pack()

plot_button = Button(
    plot_button_frame, text="PLOT", command=plot_window, state="disabled"
)
plot_button.pack()

ui.mainloop()
clear_image()
