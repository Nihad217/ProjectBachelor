import time
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random



def show_frame(frame):
    frame.tkraise()
# a frame for welcoming
welcome = Tk()
welcome.title("The visual guidance experiment!")
welcome.attributes('-fullscreen',True)

def show_frame(frame):
    frame.tkraise()

# define the slides for the experiment
slides={}
slidePause=tk.Frame(welcome)
slideCountdown=tk.Frame(welcome)
slideEnd=tk.Frame(welcome)

# Create the frames with a for loop
for i in range(1,13):
    slides[f'slide{i}']=tk.Frame(welcome)



for frame in list(slides.values())+[slidePause, slideCountdown,slideEnd]:
    frame.grid(row=0,column=0,sticky="nsew")
    welcome.rowconfigure(0, weight=1)
    welcome.columnconfigure(0, weight=1)

# Global var
image_orders=list(range(2,12))
random.shuffle(image_orders)
current_index=0
slide1=slides['slide1']

# defining a countdown system
# Developing an automatic switch to the next picture after delay
def start_counting(seconds=3):
    if seconds > 0:
        countdown_label.config(text=str(seconds))
        slideCountdown.after(1000,lambda:start_counting(seconds-1))

    else:
        global current_index
        if current_index< len(image_orders):
            slide_name = f'slide{image_orders[current_index]}'
            show_frame(slides[slide_name])
            slideCountdown.after(1000,lambda :show_frame(slidePause))
            current_index+=1
        else:

            show_frame(slideEnd)

# Pause slide logic for giving the participants momentary pause

pause_label = tk.Label(slidePause, text="Zeit ist um. Nun kannst du Pause machen und danach fortfahren", font=("Segoe UI", 18))
pause_label.pack(pady=30)
countdown_label =tk.Label(slideCountdown, text="", font=("Segoe UI",40),fg="red")
countdown_label.pack(expand=True)
pause_button=tk.Button(slidePause,text="Weiter",font=("Segoe UI",20),command=lambda:[show_frame(slideCountdown),start_counting()])
pause_button.pack(expand=True)

#slide 1 starting button
start_button= tk.Button(slide1,text="Starten", font=("Segoe UI",20),command=lambda:[show_frame(slideCountdown), start_counting()])
start_button.pack(side="bottom" ,pady=20)

#slide 1 settings


label=tk.Label(slide1, text="Willkommen im Experiment!", font=("Segoe UI",30))
label2=tk.Label(slide1, text="Deine Aufgabe ist es auf Bildern Walter zu finden. Vor jedem Bild erscheint ein Countdown, \n der von 3 runterzählt. Direkt nach dem Countdown erscheint das nächste Bild. Viel Glück!!!" ,font=("Segoe UI", 18))
label.pack(expand=True)



# waldo's picture

image= Image.open("pictures/waldo.jpg")
image=image.resize((350,350),Image.LANCZOS)
photo=ImageTk.PhotoImage(image)

image_label=tk.Label(slide1,image=photo)
image_label.image=photo
image_label.pack(expand=TRUE)

label2.pack(expand=True)




# placing the pictures for the experiment
for i in range(2, 12):
        try:
            image_path = f"pictures/whereIsWaldo{i-1}.jpg"
            img = Image.open(image_path).resize((1000, 1000), Image.LANCZOS)
            ph = ImageTk.PhotoImage(img)
            label = tk.Label(slides[f'slide{i}'], image=ph)
            label.image = ph
            label.pack(expand=True)
        except FileNotFoundError:
            print(f"Bild {image_path} nicht gefunden!")

end_label=tk.Label(slideEnd,text="Der letzte Timer war ein Witz.\n Du hast es geschafft! Danke für deine Teilnahme!!!",font=("Segoe UI",30),fg="green")
end_label.pack(expand=True)

# exiting fullscreen mode with esc

def endFullscreen(event):
    welcome.attributes("-fullscreen",False)
welcome.bind("<Escape>", endFullscreen)
show_frame(slide1)
welcome.mainloop()





