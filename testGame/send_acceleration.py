from microbit import *

while True:
    gesture = accelerometer.current_gesture()
    if gesture == "up":
        a = "up"
        display.show(Image.ARROW_N)
    elif gesture == "down":
        a = "down"
        display.show(Image.ARROW_S)
    elif gesture == "right":
        a = "right"
        display.show(Image.ARROW_E)
    elif gesture == "left":
        a = "left"
        display.show(Image.ARROW_W)
    else:
        a = "face up"
        display.show(Image.SQUARE)

    if button_a.is_pressed() and lastShot:
        print("shot")

    print(a)
    sleep(5)