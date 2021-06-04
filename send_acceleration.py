from microbit import *

dizImm = {"up":Image.ARROW_N, "down":Image.ARROW_S, "right":Image.ARROW_E, "left":Image.ARROW_W, "face up":Image.SQUARE}

while True:
    gesture = accelerometer.current_gesture()
    if gesture == "up" or gesture == "down" or gesture == "right" or gesture == "left" or gesture == "face up":
        a = gesture
        display.show(dizImm[gesture])

    if button_a.is_pressed():
        print("shot")

    print(a)
    sleep(5)