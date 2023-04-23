import cv2
import numpy as np
import time
import mss
from ahk import AHK


def detect_color(img, materials):
    Material = 0
    type_cont = ''
    start = time.time()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for i in materials:
        template = cv2.imread(f'materials/{i}', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            x = cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            Material = np.sum(x)
            if Material > 0:
                type_cont = i

        if Material > 0:
            break
    if Material > 0:
        end = time.time()
        total_time = end-start
        print('{} sec'.format(total_time))
        return Material, type_cont
    else:
        return 0, ''


ahk = AHK()
sct = mss.mss()
material = ["bumaga1.png", "bumaga2.png", "bumaga3.png", "organic1.png", "organic2.png", "plastik1.png", "plastik2.png", "steklo1.png", "steklo2.png"]
containers = {'bumaga1.png': (1466, 382), 'bumaga2.png': (1466, 382), 'bumaga3.png': (1466, 382), 'organic1.png': (1463, 720), 'organic2.png': (1463, 720),
              'plastik1.png': (461, 378), 'plastik2.png': (461, 378), 'steklo1.png': (447, 739), 'steklo2.png': (447, 739)}

while True:
    hasMaterial = 0
    type_container = ''

    monitor = {'top': 400, 'left': 850, 'width': 500, 'height': 500}
    img = np.array(sct.grab(monitor))

    hasMaterial, type_container = detect_color(img, materials)

    if hasMaterial > 0:
        ahk.mouse_position = (963, 522)
        while True:
            ahk.mouse_drag(containers[type_container])
            if ahk.mouse_position == containers[type_container]:
                break

    cv2.imshow('tutle', img)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        print(img)
