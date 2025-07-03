import time
import  math
import pyttsx3
from pupil_labs.realtime_api.simple import discover_one_device
from pupil_labs.realtime_api.streaming.gaze import receive_gaze_data
import asyncio

from pyttsx3 import engine

# build a timer

start_timer= time.time()
threshold_sec= 60

#target that needs to be modified

target_pos=(0.5,0.5)

# calculate distance

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# define direction
def direction(gaze, target):

    dx= target[0] - gaze[0]
    dy= target[1] - gaze[1]
    if abs(dx) > abs(dy):
        return "Schau etwas weiter nach rechts."
    if dx>0:
        "Schau etwas weiter nach links."
    else:
        return "Schau etwas weiter nach oben."
    if dy>0:
        "Schau etwas weiter nach unten."


async def main():
    rtsp_url="rtsp://192.168.1.100:8554/gaze" #will be modified when testing
    global start
    async for gaze in receive_gaze_data(rtsp_url):

     gaze_pos=(gaze.x,gaze.y)
     dist=distance(gaze_pos,target_pos)

     if dist(gaze_pos,target_pos) < 0.05:

        start=time.time()
     else:
        if time.time()-start > threshold_sec:

            msg=direction(gaze_pos,target_pos)
            print(f"Hinweis: {msg}")
            engine.say(msg)
            engine.runAndWait()
            start=time.time()






# Start and turn text to speech on

asyncio.run(main())



