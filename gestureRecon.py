from microbit import *

while True:
    gesture = accelerometer.current_gesture()
    if gesture == "up":
        print("up")
    elif gesture == "down":
        print("down")
    elif gesture == "left":
        print("left")
    elif gesture == "right":
        print("right")
