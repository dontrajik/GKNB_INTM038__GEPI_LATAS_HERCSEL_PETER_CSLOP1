import cv2
import numpy as np

# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('src\\barcode002.png')
image[np.where(image<50)] = 0
image[np.where(image>250)] = 255
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Detect vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,20))
vertical_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)


kernel = np.ones((3,5), np.uint8)
vertical_mask = cv2.dilate(vertical_mask,kernel,iterations = 7)

contours, hierarchy = cv2.findContours(image=vertical_mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
c = max(contours, key = cv2.contourArea)
x,y,w,h = cv2.boundingRect(c)

print(x,y,w,h)

cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 4)

cv2.imshow('vertical_mask', image)
cv2.waitKey()
cv2.destroyAllWindows()