import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


def show_frame(frame):
    frame.tkraise()
# a frame for welcoming
welcome = Tk()
welcome.title("The visual guidance experiment! ")

slide1=tk.Frame(welcome)
slide2=tk.Frame(welcome)

for frame in(slide1,slide2):
    frame.grid(row=0,column=0,sticky="nsew")
    welcome.rowconfigure(0, weight=1)
    welcome.columnconfigure(0, weight=1)

# make a fullscreen view
welcome.attributes('-fullscreen',True)

# welcoming label

label=tk.Label(slide1, text="Willkommen im Experiment!", font=("segoe UI",30))
label2=tk.Label(slide1, text="Deine Aufgaben ist nun Walter zu finden. Viel Glück!!!" ,font=("segoe UI", 20))
label.pack(expand=True)


# waldo's picture

image= Image.open("waldo.jpg")
image=image.resize((350,350),Image.Resampling.LANCZOS)
photo=ImageTk.PhotoImage(image)

image_label=tk.Label(slide1,image=photo)
image_label.image=photo
image_label.pack(expand=TRUE)

label2.pack(expand=True)

# creating a start button

start_button= tk.Button(slide1,text="Starten", font=("segoe UI",16),command=lambda:show_frame(slide2))
start_button.pack(pady=20)

# placing the picture for the experiment
waldo_image=open("WhereIsWaldo.jpg")
waldo_image=waldo_image.resize((700,700),Image.Resampling.LANCZOS)
photo=ImageTk.PhotoImage(waldo_image)

waldo_image_label=tk.label(slide2)


# exiting fullscreen mode with esc

def endFullscreen(event):
    welcome.attributes("-fullscreen",False)
welcome.bind("<Escape>", endFullscreen)

show_frame(slide1)

welcome.mainloop()





