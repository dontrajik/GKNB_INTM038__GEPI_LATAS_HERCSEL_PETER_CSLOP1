import cv2
import numpy as np

for i in range(19):
    imgNumber = i
    image = cv2.imread(f"src/barcode{imgNumber:03d}.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 400, 500)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40,
                            minLineLength=15, maxLineGap=3)

    asd = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(asd, (x1, y1), (x2, y2), (0, 255, 0), 2)

    asd = cv2.medianBlur(asd, 7)
    kernel = np.ones((5, 5), np.uint8)
    asd = cv2.dilate(asd, kernel, iterations=10)
    asd = cv2.erode(asd, kernel, iterations=15)

    edges = cv2.Canny(asd, 30, 200)

    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour = max(contours, key=cv2.contourArea)

    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 5)

    # cv2.imshow('edges', edges)
    # cv2.imshow("asd", asd)
    cv2.imshow("result", image)
    cv2.waitKey()

    cv2.destroyAllWindows()
