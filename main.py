import cv2
import numpy as np
from generator import generateRandomPicture
import os
from random import randint

output = open("result.csv", "w")

for i in range(40):
    noise = randint(0, 50)
    generateRandomPicture(noise)
    for x in os.listdir(os.getcwd()):
        if x.endswith("test.png"):
            testPicture = x[:-9]
    image = cv2.imread(testPicture+".png")
    inputBoundingBox = cv2.imread(testPicture+"_test.png")
    os.system("rm " + testPicture+".png " + testPicture + "_test.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 400, 500)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40,
                            minLineLength=15, maxLineGap=3)

    linesImage = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(linesImage, (x1, y1), (x2, y2), (0, 255, 0), 2)

    linesImage = cv2.medianBlur(linesImage, 7)
    kernel = np.ones((5, 5), np.uint8)
    linesImage = cv2.dilate(linesImage, kernel, iterations=10)
    linesImage = cv2.erode(linesImage, kernel, iterations=15)

    edges = cv2.Canny(linesImage, 30, 200)

    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour = max(contours, key=cv2.contourArea)

    rect = cv2.minAreaRect(contour)
    boundingBox = np.zeros_like(image).astype(np.uint8)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(image, [box], 0, (36, 255, 12), 3)
    cv2.drawContours(boundingBox, [box], 0,
                     (255, 255, 255), thickness=cv2.FILLED)
    boundingBox = boundingBox.astype(np.uint8)

    thresh1 = cv2.threshold(boundingBox, 120, 255, cv2.THRESH_BINARY)[1]
    thresh2 = cv2.threshold(inputBoundingBox, 120, 255, cv2.THRESH_BINARY)[1]

    bitwiseAnd = cv2.bitwise_and(thresh1, thresh2)

    matchingPercentage = np.sum(bitwiseAnd)*100/np.sum(inputBoundingBox)
    print("{:0.2f}%".format(matchingPercentage))
    output.write("{},{:0.2f}%\n".format(noise, matchingPercentage))


output.close()
