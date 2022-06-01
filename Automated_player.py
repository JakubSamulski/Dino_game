import PIL
import pyautogui
import PIL.ImageGrab
# 550,525 for cactus
import keyboard
# 1270 344
import time
import dxcam
import pyscreeze
import time



def run() -> None:
    offset = 30  # some offset to quickly adjust the x coordinates of control points
    activated = False

    while True:
        if keyboard.is_pressed('alt+k') and not activated:
            activated = True
            print("dziala")
        elif keyboard.is_pressed('alt+l') and activated:
            activated = False
            print("nie dziaala")
            time.sleep(0.6)
        elif keyboard.is_pressed('alt+q'):
            exit(0)


        if activated:
            im = pyautogui.screenshot()

            # we need more than one pixel because i could archive faster screenshots than 12/s so it isnt guaranteed to
            # catch obstacle everytime, also that's why this bot has some limitations such as it almost always fails when
            # large cactus's are at the beginning (we have to setup multiple control pixels so this means (too) early jumps
            p1 = im.getpixel((560 + offset, 530))
            p2 = im.getpixel((580 + offset, 525))
            p3 = im.getpixel((600 + offset, 500))
            p4 = im.getpixel((610 + offset, 500))

            p_bird = im.getpixel((600, 450))

            # if one of those pixels are not white it means that there is a cactus in front of dino
            if p1[0] != 255 or p2[0] != 255 or p3[0] != 255 or p4[0] != 255:
                pyautogui.keyDown('up')
                pyautogui.keyUp('up')

            # if this pixel is not white then there is a bird in front
            # only one because bird is much thicker than cactus so it almost always gets detected
            elif (p_bird[0] != 255):
                pyautogui.keyDown("down")
                time.sleep(1)
                pyautogui.keyUp("down")

run()