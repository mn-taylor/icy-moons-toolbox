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
