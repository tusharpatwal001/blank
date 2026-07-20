# image reading Flags
import cv2 as cv
import sys


# default 
img = cv.imread("opencv_demo/sample.png", cv.IMREAD_COLOR)

if img is None:
    sys.exit("Image not found")

# show image
img = cv.resize(img, (400, 400), interpolation=cv.INTER_LINEAR)
cv.imshow("My Image", img)


# Grayscale 
img = cv.imread("opencv_demo/sample.png", cv.IMREAD_GRAYSCALE)

if img is None:
    sys.exit("Image not found")

# show image
img = cv.resize(img, (400, 400), interpolation=cv.INTER_LINEAR)
cv.imshow("My Image", img)


# Alpha Channel 
img = cv.imread("opencv_demo/sample.png", cv.IMREAD_UNCHANGED)

if img is None:
    sys.exit("Image not found")

# show image
img = cv.resize(img, (400, 400), interpolation=cv.INTER_LINEAR)
cv.imshow("My Image", img)
cv.waitKey(0)

