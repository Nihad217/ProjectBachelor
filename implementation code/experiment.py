import time
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pupil_labs.real_time_screen_gaze import marker_generator



class MarkerWindow(QWidget):

 def __init__(self):
     super().__init__()
     self.setWindowFlag(Qt.FramelessWindowHint| Qt.WindowStaysOnTopHint|Qt.X11BypassWindowManagerHint)
     self.setAttribute(Qt.WA_TranslucentBackground)
     self.marker_size=200
     self.pixmaps=[self.createMarker(i) for i in range(4)]
     self.visibleMarkerIds=[]

     screen=QApplication.primaryScreen().geometry()
     self.setGeometry(0,0,screen.width(),screen.height())
     self.show()
 def createMarker(self, marker_id):
    marker=marker_generator.generate_marker(marker_id, flip_x=True, flip_y=True)
    image=QImage(10,10,QImage.Format_Mono)
    image.fill(1)
    for y in range(marker.shape[0]):
        for x in range(marker.shape[1]):
            color= marker[y][x]//255
            image.setPixel(x+1,y+1,color)
    return QPixmap.fromImage(image)
 def getCornerRect(self,cornerIdx):
     padding = 5  # Abstand vom Rand
     if cornerIdx == 0:  # Top-left
        return QRect(padding, padding, self.marker_size, self.marker_size)
     elif cornerIdx == 1:  # Top-right
        return QRect(self.width()-self.marker_size-padding, padding,
                  self.marker_size, self.marker_size)
     elif cornerIdx == 2:  # Bottom-right
        return QRect(self.width()-self.marker_size-padding,
                  self.height()-self.marker_size-padding,
                  self.marker_size, self.marker_size)
     elif cornerIdx == 3:  # Bottom-left
        return QRect(padding, self.height()-self.marker_size-padding,
                  self.marker_size, self.marker_size)
 def paintEvent(self, event):
    painter = QPainter(self)
    for cornerIdx in range(4):
        cornerRect = self.getCornerRect(cornerIdx)
        if cornerIdx not in self.visibleMarkerIds:
            painter.fillRect(cornerRect.marginsAdded(QMargins(5, 5, 5, 5)), QColor(255, 0, 0))
        painter.drawPixmap(cornerRect, self.pixmaps[cornerIdx])
        painter.fillRect(cornerRect, QColor(0, 0, 0, 128))

 def showMarkerFeedback(self, markerIds):
    self.visibleMarkerIds = markerIds
    self.repaint()


class ExperimentApp:

    def __init__(self):
        self.welcome = Tk()
        self.welcome.title("The visual guidance experiment!")
        self.welcome.attributes('-fullscreen', True)

        self.image_orders = list(range(2, 12))
        random.shuffle(self.image_orders)
        self.current_index = 0

        self.create_frames()
        self.setup_slide1()
        self.load_images()
        self.setup_end_slide()

        self.welcome.bind("<Escape>", lambda e: self.welcome.attributes("-fullscreen", False))
        self.show_frame(self.slides['slide1'])
        self.welcome.mainloop()
    def create_frames(self):
        self.slides = {}
        self.slidePause = Frame(self.welcome)
        self.slideCountdown = Frame(self.welcome)
        self.slideEnd = Frame(self.welcome)

        for i in range(1, 13):
            self.slides[f'slide{i}'] = Frame(self.welcome)

        for frame in list(self.slides.values()) + [self.slidePause, self.slideCountdown, self.slideEnd]:
            frame.grid(row=0, column=0, sticky="nsew")
            self.welcome.rowconfigure(0, weight=1)
            self.welcome.columnconfigure(0, weight=1)
    def setup_slide1(self):
        label = Label(self.slides['slide1'], text="Willkommen im Experiment!", font=("Segoe UI", 30))
        label.pack(expand=True)

        label2 = Label(self.slides['slide1'],
                       text="Deine Aufgabe ist es auf Bildern Walter zu finden. Vor jedem Bild erscheint ein Countdown, \n"
                            "der von 3 runterzählt. Direkt nach dem Countdown erscheint das nächste Bild. Viel Glück!!!",
                       font=("Segoe UI", 18))
        label2.pack(expand=True)

        try:
            image = Image.open("pictures/waldo.jpg")
            image = image.resize((350, 350), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(self.slides['slide1'], image=photo)
            image_label.image = photo
            image_label.pack(expand=True)
        except FileNotFoundError:
            print("Beispielbild nicht gefunden!")

        start_button = Button(self.slides['slide1'], text="Starten", font=("Segoe UI", 20),
                              command=lambda: [self.show_frame(self.slideCountdown), self.start_counting()])
        start_button.pack(side="bottom", pady=20)

        self.countdown_label = Label(self.slideCountdown, text="", font=("Segoe UI", 40), fg="red")
        self.countdown_label.pack(expand=True)

        pause_label = Label(self.slidePause, text="Zeit ist um. Nun kannst du Pause machen und danach fortfahren",
                            font=("Segoe UI", 18))
        pause_label.pack(pady=30)

        pause_button = Button(self.slidePause, text="Weiter", font=("Segoe UI", 20),
                              command=lambda: [self.show_frame(self.slideCountdown), self.start_counting()])
        pause_button.pack(expand=True)




    def setup_end_slide(self):
            end_label = Label(self.slideEnd,
                              text="Der letzte Timer war ein Witz.\n Du hast es geschafft! Danke für deine Teilnahme!!!",
                              font=("Segoe UI", 30), fg="green")
            end_label.pack(expand=True)


    def load_images(self):
        for i in range(2, 12):
            try:
                image_path = f"pictures/whereIsWaldo{i-1}.jpg"
                img = Image.open(image_path).resize((1000, 1000), Image.LANCZOS)
                ph = ImageTk.PhotoImage(img)
                label = Label(self.slides[f'slide{i}'], image=ph)
                label.image = ph
                label.pack(expand=True)
            except FileNotFoundError:
                print(f"Bild {image_path} nicht gefunden!")

    def show_frame(self, frame):
        frame.tkraise()

    def start_counting(self, seconds=3):
        if seconds > 0:
            self.countdown_label.config(text=str(seconds))
            self.slideCountdown.after(1000, lambda: self.start_counting(seconds-1))
        else:
            if self.current_index < len(self.image_orders):
                slide_name = f'slide{self.image_orders[self.current_index]}'
                self.show_frame(self.slides[slide_name])
                self.slideCountdown.after(1000, lambda: self.show_frame(self.slidePause))
                self.current_index += 1
            else:
                self.show_frame(self.slideEnd)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    marker_window = MarkerWindow()
    experiment = ExperimentApp()
    sys.exit(app.exec())






