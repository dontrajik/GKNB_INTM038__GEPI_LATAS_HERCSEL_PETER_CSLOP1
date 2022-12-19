import cv2
import numpy as np
from generator import generateRandomPicture
import os
from random import randint

for i in range(50):
    generateRandomPicture(randint(0, 50))
    for x in os.listdir(os.getcwd()):
        if x.endswith(".png"):
            testPicture = x
    image = cv2.imread(testPicture)
    os.system("rm " + testPicture)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 400, 500)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40,minLineLength=15, maxLineGap=3)

    linesImage = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(linesImage, (x1, y1), (x2, y2), (0, 255, 0), 2)

    linesImage = cv2.medianBlur(linesImage, 7)
    kernel = np.ones((5, 5), np.uint8)
    linesImage = cv2.dilate(linesImage, kernel, iterations=10)
    linesImage = cv2.erode(linesImage, kernel, iterations=15)

    edges = cv2.Canny(linesImage, 30, 200)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour = max(contours, key=cv2.contourArea)

    rect = cv2.minAreaRect(contour)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(image, [box], 0, (36, 255, 12), 3)

    cv2.imshow("result", image)
    cv2.waitKey()

    cv2.destroyAllWindows()
