import time
import  math
import pyttsx3
from pupil_labs.realtime_api.simple import discover_one_device
from pupil_labs.realtime_api.streaming.gaze import receive_gaze_data
import asyncio

# Text-to-speech engine
engine=pyttsx3.init()


# Look for a device on the network.
print("Looking for a device...")
device = discover_one_device(max_search_duration_seconds=10)
if device is None:
    print("No device found.")
    raise SystemExit()
    print(f"Connected to {device.serial_number_glasses}. Press Ctrl-C to stop.")


while True:
    # receive_gaze_datum() will return the next available gaze datum
    # or block until one becomes available.
    gaze = device.receive_gaze_datum()
    # The gaze datum is a named tuple containing x, y, worn, and timestamp.
    # We can access these values as attributes.
    print(
        f"Timestamp: {gaze.timestamp_unix_seconds:.3f} | "
        f"Gaze (x,y): ({gaze.x:.2f}, {gaze.y:.2f}) | "
        f"Worn: {gaze.worn}"
    )


# Stream gaze data.
# build a timer

start_timer= time.time()
threshold_sec= 20

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
    global start


    while True:


     gaze=device.receive_gaze_datum()
     gaze_pos=(gaze.x,gaze.y)
     dist=distance(gaze_pos,target_pos)

     if dist(gaze_pos,target_pos) < 0.05:

        start=time.time()
        print("Ziel gefunden")
        engine.say("Ziel gefunden")
        engine.runAndWait()
     else:
        if time.time()-start > threshold_sec:

            msg=direction(gaze_pos,target_pos)
            print(f"Hinweis: {msg}")
            engine.say(msg)
            engine.runAndWait()
            start=time.time()

# Start and turn text to speech on

_



