import cv2 as cv2
import pyautogui
import numpy as np
from time import time
import dxcam
import win32api, win32con
from pynput.mouse import Controller, Button


mouseController = Controller()
pyautogui.FAILSAFE = False
camera = dxcam.create()
loop_time = time()
while True:
    # camera.grab returns nparray, represents the image
    frame = camera.grab(region=(909, 489, 1009, 589))

    # It converts the RGB color space of image to HSV color space
    # try-except because sometimes there are strange random errors that happen for no reason
    try:
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    except cv2.error:
        continue

    # Threshold of the purple in HSV space
    lower_blue = np.array([126, 93, 48])
    upper_blue = np.array([157, 212, 255])
    # fps timer
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # preparing the mask to overlay
    kernel = np.ones((5, 5), np.uint8)
    masked = cv2.inRange(hsv, lower_blue, upper_blue)

    # scale iterations by number of white pixels so
    # further away enemies will have less dilation applied.

    whites = np.where(masked == 255)

    sumWhite = len(whites[0])

    if sumWhite > 220:
        its = 2
    else:
        its = 1

    # perform the dilation

    masked = cv2.dilate(masked, kernel, iterations=its)

    if masked[49, 49] == 255:
        mouseController.click(Button.left)

    # if sumWhite > 0:
    #     highest = max_row_index = np.amin(whites[0])
    #     max_col_index = whites[1][np.where(whites[0] == max_row_index)[0][0]]
    #
    #     cv2.circle(masked, (max_col_index, highest), 10, 255, 2)
    #     mouseController.move(max_col_index - 50, highest - 50)
    cv2.imshow('Window', masked)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break