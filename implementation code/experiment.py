import time
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
slide3=tk.Frame(welcome)
slide4=tk.Frame(welcome)
slide5=tk.Frame(welcome)
slide6=tk.Frame(welcome)
slide7=tk.Frame(welcome)
slide8=tk.Frame(welcome)
slide9=tk.Frame(welcome)
slide10=tk.Frame(welcome)


for frame in(slide1,slide2,slide3):
    frame.grid(row=0,column=0,sticky="nsew")
    welcome.rowconfigure(0, weight=1)
    welcome.columnconfigure(0, weight=1)
    welcome.columnconfigure(0,weight=1)

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

start_button= tk.Button(slide1,text="Starten", font=("Segoe UI",16),command=lambda:start_counting(3))
start_button.pack(pady=20)
countdown_label =tk.Label(slide1, text="", font=("Segoe UI",40),fg="red")
countdown_label.pack(pady=10)


# placing the pictures for the experiment
waldo_image=Image.open("WhereIsWaldo.jpg")

photo=ImageTk.PhotoImage(waldo_image)

waldo_image_label=tk.Label(slide2, image=photo)
waldo_image_label.image=photo
waldo_image_label.pack(expand=TRUE)

waldo_image2=Image.open("whereIsWaldo2.jpg")
waldo_image2= waldo_image2.resize((1000,1000),Image.Resampling.LANCZOS)
photo=ImageTk.PhotoImage(waldo_image2)

waldo_image2_label=tk.Label(slide3, image=photo)
waldo_image2_label.image=photo
waldo_image2_label.pack(expand=TRUE)

# Developing an automatic switch to the next picture after delay through slide3
def go_to_slide2():
    show_frame(slide2)
    slide2.after(6000,lambda:show_frame(slide3))

# defining a function for countdown

def start_counting(seconds):
    if seconds >= 0:
        countdown_label.config(text=str(seconds))
        slide1.after(1000,lambda:start_counting(seconds-1))

    else:
        countdown_label.config(text="")
        go_to_slide2()


# exiting fullscreen mode with esc

def endFullscreen(event):
    welcome.attributes("-fullscreen",False)
welcome.bind("<Escape>", endFullscreen)

show_frame(slide1)

welcome.mainloop()





