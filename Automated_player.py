
import pyautogui

# 550,525 for cactus
import keyboard
# 1270 344
import time
import numpy



def run() -> None:
    offset = 30  # some offset to quickly adjust the x coordinates of control points
    activated = False

    while True:
        if keyboard.is_pressed('alt+k') and not activated:
            activated = True
            print("works")
        elif keyboard.is_pressed('alt+l') and activated:
            activated = False
            print("not")
            time.sleep(0.6)
        elif keyboard.is_pressed('alt+q'):
            exit(0)


        if activated:
            im = pyautogui.screenshot('im.png',region=(500,860,400,100))

            # we need more than one pixel because i could archive faster screenshots than 12/s so it isnt guaranteed to
            # catch obstacle everytime, also that's why this bot has some limitations such as it almost always fails when
            # large cactus's are at the beginning (we have to setup multiple control pixels so this means (too) early jumps


            p1 = im.getpixel((598 + offset, 850))
            p2 = im.getpixel((700 + offset, 845))
            p3 = im.getpixel((800 + offset, 840))
            p4 = im.getpixel((900 + offset, 855))

            #p_bird = im.getpixel((600, 450))
            p_bird = im.getpixel((600, 765))
            p_bird_1 = im.getpixel((700, 765))
            p_bird_2 = im.getpixel((800, 765))
            p_bird_3 = im.getpixel((900, 765))
            # if one of those pixels are not white it means that there is a cactus in front of dino
            if p1[0] != 255 or p2[0] != 255 or p3[0] != 255 or p4[0] != 255:
                pyautogui.keyDown('up')
                pyautogui.keyUp('up')

            # if this pixel is not white then there is a bird in front
            # only one because bird is much thicker than cactus so it almost always gets detected
            elif (p_bird[0] != 255 or p_bird_1[0]!= 255 or p_bird_2[0]!= 255 or p_bird_3[0]!= 255):
                pyautogui.keyDown("down")
                time.sleep(1)
                pyautogui.keyUp("down")

counter=0
while True:
    counter+=1
    im = pyautogui.screenshot(region=(480,860,300,50))

    im2arr = numpy.array(im)
    if(83,83,83) in im2arr:
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
    else:
        print("nie")