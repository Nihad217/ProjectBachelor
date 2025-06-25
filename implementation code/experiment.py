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


for frame in(slide1,slide2,slide3,slide4,slide5,slide6,slide7,slide8,slide9,slide10):
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

start_button= tk.Button(slide1,text="Starten", font=("Segoe UI",16),command=lambda:start_counting(3))
start_button.pack(pady=20)
countdown_label =tk.Label(slide1, text="", font=("Segoe UI",40),fg="red")
countdown_label.pack(pady=10)


# placing the pictures for the experiment
waldo_image=Image.open("WhereIsWaldo2.jpg")
waldo_image= waldo_image.resize((1000,1000),Image.Resampling.LANCZOS)

photo=ImageTk.PhotoImage(waldo_image)

waldo_image_label=tk.Label(slide2, image=photo)
waldo_image_label.image=photo
waldo_image_label.pack(expand=TRUE)

waldo_image2=Image.open("whereIsWaldo.jpg")
photo2=ImageTk.PhotoImage(waldo_image2)

waldo_image2_label=tk.Label(slide3, image=photo2)
waldo_image2_label.image=photo2
waldo_image2_label.pack(expand=TRUE)

waldo_image3=Image.open("whereIsWaldo3.jpg")
waldo_image3=waldo_image3.resize((1000,1000),Image.Resampling.LANCZOS)
photo3=ImageTk.PhotoImage(waldo_image3)

waldo_image3_label=tk.Label(slide4, image=photo3)
waldo_image3_label.image=photo3
waldo_image3_label.pack(expand=True)

waldo_image4=Image.open("whereIsWaldo4.jpg")
waldo_image4=waldo_image4.resize((1000,1000),Image.Resampling.LANCZOS)
photo4=ImageTk.PhotoImage(waldo_image4)

waldo_image4_label=tk.Label(slide5, image=photo4)
waldo_image4_label.image=photo4
waldo_image4_label.pack(expand=True)


waldo_image5=Image.open("whereIsWaldo5.jpg")
waldo_image5=waldo_image5.resize((1000,1000),Image.Resampling.LANCZOS)
photo5=ImageTk.PhotoImage(waldo_image5)

waldo_image5_label=tk.Label(slide6, image=photo5)
waldo_image5_label.image=photo5
waldo_image5_label.pack(expand=True)

waldo_image6=Image.open("whereIsWaldo6.jpg")
waldo_image6=waldo_image6.resize((1000,1000),Image.Resampling.LANCZOS)
photo6=ImageTk.PhotoImage(waldo_image6)

waldo_image6_label=tk.Label(slide7, image=photo6)
waldo_image6_label.image=photo6
waldo_image6_label.pack(expand=True)

waldo_image7=Image.open("whereIsWaldo7.jpg")
photo7=ImageTk.PhotoImage(waldo_image7)

waldo_image7_label=tk.Label(slide8, image=photo7)
waldo_image7_label.image=photo7
waldo_image7_label.pack(expand=True)




# Developing an automatic switch to the next picture after delay through slide3

def go_to_slide2():
    show_frame(slide2)
    slide2.after(2000,go_to_slide3)


def go_to_slide3():
    show_frame(slide3)
    slide3.after(2000,go_to_slide4)

def go_to_slide4():
    show_frame(slide4)
    slide4.after(2000,go_to_slide5)

def go_to_slide5():
    show_frame(slide5)
    slide5.after(2000,go_to_slide6)

def go_to_slide6():
    show_frame(slide6)
    slide6.after(2000,go_to_slide7)

def go_to_slide7():
    show_frame(slide7)
    slide7.after(2000,lambda :show_frame(slide8))

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





