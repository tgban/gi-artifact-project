# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 23:29:55 2023

@author: canh_
"""
import numpy as np
from PIL import ImageGrab
import cv2 as cv
import artifact_img2text
import genshin_artifact_score as gas
import genshin_artifact as ga
import time
from os import system, name

#--- Variables
# cv.namedWindow('Window', cv.WINDOW_KEEPRATIO)
# cv.resizeWindow('Window', 1200, 700)
loffset = 120
roffset = -80
toffset = 10
boffset = 10
# loffset = 0
# roffset = 0
# toffset = 0
# boffset = 0

classifier = cv.CascadeClassifier()
if not classifier.load(cv.samples.findFile('data/cascade.xml')):
    print('Unable to load cascade')
    exit(0)


#--- Functions
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    time.sleep(0.1)
def display_image(arr):
    frame_gray = cv.cvtColor(arr, cv.COLOR_RGB2BGR)
    cv.imshow('Window', frame_gray)
def detect_and_display(arr):
    display = arr
    frame_gray = cv.cvtColor(arr, cv.COLOR_RGB2GRAY)
    frame_gray_hist = cv.equalizeHist(frame_gray)
    detected = classifier.detectMultiScale(frame_gray_hist, minSize=(410,420), maxSize=(430,470))
    scored = False
    for (x, y, w, h) in detected:
        tl = (max(0, x - loffset), max(0, y - toffset))
        br = (min(x + w + roffset, arr.shape[1] - 1), min(y + h + boffset, arr.shape[0] - 1))
        mainType, mainStat, lines, setName = artifact_img2text.phathientdv(arr[tl[1]:br[1],tl[0]:br[0],:])
        # display = cv.rectangle(arr, (tl[0], tl[1]), (br[0], br[1]), (0, 0, 255), 4)
        # display_image(display)
        if setName and len(lines) > 0:
            print('Type:', ga.types[mainType])
            print('Set:', setName)
            print('\tMain stat:', ga.stats[mainStat])
            for line in lines:
                print('\t' + ga.stats[line])
            score = gas.danhgiatdv(mainType, mainStat, lines, setName)
            # print('Score:', score)
            print('-------------------------------------')
            scored = True
            return scored, mainType, mainStat, lines, setName
    return False, None, None, None, None
#--- Main program
w = open('newset.csv', 'wt')
while True:
    print('Detecting...')
    pil_screen = ImageGrab.grab()
    numpy_screen = np.array(pil_screen, dtype=np.uint8).reshape((pil_screen.size[1], pil_screen.size[0], 3))
    result, t, st, l, s = detect_and_display(numpy_screen)
    if result:
        n = input("Press Enter to continue, s to save, or q to quit:")
        if n == 'q':
            # cv.destroyAllWindows()
            break
        elif n == 's':
            print(t, st, sep=',',end=',',file=w)
            l.sort()
            for x in l:
                print(x, end=',',file=w)
            print(list(ga.setName.keys()).index(s),file=w)
    # if cv.waitKey(10) & 0xFF == 27:
w.close()