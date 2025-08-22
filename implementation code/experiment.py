import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Label, Button
from PySide6.QtCore import Qt, QRect, QMargins
from PySide6.QtGui import QPainter, QColor, QPixmap, QImage
from PySide6.QtWidgets import QApplication, QWidget
from pupil_labs.real_time_screen_gaze import marker_generator
from pupil_labs.real_time_screen_gaze.gaze_mapper import GazeMapper
import time
import math
import pyttsx3
from pupil_labs.realtime_api.simple import discover_one_device
import threading


# Text-to-speech engine
engine=pyttsx3.init()
threshold_sec= 10
screen_size=(2880,1920)

class MarkerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.marker_size = 150
        self.pixmaps = [self.createMarker(i) for i in range(4)]
        self.visibleMarkerIds = []
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

    def update_marker_visibility(self, visible_ids):
        self.visibleMarkerIds = visible_ids
        self.repaint()
    def createMarker(self, marker_id):
        marker = marker_generator.generate_marker(marker_id, flip_x=True, flip_y=True)
        image = QImage(marker.shape[1], marker.shape[0], QImage.Format_Mono)
        for y in range(marker.shape[0]):
            for x in range(marker.shape[1]):
                color = marker[y][x] // 255
                image.setPixel(x, y, color)
        return QPixmap.fromImage(image)

    def getCornerRect(self, cornerIdx):
        padding = 30
        if cornerIdx == 0:
            # The first parameter is x and the second is y
            return QRect(padding, padding, self.marker_size, self.marker_size)
        elif cornerIdx == 1:
            return QRect(self.width() - self.marker_size - padding, padding, self.marker_size, self.marker_size)
        elif cornerIdx == 2:
            return QRect(self.width() - self.marker_size - padding, self.height() - self.marker_size - padding,
                         self.marker_size, self.marker_size)
        elif cornerIdx == 3:
            return QRect(padding, self.height() - self.marker_size - padding, self.marker_size, self.marker_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        for cornerIdx in range(4):
            cornerRect = self.getCornerRect(cornerIdx)
            if cornerIdx not in self.visibleMarkerIds:
                painter.fillRect(cornerRect.marginsAdded(QMargins(25, 25, 25, 25)), QColor(127,127,127))
            painter.drawPixmap(cornerRect, self.pixmaps[cornerIdx])
            painter.fillRect(cornerRect, QColor(0, 0, 0, 128))

    def showMarkers(self):
        self.show()
        self.repaint()






class ExperimentApp:
    def __init__(self, marker_window):

        self.marker_window = marker_window
        self.welcome = Tk()
        self.welcome.title("The visual guidance experiment!")
        self.welcome.attributes('-fullscreen', True)
        self.start_timer = time.time()
        self.hint_lock=threading.Lock()
        self.last_hint_time=0
        self.hint_cooldown=threshold_sec
        self.is_hint_active=False
        self.target_found=False
        self.gaze = None
        self.device= discover_one_device(max_search_duration_seconds=10)
        calibration= self.device.get_calibration()
        self.gazeMapper=GazeMapper(calibration)
        self.get_gaze_data()
        self.surface=None
        self.offset_x=0
        self.offset_y=0
        self.target_pos=(0,0)
        self.found_radius = 200
        self.assistance_enabled= False
        self.targets={

            "slide2":(297.67,119.71),
            "slide3":(67.71,433.93),
            "slide4":(558,163.71),
            "slide5":(310.29,128.13),
            "slide6":(256.07,422.03),
            "slide7":(57.19,375),
            "slide8":(420.94,210.48),
            "slide9":(522.98,466.05),
            "slide10":(297.95,538.69),
            "slide11":(481.99,57.26),

        }

        marker_size=self.marker_window.marker_size

        marker_verts = {
        0: [(30, 30), (30+marker_size, 30), (30+marker_size, 30+marker_size), (30, 30+marker_size)],
        1: [(screen_size[0]-30-marker_size, 30), (screen_size[0]-30, 30),
        (screen_size[0]-30, 30+marker_size), (screen_size[0]-30-marker_size, 30+marker_size)],
        2: [(screen_size[0]-30-marker_size, screen_size[1]-30-marker_size),
        (screen_size[0]-30, screen_size[1]-30-marker_size),
        (screen_size[0]-30, screen_size[1]-30),
        (screen_size[0]-30-marker_size, screen_size[1]-30)],
        3: [(30, screen_size[1]-30-marker_size), (30+marker_size, screen_size[1]-30-marker_size),
        (30+marker_size, screen_size[1]-30), (30, screen_size[1]-30)]
        }

        self.gazeMapper.clear_surfaces()
        self.surface = self.gazeMapper.add_surface(marker_verts,screen_size)
        self.get_gaze_data()



        if self.device is None:
            print("No device found.")
            raise SystemExit()
        print(f"Connected to {self.device.serial_number_glasses}. Press Ctrl-C to stop.")



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
    def get_gaze_data(self):
        frameAndGaze = self.device.receive_matched_scene_video_frame_and_gaze(timeout_seconds=0.5)
        if frameAndGaze is None:
            print("keine gaze-Daten empfangen! ")
            self.welcome.after(500,self.get_gaze_data)
            return

        frame,gaze=frameAndGaze
        result = self.gazeMapper.process_frame(frame,gaze)
        markerIds = [int(marker.uid.split(':')[-1]) for marker in result.markers]

        if self.surface.uid in result.mapped_gaze:
            for surface_gaze in result.mapped_gaze[self.surface.uid]:
                self.gaze = surface_gaze

        if self.gaze is None:
            self.welcome.after(500,self.get_gaze_data)
            print("keine gaze-Daten gefunden! ")
            return

        # The gaze datum is a named tuple containing x, y, worn, and timestamp.
        # We can access these values as attributes.
        print(
            f"Gaze (x,y): ({self.gaze.x:.2f}, {self.gaze.y:.2f}) | "
        )
        raw_gx, raw_gy = float(self.gaze.x), float(self.gaze.y)
        sx, sy = screen_size
        gaze_pos = ((raw_gx+self.offset_x) * sx, (raw_gy+self.offset_y) * sy)

        dist=self.distance(gaze_pos,self.target_pos)
### big issues here to solve
        if dist < self.found_radius:
            if not self.target_found:
                print("Ziel gefunden")
                self.speak_async("Ziel gefunden")
                needed_time = time.time()-self.start_timer
                print("Gefunden in : " + str(needed_time))
            self.target_found=True
        else:
            # move to code where next slide
            if self.target_found and dist > (self.found_radius):
                self.target_found = False
            if not self.target_found:
                elapsed = time.time() - self.start_timer
                time_since_last_hint = time.time() - self.last_hint_time
                print("dwad")
                if self.assistance_enabled and elapsed >= threshold_sec and time_since_last_hint >= self.hint_cooldown : #and not self.hint_active
                    msg = self.direction(gaze_pos, self.target_pos) # hier ist irgendwas
                    if msg:
                        print(f"Hinweis: {msg}")
                        self.last_hint_time = time.time()
                        self.speak_async(msg)



        self.welcome.after(100, self.get_gaze_data)


    def calibrate_glasses(self):
        print("Kalibrierung gestartet")
        frameAndGaze=self.device.receive_matched_scene_video_frame_and_gaze(timeout_seconds=0.5)

        if frameAndGaze is None:
            print("keine gaze-Daten empfangen! ")
            return

        frame,gaze=frameAndGaze
        result=self.gazeMapper.process_frame(frame,gaze)

        if self.surface.uid in result.mapped_gaze:
            print("dd")
            for surface_gaze in result.mapped_gaze[self.surface.uid]:
                self.offset_x = 0.501 - surface_gaze.x
                self.offset_y=  0.465 -surface_gaze.y
        print("Kalibrierung fertig!")

    def calibrate_and_continue(self, next_frame):
        self.marker_window.showMarkers()
        self.welcome.after(2000, lambda: self.finish_calibration(next_frame))


    def finish_calibration(self, next_frame):
        self.calibrate_glasses()
        self.show_frame(next_frame)

        self.start_timer = time.time()
        self.last_hint_time=time.time()
        self.target_found = False
        self.start_counting()

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
                       text="Deine Aufgabe ist es auf Bildern Walter zu finden.\nVor jedem Bild erscheint ein Countdown.",
                       font=("Segoe UI", 18))
        label2.pack(expand=True)

        try:
            image = Image.open("pictures/waldo.jpg").resize((600, 600))
            photo = ImageTk.PhotoImage(image)
            image_label = Label(self.slides['slide1'], image=photo)
            image_label.image = photo
            image_label.pack(expand=False)
        except FileNotFoundError:
            print("Beispielbild nicht gefunden!")

        start_button = Button(self.slides['slide1'], text="Starten", font=("Segoe UI", 20),
                              command=lambda: self.calibrate_and_continue(self.slideCountdown))
        start_button.pack(side="bottom", pady=20)

        self.countdown_label = Label(self.slideCountdown, text="", font=("Segoe UI", 40), fg="red")
        self.countdown_label.pack(expand=True)

        pause_label = Label(self.slidePause, text="Pause. Drücke weiter, um fortzufahren und schaue auf dem Button um zu kalibrieren",
                            font=("Segoe UI", 18))
        pause_label.pack(pady=30)

        pause_button = Button(self.slidePause, text="Weiter", font=("Segoe UI", 20),
                              command=lambda: self.calibrate_and_continue(self.slideCountdown))
        pause_button.pack(expand=True)

    def setup_end_slide(self):
        end_label = Label(self.slideEnd,
                          text="Du hast es geschafft! Danke für deine Teilnahme!",
                          font=("Segoe UI", 30), fg="green")
        end_label.pack(expand=True)

    def load_images(self):
        for i in range(2, 12):
            try:
                image_path = f"pictures/whereIsWaldo{i-1}.jpg"
                img = Image.open(image_path).resize((2200,1920))
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
            self.slideCountdown.after(1000, lambda: self.start_counting(seconds - 1))
        else:
            if self.current_index < len(self.image_orders):
                slide_name = f'slide{self.image_orders[self.current_index]}'
                if slide_name in self.targets:
                    self.target_pos = self.targets[slide_name]
                    print(f"Target für {slide_name}: {self.target_pos}")
                else:
                    self.target_pos = None
                if self.current_index < 3:
                    self.assistance_enabled = False
                else:
                    self.assistance_enabled = True
                    print(f"Assistenz aktiv: {self.assistance_enabled}")
                self.show_frame(self.slides[slide_name])
                self.slideCountdown.after(15000, lambda: self.show_frame(self.slidePause))
                self.current_index += 1
            else:
                self.show_frame(self.slideEnd)

    def distance(self,p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    # define direction
    def direction(self, gaze, target):
        print("Sie lebt")
        dx = target[0] - gaze[0]
        dy = target[1] - gaze[1]

        print(f"Gaze: {gaze}, Target: {target}, dx={dx}, dy={dy}")

        if abs(dx) > abs(dy):
            if dx>0:

                return "Schau etwas weiter nach rechts."
            else:
                return "Schau etwas weiter nach links."
        else:
            if dy>0:
                return "Schau etwas weiter nach unten."
            if dy<0:
                return "Schau etwas weiter nach oben."



    def speak_async(self,text,callback=None):
        def run():
            engine.say(text)
            engine.runAndWait()
            if callback:
                callback()
        threading.Thread(target=run).start()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    marker_window = MarkerWindow()
    ExperimentApp(marker_window)
    sys.exit(app.exec())
