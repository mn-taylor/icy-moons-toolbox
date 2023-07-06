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
    # Takes the image "display" file and resizes it to fit the window and stores the result in
    # resize image file
    return Image.open("images/display.png").resize((300, 300), Image.ANTIALIAS)


def analyze():
    def handle_no():
        global confirmed
        top.destroy()
        confirmed = False

    global ui, global_image, computation, start, stop, removed, v_scale, h_scale, units, confirmed, file_name
    confirmed = True

    # start and stop indices are ill-formed
    if len(string_to_tuples(start.get())) < 1 or len(string_to_tuples(stop.get())) < 1:
        messagebox.showerror("Please format start and stop indices as (x, y)")
        return

    # missing inputs
    if h_scale.get() == "" or v_scale.get() == "" or units.get() == "":
        messagebox.showerror("Please input the images pixels scales and units")
        return
    """
    if removed.get("1.0", "end-1c") != "":
        top = Toplevel(ui)
        confirmation = "Are you sure that you want to remove" + str(
            string_to_tuples(removed.get("1.0", "end-1c"))
        )
        confirmation_label = Label(top, text=confirmation)
        confirmation_label.pack(side="top")
        buttons_frame = Frame(top)
        buttons_frame.pack(side="top")
        yes_button = Button(buttons_frame, text="YES", command=lambda: top.destroy)
        no_button = Button(buttons_frame, text="NO", command=handle_no)
        quick_pack([yes_button, no_button], side="left")
    """
    if confirmed:
        file = "images/" + file_name.get()
        horizonal = float(h_scale.get())
        vertical = float(v_scale.get())
        if len(string_to_tuples(start.get())) == 1:
            start_idx = string_to_tuples(start.get())[0]
        else:
            start_idx = (0, 0)
        if len(string_to_tuples(stop.get())) == 1:
            stop_idx = string_to_tuples(stop.get())[0]
        else:
            stop_idx = None

        computation = facet_compute(
            file, horizonal, vertical, units.get(), start_idx, stop_idx
        )
        computation.flood_count()

        to_remove = []
        if removed.get("1.0", "end-1c"):
            to_remove = string_to_tuples(removed.get("1.0", "end-1c"))
        computation.remove_facets(to_remove)

        computation.get_image().save("images/display.png")
        global_image = ImageTk.PhotoImage(formated_image())
        image_label.config(image=global_image)


def plot():
    global computation
    computation.perimeter_vs_surface()
    pass


def offload():
    global computation, file_name
    output_file = ""
    i = 0
    while file_name.get()[i] != ".":
        output_file += file_name.get()[i]
        i += 1
    output_file += "_data.csv"
    computation.offload_data(output_file)


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
confirmed = True

image_info_frame = Frame(ui)
analysis_frame = Frame(ui)
quick_pack([image_info_frame, analysis_frame], side="top")

image_inputs_frame = Frame(image_info_frame)
load_frame = Frame(image_info_frame)
quick_pack([image_inputs_frame, load_frame], side="top")

image_inputs_frame.pack(side="top")

file_name_frame = Frame(image_inputs_frame)
h_scale_frame = Frame(image_inputs_frame)
v_scale_frame = Frame(image_inputs_frame)
units_frame = Frame(image_inputs_frame)
quick_pack([file_name_frame, h_scale_frame, v_scale_frame, units_frame], side="left")

file_label = Label(file_name_frame, text="File")
file_name = StringVar()
file_input = Entry(file_name_frame, textvariable=file_name)
quick_pack([file_label, file_input], side="top")

h_scale_label = Label(h_scale_frame, text="Horizontal Scale")
h_scale = StringVar()
h_scale_input = Entry(h_scale_frame, textvariable=h_scale)
quick_pack([h_scale_label, h_scale_input], side="top")

v_scale_label = Label(v_scale_frame, text="Vertical Scale")
v_scale = StringVar()
v_scale_input = Entry(v_scale_frame, textvariable=v_scale)
quick_pack([v_scale_label, v_scale_input], side="top")

units_label = Label(units_frame, text="Units")
units = StringVar()
units_input = Entry(units_frame, textvariable=units)
quick_pack([units_label, units_input], side="top")

load_button = Button(load_frame, text="LOAD", command=handle_image_input)
load_button.pack(side="top")

##########################
analysis_inputs_frame = Frame(analysis_frame)
display_frame = Frame(analysis_frame)
quick_pack([analysis_inputs_frame, display_frame], side="left")

start_stop_frame = Frame(analysis_inputs_frame)
remove_frame = Frame(analysis_inputs_frame)
analyze_buttons_frame = Frame(analysis_inputs_frame)
quick_pack([start_stop_frame, remove_frame, analyze_buttons_frame], side="top")

start_frame = Frame(start_stop_frame)
stop_frame = Frame(start_stop_frame)
quick_pack([start_frame, stop_frame], side="left")

start_label = Label(start_frame, text="Start")
start = StringVar()
start_input = Entry(start_frame, textvariable=start, width=10)
quick_pack([start_label, start_input], side="top")

stop_label = Label(stop_frame, text="Stop")
stop = StringVar()
stop_input = Entry(stop_frame, textvariable=stop, width=10)
quick_pack([stop_label, stop_input], side="top")

remove_label = Label(remove_frame, text="Remove")
removed = Text(remove_frame, height=5, width=30)
quick_pack([remove_label, removed], side="top")

analyze_button = Button(analyze_buttons_frame, text="ANALYZE", command=analyze)
plot_button = Button(analyze_buttons_frame, text="PLOT", command=plot)
data_button = Button(analyze_buttons_frame, text="OFFLOAD DATA", command=offload)
quick_pack([analyze_button, plot_button, data_button], side="top")

img = ImageTk.PhotoImage(formated_image())
image_label = Label(display_frame, image=img)
image_label.pack(side="left")


ui.mainloop()
clear_image()
