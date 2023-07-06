import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from facet_area import facet_compute
from utilities import string_to_tuples


def handle_image_input():
    global global_image, computation, file_name
    print(file_name.get())
    try:
        Image.open("images/" + file_name.get()).save("images/display.png")
        computation = None
        global_image = ImageTk.PhotoImage(formated_image())
        image_label.config(image=global_image)
        ui.update_idletasks()

    except:
        try:
            Image.open(file_name.get()).save("images/display.png")
            computation = None
            global_image = ImageTk.PhotoImage(formated_image())
            image_label.config(image=global_image)
            ui.update_idletasks()
        except:
            messagebox.showerror("Image not found")


def clear_image():
    blank = Image.new(mode="RGB", size=(500, 500), color=(0, 0, 0))
    blank.save("images/display.png")

    try:
        plt.close()
    except:
        pass
    # blank.save("resize_image.png")


def formated_image():
    # Takes the image "image_analysis" file and resizes it to fit the window and stores the result in
    # resize image file
    return Image.open("images/display.png").resize((500, 500), Image.ANTIALIAS)


def analyze():
    global global_image, computation
    pass


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
        quick_pack([bucket_size_label, bucker_size_entry], "top")

        threshold_frame = Frame(plot_inputs_frame)
        threshold_frame.pack(side="top")

        threshold = StringVar()
        threshold.set("0")
        threshold_label = Label(threshold_frame, text="Threshold")
        threshold_entry = Entry(threshold_frame, textvariable=threshold)
        quick_pack([threshold_label, threshold_entry], "top")

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
        quick_pack([bucket_size_label, bucker_size_entry], "left")

        threshold_frame = Frame(plot_inputs_frame)
        threshold_frame.pack(side="top")

        threshold = StringVar()
        threshold.set("0")
        threshold_label = Label(threshold_frame, text="Threshold")
        threshold_entry = Entry(threshold_frame, textvariable=threshold)
        quick_pack([threshold_label, threshold_entry], "left")

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


def quick_pack(args, side):
    for elt in args:
        elt.pack(side=side)


clear_image()
ui = Tk()
ui.title("Image Analysis Workspace")
ui.resizable(False, False)
global_image = None
computation = None
plot_inputs_frame = None

ui.mainloop()
clear_image()
